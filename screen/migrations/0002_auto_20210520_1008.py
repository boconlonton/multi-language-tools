# Generated by Django 2.0.1 on 2021-05-20 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screen', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screen',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
