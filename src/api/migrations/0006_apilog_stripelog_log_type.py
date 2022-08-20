# Generated by Django 4.1 on 2022-08-20 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_request_data_stripelog_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='APILog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('log_type', models.CharField(default='request', max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='stripelog',
            name='log_type',
            field=models.CharField(default='request', max_length=10),
        ),
    ]