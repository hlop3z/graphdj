Welcome to **GraphDJ**.

**GraphDJ** is a Django Module (aka: **App**) that’s written to **ease-development**. Which makes your **Django-Models** more powerful right **out-of-the-box**.

## Install
```sh
python -m pip install graphdj
```

## Dependencies
* [Django](https://github.com/django/django)
* [Graphene-Django](https://github.com/graphql-python/graphene-django)
* [Django-Filter](https://github.com/carltongibson/django-filter)
* [PyYAML](https://github.com/yaml/pyyaml)
* [Python-JSON-Logger](https://github.com/madzak/python-json-logger)

## Goal
> To simplify building the **C.R.U.D** system & automate the **Documentation** of the **API**.

## Features
* Role Based Access Control (**RBAC**).
* Model's Create, Read, Update & Delete (**CRUD**) integrated functions yet customizables.
* Transform Roles & Models into **JavaScript** files.
* Auto-generated **documentation** from the apps and their models.
* **Pluralization** of the model's name.
> **Example:** Person —> People

## Important **paths** to **remember**.
* project_name/setup/roles/**any-custom-role-belongs-here.yaml**
* project_name/setup/**plurals.py**
* project_name/project_name/**urls.py**
* project_name/project_name/**settings.py**
> In the **Tutorial** this file is called **common.py** <br />
> project_name/project_name/settings/**common.py**

<br /><br />