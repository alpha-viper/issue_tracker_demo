# Generated by Django 4.2.1 on 2023-06-30 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0004_alter_story_description_alter_story_estimated_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
