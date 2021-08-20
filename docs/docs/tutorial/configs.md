## Important **paths** to remember.
* project_name/settings/common.py —> **settings.py**
* project_name/urls.py
* setup/roles/any-custom-role-belongs-here.yaml

=== "settings.py"

    ```py
    import os
    import sys

    from core.roles import ROLES

    # Include apps/
    sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

    # Include Core Apps
    INSTALLED_APPS += [
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
            0: "admin",
            1: "customer",
            2: "employee",
            3: "manager",
        },
        "APPS": [
            "app_1",
            "app_2",
            "app_3",
            "app_4",
            # ...
        ],
    }
    INSTALLED_APPS.extend(GRAPHDJ["APPS"])
    ```

=== "urls.py"

    ```py
    import graphdj
    from django.conf import settings
    from django.contrib import admin
    from django.urls import path
    from django.views.decorators.csrf import csrf_exempt
    from graphene_django.views import GraphQLView

    # Require Login
    class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
        pass

    # The Schema
    schema = graphdj.schema()

    # Setup
    middleware = []
    if not settings.DEBUG:
        middleware.append(graphdj.DisableIntrospect)

    # GraphQL Api
    GapiView = csrf_exempt(
        #GraphQLView
        PrivateGraphQLView.as_view(graphiql=settings.DEBUG, schema=schema, middleware=middleware)
    )

    # URLs
    urlpatterns = [
        path("admin/", admin.site.urls),
        path("graphql/", GapiView),
    ]
    ```

=== "setup/roles/example.yaml"
    ```yaml 
    # Role
    customer:
    
        # App
        cookbook:

            # Model-1
            category: 
                create : [id, name]
                update : [id, name]
                read   : [id, name, ingredients: cookbook.ingredient]
                delete : [del]

            # Model-2
            ingredient: 
                create : [id, name, category: cookbook.category]
                update : [id, name, category: cookbook.category]
                read   : [id, name, recipes: cookbook.recipe]
                delete : [del]

            # Model-3
            recipe: 
                create : [id, name]
                update : [id, name]
                read   : [id, name]
                delete : [del]
    ```

=== "setup/plurals.py"
    ```py 
    NOUNS = {
        "person": "people",
        "man": "men",
        "woman": "women"
    }
    ```