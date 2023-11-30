from app import app, db
from flask import render_template, request, jsonify
from app.models import Task

@app.route("/", methods=["GET"])
def home():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/submit", methods=["POST"])
def submit():
    global_task_object = Task()

    title = request.form["title"]
    estimate = request.form["estimate"]
    status = request.form["status"]
    print(status)
    task = Task(title=title, estimate=estimate, status=status)
    db.session.add(task)
    db.session.commit()
    global_task_object = task

    response = f"""
    <tr>
        <td>{global_task_object.task_id}</td>
        <td>{title}</td>
        <td>{estimate}</td>
        <td>{global_task_object.status}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{global_task_object.task_id}">
                Edit Task
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{global_task_object.task_id}"
                class="btn btn-primary">
                Delete
            </button>
        </td>
    </tr>
    """
    return response

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return ""

@app.route("/get-edit-form/<int:id>", methods=["GET"])
def get_edit_form(id):
    task = Task.query.get(id)

    response = f"""
    <tr hx-trigger='cancel' class='editing' hx-get="/get-task-row/{id}">
  <td><input name="title" value="{task.title}"/></td>
  <td>{task.estimate}</td>
  <td>{task.status}</td>
  <td>
    <button class="btn btn-primary" hx-get="/get-task-row/{id}">
      Cancel
    </button>
    <button class="btn btn-primary" hx-put="/update/{id}" hx-include="closest tr">
      Save
    </button>
  </td>
    </tr>
    """
    return response

@app.route("/get-task-row/<int:id>", methods=["GET"])
def get_task_row(id):
    task = Task.query.get(id)

    response = f"""
    <tr>
        <td>{task.title}</td>
        <td>{task.estimate}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{id}">
                Edit Title
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{id}"
                class="btn btn-primary">
                Delete
            </button>
        </td>
    </tr>
    """
    return response

@app.route("/update/<int:id>", methods=["PUT"])
def update_task(id):
    db.session.query(Task).filter(Task.task_id == id).update({"title": request.form["title"]})
    db.session.commit()
    task = Task.query.get(id)

    response = f"""
    <tr>
        <td>{task.id}
        <td>{task.title}</td>
        <td>{task.estimate}</td>
        <td>{task.status}
        <td>{task.notes}
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{id}">
                Edit Task
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{id}"
                class="btn btn-primary">
                Delete
            </button>
        </td>
    </tr>
    """
    return response

    
