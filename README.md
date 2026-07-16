# Book Inventory API

## Project Description

The Book Inventory API is a backend application developed using **FastAPI** and **SQLModel**. It provides a RESTful API for managing a bookstore inventory system.

The API allows users to create, view, search, update, and delete books stored in a PostgreSQL database.

## Technologies Used

- Python 3.12
- FastAPI
- Uvicorn
- SQLModel
- PostgreSQL 16
- Docker
- Alembic
- python-dotenv

## Project Structure
bookstore-api/
│
├── main.py
├── README.md
├── .env
├── docker-compose.yml
├── alembic.ini
│
├── database/
│ ├── init.py
│ └── session.py
│
└── models/
├── init.py
└── book.py

---

# Installation and Setup

## 1. Clone the Repository

```bash
git clone <repository-url>
