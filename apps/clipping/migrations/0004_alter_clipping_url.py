# Generated by Django 4.2.2 on 2023-06-17 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clipping', '0003_alter_clipping_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clipping',
            name='url',
            field=models.URLField(error_messages='This url has already been uploaded.', unique=True, verbose_name='URL'),
        ),
    ]