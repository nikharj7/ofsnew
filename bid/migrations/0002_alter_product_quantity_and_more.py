# Generated by Django 4.1.7 on 2023-03-13 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bid', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.CharField(blank=True, default=1, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='step_up_quantity',
            field=models.CharField(blank=True, default=1, max_length=8, null=True),
        ),
    ]
