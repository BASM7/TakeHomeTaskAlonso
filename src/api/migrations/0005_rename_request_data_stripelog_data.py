# Generated by Django 4.1 on 2022-08-20 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_striperequest_stripelog_delete_striperesponse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stripelog',
            old_name='request_data',
            new_name='data',
        ),
    ]
