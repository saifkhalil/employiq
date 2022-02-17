# Generated by Django 3.2.9 on 2022-02-15 20:15

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='city',
            field=models.CharField(choices=[('Al Anbar', 'Al Anbar'), ('Babylon', 'Babylon'), ('Baghdad', 'Baghdad'), ('Basra', 'Basra'), ('Dhi Qar', 'Dhi Qar'), ('Al-Qadisiyyah', 'Al-Qadisiyyah'), ('Diyala', 'Diyala'), ('Duhok', 'Duhok'), ('Erbil', 'Erbil'), ('Halabja', 'Halabja'), ('Karbala', 'Karbala'), ('Kirkuk', 'Kirkuk'), ('Maysan', 'Maysan'), ('Muthanna', 'Muthanna'), ('Najaf', 'Najaf'), ('Nineveh', 'Nineveh'), ('Saladin', 'Saladin'), ('Sulaymaniyah', 'Sulaymaniyah'), ('Wasit', 'Wasit')], default='Baghdad', max_length=500, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='country',
            field=django_countries.fields.CountryField(default='IQ', max_length=2, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='job',
            name='city',
            field=models.CharField(choices=[('Al Anbar', 'Al Anbar'), ('Babylon', 'Babylon'), ('Baghdad', 'Baghdad'), ('Basra', 'Basra'), ('Dhi Qar', 'Dhi Qar'), ('Al-Qadisiyyah', 'Al-Qadisiyyah'), ('Diyala', 'Diyala'), ('Duhok', 'Duhok'), ('Erbil', 'Erbil'), ('Halabja', 'Halabja'), ('Karbala', 'Karbala'), ('Kirkuk', 'Kirkuk'), ('Maysan', 'Maysan'), ('Muthanna', 'Muthanna'), ('Najaf', 'Najaf'), ('Nineveh', 'Nineveh'), ('Saladin', 'Saladin'), ('Sulaymaniyah', 'Sulaymaniyah'), ('Wasit', 'Wasit')], default='Baghdad', max_length=500, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='job',
            name='country',
            field=django_countries.fields.CountryField(default='IQ', max_length=2, verbose_name='Country'),
        ),
    ]
