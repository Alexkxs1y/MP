# Generated by Django 4.0.2 on 2022-05-12 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_rename_listing_id_bids_listingid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='whatchlist',
            name='on_watchlist',
        ),
        migrations.AddField(
            model_name='whatchlist',
            name='inwatchlist',
            field=models.BooleanField(default=False),
        ),
    ]
