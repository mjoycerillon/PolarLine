# Generated by Django 3.1.7 on 2021-04-13 19:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]