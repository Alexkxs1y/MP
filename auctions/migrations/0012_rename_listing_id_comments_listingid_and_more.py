# Generated by Django 4.0.2 on 2022-05-02 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_bids_created_comments_created_whatchlist_created_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='listing_id',
            new_name='listingid',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='user_id',
            new_name='userid',
        ),
    ]
