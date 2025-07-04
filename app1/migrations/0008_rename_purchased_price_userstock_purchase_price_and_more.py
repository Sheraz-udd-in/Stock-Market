# Generated by Django 5.2.3 on 2025-07-03 04:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_rename_current_price_stocks_curr_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='userstock',
            old_name='purchased_price',
            new_name='purchase_price',
        ),
        migrations.RenameField(
            model_name='userstock',
            old_name='purchased_quantity',
            new_name='purchase_quantity',
        ),
        migrations.RemoveField(
            model_name='stocks',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='userstock',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.stocks'),
        ),
        migrations.AlterField(
            model_name='userstock',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
