from django.core.management import BaseCommand
from helios_server.helios_auth.models import User


class Command(BaseCommand):
    args = ""
    help = "add testing user"

    def handle(self, *args, **options):
        User.objects.create(
            user_type="google",
            user_id="test@example.net",
            admin_p=True,
            info={"name": "Test User"},
        )
