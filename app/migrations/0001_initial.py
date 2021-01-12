# Generated by Django 3.1.5 on 2021-01-12 15:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Validated', 'Validated')], default='Pending', max_length=20)),
                ('card_number', models.CharField(default='0000000000000000', max_length=16, validators=[django.core.validators.MinLengthValidator(16), django.core.validators.MaxLengthValidator(16)])),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('amount', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999999)])),
            ],
        ),
    ]
