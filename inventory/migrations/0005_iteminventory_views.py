# Generated by Django 3.0.6 on 2020-05-20 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20200520_0549'),
    ]

    operations = [
        migrations.AddField(
            model_name='iteminventory',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
