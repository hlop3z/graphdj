import json
import pathlib
import sys

from django.apps import apps as django_apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# sys.path.append(pathlib.Path(__file__).parents[2])
from graphdj.core.__base__ import model_to_app_info

# Get Settings
if not settings.GRAPHDJ:
    raise ValueError("Please configure GraphDJ.")

GRAPHDJ_APPS = settings.GRAPHDJ.get("APPS") or []

BASE_DIR = pathlib.Path(sys.argv[0]).parents[0].resolve()
FILE_OUT_JS = BASE_DIR / "core" / "javascript" / "models.js"


def create_models_js(apps_list=GRAPHDJ_APPS):
    the_project = {}
    for app in apps_list:
        for model in django_apps.get_app_config(app).get_models():
            fields = [field.name for field in model._meta.fields]
            conf = model_to_app_info(model)
            uri = f"{conf.name}.{conf.model.one}"
            form = {key: None for key in fields}
            fields_required = [
                field.name
                for field in model._meta.fields
                if not field.null and not field.name == "id"
            ]
            javascript = {
                "required": fields_required,
                "fields": fields,
                "create": form,
                "update": form,
                "objects": {},
                "meta": {
                    "uri": uri,
                    "app": conf.name,
                    "instance": conf.model.one,
                    "objects": conf.model.many,
                },
            }
            the_project[javascript["meta"]["uri"]] = javascript
    with open(FILE_OUT_JS, "w") as file:
        json_data = json.dumps(list(the_project.values()), sort_keys=True, indent=4)
        file.write(f"export default {json_data}")


class Command(BaseCommand):
    help = "Create <models.js> from each <app/models.py>"

    def handle(self, *args, **kwargs):
        try:
            create_models_js()
            msg = "successfully created <models.js>"
            size = len(msg) + 4
            print("\n" + ("#" * size) + "\n# " + msg + " #\n" + ("#" * size))
        except Exception as e:
            print(e)
            raise CommandError("Initalization failed.")
