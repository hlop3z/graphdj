## Add to **apps/users/models.py**
```py
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models
from graphdj.models import GraphqlMixin

ROLES = settings.GRAPHDJ.get("ROLES")
DEFAULT_ROLE = settings.GRAPHDJ.get("DEFAULT_ROLE")


class User(AbstractUser):
    username = models.CharField(max_length=128, unique=True)
    role = models.PositiveSmallIntegerField(
        choices=ROLES.items(), blank=True, null=True, default=DEFAULT_ROLE
    )

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user"

    class Graphql(GraphqlMixin):
        pass
```

## Run Migrations
```sh
python manage.py makemigrations users
python manage.py migrate
```
