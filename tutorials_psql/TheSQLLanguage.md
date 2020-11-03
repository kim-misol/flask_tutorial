# [The SQL Language](https://www.postgresql.org/docs/12/tutorial-sql-intro.html)

### [Creating a New Table](https://www.postgresql.org/docs/12/tutorial-table.html)
You can create a new table by specifying the table name, along with all column names and their types:
~~~sql
CREATE TABLE weather (
    city            varchar(80),
    temp_lo         int,           -- low temperature
    temp_hi         int,           -- high temperature
    prcp            real,          -- precipitation
    date            date
);
~~~

You can enter this into psql with the line breaks. 
`psql` will recognize that the command is not terminated **until the semicolon**.
White space (i.e., spaces, tabs, and newlines) can be used freely in SQL commands. 

Two dashes (“--”) introduce comments.

SQL is case insensitive about key words and identifiers, except when identifiers are double-quoted to preserve the case (not done above).

- **varchar(80)** specifies a data type that can store arbitrary character strings up to 80 characters in length. 
- **int** is the normal integer type. 
- **real** is a type for storing single precision floating-point numbers. 
- **date** should be self-explanatory.  
(Yes, the column of type date is also named date. This might be convenient or confusing — you choose.)

PostgreSQL supports the standard SQL types int, smallint, real, double precision, char(N), varchar(N), date, time, timestamp, and interval, 
as well as other types of general utility and a rich set of geometric types. 
Consequently, type names are not key words in the syntax, except where required to support special cases in the SQL standard.

The second example will store cities and their associated geographical location:
~~~sql
CREATE TABLE tablename (
    name            varchar(80),
    location        point
);
~~~
The point type is an example of a PostgreSQL-specific data type.

Finally, it should be mentioned that if you don't need a table any longer or want to recreate it differently, 
you can remove it using the following command:
~~~sql
DROP TABLE tablename;
~~~

### [Populating a Table With Rows](https://www.postgresql.org/docs/12/tutorial-populate.html)
The INSERT statement is used to populate a table with rows:
~~~sql
INSERT INTO weather VALUES ('San Francisco', 46, 50, 0.25, '1994-11-27');
~~~
Constants that are not simple numeric values usually must be surrounded by single quotes (')

The point type requires a coordinate pair as input, as shown here:
~~~sql
INSERT INTO cities VALUES ('San Francisco', '(-194.0, 53.0)');
~~~

You could also have used COPY to load large amounts of data from flat-text files. 
This is usually faster because the COPY command is optimized for this application while allowing less flexibility than INSERT. 
An example would be:

~~~sql
COPY weather FROM '/home/user/weather.txt';
~~~
where the file name for the source file must be available on the machine running the backend process, 
not the client, since the backend process reads the file directly. 
You can read more about the COPY command in **COPY**.