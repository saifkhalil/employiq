# Generated by Django 3.2.9 on 2022-02-03 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20211106_2326'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_candidate',
            field=models.BooleanField(default=False),
        ),
    ]