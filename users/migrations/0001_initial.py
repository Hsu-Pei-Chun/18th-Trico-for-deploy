# Generated by Django 5.1.4 on 2025-01-13 04:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profile_photos/')),
                ('bio', models.TextField(max_length=200, null=True)),
                ('location', models.CharField(max_length=50, null=True)),
                ('is_client', models.BooleanField(default=True, null=True)),
                ('is_freelancer', models.BooleanField(default=False, null=True)),
                ('freelancer_verified', models.BooleanField(default=False, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
