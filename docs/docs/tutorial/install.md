## **Create** a file named **startproject.sh**
```sh
touch startproject.sh
nano startproject.sh
```

## **Copy & Paste** the content in **startproject.sh** to the file.

=== "run command"

    ```sh
    sh startproject.sh -n project_name
    ```

=== "startproject.sh"

    ```sh
    ISVALID=true

    # Command-Line <Arguments>
    while getopts n: flag
    do
        case "${flag}" in
            n) name=${OPTARG};;
        esac
    done

    if [ -z "$name" ]
        then
            ISVALID=false
            printf "\nPlease enter a name for the project. \n\n"
            printf "For example: \n"
            printf "\tstartproject -n project_name\n"
    fi


    # Do something with the <Arguments>
    if [ "$ISVALID" = true ] ; then
        # Create Folder (Project-Root)
        mkdir -p $name 

        # Change Directory
        cd $name

        # Project Folders
        mkdir -p docs scripts

        # Python Files
        touch .gitignore
        touch LICENSE.txt
        touch MANIFEST.in
        touch README.md

        # Django
        python -m pipenv install Django

        # GraphDJ
        #python -m pipenv install graphdj/dist/graphdj-0.0.1.tar.gz

        # Start Project
        python -m pipenv run django-admin startproject $name

        # Change Directory (Project-Django)
        cd $name

        # Create Folders
        mkdir -p apps core setup configs
        mkdir -p setup/roles
        mkdir -p core/javascript

        # Create Files
        touch __init__.py
        touch apps/__init__.py
        touch core/__init__.py
        touch setup/__init__.py
        touch setup/roles/visitor.yaml
        touch setup/plurals.py

        # Start App —> **API**
        python -m pipenv run python manage.py startapp api

        # Move App
        mv api apps/api

        # Change Directory (Core-Setup)
        cd $name

        # Make Settings Directory
        mkdir -p settings
        mv settings.py settings/base.py
        cd settings
        touch __init__.py
        echo "from .development import *" > __init__.py
        touch common.py
        touch development.py
        echo "from .base import *" > development.py
        touch i18n.py
        touch production.py
        echo "from .base import *" > production.py
        touch test.py
        
    fi
    ```

## Go to your **Project Folder**
```sh
cd project_name
```

## Go to your **Virtual-Environment**
```sh
python -m pipenv shell
```

## Go to your **Django Project**
```sh
cd project_name
```
