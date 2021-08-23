## **Run Server** — Development Mode
```sh
sh rundevops.sh
```

## <a href="http://127.0.0.1:8000/graphql/" target="_blank">Go to the Server!</a>

> **Copy & Paste** the code below.

```graphql
query availableQueries {
  __schema {
    queryType {
      fields {
        name
      }
    }
  }
}

query availableMutations {
  __schema {
    mutationType {
      fields {
        name
      }
    }
  }
}

mutation createCategory {
  cookbookCategoryEditor(input: {name: "hello"}) {
    category {
      id
      name
    }
  }
}

mutation updateCategory {
  cookbookCategoryEditor(input: {ids: "a_relay_id(s)", name: "proteins"}) {
    category {
      id
      name
    }
  }
}

mutation deleteCategory {
  cookbookCategoryEditor(input: {ids: "a_relay_id(s)", del: true}) {
    category {
      id
      name
    }
  }
}

query cookbookCategory {
  cookbookCategory(id: "a_relay_id") {
    id
    name
  }
}

query cookbookCategories {
  cookbookCategories {
    edges {
      node {
        id
        name
        ingredients {
          edges {
            node {
              id
              name
              recipes {
                edges {
                  node {
                    id
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```