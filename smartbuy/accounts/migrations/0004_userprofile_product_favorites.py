# Generated by Django 4.0 on 2022-01-01 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_options'),
        ('accounts', '0003_remove_userprofile_address2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='product_favorites',
            field=models.ManyToManyField(to='products.Product'),
        ),
    ]
