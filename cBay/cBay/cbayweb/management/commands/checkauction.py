from django.core.management.base import BaseCommand, CommandError
from cbayweb.models import *

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        print(datetime.now())
        tmp_auctions = Auction.objects.filter(end_time__lte=datetime.now(), is_ended = False)
        for auction in tmp_auctions:
            winning_bids = Bid.objects.filter(bid_price = auction.current_max_bid, auction=auction)
            if winning_bids.count() == 0:
                self.stdout.write("hahahahah", ending='')
                auction.is_ended = True
                auction.save()
            else:
                self.stdout.write("find an unended auction", ending='')
                winning_bid = winning_bids[0]
                auction.winner = winning_bid.bidder
                auction.is_ended = True
                auction.save()
