# Generated by Django 3.2.5 on 2023-05-29 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0006_alter_userbasecall_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='callshistory',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='research.updates'),
        ),
    ]