"""(RBAC) — Role Based Access Control
    check_request        : Check if the <User> has access to the requested <Model & Fields>
    get_role             : Get the <Role> of the <User>
    get_allowed_fields   : Get all of the allowed fields for the current <User>
    access_extra         : Get the fields that are <ForeignKeys>
    get_related          : Get the <related_model> of <ForeignKeys> from <RBAC>
    get_related_superuser: Get the <related_model> of <ForeignKeys> from the <Model> itself
    get_access           : Check what <access-rights> the current <User> has.
"""
import logging
import types

from django.apps import apps
from django.utils import timezone
from graphql import GraphQLError
from graphql_relay import from_global_id

from .__base__ import GUEST_NAME, LOGGING, ROLES, ROLES_ACCESS

# Logging & Error
logging.config.fileConfig("logging.ini", disable_existing_loggers=False)

ACCESS_ERROR_MESSAGE = "You don't have access."


get_id = lambda uid: from_global_id(uid)[1]


def check_request(user, requested) -> bool:
    """
    Check if user is allowed to do request.
    """
    if isinstance(requested, dict):
        requested = list(requested.keys())

    # Check Request
    is_allowed = all(elem in user.access for elem in requested)

    if user.user.is_superuser:
        is_allowed = True

    if LOGGING:
        # Log Request
        logging.info(
            {
                "meta": {
                    "type": "request",
                    "crud": user.crud,
                    "model": user.model,
                    "datetime": timezone.now(),
                },
                "message": {
                    "user_id": user.user.id,
                    "role": user.role,
                    "role_id": user.role_id,
                    "allowed": user.access,
                    "requested": requested,
                    "is_valid": is_allowed,
                },
            }
        )

    # Return Values
    if is_allowed:
        return is_allowed
    raise GraphQLError(ACCESS_ERROR_MESSAGE)


def get_role(user):
    """
    Get the user's role or default(GUEST_NAME)
    """
    if user.is_anonymous:
        return_value = types.SimpleNamespace(
            role=GUEST_NAME, role_id=0, user=user, relay_id=get_id
        )
    else:
        return_value = types.SimpleNamespace(
            role=ROLES[user.role], role_id=user.role, user=user, relay_id=get_id
        )
    # Role-User
    return return_value


def get_allowed_fields(access_rights):
    """
    Get fields names
    """
    get_val = lambda i: i if not "." in i else i.split(".")[1]
    return [get_val(i) for i in access_rights]


def access_extra(access_rights):
    """
    Check if field is related-model.
    """
    return_value = []
    for i in access_rights:
        if "." in i:
            item = i.split(".")
            return_value.append(tuple(item))
    return return_value


def get_related(user, kwargs):
    """
    Get related model from user's input.
    """
    for item in user.access_extra:
        if item[1] in kwargs:
            related_model = apps.get_model(item[0], item[1])
            kwargs[item[1]] = related_model.objects.get(pk=get_id(kwargs[item[1]]))
    return kwargs


def get_related_superuser(model, kwargs):
    """
    Get related model from user's input Super-User(ONLY).
    """
    for field in model._meta.fields:
        if field.related_model and field.name in kwargs.keys():
            kwargs[field.name] = field.related_model.objects.get(
                pk=get_id(kwargs[field.name])
            )
    return kwargs


def get_access(user, perm):
    """
    Get role from <core.roles> and access-rights.
    """
    if not user.user.is_superuser:
        active_access = ROLES_ACCESS.get(user.role) or {}
        user.is_allowed = False
        try:
            if perm.endswith("create") or perm.endswith("update"):
                user.access = get_allowed_fields(active_access[perm])
                user.access_extra = access_extra(active_access[perm])
            else:
                user.access = active_access[perm]
                user.access_extra = None
        except:
            if LOGGING:
                # Log Request
                logging.info(
                    {
                        "meta": {
                            "type": "access-error",
                            "datetime": timezone.now(),
                        },
                        "message": {
                            "requested": perm,
                            "user_id": user.user.id,
                            "role": user.role,
                            "role_id": user.role_id,
                        },
                    }
                )
            raise GraphQLError(ACCESS_ERROR_MESSAGE)
    else:
        user.access = []
        user.access_extra = []
    return user
