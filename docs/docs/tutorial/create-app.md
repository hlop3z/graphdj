> Where **{app_name}** is your app.

```sh
python -m pipenv run python manage.py create-app {app_name}
```

<br />

The following example is a modified copy from [Graphene Django](https://docs.graphene-python.org/)

## Create 
```sh
python -m pipenv run python manage.py create-app cookbook
```

## Models
```py
# apps/cookbook/models.py
from django.db import models
from graphdj.models import GraphqlBase

class Category(GraphqlBase):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ingredient(GraphqlBase):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    category = models.ForeignKey(
        Category, related_name="ingredients", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Recipe(GraphqlBase):
    name = models.CharField(max_length=100)
    ingredient = models.ForeignKey(
        Ingredient, related_name="recipes", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
```

## Add in **settings/common.py** under "**APPS**"
```py
GRAPHDJ = {
    # ...
    "APPS": [
        "cookbook",
        # ...
    ],
}
INSTALLED_APPS.extend(GRAPHDJ["APPS"])
```


## Run Migrations
```sh
python -m pipenv run python manage.py makemigrations cookbook
python -m pipenv run python manage.py migrate
```