# **Setup/**

## **Roles** & **Plural** words.
* roles/ 
> Use `yaml` **files** to create your **role(s)** configurations.
* plurals.py
> Configure `NOUNS = {}` to pluralize manually. For example: `{ "man" : "men" }` meaning `{ "singular" : "plural" }`

In the **example below** you will see that for the **create** and **update** we use the singular verb.
And for **read** we use the plural version of the word.

### **Create** & **Update**
> Use the "**singular**" verb as the **field-name**.

### **Read**
> Use the "**plural**" verb as the **field-name**.


<br />

### But . . . **Why?**
In the **example below** we have 2—Models (**Category & Ingredient**). <br />
When we want to call the **ingredients** from our **category** model we are calling for any **X—amount** of ingredients belonging to the selected category. <br />
Therefore, is easier to keep consistency if we make things singular and plural from the get-go.
You either want a **singular-object** or a **list-of-objects**.

```py
class Category(models.Model):
    name = models.CharField(max_length=100)


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="ingredients"
    )

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="recipes"
    )
```

<br />

## **Roles**
>
* Columns:  `[field_1, field_2, field_3: app.model]`
* Related: `[field_3 : app.model]`


## **Examples**
=== "setup/roles/example.yaml"
    ### Role.yaml
    > Role: **visitor**
    
    > App: **cookbook**

    > Models: **category, ingredient & recipe**

    ```yaml 
    # Role
    visitor:
    
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
    ### Plurals.py

    > It also uses **regex** to replace patterns based on **english pluralization rules** but in case something is misspelled you can fix it manually.

    > For example: **category —> categories**

    ```py 
    NOUNS = {
        "person": "people",
        "man"   : "men",
        "woman" : "women"
    }
    ```

=== "(Built-in) plurals"
    ### Built-in

    > It also uses **regex** to replace patterns based on **english pluralization rules** but in case something is misspelled you can fix it manually.
   
    > For example: **category —> categories**

    ```py
    NOUNS = {
        "aircraft"  : "aircraft",
        "alumna"    : "alumnae",
        "analysis"  : "analyses",
        "apex"      : "apices",
        "bison"     : "bison",
        "cactus"    : "cacti",
        "child"     : "children",
        "codex"     : "codices",
        "crisis"    : "crises",
        "criterion" : "criteria",
        "curriculum": "curricula",
        "datum"     : "data",
        "diagnosis" : "diagnoses",
        "ellipsis"  : "ellipses",
        "erratum"   : "errata",
        "fish"      : "fish",
        "focus"     : "foci",
        "foot"      : "feet",
        "genus"     : "genera",
        "goose"     : "geese",
        "index"     : "indices",
        "larva"     : "larvae",
        "louse"     : "lice",
        "man"       : "men",
        "means"     : "means",
        "mouse"     : "mice",
        "oasis"     : "oases",
        "ox"        : "oxen",
        "person"    : "people",
        "quiz"      : "quizzes",
        "series"    : "series",
        "sheep"     : "sheep",
        "species"   : "species",
        "swine"     : "swine",
        "tooth"     : "teeth",
        "trout"     : "trout",
        "tuna"      : "tuna",
        "vita"      : "vitae",
        "woman"     : "women",
    }
    ```

<br /><br />

