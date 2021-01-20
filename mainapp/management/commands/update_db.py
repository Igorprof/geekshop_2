from django.core.management import BaseCommand

from authapp.models import User, ShopUserProfile

class Command(BaseCommand):

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            ShopUserProfile.objects.create(user=user)