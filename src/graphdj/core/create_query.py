"""
[Expected Example-Output]
class Query(graphene.ObjectType):
    # ONE-or-MANY
    <app-name>_mymodel = relay.Node.Field(MyModelNode)
    <app-name>_mymodels = DjangoFilterConnectionField(MyModelNode)
"""

import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .access import check_request, get_access, get_role
from .base_model import ModelGraphQL
from .create_docs import description
from .create_node import create_node
from .get_fields import get_fields


# Create => class Query(graphene.ObjectType)
def create_query(model, app) -> graphene.ObjectType:
    """Create GraphQL Query"""
    relay_node = create_node(model, app)
    app_name_lower = app.name.lower()
    get_one = f"{ app_name_lower }_{ app.model.one }"
    get_many = f"{ app_name_lower }_{ app.model.many }"
    model_uri = f"{ app_name_lower }.{ app.model.one }"

    methods = [i for i in dir(model.Graphql) if not i.startswith("__")]
    for method in methods:
        current_method = getattr(model.Graphql, method)
        setattr(model.Graphql, method, staticmethod(current_method))

    def resolve_all(self, info, **kwargs):
        """
        .#####...######...####...#####...........##......######...####...######.
        .##..##..##......##..##..##..##..........##........##....##........##...
        .#####...####....######..##..##..######..##........##.....####.....##...
        .##..##..##......##..##..##..##..........##........##........##....##...
        .##..##..######..##..##..#####...........######..######...####.....##...
        """
        user_base = get_role(info.context.user)
        user = get_access(user_base, app.perm.read)
        requested = get_fields(info)  # This?
        user.model = model_uri
        user.crud = "read-many"
        user.is_allowed = check_request(user, requested)
        return_value = ModelGraphQL.read_all(user, model, info, **kwargs)
        if return_value is None:
            return model.objects.none()
        return return_value

    # Create Description
    model_description = description(app, model, model_uri)

    # Return ObjectType
    return type(
        "Query",
        (graphene.ObjectType,),
        {
            get_one: graphene.relay.Node.Field(
                relay_node,
                description=model_description,
            ),
            get_many: DjangoFilterConnectionField(
                relay_node, description=model_description
            ),
            f"resolve_{ get_many }": resolve_all,
        },
    )
