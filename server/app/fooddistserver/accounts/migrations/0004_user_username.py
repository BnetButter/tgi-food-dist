# Generated by Django 5.1.4 on 2025-01-19 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.TextField(blank=True, null=True),
        ),
    ]
