# Generated by Django 3.1 on 2020-09-05 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200815_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
