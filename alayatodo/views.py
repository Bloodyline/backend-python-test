from alayatodo import app, db
from .orm import Users, Todos
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

    user = Users.query.filter(Users.username == username, Users.password == password).all()
    if user:
        session['user'] = user[0].as_dict()
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
    if not session.get('logged_in'):
        return redirect('/login')

    user_id = session['user']['id']
    
    todo = Todos.query.filter_by(id=id).first()

    if todo.user_id == user_id:
        return render_template('todo.html', todo=todo)
    else:
        flash("You can't see other peoples description.")
        return redirect("/todo")


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
@app.route('/todo/page/<page>', methods=['GET'])
def todos(page=0):
    if not session.get('logged_in'):
        return redirect('/login')

    user_id = session['user']['id']

    todos = 10 # todos number
    page = int(page)

    # 10 todos per page
    todos = Todos.query.filter(Todos.user_id == user_id).offset(page*todos).limit(10)
    todos = [todo.as_dict() for todo in todos]

    # Get the current page number
    page_number = request.referrer[-1] if request.referrer != None else 0

    # If next page clicked check if there's data
    if len(todos):
        return render_template('todos.html', todos=todos, page=page, next=True)

    # If there's nothing go to the first page    
    if page >= 1 and not len(todos):
        return redirect("/todo")

    return render_template('todos.html', todos=todos, page=page, next=False)

@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    
    description = str(request.form.get('description', '')).strip()
    id = session['user']['id']

    if len(description):
        todo = Todos(user_id=id, description=description)
        db.session.add(todo)
        db.session.commit()

        flash(f"Your task {description} has been successfully added." )
    else:
        flash("You need at least a character in your description to post a todo.", category="warning")

    # Get the current page number
    page_number = request.referrer[-1]
    if page_number != "/":
        return redirect(f'/todo/page/{page_number}')
    else:
        return redirect('/todo')


@app.route('/todo/delete/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')

    user_id = session['user']['id']

    toDelete = Todos.query.filter_by(id=id).first()
    description = toDelete.description
    db.session.delete(toDelete)
    db.session.commit()
    
    flash(f"Your task {description} has been successfully deleted." )
    
    # Get the current page number
    page_number = request.referrer[-1]
    if page_number != "/":
        return redirect(f'/todo/page/{page_number}')
    else:
        return redirect('/todo')


@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    if not session.get('logged_in'):
        return redirect('/login')
    
    user_id = session['user']['id']

    todo = Todos.query.filter_by(id=id).first()
    if todo.user_id == user_id:
        return jsonify(todo.as_dict())
    else:
        flash("You can't see other peoples description.")
        return redirect("/todo")

@app.route('/todo/complete/<id>', methods=['POST'])
def todo_completed(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todos.query.filter_by(id=id).first()

    # Switch between completed and not
    todo.completed = True if not todo.completed else False
    db.session.commit()

    # Get the current page number
    page_number = request.referrer[-1]
    if page_number != "/":
        return redirect(f'/todo/page/{page_number}')
    else:
        return redirect('/todo')

