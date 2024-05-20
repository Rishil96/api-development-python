# Python API Development

## Table of Contents

| Sr. No. |                         Topic |
|:-------:|------------------------------:|
|    1    | [Basic API Terminologies](#1) |
|    2    |                 [FastAPI](#2) |

---

<h2 id="1">Basic API Terminologies</h2>

- An **API (Application Programming Interface)** is a set of rules, protocols, and tools that allows different software applications to communicate with each other. It defines the methods and data formats that applications can use to request and exchange information.
---
- **REST (Representational State Transfer)** is an architectural style for designing networked applications. It relies on a stateless client-server communication protocol, typically HTTP, and uses standard HTTP methods (GET, POST, PUT, DELETE) to perform operations on resources.
---
- An **Endpoint** is a specific URL (Uniform Resource Locator) or URI (Uniform Resource Identifier) where an API can be accessed. Each endpoint represents a specific resource or functionality provided by the API.
---
- **HTTP (HyperText Transfer Protocol)** is basically the system that makes it possible for you to browse the internet by letting your computer ask for things (requests) and servers give them to you (responses).
---
- **HTTP methods**, also known as HTTP verbs, define the actions that can be performed on resources. Common HTTP methods include GET (retrieve data), POST (create data), PUT (update data completely), PATCH (update data partially), and DELETE (remove data).
---
- **Status codes** are short numbers or phrases that tell you if something went right or wrong when you're using the internet. They help computers communicate about what happened when you try to access a webpage or do something online.
---
- **1xx Informational:**

  - 100 Continue: The server has received the initial part of the request and is waiting for the client to send the rest.
  - 101 Switching Protocols: The server is changing the protocol being used on this connection.
---
- **2xx Success:**

  - 200 OK: The request was successful.
  - 201 Created: The request has been fulfilled and a new resource has been created.
  - 202 Accepted: The request has been accepted for processing, but the processing has not been completed.
  - 204 No Content: The server successfully processed the request but is not returning any content.
---
- **3xx Redirection:**

  - 300 Multiple Choices: The requested resource has multiple representations, each with its own specific location.
  - 301 Moved Permanently: The requested resource has been permanently moved to a new location.
  - 302 Found: The requested resource has been temporarily moved to a different location.
  - 304 Not Modified: The requested resource has not been modified since the last time it was accessed.
---
- **4xx Client Error:**

  - 400 Bad Request: The server cannot process the request due to a client error.
  - 401 Unauthorized: The request requires user authentication.
  - 403 Forbidden: The server understood the request but refuses to authorize it.
  - 404 Not Found: The requested resource could not be found.
---
- **5xx Server Error:**

  - 500 Internal Server Error: A generic error message indicating that the server encountered an unexpected condition that prevented it from fulfilling the request.
  - 501 Not Implemented: The server does not support the functionality required to fulfill the request.
  - 502 Bad Gateway: The server received an invalid response from an upstream server while attempting to fulfill the request.
  - 503 Service Unavailable: The server is currently unable to handle the request due to temporary overloading or maintenance of the server.

---

<h2 id="2">FastAPI</h2>

- In FastAPI, a route is created using a decorator function `@app.request_type("/url-path")`. Here app is the FastAPI object name, request_type is the type of request that route will handle and inside the () is the URL Path.
---
- **Schema**: means a defined structure that must be followed to send/receive data via requests. Basically minimizing the errors a server has to handle as we regulate in what form we are receiving the data for specific endpoints.
---
- **CRUD** represents the 4 most common functionalities of any database/social media applications i.e. Create, Read, Update and Delete.
    - Create a resource using POST request.
    - Read resources using GET request.
    - Update resources using PUT/PATCH request.
    - Delete resources using DELETE request.
---
- FastAPI supports automatic documentation, by running the application and going to /docs URL we get auto-generated document for our API from Swagger UI.