from __future__ import annotations
import sqlite3
from dataclasses import dataclass
from pathlib import Path

# DB_PATH = where SQLite file will live
DB_PATH = Path("crm.db")


def get_connection() -> sqlite3.Connection:
    """
    Open a connection to the SQLite database file.
    """
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db() -> None:
    """
    Create the 'customers' table if it does not exist.
    """
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT
            )
            """
        )


# ORM-ish dataclass: maps a row in DB to a Python object
@dataclass
class Customer:
    id: int | None
    name: str
    email: str
    phone: str | None


# C in CRUD: Create
def create_customer(name: str, email: str, phone: str | None = None) -> Customer:
    """
    Insert a new customer row and return a Customer object.
    """
    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO customers (name, email, phone)
            VALUES (?, ?, ?)
            """,
            (name, email, phone),
        )
        new_id = cur.lastrowid

    return Customer(id=new_id, name=name, email=email, phone=phone)


# R in CRUD: Read list
def list_customers() -> list[Customer]:
    """
    Return all customers ordered by id DESC.
    """
    with get_connection() as conn:
        cur = conn.execute(
            """
            SELECT id, name, email, phone
            FROM customers
            ORDER BY id DESC
            """
        )
        rows = cur.fetchall()

    return [
        Customer(id=row[0], name=row[1], email=row[2], phone=row[3])
        for row in rows
    ]


# R in CRUD: Read single
def get_customer(customer_id: int) -> Customer | None:
    """
    Return a single customer by id, or None if not found.
    """
    with get_connection() as conn:
        cur = conn.execute(
            """
            SELECT id, name, email, phone
            FROM customers
            WHERE id = ?
            """,
            (customer_id,),
        )
        row = cur.fetchone()

    if row is None:
        return None

    return Customer(id=row[0], name=row[1], email=row[2], phone=row[3])


# R in CRUD: Search
def search_customers(query: str) -> list[Customer]:
    """
    Simple LIKE search on name, email, phone.
    """
    like_q = f"%{query}%"

    with get_connection() as conn:
        cur = conn.execute(
            """
            SELECT id, name, email, phone
            FROM customers
            WHERE name  LIKE ?
               OR email LIKE ?
               OR phone LIKE ?
            ORDER BY id DESC
            """,
            (like_q, like_q, like_q),
        )
        rows = cur.fetchall()

    return [
        Customer(id=row[0], name=row[1], email=row[2], phone=row[3])
        for row in rows
    ]
