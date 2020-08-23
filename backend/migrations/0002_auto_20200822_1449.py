# Generated by Django 3.1 on 2020-08-22 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OpeningHours',
            new_name='OpeningHour',
        ),
        migrations.AlterModelOptions(
            name='business',
            options={'verbose_name_plural': 'businesses'},
        ),
        migrations.AlterModelOptions(
            name='phone',
            options={'verbose_name_plural': 'phones'},
        ),
        migrations.AlterField(
            model_name='address',
            name='province',
            field=models.CharField(choices=[('qc', 'Quebec'), ('on', 'Ontario'), ('ns', 'Nova Scotia'), ('nb', 'New Brunswick'), ('pe', 'Prince Edward Island'), ('ab', 'Alberta'), ('nu', 'Nunavut'), ('sk', 'Saskatchewan'), ('bc', 'British Columbia'), ('nl', 'Newfoundland and Labrador'), ('mn', 'Manitoba')], default='qc', max_length=100),
        ),
        migrations.AlterField(
            model_name='business',
            name='description',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='business',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='business',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='slogan',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='business',
            name='website',
            field=models.URLField(blank=True),
        ),
    ]