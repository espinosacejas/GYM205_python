# Generated by Django 4.0.3 on 2023-01-20 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_cabinets', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to='test'),
        ),
    ]
