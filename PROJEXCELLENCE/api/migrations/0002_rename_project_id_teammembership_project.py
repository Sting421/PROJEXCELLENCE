# Generated by Django 5.1.2 on 2024-11-19 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teammembership',
            old_name='project_id',
            new_name='project',
        ),
    ]