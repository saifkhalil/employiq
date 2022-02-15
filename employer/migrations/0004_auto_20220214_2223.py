# Generated by Django 3.2.9 on 2022-02-14 19:23

from decimal import Decimal
from django.db import migrations, models
import django_countries.fields
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0006_alter_certificate_expired_certificate'),
        ('employer', '0003_auto_20220214_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription_plan',
            name='price',
            field=djmoney.models.fields.MoneyField(decimal_places=0, default=Decimal(
                '1'), default_currency='USD', max_digits=10, verbose_name='Price'),
        ),
    ]