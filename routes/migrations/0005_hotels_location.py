# Generated by Django 4.0.3 on 2022-04-20 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0004_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotels',
            name='location',
            field=models.TextField(default='', max_length=50),
        ),
    ]