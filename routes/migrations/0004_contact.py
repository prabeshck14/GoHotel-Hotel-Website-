# Generated by Django 4.0.3 on 2022-04-20 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0003_booking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('Msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(default='', max_length=100)),
                ('message', models.CharField(default='', max_length=500)),
            ],
        ),
    ]