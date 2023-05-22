# Generated by Django 4.2.1 on 2023-05-19 09:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0015_order_is_takeaway_order_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='is_takeaway',
            field=models.IntegerField(choices=[(0, 'Here'), (1, 'Takeaway order')], default=0),
        ),
    ]
