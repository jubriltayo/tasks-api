# Generated by Django 5.0.4 on 2024-05-18 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_task_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]