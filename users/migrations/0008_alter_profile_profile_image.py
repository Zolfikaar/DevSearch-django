# Generated by Django 3.2.16 on 2023-01-03 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_rename_name_skills_skillname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='images/user-default.png', null=True, upload_to='uploaded-images/profiles'),
        ),
    ]
