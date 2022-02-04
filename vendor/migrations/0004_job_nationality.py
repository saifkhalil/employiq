# Generated by Django 3.2.9 on 2022-02-04 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_auto_20220205_0049'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='nationality',
            field=models.CharField(choices=[('international', 'International'), ('national', 'National'), ('both', 'Both')], default='both', max_length=15, verbose_name='Nationality'),
        ),
    ]