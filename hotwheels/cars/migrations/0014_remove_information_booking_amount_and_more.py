# Generated by Django 4.1.4 on 2023-01-06 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0013_additionalaccessories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='information',
            name='booking_amount',
        ),
        migrations.RemoveField(
            model_name='information',
            name='delivery_cost',
        ),
        migrations.RemoveField(
            model_name='information',
            name='delivery_days',
        ),
        migrations.RemoveField(
            model_name='information',
            name='tax_amount',
        ),
        migrations.AlterField(
            model_name='additionalaccessories',
            name='Product',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Product Name (Pixel Size 62x62)'),
        ),
    ]
