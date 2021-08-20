Welcome to the **GraphDJ**.

**GraphDJ** is a Django Module (aka: **App**) that’s written to **ease-development**. Which makes your **Django-Models** more powerful right **out-of-the-box**.

## Dependencies
* [Django](https://github.com/django/django)
* [Graphene-Django](https://github.com/graphql-python/graphene-django)
* [Django-Filter](https://github.com/carltongibson/django-filter)
* [PyYAML](https://github.com/yaml/pyyaml)
* [Python-JSON-Logger](https://github.com/madzak/python-json-logger)

## Goal
> To simplify building the **C.R.U.D** system & automate the **Documentation** of the **API**.

## **Skeleton**
```
[project_name]/                     -->  Project Root.
├── data/                           -->  Any <data> for the project.
├── docs/                           -->  Write the <documentation> here.
├── scripts/                        -->  Write the <shell/bash> here.
├── [project_name]/                 -->  Write the <code> here. (Django Root)
│   ├── __init__.py
│   ├── apps/
│   ├── configs/
│   ├── core/
│   ├── scripts/
│   │
│   ├── [project_name]/
│   │   ├── settings/               -->  (Django Settings)
│   │   │   ├── __init__.py
│   │   │   ├── base.py             -->  (Django Defaults)
│   │   │   ├── common.py
│   │   │   ├── development.py
│   │   │   ├── i18n.py
│   │   │   ├── production.py
│   │   │   └── test.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── setup/                      -->  App Setup — [Roles]
│   │   ├── roles/
│   │   │   └── visitor.yaml
│   │   ├── __init__.py
│   │   └── plurals.py
│   │
│   ├── utils/
│   └── manage.py
├── run_server.sh
└── watcher.py                      -->  Code style enforcer & rating.
```

<br/><br/>


## **Setup/** — See [Configs](/tutorial/configs/) for example.
* roles/ 
> Use `yaml` **files** to create your **role(s)** configurations.
* plurals.py
> Configure `NOUNS = {}` to pluralize manually. For example: `{ "man" : "men" }` meaning `{ "singular" : "plural" }`

## **Roles**
* Columns:  `[field_1, field_2, field_3: app.model]`
* Related: `[field_3 : app.model]`

### **Create** & **Update**
> Use the "**singular**" verb as the **field-name**.

### **Read**
> Use the "**plural**" verb as the **field-name**.

<br/><br/>

## **Settings/** — See [Configs](/tutorial/configs/) for example.
* base.py — Django's default settings.
* common.py — Used in (development, test & production)
* development.py
* i18n.py
* production.py
* test.py