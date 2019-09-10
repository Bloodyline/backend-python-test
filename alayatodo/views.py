from alayatodo import app
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    flash,
    jsonify
    )


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    # Remove whitespaces for security
    username = str(request.form.get('username')).replace(' ','')
    password = str(request.form.get('password')).replace(' ','')

    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'"
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
    if user:
        session['user'] = dict(user)
        session['logged_in'] = True

        # Welcome message after the first connection
        flash(f"Welcome back {username}.")
        return redirect('/todo')
    else:
        # Flash message to show
        flash("Your credentials are incorrect.", category="error")
        return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)

    flash("You disconnected successfully.")
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = cur.fetchone()
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    cur = g.db.execute("SELECT * FROM todos")
    todos = cur.fetchall()
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    
    description = str(request.form.get('description', '')).strip()
    id = session['user']['id']

    if len(description):
        g.db.execute(
            "INSERT INTO todos (user_id, description) VALUES ('%s', '%s')"
            % (id, description)
        )
        g.db.commit()
    else:
        flash("You need at least a character in your description to post a todo.", category="warning")

    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute("DELETE FROM todos WHERE id ='%s'" % id)
    g.db.commit()
    return redirect('/todo')

@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    if not session.get('logged_in'):
        return redirect('/login')
    
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    
    return jsonify(dict(cur.fetchone()))

@app.route('/todo/<id>', methods=['POST'])
def todo_completed(id):
    if not session.get('logged_in'):
        return redirect('/login')
    pass
    return redirect('/todo')
