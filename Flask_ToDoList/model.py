import sqlite3

#création de l'objet tâche
class Task:
    def __init__(self, id, title, description, completed, deadline, creation_date):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.deadline = deadline
        self.creation_date = creation_date

#création de l'objet liste de tache
class TaskList:
    
    #connection à la BDD SQlite3
    #création de la table tache dans la base de donnée si elle n'existe pas
    def __init__(self):
        self.conn = sqlite3.connect('tdlist.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                description TEXT,
                                deadline DATE,
                                completed INTEGER DEFAULT 0,
                                creation_date DATETIME
                            )''')
        self.conn.commit()

    #fonction qui ajoute la tâche dans la base de donnée avec les spécificités entrés sur l'Interface graphique
    def add_task(self, title, description, deadline, creation_date):
        conn = sqlite3.connect('tdlist.db')
        cursor = conn.cursor()
        creation_date_str = creation_date.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO tasks (title, description, deadline, creation_date) VALUES (?, ?, ?, ?)', (title, description, deadline, creation_date_str))
        conn.commit()
        cursor.close()
        conn.close()

    #fonction qui permet de mettre une tâche comme complétée
    def complete_task(self, completed, task_id):
        conn = sqlite3.connect('tdlist.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (int(completed), task_id))
        conn.commit()
        cursor.close()
        conn.close()

    #fonction pour avoir la liste des tâches afin de l'afficher sur l'interface graphique
    def get_task_list(self):
        conn = sqlite3.connect('tdlist.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, description, completed, deadline, creation_date FROM tasks ORDER BY completed ASC, creation_date DESC')
        tasks = []
        for row in cursor.fetchall():
            task_id, title, description, completed, deadline, creation_date = row
            task = Task(task_id, title, description, completed, deadline, creation_date)
            tasks.append(task)
        cursor.close()
        conn.close()
        return tasks
    
    #fonction qui vise à afficher une tache
    def get_task_by_id(self, task_id):
        conn = sqlite3.connect('tdlist.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, description, completed, deadline, creation_date FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        if row is not None:
            task_id, title, description, completed, deadline, creation_date = row
            task = Task(task_id, title, description, completed, deadline, creation_date)
            cursor.close()
            conn.close()
            return task
        else:
            cursor.close()
            conn.close()
            return None

    #fonction pour supprimer la tache sélectionnée 
    def delete_task(self, task_id):
        conn = sqlite3.connect('tdlist.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        cursor.close()
        conn.close()

    #fonction pour mettre à jour les informations d'une tâche suite à la modification par l'utilisateur via IU
    def update_task(self, updated_task):
        conn = sqlite3.connect('tdlist.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET title = ?, description = ?, deadline = ? WHERE id = ?', (updated_task.title, updated_task.description, updated_task.deadline, updated_task.id))
        conn.commit()
        cursor.close()
        conn.close()

