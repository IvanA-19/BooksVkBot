# Importing libraries
import sqlite3
from config import api, group_id


# Creating of database
db = sqlite3.connect('data/users.db')
cursor = db.cursor()


# Creating of table
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
id INT);""")
db.commit()


# Adding followed members to database
def add_following_users(users: list) -> None:
    for user_id in users:
        cursor.execute(f"SELECT id FROM users WHERE id = {user_id}")
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO users VALUES({user_id})")
            db.commit()


# Getting members in the group
def get_members() -> list:
    members = api.method('groups.getMembers', {'group_id': group_id})
    members = members['items']
    return members


# Checking user in database
def check_member(user_id: int) -> bool:
    cursor.execute(f"SELECT id FROM users WHERE id = {user_id}")
    if cursor.fetchone() is not None:
        return True
    return False


# Adding new member to database
def add_member(user_id: int) -> None:
    cursor.execute(f"SELECT id FROM users WHERE id = {user_id}")
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES({user_id})")
        db.commit()


# Removing user from database
def remove_member(user_id: int) -> None:
    cursor.execute(f"SELECT id FROM users WHERE id = {user_id}")
    if cursor.fetchone() is not None:
        cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
        db.commit()


# Show id of users in database
def show_db():
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    return data

