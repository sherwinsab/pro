# Generated by Django 4.1.4 on 2023-01-12 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0020_alter_taxandother_insurance_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='INSURANCE',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Insurance Company')),
                ('Insurance_amt', models.IntegerField(verbose_name='Insurance Amount')),
            ],
            options={
                'verbose_name': 'Add Insurance',
                'verbose_name_plural': 'Insurance',
                'db_table': 'INSURANCE',
            },
        ),
        migrations.AddField(
            model_name='taxandother',
            name='insu_nameid',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.insurance', verbose_name='Insurance Name'),
        ),
    ]
