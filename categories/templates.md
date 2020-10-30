# [Templates](https://flask.palletsprojects.com/en/1.1.x/tutorial/templates/)
### The Base Layout
Each page in the application will have the same basic layout around a different body. 
Instead of writing the entire HTML structure in each template, each template will extend a base template and override specific sections.

flaskr/templates/`base.html`
```html
<!doctype html>
<title>{% block title %}{% endblock %} - Flaskr</title>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<nav>
  <h1>Flaskr</h1>
  <ul>
    {% if g.user %}
      <li><span>{{ g.user['username'] }}</span>
      <li><a href="{{ url_for('auth.logout') }}">Log Out</a>
    {% else %}
      <li><a href="{{ url_for('auth.register') }}">Register</a>
      <li><a href="{{ url_for('auth.login') }}">Log In</a>
    {% endif %}
  </ul>
</nav>
<section class="content">
  <header>
    {% block header %}{% endblock %}
  </header>
  {% for message in get_flashed_messages() %}
    <div class="flash">{{ message }}</div>
  {% endfor %}
  {% block content %}{% endblock %}
</section>
```
**g** is automatically available in templates. 
Based on if `g.user` is set (from `load_logged_in_user`)
, either the username and a log out link are displayed, or links to register and log in are displayed.  
`url_for()` is also automatically available, and is used to generate URLs to views instead of writing them out manually.

After the page title, and before the content, the template loops over each message returned by `get_flashed_messages()`. 
You used flash() in the views to show error messages, and this is the code that will display them.

There are three blocks defined here that will be overridden in the other templates:

1. `{% block title %}` will change the title displayed in the browser’s tab and window title.
2. `{% block header %}` is similar to title but will change the title displayed on the page.
3. `{% block content %}` is where the content of each page goes, such as the login form or a blog post.

The base template is directly in the `templates` directory. 
To keep the others organized, the templates for a blueprint will be placed in a directory with the same name as the blueprint.


___

### Register A User
Now that the authentication templates are written, you can register a user. 
Make sure the server is still running (flask run` if it’s not), then go to http://127.0.0.1:5000/auth/register.

Try clicking the “Register” button without filling out the form and see that the browser shows an error message. 
Try removing the `required` attributes from the `register.html` template and click “Register” again. 
Instead of the browser showing an error, the page will reload and the error from `flash()` in the view will be shown.

Fill out a username and password and you’ll be redirected to the login page. 
Try entering an incorrect username, or the correct username and incorrect password. 
If you log in you’ll get an error because there’s no `index` view to redirect to yet.