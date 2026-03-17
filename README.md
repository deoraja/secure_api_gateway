# Secure API Gateway with JWT Authentication and Rate Limiting

A production-oriented authentication system built with FastAPI, implementing JWT-based authentication with refresh token rotation, rate-limited endpoints, and secure session management.

Designed to demonstrate real-world backend security practices including token lifecycle management and API protection against abuse.

---

## Features

-  **JWT**-based Authentication (Access + Refresh Tokens)
-  **Refresh Token Rotation**
-  **Logout with Token Invalidation**
-  **Rate Limiting on Authentication Endpoints**
-  Secure Password Hashing using **bcrypt**
-  Token Expiration Handling
-  Stateless Authentication Architecture

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

### 5. Refresh Token Rotation

#### Problem
If a refresh token is reused or stolen, attackers can continuously generate new access tokens.

#### Solution
- Generate a **new refresh token on every refresh request**
- Store latest valid token per user
- Invalidate old refresh tokens automatically

#### Result
- Prevents replay attacks
- Ensures only the latest token is valid
- Enhances session security

---

### 6. Logout with Token Invalidation

#### Problem
JWT is stateless → tokens remain valid even after logout.

#### Solution
- On logout, stored refresh token is cleared
- Future refresh attempts are rejected

#### Result
- Immediate session termination
- Prevents unauthorized reuse of tokens

---

### 7. Rate Limiting (Brute-force Protection)

#### Problem
Authentication endpoints are vulnerable to:
- Brute-force attacks  
- Credential stuffing  
- API abuse  

#### Solution
Applied **rate limiting** on critical endpoints:

- `/login` → 5 requests/minute  
- `/register` → 3 requests/minute  
- `/refresh` → 10 requests/minute
- `/logout` → 20 requests/minute  

#### Result
- Prevents repeated login attempts
- Protects backend from abuse
- Improves system stability under attack

---

## Authentication Flow

1. User registers with username and password
2. Password is hashed using bcrypt and stored securely
3. User logs in → receives:
   - Access Token (short-lived)
   - Refresh Token (long-lived)
4. Access token is used to access protected APIs
5. When access token expires:
   - Client sends refresh token
   - Server verifies and rotates refresh token
6. Logout:
   - Stored refresh token is invalidated
   - Future refresh attempts are rejected

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
│   │   ├── refresh_model.py
│   │   ├── task_model.py
│   │   └── user_model.py
│   │
│   ├── routers
│   │   ├── auth_routes.py
│   │   └── task_routes.py
│   │
│   ├── services
│   │    ├── auth_service.py
│   │    └── task_service.py
│   │
│   └── core
│        ├── dependencies.py
│        ├── rate_limiter.py   
│        └── security.py
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
POST | `/refresh` | Rotate refresh token and issue new access token |
POST | `/logout` | Invalidate session |

### Tasks 

| Method | Endpoint | Description |
|------|------|------|
POST | `/tasks` | Create a new task |
GET | `/tasks` | Get all tasks |
GET | `/tasks/{id}` | Get specific task |
DELETE | `/tasks/{id}` | Delete specific task |

