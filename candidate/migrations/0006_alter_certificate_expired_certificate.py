# Generated by Django 3.2.9 on 2022-02-13 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0005_alter_certificate_expired_certificate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='expired_certificate',
            field=models.BooleanField(default=False, verbose_name='This credential does not expire'),
        ),
    ]