DefineAndAccessDatabase.md
# [Define and Access the Database](https://flask.palletsprojects.com/en/1.1.x/tutorial/database/)

The application will use a SQLite database to store users and posts. 
Python comes with built-in support for SQLite in the sqlite3 module.

SQLite is convenient because it doesn’t require setting up a separate database server and is built-in to Python. 
However, if concurrent requests try to write to the database at the same time, they will slow down as each write happens sequentially.
Once you become big, you may want to switch to a different database such as postgresql.

### Connect to the Database

The first thing to do when working with a SQLite database is to create a connection to it. 
Any queries and operations are performed using the connection.

In web applications this connection is typically tied to the request. 
It is created at some point when handling a request, and closed before the response is sent.

flaskr/`db.py`
```
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
```
**g** is a special object that is unique for each request. 
It is used to store data that might be accessed by multiple functions during the request. 
The connection is stored and reused instead of creating a new connection if `get_db` is called a second time in the same request.

`current_app` is another special object that points to the Flask application handling the request. 
Since you used an application factory, there is no application object when writing the rest of your code. 
`get_db` will be called when the application has been created and is handling a request, so `current_app` can be used.

`sqlite3.connect()` establishes a connection to the file pointed at by the DATABASE configuration key. 
This file doesn’t have to exist yet, and won’t until you initialize the database later.

`sqlite3.Row` tells the connection to return rows that behave like dicts. This allows accessing the columns by name.

`close_db` checks if a connection was created by checking if `g.db` was set. 
If the connection exists, it is closed.  
Further down you will tell your application about the `close_db` function in the application factory so that it is called after each request.

### Create the Tables
In SQLite, data is stored in tables and columns. 
These need to be created before you can store and retrieve data. 
Flaskr will store users in the user table, and posts in the post table. 
Create a file with the SQL commands needed to create empty tables:

flaskr/`schema.sql`
```
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
```