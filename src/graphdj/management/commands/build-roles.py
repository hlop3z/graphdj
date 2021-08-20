import json
import os
import pathlib
import sys

import yaml
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# Get Settings
if not settings.GRAPHDJ:
    raise ValueError("Please configure GraphDJ.")

GRAPHDJ_APPS = settings.GRAPHDJ.get("APPS") or []

BASE_DIR = pathlib.Path(sys.argv[0]).parents[0].resolve()
FILES_IN_YAML = list(pathlib.Path(BASE_DIR / "setup" / "roles").glob("**/*.yaml"))
FILE_OUT_JS = BASE_DIR / "core" / "javascript" / "roles.js"
FILE_OUT_PY = BASE_DIR / "core" / "roles.py"

YAML_EXAMPLE = """
# Role
customer:
  # App
  cookbook:
    # Model
    category: 
      create : [id, name]
      read   : [id, name, ingredients: cookbook.ingredient]
      update : [id, name]
      delete : [id, name]
    # Model
    ingredient: 
      create : [id, name]
      read   : [id, name]
      update : [id, name]
      delete : [id, name]
""".strip()


def get_nodes(role):
    perms = {}

    def get_fields(fields, action=None):
        return_value = []
        for col in fields:
            if isinstance(col, dict):
                if action.lower() == "read":
                    first_value = next(iter(col.items()))
                    selected = first_value[1]
                    model = first_value[0]
                    get_keys = role[f"{selected}.{action}"]
                    items = get_fields(get_keys, action)
                    return_value.extend([f"{model}.{i}" for i in items])
                else:
                    return_value.append(next(iter(col.items()))[1])
            else:
                return_value.append(col)
        return return_value

    for uri, fields in role.items():
        action = uri.split(".")[2]
        items = get_fields(fields, action)
        perms[uri] = items
    return perms


def get_yaml_documents(paths=FILES_IN_YAML):
    roles = {}
    for filepath in paths:
        with open(filepath) as file:
            document = yaml.full_load(file)
            roles.update(document)
    return roles


def load_yaml():
    document = get_yaml_documents()
    # Create Roles
    roles = {}
    for role, apps in document.items():
        actions = {}
        for app, models in apps.items():
            for model, opts in models.items():
                for method in ["create", "read", "update", "delete"]:
                    allowed_keys = opts.get(method)
                    actions.update(
                        {f"{ app }.{ model }.{ method }": allowed_keys or []}
                    )
        roles[role] = get_nodes(actions)
    return roles


def write_roles(roles):
    with open(FILE_OUT_PY, "w") as file:
        file.write(f"ROLES = { roles }")
    with open(FILE_OUT_JS, "w") as file:
        file.write(f"export default { json.dumps(roles, sort_keys=True, indent=4) }")


class Command(BaseCommand):
    help = "Create <roles.py> from <configs/roles.yaml>"

    def handle(self, *args, **kwargs):
        try:
            write_roles(load_yaml())
            msg = "successfully created <roles.py> and <roles.js>"
            size = len(msg) + 4
            print("\n" + ("#" * size) + "\n# " + msg + " #\n" + ("#" * size))
        except Exception as e:
            print(e)
            raise CommandError("Initalization failed.")
