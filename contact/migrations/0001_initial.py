# Generated by Django 5.1.4 on 2025-01-13 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('email', models.EmailField(max_length=254, verbose_name='電子郵件')),
                ('message', models.TextField(verbose_name='訊息內容')),
                ('reply', models.TextField(blank=True, null=True, verbose_name='回覆內容')),
                ('is_replied', models.BooleanField(default=False, verbose_name='是否已回覆')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='訊息時間')),
            ],
        ),
    ]
