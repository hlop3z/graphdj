"""Base
    * Get the app-settings.
    * Create permissions.
    * Get all available filters.
    * Get model's info.
"""
import types

from django.conf import settings
from django.db import models

from .pluralize import pluralize

# Get Settings
if not settings.GRAPHDJ:
    raise ValueError("Please configure GraphDJ.")

ROLES = settings.GRAPHDJ.get("ROLES") or {}
ROLES_ACCESS = settings.GRAPHDJ.get("ROLES_ACCESS") or {}
GRAPHDJ_APPS = settings.GRAPHDJ.get("APPS") or []
QUERY_INFO = settings.GRAPHDJ.get("QUERIES_INFO") or "My Queries description"
MUTATION_INFO = settings.GRAPHDJ.get("MUTATIONS_INFO") or "My Mutations description"
DJANGO_ADMIN = settings.GRAPHDJ.get("ADMIN")
CAMELCASE = settings.GRAPHDJ.get("CAMELCASE")
LOGGING = settings.GRAPHDJ.get("LOGGING")


if LOGGING is None:
    LOGGING = False

if CAMELCASE is None:
    CAMELCASE = False

if DJANGO_ADMIN is None:
    DJANGO_ADMIN = False


def get_filters(field):
    """Filter depending on the Field-Type"""
    if field.name == "id":
        the_lookups = ["exact", "in", "isnull"]
    elif field.get_internal_type() in ["BooleanField"]:
        the_lookups = ["exact", "isnull"]
    elif field.get_internal_type() in [
        "PositiveSmallIntegerField",
        "Positi­veI­nte­ger­Field",
        "Intege­rField",
        "FloatField",
        "SmallI­nte­ger­Field",
        "BigInt­ege­rField",
    ]:
        the_lookups = ["exact", "gt", "gte", "lt", "lte", "in", "range", "isnull"]
    elif field.get_internal_type() in ["CharField", "TextField"]:
        the_lookups = [
            f
            for f in list(field.get_lookups().keys())
            if f not in ["gt", "gte", "lt", "lte", "range", "iexact"]
        ]
    elif field.related_model:
        the_lookups = ["in", "exact", "isnull"]
    else:
        the_lookups = list(field.get_lookups().keys())
    return the_lookups


def create_perms(app: str, model: str) -> str:
    """Create permissions for C.R.U.D role-based system."""
    perm = lambda crud: f"""{ app }.{ model }.{ crud }"""
    return types.SimpleNamespace(
        **{method: perm(method) for method in ["create", "read", "update", "delete"]}
    )


def model_filters(model):
    """Get all of the available filters in each field."""
    filters = {}
    for field in model._meta.fields:
        field.blank = True
        if field.related_model:
            for child in field.related_model._meta.fields:
                the_lookups = get_filters(child)
                filters[f"{field.name}__{child.name}"] = the_lookups
        else:
            the_lookups = get_filters(field)
            filters[field.name] = the_lookups
    # Easy IDs
    filters["id"] = ["exact", "in"]
    return filters


def model_to_app_info(model):
    """Get the model's info."""
    # Original <Fields>
    the_filters = model_filters(model)
    app_name = model._meta.app_label
    model_name = model.__name__
    # Transform
    model_name_singular = model_name.lower()
    model_name_plural = pluralize(model_name_singular)
    model_perms = create_perms(app_name, model_name_singular)
    # Namespacing
    model_namespace = types.SimpleNamespace(
        name=model_name,
        one=model_name_singular,
        many=model_name_plural,
        filters=the_filters,
    )
    return types.SimpleNamespace(model=model_namespace, name=app_name, perm=model_perms)
