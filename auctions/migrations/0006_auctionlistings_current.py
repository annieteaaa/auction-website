# Generated by Django 3.1.1 on 2020-10-02 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auctionlistings_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlistings',
            name='current',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]
