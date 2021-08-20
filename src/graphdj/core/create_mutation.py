"""
[Expected Example-Output]
class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = "__all__"

class ModelType(DjangoObjectType):
    class Meta:
        model = Model
        fields = "__all__"
        interfaces = (graphene.relay.Node,)

class ModelMutation(DjangoModelFormMutation, relay.ClientIDMutation):
    Model = graphene.Field(ModelNode)

    class Meta:
        form_class = ModelForm

    class Input:
        ids = graphene.List(graphene.ID)
        del = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        # ...
        pass
"""

import graphene
from django.forms import ModelForm
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_relay import from_global_id

from .access import (
    check_request,
    get_access,
    get_related,
    get_related_superuser,
    get_role,
)
from .base_model import ModelGraphQL
from .create_docs import description


def create_class_meta(meta):
    """Create <Meta> Class."""
    return {"Meta": type("Meta", (object,), meta)}


def update_many(objects, inputs):
    """Django-Model objects.update with save()"""
    first_instance = None
    if objects:
        objects.update(**inputs)
        for instance in objects:
            instance.save()
            if not first_instance:
                first_instance = instance
    return first_instance


def create_mutation(model, app):
    """Create Class-Mutation."""
    app_name_lower = app.name.lower()
    type_name = f"{ app_name_lower }{ app.model.name }Type"
    mutation_name = f"{ app_name_lower }{ app.model.name }Mutation"
    form_name = f"{ app_name_lower }{ app.model.name }Form"
    api_uri = f"{ app_name_lower }_{ app.model.one }_editor"
    model_uri = f"{ app_name_lower }.{ app.model.one }"

    # Setup Form Configurations
    meta_form = dict()
    meta_form["model"] = model
    meta_form["fields"] = "__all__"

    # Setup Type Configurations
    meta_type = dict()
    meta_type["model"] = model
    meta_type["interfaces"] = (graphene.relay.Node,)

    # Create ModelForm
    create_class_form = type(
        form_name,
        (ModelForm,),
        create_class_meta(meta_form),
    )

    # Create ModelType
    create_class_type = type(
        type_name,
        (DjangoObjectType,),
        create_class_meta(meta_type),
    )

    # Create Real Mutation
    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        user_base = get_role(info.context.user)
        user_base.model = model_uri
        user_base.form = create_class_form
        instance = None
        ids = None
        if "id" in kwargs:
            kwargs["id"] = from_global_id(kwargs["id"])[1]
            ids = [kwargs["id"]]
            del kwargs["id"]
        if "ids" in kwargs:
            kwargs["ids"] = [from_global_id(xid)[1] for xid in kwargs["ids"]]
            ids = kwargs["ids"]
            del kwargs["ids"]
        # Do => <UPDATE>
        if ids and not kwargs.get("del"):
            """
            .##..##..#####...#####....####...######..######.
            .##..##..##..##..##..##..##..##....##....##.....
            .##..##..#####...##..##..######....##....####...
            .##..##..##......##..##..##..##....##....##.....
            ..####...##......#####...##..##....##....######.
            """
            user = get_access(user_base, app.perm.update)
            user.crud = "update"
            user.is_allowed = check_request(user, kwargs)
            user.update = update_many
            if info.context.user.is_superuser:
                kwargs = get_related_superuser(model, kwargs)
            else:
                kwargs = get_related(user, kwargs)
            instance = ModelGraphQL.update(
                user,
                model,
                info,
                ids,
                kwargs,
            )
        # Do => <DELETE>
        elif ids and kwargs.get("del"):
            """
            .#####...######..##......######..######..######.
            .##..##..##......##......##........##....##.....
            .##..##..####....##......####......##....####...
            .##..##..##......##......##........##....##.....
            .#####...######..######..######....##....######.
            """
            user = get_access(user_base, app.perm.delete)
            user.crud = "delete"
            user.is_allowed = check_request(user, kwargs)
            objects = ModelGraphQL.delete(
                user,
                model,
                info,
                ids,
            )
            if objects:
                objects.delete()
        # Do => <CREATE>
        else:
            """
            ..####...#####...######...####...######..######.
            .##..##..##..##..##......##..##....##....##.....
            .##......#####...####....######....##....####...
            .##..##..##..##..##......##..##....##....##.....
            ..####...##..##..######..##..##....##....######.
            """
            user = get_access(user_base, app.perm.create)
            user.crud = "create"
            user.is_allowed = check_request(user, kwargs)
            user.create = model.objects.create
            if info.context.user.is_superuser:
                kwargs = get_related_superuser(model, kwargs)
            else:
                kwargs = get_related(user, kwargs)
            instance = ModelGraphQL.create(
                user,
                model,
                info,
                kwargs,
            )
        dict_out = {app.model.one: instance}
        return class_mutation(**dict_out)

    # Create Description
    model_description = description(app, model, model_uri)

    # Setup Mutation
    setup_mutation = create_class_meta(
        {"form_class": create_class_form, "description": model_description}
    )
    setup_mutation[app.model.one] = graphene.Field(create_class_type)
    setup_mutation["mutate_and_get_payload"] = mutate_and_get_payload
    setup_mutation["Input"] = type(
        "Input",
        (object,),
        {
            "ids": graphene.List(
                graphene.ID, description="List of IDs to UPDATE or DELETE."
            ),
            "del": graphene.Boolean(description="Use (del: true) to DELETE."),
        },
    )
    class_mutation = type(
        mutation_name,
        (DjangoModelFormMutation,),
        setup_mutation,
    )

    # Return: class Mutation(graphene.ObjectType)
    return type(
        "Mutation",
        (graphene.ObjectType,),
        {api_uri: class_mutation.Field()},
    )
