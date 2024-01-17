# Generated by Django 3.2.23 on 2024-01-17 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0014_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='paymentgetway_status',
            field=models.JSONField(blank=True, null=True, verbose_name='Paymentgate response'),
        ),
        migrations.DeleteModel(
            name='Payment_status',
        ),
    ]
