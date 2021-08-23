```py
import graphdj
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.views import GraphQLView

# Require Login
class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass

# The Schema
schema = graphdj.schema()

# Middleware Setup
middleware = []
if not settings.DEBUG:
    middleware.append(graphdj.DisableIntrospect)

# GraphQL Api
GapiView = csrf_exempt(
    #GraphQLView or PrivateGraphQLView
    PrivateGraphQLView.as_view(graphiql=settings.DEBUG, schema=schema, middleware=middleware)
)

# URLs
urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", GapiView),
]
```