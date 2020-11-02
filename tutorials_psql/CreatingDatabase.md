# [Creating a Database](https://www.postgresql.org/docs/12/tutorial-createdb.html)

The first test to see whether you can access the database server is to try to create a database. 
A running PostgreSQL server can manage many databases. 
Typically, a separate database is used for each project or for each user.

To create a new database, in this example named mydb, you use the following command:
~~~sql
$ createdb mydb
~~~

If this produces no response then this step was successful and you can skip over the remainder of this section.

If you see a message similar to:
~~~sql
createdb: command not found
~~~

then PostgreSQL was not installed properly. Either it was not installed at all or your shell's search path was not set to include it. Try calling the command with an absolute path instead:
~~~sql
$ /usr/local/pgsql/bin/createdb mydb
~~~

Another response could be this:
~~~sql
createdb: could not connect to database postgres: could not connect to server: No such file or directory
        Is the server running locally and accepting
        connections on Unix domain socket "/tmp/.s.PGSQL.5432"?
~~~
This means that the server was not started, or it was not started where createdb expected it. Again, check the installation instructions or consult the administrator.

Another response could be this:
~~~sql
createdb: could not connect to database postgres: FATAL:  role "joe" does not exist
~~~
where your own login name is mentioned. This will happen if the administrator has not created a PostgreSQL user account for you. (PostgreSQL user accounts are distinct from operating system user accounts.) If you are the administrator, see Chapter 21 for help creating accounts. You will need to become the operating system user under which PostgreSQL was installed (usually postgres) to create the first user account. It could also be that you were assigned a PostgreSQL user name that is different from your operating system user name; in that case you need to use the -U switch or set the PGUSER environment variable to specify your PostgreSQL user name.

If you have a user account but it does not have the privileges required to create a database, you will see the following:
~~~sql
createdb: database creation failed: ERROR:  permission denied to create database
~~~
Not every user has authorization to create new databases. If PostgreSQL refuses to create databases for you then the site administrator needs to grant you permission to create databases. Consult your site administrator if this occurs. If you installed PostgreSQL yourself then you should log in for the purposes of this tutorial under the user account that you started the server as. [1]

You can also create databases with other names. PostgreSQL allows you to create any number of databases at a given site. Database names must have an alphabetic first character and are limited to 63 bytes in length. A convenient choice is to create a database with the same name as your current user name. Many tools assume that database name as the default, so it can save you some typing. To create that database, simply type:
~~~sql
$ createdb
~~~
If you do not want to use your database anymore you can remove it. For example, if you are the owner (creator) of the database mydb, you can destroy it using the following command:
~~~sql
$ dropdb mydb
~~~
(For this command, the database name does not default to the user account name. You always need to specify it.) This action physically removes all files associated with the database and cannot be undone, so this should only be done with a great deal of forethought.