# Generated by Django 2.2.7 on 2020-01-19 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VDJ_Anchors', '0002_auto_20191204_0534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anchor',
            name='document',
            field=models.FileField(default='', upload_to='VDJ_fasta'),
        ),
    ]
