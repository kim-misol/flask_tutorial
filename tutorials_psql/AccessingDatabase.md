# [Accessing a Data](https://www.postgresql.org/docs/12/tutorial-accessdb.html)
Once you have created a database, you can access it by:

- Running the PostgreSQL interactive terminal program, called psql, 
which allows you to interactively enter, edit, and execute SQL commands.

- Using an existing graphical frontend tool like pgAdmin or an office suite with ODBC or JDBC support to create and manipulate a database. 
These possibilities are not covered in this tutorial.

You probably want to start up `psql` to try the examples in terminal. It can be activated for the `mydb` database by typing the command:
~~~sql
$ psql mydb
~~~

The last line could also be:
~~~sql
mydb=#
~~~
That would mean you are a database superuser, which is most likely the case if you installed the PostgreSQL instance yourself. 
Being a superuser means that you are not subject to access controls.

---
Note:
    Postgresql is case insensitive
---
Try out these commands:
~~~sql
mydb=> SELECT version();
                                         version
------------------------------------------------------------------------------------------
 PostgreSQL 12.4 on x86_64-pc-linux-gnu, compiled by gcc (Debian 4.9.2-10) 4.9.2, 64-bit
(1 row)

mydb=> SELECT current_date;
    date
------------
 2016-01-07
(1 row)

mydb=> SELECT 2 + 2;
 ?column?
----------
        4
(1 row)
~~~