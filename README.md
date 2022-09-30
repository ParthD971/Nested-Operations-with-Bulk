## Nested Operations And Bulk Nested Operation

### Installing Project
1. Clone Project
```code
git clone https://github.com/ParthD971/Nested-Operations-with-Bulk.git
```
2. Install requirements.txt [Recommended: Create virtual environment]
```code
pip install -r requirements.txt
```
3. Create Database
```code
python manage.py migrate
```
4. Create SuperUser [Optional]
```code
python manage.py createsuperuser
```

### Endpoints
1. Creating Todo <br>

```code
Request type: POST 
Request URL: todo-nested/
```

<table>
  <tr>
    <th>Expected input data</th>
    <th>Expected output data</th>
  </tr>
  <tr>
    <td>
  
  ```python
  {
    "title": "Title of todo",
    "tasks": [
        {
            "title": "Title of task 1",
            "description": ""
        },
        {
            "title": "Title of task 1",
            "description": ""
        },
        ...
    ]
  }
  ```

  </td>
  <td>

  ```python
  {
    "id": 1,
    "title": "Title of todo",
    "tasks": [
        {
            "id": 1,
            "title": "Title of task 1",
            "description": ""
        },
        {
            "id": 2,
            "title": "Title of task 1",
            "description": ""
        },
        ...
    ]
  }
  ```

  </td>
  </tr>
</table>

2. Creating Task <br>

```code
Request type: POST 
Request URL: task-nested/
```

<table>
  <tr>
    <th>Expected input data</th>
    <th>Expected output data</th>
  </tr>
  <tr>
    <td>
  
  ```python
  {
    "title": "Task for drf",
    "description": "This is for DRF",
    "todo": {
        "title": "Todo 2"
    }
  }
  ```

  </td>
  <td>

  ```python
  {
    "id": 32,
    "title": "Task for drf",
    "description": "This is for DRF",
    "todo": {
        "id": 17,
        "title": "Todo 2"
    }
  }
  ```

  </td>
  </tr>
</table>


3. Bulk Creating Todo <br>

```code
Request type: POST 
Request URL: bulk-todo-nested/
```

<table>
  <tr>
    <th>Expected input data</th>
    <th>Expected output data</th>
  </tr>
  <tr>
    <td>
  
  ```python
  [
    {
        "title": "Todo 1",
        "tasks": [
            {
                "title": "Task 1",
                "description": "Complete DRF"
            },
            {
                "title": "Task 9",
                "description": "Complete DRF"
            }
        ]
    },
    {
        "title": "Todo 0",
        "tasks": [
            {
                "title": "Task 5",
                "description": "Complete DRF"
            },
            {
                "title": "Task 4",
                "description": "Complete DRF"
            }
        ]
    }
  ]
  ```

  </td>
  <td>

  ```python
  [
    {
        "id": 21,
        "title": "Todo 1",
        "tasks": [
            {
                "id": 39,
                "title": "Task 1",
                "description": "Complete DRF"
            },
            {
                "id": 40,
                "title": "Task 9",
                "description": "Complete DRF"
            }
        ]
    },
    {
        "id": 22,
        "title": "Todo 0",
        "tasks": [
            {
                "id": 41,
                "title": "Task 5",
                "description": "Complete DRF"
            },
            {
                "id": 42,
                "title": "Task 4",
                "description": "Complete DRF"
            }
        ]
    }
  ]
  ```

  </td>
  </tr>
</table>


4. Creating Post <br>

```code
Request type: POST 
Request URL: post/
```

<table>
  <tr>
    <th>Expected input data</th>
    <th>Expected output data</th>
  </tr>
  <tr>
    <td>
  
  ```python
  {
    "title": "post 7",
    "tags": [
        {
            "name": "tag 11"
        }, 
        {
            "name": "tag 2"
        }
    ]
  }
  ```

  </td>
  <td>

  ```python
  {
    "id": 7,
    "title": "post 7",
    "description": null,
    "published": true,
    "tags": [
        {
            "id": 4,
            "name": "tag 11"
        },
        {
            "id": 2,
            "name": "tag 2"
        }
    ]
  }
  ```

  </td>
  </tr>
</table>



5. Creating Book Details <br>

```code
Request type: POST 
Request URL: book-details/
```

<table>
  <tr>
    <th>Expected input data</th>
    <th>Expected output data</th>
  </tr>
  <tr>
    <td>
  
  ```python
  {
    "category": "Category 1",
    "rating": 2,
    "price": 20,
    "publish_date": "2022-09-12",
    "book": {
        "name": "Book 2",
        "author_name": "Author 1"
    }
    
  }
  ```

  </td>
  <td>

  ```python
  {
    "id": 4,
    "category": "Category 1",
    "rating": 2,
    "price": 20,
    "publish_date": "2022-09-12",
    "book": {
        "id": 4,
        "name": "Book 2",
        "author_name": ""
    }
  }
  ```

  </td>
  </tr>
</table>


6. Reading Todo <br>

```code
Request type: GET 
Request URL: todo-nested/
```

<table>
  <tr>
    <th>Expected output data</th>
  </tr>
  <tr>
    <td>
  
  ```pythonPOST
  [
    {
        "id": 29,
        "title": "Todo 2",
        "tasks": [
            {
                "id": 82,
                "title": "Title 1",
                "description": "Hey there!"
            }
        ]
    },
    {
        "id": 30,
        "title": "Todo 1",
        "tasks": [
            {
                "id": 83,
                "title": "Title 1",
                "description": "Hey there!"
            },
            {
                "id": 84,
                "title": "Title 1",
                "description": "Hey there!"
            }
        ]
    }
  ]
  ```

  </td>
  </tr>
</table>




7. Reading Task <br>

```code
Request type: GET 
Request URL: task-nested/
```

<table>
  <tr>
    <th>Expected output data</th>
  </tr>
  <tr>
    <td>
  
  ```pythonPOST
  [
    {
        "id": 79,
        "title": "Title 1",
        "description": "Hey there!",
        "todo": {
            "id": 29,
            "title": "Todo 2"
        }
    },
    {
        "id": 80,
        "title": "Title 1",
        "description": "Hey there!",
        "todo": {
            "id": 29,
            "title": "Todo 2"
        }
    }
  ]
  ```

  </td>
  </tr>
</table>



8. Reading Post <br>

```code
Request type: GET 
Request URL: post/
```

<table>
  <tr>
    <th>Expected output data</th>
  </tr>
  <tr>
    <td>
  
  ```pythonPOST
  [
    {
        "id": 1,
        "title": "post 1",
        "description": "",
        "published": true,
        "tags": [
            {
                "id": 1,
                "name": "tag 1"
            }
        ]
    },
    {
        "id": 2,
        "title": "post 2",
        "description": "",
        "published": true,
        "tags": [
            {
                "id": 3,
                "name": "Tag XYZ"
            },
            {
                "id": 2,
                "name": "tag 2"
            }
        ]
    },
    {
        "id": 4,
        "title": "post 4",
        "description": null,
        "published": true,
        "tags": []
    }
  ]
  ```

  </td>
  </tr>
</table>


9. Reading BookDetails <br>

```code
Request type: GET 
Request URL: book-details/
```

<table>
  <tr>
    <th>Expected output data</th>
  </tr>
  <tr>
    <td>
  
  ```pythonPOST
  [
    {
        "id": 1,
        "category": "Category 1",
        "rating": 2,
        "price": 20,
        "publish_date": "2022-09-12",
        "book": {
            "id": 1,
            "name": "Book 1",
            "author_name": ""
        }
    },
    {
        "id": 4,
        "category": "Category 1",
        "rating": 2,
        "price": 20,
        "publish_date": "2022-09-12",
        "book": {
            "id": 4,
            "name": "Book 2",
            "author_name": ""
        }
    }
  ]
  ```

  </td>
  </tr>
</table>


10. Updating BookDetails <br>

```code
Request type: PUT 
Request URL: book-details/
```

<table>
  <tr>
    <th>Expected input data</th>
    <th>Expected output data</th>
  </tr>
  <tr>
    <td>
  
  ```pythonPOST
  {
    "category": "Category 12",
    "rating": 6,
    "price": 10,
    "publish_date": "2022-09-12",
    "book": {
        "name": "Book 2",
        "author_name": "Author 1 updated"
    }
    
  }
  ```

  </td>
  <td>
  
  ```pythonPOST
  {
    "id": 4,
    "category": "Category 12",
    "rating": 6,
    "price": 10,
    "publish_date": "2022-09-12",
    "book": {
        "id": 4,
        "name": "Book 2",
        "author_name": "Author 1 updated"
    }
  }
  ```

  </td>
  </tr>
</table>



11. Updating Todo <br>

```code
Request type: PUT 
Request URL: todo-nested/
```

<table>
  <tr>
    <th>Expected input data</th>
    <th>Expected output data</th>
  </tr>
  <tr>
    <td>
  
  ```pythonPOST
  {
    "title": "Todo 1",
    "tasks": [
        {
            "id": 83,
            "title": "Title 83",
            "description": "Hey there! Updated for 83"
        },
        {
            "id": 84,
            "title": "Title 84",
            "description": "Hey there! Updated for 84"
        }
    ]
  }
  ```

  </td>
  <td>
  
  ```pythonPOST
  {{
    "title": "Todo 1",
    "tasks": [
        {
            "title": "Title 83",
            "description": "Hey there! Updated for 83"
        },
        {
            "title": "Title 84",
            "description": "Hey there! Updated for 84"
        }
    ]
  }
  ```

  </td>
  </tr>
</table>



12. Reading Bulk Todo <br>

```code
Request type: PUT 
Request URL: bulk-todo-nested/
```

<table>
  <tr>
    <th>Expected output data</th>
  </tr>
  <tr>
    <td>
  
  ```pythonPOST
  [
    {
        "id": 29,
        "title": "Todo 2",
        "tasks": [
            {
                "id": 79,
                "title": "Title 1",
                "description": "Hey there!"
            },
            {
                "id": 82,
                "title": "Title 1",
                "description": "Hey there!"
            }
        ]
    },
    {
        "id": 30,
        "title": "Todo 1",
        "tasks": [
            {
                "id": 84,
                "title": "Title 84",
                "description": "Hey there! Updated for 84"
            }
        ]
    }
  ]
  ```

  </td>
  </tr>
</table>



13. Deleting Tasks from Todo <br>

```code
Request type: DELETE 
Request URL: todo-nested/
```

<table>
  <tr>
    <th>Expected input data</th>
  </tr>
  <tr>
    <td>
  
  ```pythonPOST
  {
    "title": "Todo 1",
    "tasks": [
        {
            "id": 83
        }
    ]
  }
  ```

  </td>
  </tr>
</table>




