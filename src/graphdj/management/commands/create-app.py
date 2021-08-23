import shutil
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

TEMPLATES_PATH = Path(__file__).parents[1] / "templates"


class Command(BaseCommand):
    help = "Create a new app from Custom-Template."

    def add_arguments(self, parser):
        parser.add_argument("app_name", nargs=1, type=str)

    def handle(self, *args, **kwargs):
        try:
            app_name = kwargs["app_name"][0]
            template = TEMPLATES_PATH / "django_app_template.zip"
            call_command("startapp", f"--template={ template }", app_name)
            shutil.move(
                # Source —> Destination
                (settings.BASE_DIR / app_name),
                (settings.BASE_DIR / "apps" / app_name),
            )
            msg = f"successfully created app: <{app_name}>"
            size = len(msg) + 4
            print("\n" + ("#" * size) + "\n# " + msg + " #\n" + ("#" * size))
        except Exception as e:
            print(e)
            raise CommandError("Initalization failed.")
