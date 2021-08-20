"""Documentation
    * Create Node Description
    * Create Api Documentation
"""

import string

from django.apps import apps as django_apps


def description(app, model, model_uri):
    """Node Description"""
    all_fields = []
    for i in model._meta.fields:
        if not i.related_model:
            all_fields.append(("\n* `" + i.name + "`"))
        else:
            all_fields.append(("\n* `" + i.name + "(model)`"))

    model_fields = "".join(all_fields)

    return string.Template(
        """
**App:** `$app`

---

**Model:** `$model —> [$models]`

---

**URI:** `$uri`

---

**Fields:** $fields

---

**Description:**
```
$description
```

---
        """
    ).substitute(
        app=app.name.title(),
        model=app.model.one.title(),
        models=app.model.many.title(),
        uri=model_uri,
        fields=model_fields,
        description=model.__doc__,
    )


def core_description(apps_list):
    """Api Documentation"""
    return_value = {}
    for app in apps_list:
        return_value[app.title()] = list()
        for model in django_apps.get_app_config(app).get_models():
            return_value[app.title()].append(model.__name__)
    the_docs = []
    for app, models in return_value.items():
        the_docs.append(("**" + app + ":**" + "\n\n`(" + ", ".join(models) + ")`\n"))
    return lambda description: string.Template(
        """
# Applications

---

$apps

# Description

---

$description
        """
    ).substitute(apps="\n".join(sorted(the_docs)), description=description)
