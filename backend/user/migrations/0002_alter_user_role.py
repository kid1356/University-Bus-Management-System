# Generated by Django 5.1.2 on 2024-10-30 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('Student', 'student'), ('University_admin', 'university_admin')], max_length=20, null=True),
        ),
    ]
