# Generated by Django 4.2.14 on 2025-03-05 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='otp_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
