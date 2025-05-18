# Introduction

MVP GraphQL API with Flask

## Getting Started

- git clone
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- flask run
- Checkout `http://127.0.0.1:5000/graphql`

## Code

1. Create

```graphql
mutation {
  createTodo(
    title: "Learn Flask"
    description: "Build a CRUD app with GraphQL"
    done: false
    status: PENDING
  ) {
    todo {
      id
      title
      description
      done
      status
    }
  }
}
```

2. Read

```graphql
query {
  allTodos {
    id
    title
    description
    done
    status
  }
}
```

3. Update

```graphql
mutation {
  updateTodo(id: "1", title: "Learn Flask & GraphQL") {
    todo {
      id
      title
      description
      done
      status
    }
  }
}
```

4. Delete

```graphql
mutation {
  deleteTodo(id: "1") {
    success
  }
}
```

5. Search Todos by title

```graphql
query {
  todosByTitle(title: "learn") {
    id
    title
    description
    done
  }
}
```

6. Search Todos by title or description

```graphql
query {
  todosSearch(term: "flask") {
    id
    title
    description
    done
  }
}
```
