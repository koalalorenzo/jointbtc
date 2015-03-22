# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from blockchain.wallet import Wallet
# Create your models here.


class Address(models.Model):
    address = models.CharField("Common Address", max_length=50, editable=False)
    total_amount = models.IntegerField("Outgoing", default=0)
    service_fee = models.IntegerField("Fee", default=0)
    balance = models.IntegerField("Balance", default=0)

    transactions_required = models.IntegerField(default=3)
    transaction_fee = models.IntegerField(default=settings.DEFAULT_TRANSACTION_FEE)
    transaction_id = models.CharField("Transaction ID", max_length=256, editable=True)

    is_used = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Common Address')
        verbose_name_plural = _('Common Addresses')

    def __unicode__(self):
        return u"%s" % self.address

    @classmethod
    def create(cls):
        address = cls()
        address.generate_new_address()
        return address

    def save(self):
        """
            Check if the address is available, if not we have to
            generate one saving also the label to recognize it easily.
        """
        if len(self.address) == 0:
            self.generate_new_address()
        return super(Address, self).save()

    def __get_wallet(self):
        return Wallet(
            settings.WALLET_ID,
            settings.WALLET_PASSWORD
        )

    def generate_new_address(self):
        wallet = self.__get_wallet()
        self.address = wallet.new_address().address
        return self.address

    def get_balance(self, confirmations=1):
        wallet = self.__get_wallet()
        balance = wallet.get_address(
            self.address, confirmations=confirmations
        ).balance

        if confirmations >= 1:
            self.balance = balance # Satoshi
            self.save()

        return balance

    def payout(self):
        """
            Calculate all the amount that we have to pay and perform a multiple
            payment transaction.
        """
        if self.transactionrequest_set.count() < self.transactions_required:
            raise Exception('Not enough transaction requests')

        recipients = dict()
        total_amount = 0

        transaction_requests = self.transactionrequest_set.all()
        for transaction in transaction_requests:
            addr = transaction.destination_address
            amount = transaction.amount # Satoshi

            # This will avoid problem with money going to the same address.
            if not recipients.has_key(addr):
                recipients[addr] = 0

            recipients[addr] += int(amount)
            total_amount += int(amount)

        current_balance = self.get_balance()
        if current_balance < total_amount:
            raise Exception(
                "Not enough founds available: %s < %s" % (
                    current_balance, total_amount
                )
            )

        # Calculating the service fee: what is over (?)
        service_fee = current_balance - ( total_amount + self.transaction_fee )
        recipients[settings.SERVICE_FEE_ADDRESS] = int(service_fee)

        note = settings.DEFAULT_TRANSACTION_NOTE
        fee = settings.DEFAULT_TRANSACTION_FEE

        wallet = self.__get_wallet()
        transaction_id = wallet.send_many_payments(
            recipients, self.address,
            fee=fee, note=note
        )

        self.is_used = True
        self.transaction_id = transaction_id # it must be there
        self.save()

        return transaction

    def expire(self):
        balance = self.get_balance(confirmations=0)
        if balance > 0:
            return

        wallet = self.__get_wallet()
        archived = wallet.archive_address(self.address)
        if archived == self.address:
            self.is_used = True
        self.save()


@receiver(post_save, sender=Address, dispatch_uid="set_transactions_received")
def set_transactions_received(sender, instance, signal, created, **kwargs):
    """ Check if a transactions was received """
    if instance.balance <= 0:
        return # Balance too small

    for transaction_request in instance.transactionrequest_set.all():
        if transaction_request.payment_received:
            continue

        amount = transaction_request.amount + transaction_request.service_fee
        if instance.balance >= amount:
            transaction_request.payment_received = True
            transaction_request.save()


@receiver(post_save, sender=Address, dispatch_uid="set_transactions_sent")
def set_transactions_sent(sender, instance, signal, created, **kwargs):
    """ If the payout was performed, update all the transaction requests """
    if not len(instance.transaction_id) > 0:
        return # Transaction not created

    for transaction_request in instance.transactionrequest_set.all():
        transaction_request.payment_sent = True
        transaction_request.save()


@receiver(pre_save, sender=Address, dispatch_uid="update_outgoing_amount")
def update_outgoing_amount(sender, instance, **kwargs):
    """ Update the AddressCommon outgoing amount """

    total_amount = 0
    for transaction_request in instance.transactionrequest_set.all():
        total_amount += transaction_request.amount

    instance.total_amount = total_amount + instance.transaction_fee
    instance.service_fee = instance.balance - instance.total_amount


class TransactionRequest(models.Model):
    origin_address = models.CharField("Origin Address", max_length=50)
    destination_address = models.CharField("Destination Address", max_length=50)

    amount = models.IntegerField("Outgoing", default=0)
    service_fee = models.IntegerField("Service Fee", default=settings.SERVICE_FEE_AMOUNT)
    total_amount = models.IntegerField("Total", default=0, editable=False)

    common_address = models.ForeignKey(Address)

    payment_received = models.BooleanField(default=False)
    payment_sent = models.BooleanField(default=False)

    received = models.DateTimeField(null=True, editable=False)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __unicode__(self):
        return u"%s %s" % (self.origin_address, self.amount)


@receiver(pre_save, sender=TransactionRequest, dispatch_uid="tr_update_outgoing")
def update_outgoing_transaction_request_amount(sender, instance, **kwargs):
    """ Update the TransactionRequest outgoing amount """

    instance.total_amount = instance.amount + instance.service_fee