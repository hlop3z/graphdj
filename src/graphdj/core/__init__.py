"""Graphene-Django C.R.U.D Util
    Auto-Generate C.R.U.D Function from Model.

"""
import types

import graphene
from django.apps import apps as django_apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from .__base__ import *
from .create_docs import core_description
from .create_mutation import create_mutation
from .create_query import create_query
from .pluralize import pluralize


def register_admin(apps_list):
    """Register to Django's Admin"""
    for app in apps_list:
        for model in django_apps.get_app_config(app).get_models():
            try:
                admin.site.register(model)
            except AlreadyRegistered:
                pass


def register_graphql(apps_list):
    """Register Graphene Query & Mutation"""
    if DJANGO_ADMIN:
        register_admin(apps_list)
    queries = []
    mutations = []
    for app in apps_list:
        for model in django_apps.get_app_config(app).get_models():
            setup_info = model_to_app_info(model)
            # Fix Plural
            model._meta.verbose_name_plural = setup_info.model.many
            # Append Query
            queries.append(create_query(model, setup_info))
            # Append Mutation
            mutations.append(create_mutation(model, setup_info))
    return types.SimpleNamespace(Query=queries, Mutation=mutations)


def schema():
    """Build Graphene Schema"""
    params = dict()
    the_docs = core_description(GRAPHDJ_APPS)
    the_apps = register_graphql(GRAPHDJ_APPS)

    class Query(*the_apps.Query, graphene.ObjectType):
        """Query Wrapper"""

        class Meta:
            description = the_docs(QUERY_INFO)

    class Mutation(*the_apps.Mutation, graphene.ObjectType):
        """Mutation Wrapper"""

        class Meta:
            description = the_docs(MUTATION_INFO)

    if GRAPHDJ_APPS:
        params["query"] = Query
        params["mutation"] = Mutation

    return graphene.Schema(**params, auto_camelcase=CAMELCASE)
