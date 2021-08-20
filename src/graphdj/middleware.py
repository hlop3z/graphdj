from graphql import GraphQLError


class DisableIntrospect:
    def resolve(self, next, root, info, **kwargs):
        if info.field_name.lower() in ["__schema", "__introspection"]:
            raise GraphQLError("Introspection disabled.")
        return next(root, info, **kwargs)
