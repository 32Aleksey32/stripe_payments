# Generated by Django 5.0.2 on 2024-02-28 18:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL('CREATE SCHEMA payment_system;'),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Наименование')),
                ('description', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Цена')),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('RUB', 'RUB')], default='USD', max_length=3, verbose_name='Валюта')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'payment_system"."items',
                'ordering': ['name'],
            },
        ),
    ]
