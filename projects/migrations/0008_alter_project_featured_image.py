# Generated by Django 3.2.16 on 2022-12-31 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_project_featured_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='featured_image',
            field=models.ImageField(blank=True, default='project-default.jpg', null=True, upload_to='uploaded-images/projects'),
        ),
    ]
