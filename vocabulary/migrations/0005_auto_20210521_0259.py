# Generated by Django 2.0.1 on 2021-05-21 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screen', '0003_auto_20210521_0150'),
        ('vocabulary', '0004_vocabulary_screen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vocabulary',
            name='screen',
        ),
        migrations.AddField(
            model_name='vocabulary',
            name='screen',
            field=models.ManyToManyField(to='screen.Screen'),
        ),
    ]
