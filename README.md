# Authentication API (FastAPI)

A secure authentication module built with **FastAPI**, implementing password hashing and **JWT-based authentication**.  
The project focuses on building **Backend authentication logic with security best practices**.

---

## Features

- Password hashing using **bcrypt**
- Secure password verification
- Password normalization to handle **bcrypt 72-byte limitation**
- JWT-based authentication
- Token expiration handling
- Stateless authentication design

---

## Problems Faced & Solutions Implemented

### 1. bcrypt Password Length Limitation

#### Problem
The **bcrypt hashing algorithm only considers the first 72 bytes of a password**.  
If a password exceeds this limit, the remaining characters are ignored.

This can lead to:

- Authentication inconsistencies  
- Security confusion  
- Different passwords producing the same hash  

#### Solution
Implemented password normalization before hashing.

```python
def normalize_password(password: str):
    return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
```

#### Result
- Ensures bcrypt receives a valid password length
- Prevents silent truncation issues
- Improves authentication reliability

---

### 2. Secure Password Storage

#### Problem
Storing passwords in plaintext is insecure and exposes users if the database is compromised.

#### Solution
Used **Passlib CryptContext** with bcrypt.

```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)
```

#### Result

- Passwords stored as **secure salted hashes**
- Protection against rainbow table attacks
- Industry-standard password security

---

### 3. Password Verification

#### Problem
Hashed passwords cannot be compared directly.

#### Solution

```python
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)
```

#### Result

- Safely compares plaintext password with stored hashed password
- Passlib handles hashing algorithm internally

---

### 4. Stateless Authentication using JWT

#### Problem
Session-based authentication requires server-side storage and does not scale easily.

#### Solution
Implemented **JWT token-based authentication**.

```python
from jose import jwt

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

#### Result

- No session storage required
- Scalable authentication
- Secure API access via tokens

---

### 5. Token Expiration Handling

#### Problem
Without expiration, JWT tokens remain valid indefinitely if leaked.

#### Solution

```python
expire = datetime.utcnow() + timedelta(minutes=30)
```

#### Result

- Tokens automatically expire after **30 minutes**
- Improves security
- Limits damage from leaked tokens

---

## Tech Stack

- Python
- FastAPI
- Passlib
- bcrypt
- python-jose (JWT)

---

## Purpose

This project was built to understand **real-world backend authentication systems used in production APIs**.

## Project Structure

```
secure_api_gateway
│
├── app
│   ├── main.py
│   │
│   ├── models
│   │   ├── task_model.py
│   │   └── user_model.py
│   │
│   ├── routers
│   │   ├── task_routes.py
│   │   └── auth_routes.py
│   │
│   ├── services
│   │   └── auth_service.py
│   │
│   └── utils
│       └── security.py
│
├── requirements.txt
└── README.md
```

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/deoraja/secure-api-gateway.git
cd secure-api-gateway
```

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate environment:

Windows
```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

Swagger API docs:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

### General

| Method | Endpoint | Description |
|------|------|------|
GET | `/` | API health check / welcome message |

### Authentication

| Method | Endpoint | Description |
|------|------|------|
POST | `/register` | Register new user |
POST | `/login` | Authenticate user and get JWT token |

### Tasks (protected)

| Method | Endpoint | Description |
|------|------|------|
POST | `/tasks` | Create a new task |
GET | `/tasks` | Get all tasks |
GET | `/tasks/{id}` | Get specific task |
DELETE | `/tasks/{id}` | Delete specific task |

Protected endpoints require **Bearer Token authentication**.
