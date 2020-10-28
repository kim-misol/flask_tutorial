# [Project Layout](https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/)

The project directory will contain:

 - flaskr/: a Python package containing your application code and files.
 - tests/: a directory containing test modules.
 - venv/: a Python virtual environment where Flask and other dependencies are installed.
 - Installation files telling Python how to install your project.
 - Version control config, such as git. You should make a habit of using some type of version control for all your projects, no matter the size.
 - Any other project files you might add in the future.

### Virtualenv modules installation 
Unix based systems

```bash
$ virtualenv --no-site-packages env
$ source env/bin/activate
```
    
Windows based systems

```bash
$ virtualenv --no-site-packages env
$ .\env\Scripts\activate
```

your project layout will look like this:
```
/home/user/Projects/flask-tutorial
├── flaskr/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── blog.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── blog/
│   │       ├── create.html
│   │       ├── index.html
│   │       └── update.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
├── venv/
├── setup.py
└── MANIFEST.in
```

If you’re using version control, the following files that are generated while running your project should be ignored. 
There may be other files based on the editor you use. In general, ignore files that you didn’t write. 
For example, with git:

.gitignore
```
venv/

*.pyc
__pycache__/

instance/

.pytest_cache/
.coverage
htmlcov/

dist/
build/
*.egg-info/
```