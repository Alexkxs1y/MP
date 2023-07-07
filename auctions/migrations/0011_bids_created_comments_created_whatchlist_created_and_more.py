# Generated by Django 4.0.2 on 2022-04-27 07:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_auction_listing_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='comments',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='whatchlist',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='listing_description',
            field=models.TextField(blank=True, default=None, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='picture',
            field=models.ImageField(blank=True, default='images/No_Image_Available.jpg', upload_to='images'),
        ),
        migrations.AlterField(
            model_name='whatchlist',
            name='on_watchlist',
            field=models.IntegerField(default=0),
        ),
    ]