# Generated by Django 5.1.4 on 2024-12-09 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='empresa',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Empresa'),
        ),
    ]
