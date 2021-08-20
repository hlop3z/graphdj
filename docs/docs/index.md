Welcome to the **GraphDJ**.

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

## **Setup/** — See [Configs](/tutorial/configs.html) for example.
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

## **Settings/** — See [Configs](/tutorial/configs.html) for example.
* base.py — Django's default settings.
* common.py — Used in (development, test & production)
* development.py
* i18n.py
* production.py
* test.py