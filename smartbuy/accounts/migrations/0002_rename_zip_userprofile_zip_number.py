# Generated by Django 4.0 on 2021-12-31 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='zip',
            new_name='zip_number',
        ),
    ]
