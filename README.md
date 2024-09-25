# FBA Finance Backend API

## 🚀 Introduction

Welcome to the FBA (Financial Business Association) Pool Management API! This powerful and flexible API is designed to facilitate the creation, management, and participation in financial pools for businesses. It provides a robust platform for businesses to collaborate, share resources, and manage their financial interactions efficiently.

## ✨ Current Features - (Will be updated as more are added)

- **🔐 Secure Authentication**: JWT-based authentication system for user security.
- **👥 User Management**: Create and manage business user profiles with detailed information.
- **🏊‍♂️ Pool Operations**: Create, join, and manage FBA pools with ease.(not yet implemented)
- **💼 Business Search**: Advanced search and filtering capabilities for businesses.
- **💰 Wallet Functionality**: Manage funds, track transactions, and handle financial operations.(not yet implemented)
- **📊 Dashboard**: Comprehensive overview of business metrics and pool participation. (not yet implemented)

## 🛠 Technology Stack

- **Framework**: FastAPI
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **Documentation**: Automatic API documentation with Swagger UI

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- pip (Python package manager)

### Installation

1. Clone the repository:

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`.

## 📚 API Documentation

Once the server is running, you can access the automatic API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔑 Authentication

The API uses JWT for authentication. To access protected endpoints:

1. Register a user at `/api/auth/create_user`
2. Obtain a token from `/api/auth/login`
3. Include the token in the Authorization header: `Bearer <your_token>` or use the Authorize button and login with the password and email from the created user


## 🛡 Security

- Passwords are hashed using bcrypt
- JWT tokens are used for stateless authentication
- Input validation is performed using Pydantic models


## 📄 License

This project is licensed under the MIT License 


---
