# **Settings.py**

After setting up your **roles**. You can update your **core/roles.py** file by running the following custom **django command**.
```sh
python manage.py build-roles
```

You can then use the roles inside your settings following the example below.

## **Fields**:
* **ADMIN** —> (Default: `False`) Auto-include models in your **Django's Admin** page. 
* **CAMELCASE** —>  (Default: `False`) Transform **cookbook_category** into **cookbookCategory**.
* **LOGGING** —> (Default: `False`) Log the requests.
* **ROLES_ACCESS** —> Roles and their corresponding rights.
* **DEFAULT_ROLE**  —> Default role for new users.
* **QUERIES_INFO**  —> Query's description.
* **MUTATIONS_INFO**  —> Mutation's description.
* **ROLES**  —> Your roles.
* **APPS**  —> Your apps.


```py
import os
import sys

from core.roles import ROLES

# Include apps/
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# Include Core Apps
INSTALLED_APPS += [
    # Users
    "users",
    # Filters
    "django_filters",
    # GraphQL
    "graphene_django",
    # GraphDJ
    "graphdj",
    # CORS
    #"corsheaders",
]

# GraphQL -> Graphene
GRAPHENE = {
    "ATOMIC_MUTATIONS": True,
    "RELAY_CONNECTION_MAX_LIMIT": 100,
}

# Add your <project-apps> here.
GRAPHDJ = {
    "ADMIN": True,
    "CAMELCASE": True,
    "LOGGING": True,
    "ROLES_ACCESS": ROLES,
    "DEFAULT_ROLE": 1,
    "QUERIES_INFO": "Awesome Queries!",
    "MUTATIONS_INFO": "Awesome Mutations!",
    "ROLES": {
        0: "visitor",
        1: "admin",
        2: "customer",
        # etc . . . 
    },
    "APPS": [
        "app_1",
        "app_2",
        "app_3",
        # etc . . . 
    ],
}
INSTALLED_APPS.extend(GRAPHDJ["APPS"])
```
