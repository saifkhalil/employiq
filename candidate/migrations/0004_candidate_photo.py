# Generated by Django 3.2.9 on 2021-11-07 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0003_candidate_cv'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='photo',
            field=models.ImageField(default='', upload_to='media/photos/candidate'),
            preserve_default=False,
        ),
    ]
