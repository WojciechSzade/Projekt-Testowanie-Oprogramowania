# Generated by Django 4.2.6 on 2023-10-26 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRUD', '0008_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
