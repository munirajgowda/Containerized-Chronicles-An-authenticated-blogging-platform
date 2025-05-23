# Generated by Django 5.1.3 on 2024-12-09 11:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogs',
            old_name='is_feacherd',
            new_name='is_featured',
        ),
        migrations.AlterField(
            model_name='blogs',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blogs.category'),
        ),
    ]
