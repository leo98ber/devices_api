# Generated by Django 3.2.8 on 2024-03-02 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_alter_device_ip_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='code',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
