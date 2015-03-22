# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(verbose_name=b'Common Address', max_length=50, editable=False)),
                ('total_amount', models.IntegerField(default=0, verbose_name=b'Outgoing')),
                ('service_fee', models.IntegerField(default=0, verbose_name=b'Fee')),
                ('balance', models.IntegerField(default=0, verbose_name=b'Balance')),
                ('transactions_required', models.IntegerField(default=3)),
                ('transaction_fee', models.IntegerField(default=20000)),
                ('transaction_id', models.CharField(max_length=256, verbose_name=b'Transaction ID')),
                ('is_used', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Common Address',
                'verbose_name_plural': 'Common Addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('origin_address', models.CharField(max_length=50, verbose_name=b'Origin Address')),
                ('destination_address', models.CharField(max_length=50, verbose_name=b'Destination Address')),
                ('amount', models.IntegerField(default=0, verbose_name=b'Outgoing')),
                ('service_fee', models.IntegerField(default=59999, verbose_name=b'Service Fee')),
                ('total_amount', models.IntegerField(default=0, verbose_name=b'Total', editable=False)),
                ('payment_received', models.BooleanField(default=False)),
                ('payment_sent', models.BooleanField(default=False)),
                ('received', models.DateTimeField(null=True, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('common_address', models.ForeignKey(to='payments.Address')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
            bases=(models.Model,),
        ),
    ]
