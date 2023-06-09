# Generated by Django 4.2.1 on 2023-05-15 10:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0005_rename_table_id_cart_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('quantity', models.PositiveIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cafe.cart')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cafe.dish')),
            ],
        ),
    ]
