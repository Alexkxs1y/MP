# Generated by Django 4.0.2 on 2022-07-17 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_remove_whatchlist_userid_whatchlist_userid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='whatchlist',
            name='userid',
        ),
        migrations.AddField(
            model_name='whatchlist',
            name='userid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_reverse4', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
