from model import TaskList
from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)
task_list = TaskList()


@app.route('/', methods=['GET'])
def task_list_view():
    tasks = task_list.get_task_list()
    return render_template('index.html', tasks=tasks)


@app.route('/add_task', methods=['POST'])
#Ajout de tache
def add_task():
    title = request.form['title']
    description = request.form['description']
    deadline = request.form['deadline']
    creation_date = datetime.now()

#s'il manque le titre la description ou la deadline, la tache sera considérée comme incomplete et un message apparaitra sur la page
    if not title or not description or not deadline:
        error_message = "Tâche incomplète, veuillez remplir tous les champs."
        tasks = task_list.get_task_list()
        return render_template('index.html', tasks=tasks, error_message=error_message)
    
    deadline_date = datetime.strptime(deadline, '%Y-%m-%d').date()

#si la deadline est mise avant la date actuelle, un message d'erreur d'affichera aussi
    if deadline_date < datetime.now().date():
        error_message = "La date limite doit être ultérieure à aujourd'hui."
        tasks = task_list.get_task_list()
        return render_template('index.html', tasks=tasks, error_message=error_message)

#si tout va bien et que la tacche est conforme, la tahc est ajoutée à l'objet task_list qui va l'écrire dans la base de données
    task_list.add_task(title, description, deadline, creation_date)
    return redirect('/')

#complète la tache qui va se faire barrer avec le css ensuite
@app.route('/complete_task', methods=['POST'])
def complete_task():
    task_id = int(request.form['id'])
    completed = 'completed' in request.form
    task_list.complete_task(completed, task_id)
    return redirect('/')

#supprime la page et la refresh pour ne plus afficher la tache supprimée
@app.route('/delete_task', methods=['POST'])
def delete_task():
    task_id = int(request.form['id'])
    task_list.delete_task(task_id)
    return redirect('/')

#affiche le message "Tache non trouvée si la fonction dans le model:get_task_by_id ne trouve pas la tâche en question "
@app.route('/edit_task/<int:task_id>', methods=['GET'])
def edit_task(task_id):
    task = task_list.get_task_by_id(task_id)
    if task is None:
        return "Tâche non trouvée."
    return render_template('edit.html', task=task)

#renvoie à la page de mise à jour de la tâche contenant un formulaire pour changer les attributs de la tâches
@app.route('/update_task', methods=['POST'])
def update_task():
    task_id = int(request.form['id'])
    title = request.form['title']
    description = request.form['description']
    deadline = request.form['deadline']

    task = task_list.get_task_by_id(task_id)
    if task is None:
        return "Tâche non trouvée."

    # Mettre à jour les attributs de la tâche
    task.title = title
    task.description = description
    task.deadline = deadline

    # Mettre à jour la tâche dans la liste
    task_list.update_task(task)

    return redirect('/')




if __name__ == "__main__":
    app.run(threaded=True)
