"""C.R.U.D
    Basic C.R.U.D handler.
"""


class ModelGraphQL:
    """Django GraphQL Crud System"""

    @staticmethod
    def create(this, model, info, kwargs):
        """Create"""
        return_value = None
        if this.is_allowed:
            return_value = model.Graphql.create(this, model, info, kwargs)
        return return_value

    @staticmethod
    def update(this, model, info, ids, kwargs):
        """Update"""
        return_value = None
        if this.is_allowed:
            return_value = model.Graphql.update(this, model, info, ids, kwargs)
        return return_value

    @staticmethod
    def delete(this, model, info, ids):
        """Delete"""
        return_value = None
        if this.is_allowed:
            return_value = model.Graphql.delete(this, model, info, ids)
        return return_value

    @staticmethod
    def read_one(this, model, info, id):
        """Read-One"""
        return_value = None
        if this.is_allowed:
            return_value = model.Graphql.read_one(this, model, info, id)
        return return_value

    @staticmethod
    def read_all(this, model, info, **kwargs):
        """Read-All"""
        return_value = None
        if this.is_allowed:
            return_value = model.Graphql.read_all(this, model, info, **kwargs)
        return return_value
