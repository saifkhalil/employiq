# Generated by Django 3.2.12 on 2022-04-23 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_i_agree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='i_agree',
            field=models.BooleanField(default=False, verbose_name='Please confirm that you read and agree to our terms & conditions'),
        ),
    ]
