# Python API Development

## Table of Contents

| Sr. No. |                         Topic |
|:-------:|------------------------------:|
|    1    | [Basic API Terminologies](#1) |
|    2    |                 [FastAPI](#2) |

---

<h2 id="1">Basic API Terminologies</h2>

- An **API (Application Programming Interface)** is a set of rules, protocols, and tools that allows different software applications to communicate with each other. It defines the methods and data formats that applications can use to request and exchange information.

- **REST (Representational State Transfer)** is an architectural style for designing networked applications. It relies on a stateless client-server communication protocol, typically HTTP, and uses standard HTTP methods (GET, POST, PUT, DELETE) to perform operations on resources.

- An **Endpoint** is a specific URL (Uniform Resource Locator) or URI (Uniform Resource Identifier) where an API can be accessed. Each endpoint represents a specific resource or functionality provided by the API.

- **HTTP (HyperText Transfer Protocol)** is basically the system that makes it possible for you to browse the internet by letting your computer ask for things (requests) and servers give them to you (responses).

- **HTTP methods**, also known as HTTP verbs, define the actions that can be performed on resources. Common HTTP methods include GET (retrieve data), POST (create data), PUT (update data completely), PATCH (update data partially), and DELETE (remove data).

---

<h2 id="2">FastAPI</h2>

- In FastAPI, a route is created using a decorator function `@app.request_type("/url-path")`. Here app is the FastAPI object name, request_type is the type of request that route will handle and inside the () is the URL Path.
- **Schema**: means a defined structure that must be followed to send/receive data via requests. Basically minimizing the errors a server has to handle as we regulate in what form we are receiving the data for specific endpoints.
- 