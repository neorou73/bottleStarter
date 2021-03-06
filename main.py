"""
requires bottle
"""
from bottle import route, run, template, request, response

def check_login(username, password):
    if username == 'asdf' and password == 'asdf':
        return True
    else:
        return False

@route('/')
def theroot():
    return "<b>Hello</b>!"

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


@route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''


@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        response.set_cookie("account", username, secret='some-secret-key')
        return "<p>Your login information was correct.</p><p><a href='/logout?username=" + username + "'>LOG OUT</a></p>"
    else:
        return "<p>Login failed.</p>"


@route('/logout')
def do_logout():
    # return request.query.get('username')
    username = request.query.get('username')
    response.set_cookie("account", username, secret='some-secret-key', expires=0)
    return template('<b>Adios {{name}}! You have been logged out.</b>', name=username)

@route('/restricted')
def restricted_area():
    username = request.get_cookie("account", secret='some-secret-key')
    if username:
        return template("Hello {{name}}. Welcome back.", name=username)
    else:
        return "You are not logged in. Access denied."


# run(host='localhost', port=8080)
run(server='gunicorn', port=8000, host='localhost', workers=4)
