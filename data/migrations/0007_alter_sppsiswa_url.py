# Generated by Django 3.2 on 2010-09-03 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_alter_sppitem_spp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sppsiswa',
            name='url',
            field=models.CharField(blank=True, default='0', max_length=200, null=True),
        ),
    ]
