# Generated by Django 3.2.4 on 2021-07-12 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0016_alter_imagepost_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagepost',
            name='date_created',
            field=models.DateField(blank=True, editable=False),
        ),
    ]
