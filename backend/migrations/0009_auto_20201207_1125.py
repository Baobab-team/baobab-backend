# Generated by Django 3.1.1 on 2020-12-07 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0008_auto_20201204_2309"),
    ]

    operations = [
        migrations.AlterField(
            model_name="business",
            name="slug",
            field=models.SlugField(max_length=100),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=100),
        ),
    ]
