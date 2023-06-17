# Generated by Django 3.2.5 on 2023-05-22 09:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0012_auto_20230518_1747'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpiryDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekly', models.DateField()),
                ('monthly', models.DateField()),
                ('finnifty', models.DateField()),
                ('commodity', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Lotsize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_name', models.CharField(max_length=100, unique=True)),
                ('lotsize', models.CharField(blank=True, max_length=100, null=True)),
                ('date_exp', models.CharField(blank=True, choices=[('WEEKLY', 'Weekly'), ('MONTHLY', 'Monthly'), ('FINNIFTY', 'Finnifty'), ('COMMODITY', 'Commodity')], max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_id', models.CharField(default=uuid.uuid4, max_length=100, unique=True)),
                ('category', models.CharField(choices=[('CASH', 'cash'), ('FUTURE', 'future'), ('OPTION', 'option')], max_length=50)),
                ('sub_category', models.CharField(blank=True, max_length=100, null=True)),
                ('calculation', models.CharField(choices=[('PROFIT', 'Profit'), ('PERCENTAGE', 'Percentage')], max_length=20)),
                ('tgt_prcnt', models.CharField(blank=True, max_length=10, null=True)),
                ('sl_prcnt', models.CharField(blank=True, max_length=10, null=True)),
                ('profit', models.CharField(blank=True, max_length=20, null=True)),
                ('loss', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Updates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('update_format', models.TextField()),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='research.product', unique=True)),
            ],
            options={
                'unique_together': {('product_category', 'title')},
            },
        ),
    ]