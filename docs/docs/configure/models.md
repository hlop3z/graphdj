=== "models.py"

    ```py
    from django.db import models

    class Category(models.Model):
        """This is a Model Description."""

        name = models.CharField(
            max_length=100, 
            help_text="Field Description."
        )

        def __str__(self):
            return self.name

        class Graphql:
            """Model C.R.U.D"""

            def create(this, model, info, kwargs):
                form = this.form(kwargs)
                if form.is_valid():
                    return this.create(**kwargs)

            def update(this, model, info, ids, kwargs):
                form = this.form(kwargs)
                if form.is_valid():
                    objects = model.objects.filter(id__in=ids)
                    return this.update(objects, kwargs)

            def delete(this, model, info, ids):
                return model.objects.filter(id__in=ids)

            def read_one(this, model, info, id):
                return model.objects.get(pk=id)

            def read_all(this, model, info, **kwargs):
                return model.objects.filter()
    ```


=== "with GraphqlBase"

    ```py
    from django.db import models
    from graphdj.models import GraphqlBase

    class Category(GraphqlBase):
        """This is a Model Description."""

        name = models.CharField(
            max_length=100, 
            help_text="Field Description."
        )

        def __str__(self):
            return self.name
    ```

=== "with GraphqlMixin"

    ```py
    from django.db import models
    from graphdj.models import GraphqlMixin

    class Category(models.Model):
        """This is a Model Description."""

        name = models.CharField(
            max_length=100, 
            help_text="Field Description."
        )

        def __str__(self):
            return self.name

        class Graphql(GraphqlMixin):
            pass
    ```