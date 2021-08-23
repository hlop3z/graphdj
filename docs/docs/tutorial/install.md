```sh
python -m pipenv install django
```

## Start project from **Template**
```sh
python -m pipenv run django-admin startproject \
--template=https://github.com/hlop3z/graphdj-template/archive/refs/heads/main.zip \
--name=Procfile \
write_your_project_name_here
```

## **Settings/** 
* base.py — Django's default settings.
* **common.py** — Used in (development, test & production)
* development.py
* i18n.py
* production.py
* test.py

> **common.py** This is where most **settings** will live under.

## Then Change Directory (**cd**) to your project.

```sh
cd write_your_project_name_here
```

## Then — Recreate **Development**
```sh
python -m pipenv install --dev
```

## Then — Move file **.env**
```sh
mv .env_example.cfg .env.cfg
```

## Create **Logs Dir** & **Server-Log File**.
```sh
mkdir -p logs
touch logs/server.jsonl
```

## Then — Create a **Secret-Key**
> After creating the **Secret-Key** add it inside the **.env.cfg** file in the **DJANGO_SECRET_KEY** variable.

> **Optionally**: You can **choose a size** as a parameter for example —> `keygen.sh 64`
```sh
sh scripts/keygen.sh
```

## Run Migrations
```sh
python -m pipenv run python manage.py makemigrations users
python -m pipenv run python manage.py migrate
```