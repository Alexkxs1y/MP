# Generated by Django 4.0.2 on 2022-04-16 03:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction_listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing_title', models.CharField(max_length=64)),
                ('listing_description', models.TextField()),
                ('starting_bid', models.IntegerField()),
                ('picture_url', models.URLField()),
                ('actual', models.IntegerField()),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_reverse', to=settings.AUTH_USER_MODEL)),
                ('winner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winner_reverse', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Whatchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('on_watchlist', models.IntegerField()),
                ('listing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_reverse4', to='auctions.auction_listing')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reverse4', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('listing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_reverse3', to='auctions.auction_listing')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reverse3', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_reverse5', to='auctions.category')),
                ('listing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_reverse5', to='auctions.auction_listing')),
            ],
        ),
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.IntegerField()),
                ('listing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_reverse2', to='auctions.auction_listing')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reverse2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
