# Generated by Django 3.1.7 on 2021-04-15 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20210415_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='productSlug',
            field=models.SlugField(default=models.CharField(max_length=100), max_length=40),
        ),
    ]