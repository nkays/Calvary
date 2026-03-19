# sync_youtube.py/management-command
# sync_youtube.py/management-command/final
from django.core.management.base import BaseCommand
from sermons.integrations.youtube import full_sync_channel
from decouple import config


class Command(BaseCommand):
    help = "Sync YouTube channel (playlists → series → sermons)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--channel_id",
            type=str,
            required=False,  # 👈 allow fallback
            help="YouTube Channel ID"
        )

    def handle(self, *args, **options):
        # ✅ correct place to resolve channel_id
        channel_id = options.get("channel_id") or config("GBC_CHANNEL_ID")

        if not channel_id:
            self.stderr.write("Error: channel_id is required")
            return

        self.stdout.write(f"Starting sync for channel: {channel_id}")

        result = full_sync_channel(channel_id)

        self.stdout.write(self.style.SUCCESS("Sync complete!"))
        self.stdout.write(str(result))