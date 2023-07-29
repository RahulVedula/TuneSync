# Generated by Django 3.2.11 on 2023-07-23 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20230721_0349'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='added_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='album_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='song',
            name='duration',
            field=models.PositiveIntegerField(default=0),
        ),
    ]