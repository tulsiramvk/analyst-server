# Generated by Django 3.2.5 on 2023-06-16 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_banner_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('r1', models.CharField(max_length=10)),
                ('r2', models.CharField(max_length=10)),
                ('s1', models.CharField(max_length=10)),
                ('s2', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]