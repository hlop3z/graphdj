"""
[Expected Example-Output]
class MyModelNode(DjangoObjectType):
    class Meta:
        model = MyModel
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "category": ["exact"],
            "category__name": ["exact"],
        }
        interfaces = (graphene.relay.Node,)
"""
import graphene
from graphene_django import DjangoObjectType

from .access import check_request, get_access, get_role
from .base_model import ModelGraphQL
from .get_fields import get_fields


def create_class_meta(meta):
    """Create <Meta> Class."""
    return type("Meta", (object,), meta)


def create_node(model, app):
    """Create GraphQL Node."""
    meta_setup = {
        "model": model,
        "fields": "__all__",
        "interfaces": (graphene.relay.Node,),
        "filter_fields": app.model.filters,
    }

    model_uri = f"{ app.name }.{ app.model.one }"

    # get_node => resolve_one
    @classmethod
    def resolve_one(cls, info, id):
        """
        .#####...######...####...#####............####...##..##..######.
        .##..##..##......##..##..##..##..........##..##..###.##..##.....
        .#####...####....######..##..##..######..##..##..##.###..####...
        .##..##..##......##..##..##..##..........##..##..##..##..##.....
        .##..##..######..##..##..#####............####...##..##..######.
        """
        user_base = get_role(info.context.user)
        user_base.model = model_uri
        user = get_access(user_base, app.perm.read)
        requested = get_fields(info)
        user.crud = "read-one"
        user.model = model_uri
        user.is_allowed = check_request(user, requested)
        return ModelGraphQL.read_one(user, model, info, id)

    # Create => class ModelNode(DjangoObjectType)
    class_name = f"""{ app.name.title() }{ app.model.name }Node"""
    return type(
        class_name,
        (DjangoObjectType,),
        {"Meta": create_class_meta(meta_setup), "get_node": resolve_one},
    )
