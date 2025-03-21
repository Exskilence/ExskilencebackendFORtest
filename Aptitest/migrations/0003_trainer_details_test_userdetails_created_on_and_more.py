# Generated by Django 4.1.13 on 2025-03-21 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aptitest', '0002_rename_duration_test_userdetails_coding_duration_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainer_details',
            fields=[
                ('UID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=25)),
                ('Email', models.CharField(max_length=25, unique=True)),
                ('Created_on', models.DateTimeField(auto_now_add=True)),
                ('Category', models.CharField(default='Trainer', max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='test_userdetails',
            name='Created_on',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='test_userdetails',
            name='batch',
            field=models.CharField(default='2024', max_length=25),
        ),
    ]
