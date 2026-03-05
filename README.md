Authentication API (FastAPI)

A secure authentication module built with FastAPI, implementing password hashing and JWT-based authentication. The project focuses on building production-like backend authentication logic with security best practices.

Features

User password hashing using bcrypt

Password verification

Password normalization to handle bcrypt limitations

JWT-based access token generation

Token expiration handling

Secure authentication utilities

Problems Faced & Solutions Implemented
1️. Password Length Limitation in bcrypt
Problem

The bcrypt hashing algorithm only considers the first 72 bytes of a password.
If a user enters a password longer than 72 bytes, the remaining characters are ignored.

This can cause:

Authentication inconsistencies

Security confusion

Different passwords producing the same hash

Example
password123456789012345678901234567890123456789012345678901234567890123

Characters after 72 bytes are ignored.

Solution Implemented

A password normalization function was added before hashing.

def normalize_password(password: str):
    return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
Result

Ensures bcrypt always receives a valid password length

Prevents silent truncation issues

Improves authentication consistency

2️. Secure Password Storage
Problem

Storing passwords in plaintext is extremely insecure and exposes users if the database is compromised.

Solution Implemented

Used Passlib CryptContext with bcrypt.

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Password hashing function:

def hash_password(password: str):
    return pwd_context.hash(password)
Result

Passwords are stored as secure salted hashes

Resistant to rainbow table attacks

Industry-standard password protection

3️. Password Verification
Problem

Passwords cannot be directly compared once hashed.

Solution Implemented

Used Passlib's built-in verification.

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)
Result

Safely compares plaintext password with hashed password

Handles hashing algorithm internally

4️. Stateless Authentication
Problem

Traditional session-based authentication requires server-side session storage, which becomes difficult to scale.

Solution Implemented

Used JWT (JSON Web Tokens) for stateless authentication.

from jose import jwt

Token generation:

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
Result

No session storage required

Horizontally scalable authentication

Token-based API security

5️. Token Expiration Handling
Problem

Without expiration, JWT tokens remain valid forever if leaked.

Solution Implemented

Added expiration claim (exp) in token.

expire = datetime.utcnow() + timedelta(minutes=30)
Result

Tokens automatically expire after 30 minutes

Improves security

Limits damage if token is compromised

⚙️ Tech Stack

FastAPI

Python

Passlib

bcrypt

python-jose (JWT)
