# Generated by Django 3.2.15 on 2023-11-07 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employer', '0011_auto_20230721_2247'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(max_length=20)),
                ('checkout_id', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checkout_createdby', to=settings.AUTH_USER_MODEL)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employer.employer')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checkout_modifiedby', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='subscription_features',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('feature', models.CharField(max_length=200, verbose_name='Feature')),
            ],
        ),
        migrations.AddField(
            model_name='subscription_plan',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Disabled', 'Disabled'), ('ComingSoon', 'Coming Soon')], default='Disabled', max_length=20, verbose_name='Status'),
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
        migrations.AddField(
            model_name='checkout',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employer.subscription_plan', verbose_name='Plan'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='checkout',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employer.checkout', verbose_name='Checkout'),
        ),
        migrations.AddField(
            model_name='subscription_plan',
            name='features',
            field=models.ManyToManyField(blank=True, related_name='features', to='employer.subscription_features', verbose_name='Features'),
        ),
    ]
