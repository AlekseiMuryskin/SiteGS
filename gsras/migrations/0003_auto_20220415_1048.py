# Generated by Django 3.2.12 on 2022-04-15 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gsras', '0002_auto_20220414_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datarequesterpersonal',
            name='data_requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsras.datarequester'),
        ),
        migrations.AlterField(
            model_name='datarequesterphone',
            name='data_requester_personal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsras.datarequesterpersonal'),
        ),
    ]