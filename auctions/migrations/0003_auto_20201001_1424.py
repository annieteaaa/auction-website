# Generated by Django 3.1.1 on 2020-10-01 21:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlistings_bids_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='auctionlistings',
            name='running',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='auctionlistings',
            name='watcher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='auctionlistings',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='listings', to='auctions.categories'),
        ),
    ]