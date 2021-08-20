from django.db import models
from graphql import GraphQLError


class GraphqlMixin:
    """Django Base-Model"""

    def create(this, model, info, kwargs):
        form = this.form(kwargs)
        if form.is_valid():
            return this.create(**kwargs)
        raise GraphQLError("Invalid values.")

    def update(this, model, info, ids, kwargs):
        form = this.form(kwargs)
        if form.is_valid():
            objects = model.objects.filter(id__in=ids)
            return this.update(objects, kwargs)
        raise GraphQLError("Invalid values.")

    def delete(this, model, info, ids):
        return model.objects.filter(id__in=ids)

    def read_one(this, model, info, id):
        return model.objects.get(pk=id)

    def read_all(this, model, info, **kwargs):
        return model.objects.all()


class GraphqlBase(models.Model):
    class Graphql(GraphqlMixin):
        pass

    class Meta:
        abstract = True
