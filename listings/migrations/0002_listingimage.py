# Generated by Django 3.1.3 on 2020-11-29 17:39

from django.db import migrations, models
import django.db.models.deletion
import listings.models.listing
import subletshark.storage_backends
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('filename', models.CharField(max_length=255)),
                ('image', models.ImageField(storage=subletshark.storage_backends.PublicImageStorage(), upload_to=listings.models.listing.image_filename)),
                ('listing', models.ForeignKey(help_text='The listing that this image belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='images', to='listings.listing')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]