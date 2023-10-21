# 🍺 Beer Catalog Project

# 🍺 Beer Catalog Project

## 🌐 Overview

This project provides a beer catalog with search functionality, leveraging a blend of **Python, Django, React**, and **Elasticsearch**.

## 🖥️ Frontend

### 🛠️ Technologies:

- `React.js`

### 🔍 Features:

- **Search Component**: A React component allowing users to search within the beer catalog.
- **ResultList Component**: Displays the search results.
- **Paginator Component**: A pagination tool for search results.

### 📤 Execution:

The front-end sends a GET request to the API:

````javascript
http://localhost:8003/api/v1/catalog/es-beers/



## 🚀 Backend

### 🛠️ Technologies:

- `Python`
- `Django`
- `Elasticsearch` (for optimized searches within the catalog)

### 📄 Details:

The backend was developed using **Python** and **Django**, and it integrates with **Elasticsearch** to offer efficient searches in the beer catalog. The system was containerized using `Docker`, which makes deployment easier and ensures consistency across different environments.

### 📦 Infrastructure:

The system is containerized with `Docker`. Below is a simplified example of a `Dockerfile` (assuming you might have one) for illustration:

```dockerfile
FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver"]
````
