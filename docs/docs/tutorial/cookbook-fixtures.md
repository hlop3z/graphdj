Copy and Paste the data in **fixtures.JSON** to the file **apps/cookbook/fixtures/cookbook.json**

```sh
mkdir apps/cookbook/fixtures
touch apps/cookbook/fixtures/cookbook.json
```

=== "Run Command"
    ```sh
    python -m pipenv run python manage.py loaddata cookbook
    ```

=== "fixtures.JSON"
    ```json 
    [
        {
          "model": "cookbook.category",
          "pk": 1,
          "fields": {
            "name": "Dairy"
          }
        },
        {
          "model": "cookbook.category",
          "pk": 2,
          "fields": {
            "name": "Meat"
          }
        },
        {
          "model": "cookbook.ingredient",
          "pk": 1,
          "fields": {
            "name": "Eggs",
            "notes": "Good old eggs",
            "category": 1
          }
        },
        {
          "model": "cookbook.ingredient",
          "pk": 2,
          "fields": {
            "name": "Milk",
            "notes": "Comes from a cow",
            "category": 1
          }
        },
        {
          "model": "cookbook.ingredient",
          "pk": 3,
          "fields": {
            "name": "Beef",
            "notes": "Much like milk, this comes from a cow",
            "category": 2
          }
        },
        {
          "model": "cookbook.ingredient",
          "pk": 4,
          "fields": {
            "name": "Chicken",
            "notes": "Definitely doesn't come from a cow",
            "category": 2
          }
        },
        {
          "model": "cookbook.recipe",
          "pk": 1,
          "fields": {
            "name": "Recipe-1",
            "ingredient": 1
          }
        },
        {
          "model": "cookbook.recipe",
          "pk": 2,
          "fields": {
            "name": "Recipe-2",
            "ingredient": 1
          }
        },
        {
          "model": "cookbook.recipe",
          "pk": 2,
          "fields": {
            "name": "Recipe-3",
            "ingredient": 2
          }
        }
    ]
    ```  