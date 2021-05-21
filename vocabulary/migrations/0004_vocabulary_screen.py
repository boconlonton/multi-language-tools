# Generated by Django 2.0.1 on 2021-05-21 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('screen', '0003_auto_20210521_0150'),
        ('vocabulary', '0003_auto_20210520_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='vocabulary',
            name='screen',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='screen.Screen'),
            preserve_default=False,
        ),
    ]
