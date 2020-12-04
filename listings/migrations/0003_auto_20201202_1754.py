# Generated by Django 3.1.3 on 2020-12-02 17:54

from django.db import migrations, models
import listings.models.listing


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_listingimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listingimage',
            name='image',
            field=models.ImageField(storage=listings.models.listing.select_storage, upload_to=listings.models.listing.image_filename),
        ),
    ]
