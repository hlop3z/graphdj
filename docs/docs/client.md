# Client — **Request**

=== "JavaScript"

    ```js
    /**
    * GraphQL - Quering
    */
    
    const Query = `
    query getMovie($id: Int) {
      movie(id: $id) {
        id
        title
        actors {
          id
          name
        }
      }
    }
    `

    /**
    * GraphQL - Variables
    */

    const Variables = {
      "id" : 1
    }


    /**
    * Fetch - Data
    */

    fetch('http://127.0.0.1:8000/graphql/', {
      method: 'POST',
      mode: 'cors',
      body: JSON.stringify({
        query: Query,
        variables: Variables,
      }),
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then( (res) => res.json() )
    .then( (result) => console.log( result ) );
    ```

=== "Python"

    ```py 
    import requests

    Query = """
    query getMovie($id: Int) {
      movie(id: $id) {
        id
        title
        actors {
          id
          name
        }
      }
    }
    """

    Variables = { 
      "id" : 1
    }

    url = 'http://127.0.0.1:8000/graphql/'

    r = requests.post(url, json={
        'query': Query,
        'variables' : Variables
    })

    print( r.status_code )
    print( r.json() )
    ```