# Generated by Django 3.2.5 on 2023-04-21 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_package_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
