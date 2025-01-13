
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='service_photos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('standard_title', models.CharField(max_length=100)),
                ('standard_description', models.TextField()),
                ('standard_price', models.PositiveIntegerField()),
                ('standard_delivery_time', models.PositiveIntegerField(blank=True, null=True)),
                ('premium_title', models.CharField(blank=True, max_length=100, null=True)),
                ('premium_description', models.TextField(blank=True, null=True)),
                ('premium_price', models.PositiveIntegerField(blank=True, null=True)),
                ('premium_delivery_time', models.PositiveIntegerField(blank=True, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, default=None, help_text='Client rating for the service (e.g., 4.5 stars)', max_digits=2, null=True)),
                ('category', models.ManyToManyField(related_name='services', to='categories.category')),
                ('freelancer_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='services', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='services.service')),
            ],
        ),
    ]
