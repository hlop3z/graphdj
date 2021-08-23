## **Shell** 
```sh
python -m pipenv shell
```

## **Run** 
```sh
python -m pipenv run {command}
```

## Install to **Core** 
```sh
python -m pipenv install {package_or_module_name}
```


## Install to **Development** 
```sh
python -m pipenv install {package_or_module_name} --dev
```


## Save **Requirements** for Production & Development 
```sh
python -m pipenv lock
```


## Recreate in **Production** 
```sh
python -m pipenv install --ignore-pipfile
```


## Recreate in **Development** 
```sh
python -m pipenv install --dev
```


## Detection of **Security Vulnerabilities**
```sh
python -m pipenv check
```


## Tree-like structure **Dependencies**
```sh
python -m pipenv graph
```
