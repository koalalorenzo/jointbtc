from django.contrib import admin

from .models import Address
from .models import TransactionRequest
# Register your models here.

class TransactionRequestAdmin(admin.ModelAdmin):
    readonly_fields = ['total_amount', 'edited', 'created', 'payment_received', 'payment_sent']
    list_display = ['origin_address', 'total_amount', 'payment_sent']

admin.site.register(TransactionRequest, TransactionRequestAdmin)


class TransactionRequestInLine(admin.TabularInline):
    readonly_fields = ['total_amount', 'edited', 'created', 'payment_received', 'payment_sent']
    model = TransactionRequest
    extra = 1
    allow_add = True


def update_balance(self, request, queryset):
    for address in queryset:
        balance = address.get_balance(confirmations=1)/100000000.0

        self.message_user(request, u'%s balance: %s' % (address, balance) )


def check_balance_unconfirmed(self, request, queryset):
    for address in queryset:
        balance = address.get_balance(confirmations=0)/100000000.0
        print balance
        self.message_user(request, u'%s balance unconfirmed: %s' % (address, balance) )


def payout(self, request, queryset):
    for address in queryset:
        address.payout()


def expire(self, request, queryset):
    for address in queryset:
        address.expire()


class AddressAdmin(admin.ModelAdmin):
    readonly_fields = ['address', 'balance', 'total_amount', 'service_fee', 'is_used', 'transaction_id', 'edited', 'created']
    list_filter = ['is_used', 'created', 'is_used']
    list_display = ['address', 'total_amount', 'service_fee', 'balance', 'is_used', 'transactions_required', 'transaction_fee']
    search_fields = ['is_used', 'address', 'transactionrequest_set__address']
    inlines = [TransactionRequestInLine]
    actions = [update_balance, check_balance_unconfirmed, payout, expire]

admin.site.register(Address, AddressAdmin)
