# Generated by Django 3.2.4 on 2021-07-12 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0010_auto_20210711_1953'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcomment',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='postlikes',
            options={'ordering': ['-id']},
        ),
    ]