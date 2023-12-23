from flask import Flask, request, jsonify, json, render_template
from mysql.connector import connect, Error
import os




app = Flask(__name__, static_url_path='/static')
app.config["UPLOAD_FOLDER"] = 'files'
os.makedirs('files', exist_ok='True') # Création du dossier nommé "files"




# Connexion à la base de donnée SQL :

user_input = 'root'
password = 'CentreTesniere1'
dbname = 'questionsreponses'

try:
    connection = connect(
        host="localhost",
        user = user_input,
        password = password,
        database=dbname
    )
    print(connection)
except Error as e:
    print(e)



# A dé-commenter si le problème apparaît de nouveau.
# Gestion de la suppression d'une réponse si la question qui lui est liée est supprimée :
#alter_query = """
#ALTER TABLE reponses
#ADD CONSTRAINT fk_question_id
#FOREIGN KEY (question_id)
#REFERENCES questions(id)
#”ON DELETE CASCADE;
#"""
#with connection.cursor() as cursor:
        #cursor.execute(alter_query)
        #connection.commit()



# Accès à la page de base :

@app.route('/api/v1/resources/base', methods=['GET'])
def home():
    return render_template('base.html')




# Accès à toutes les données de la table "questions" :

@app.route('/api/v1/resources/questions/all', methods=['GET'])
def api_questions_all():
    """
    Fonction qui permet d'afficher toutes les données de la table ”question”, issue de la base de données ”questionsreponses”
    
    :return: un dictionnaire JSON contenant toutes les questions de la table ”questions”.
    """

    query = 'SELECT * FROM questions'

   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return jsonify(results)




# Accès à toutes les données de la table "reponses" :

@app.route('/api/v1/resources/reponses/all', methods=['GET'])
def api_reponses_all():
    """
    Fonction qui permet d'afficher toutes les données de la table ”reponses”, issue de la base de données ”questionsreponses”
    
    :return: un dictionnaire JSON contenant toutes les réponses de la table ”reponses”.
    """

    query = 'SELECT * FROM reponses'

   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return jsonify(results)




# Accès à toutes les données de la base de données :

@app.route('/api/v1/resources/questions_reponses/all', methods=['GET'])
def api_questions_reponses_all():
    """
    Fonction qui permet d'afficher toutes les données jointes la table ”questions” et de la table ”reponses”, issues de la base de données ”questionsreponses”
    
    :return: un dictionnaire JSON contenant toutes les questions et leurs réponses liées.
    """

    query = '''
    SELECT q.*, r.id AS reponse_id, r.reponse, r.niveau 
    FROM questions q
    LEFT JOIN reponses r ON q.id = r.question_id
    '''
   
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    
    return jsonify(results)




# Accès à des données spécifiques de la base (en se basant sur l'ID) :

@app.errorhandler(404) # Erreur 404 si l'utilisateur demande un ID qui n'existe pas
def page_not_found(e):
    """
    Fonction qui permet de retourner un message d'erreur si l'utilisateur demande in ID qui n'existe pas.
    
    :return: un message d'erreur
    """

    return "<h1>404</h1><p>L'identifiant demandé n'existe pas.</p>", 404


@app.route('/api/v1/resources/questions', methods=['GET']) # Pour la table des questions
def api_questions():
    """
    Fonction qui permet d'afficher des données spécifiques de la table ”question” en se basant sur l'ID de la question.
    
    :return: un dictionnaire JSON contenant la question dont l'utilisateur a spécifié l'ID.
    """

    query = 'SELECT * FROM questions WHERE'
    to_filter = []

    query_parameters = request.args
    print(query_parameters)

    id = query_parameters.get('id')
        
    if id: 
        query += ' id=%s AND ' 
        to_filter.append(id)

    if not (id) :
        return page_not_found(404) # Redirection vers la page 404 si aucun paramètre n'est donné

    query = query[:-4] # Supression du dernier AND à la fin de la requête
    print(query, to_filter)
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query, to_filter)
        results = cursor.fetchall()

    return jsonify(results)


@app.route('/api/v1/resources/reponses', methods=['GET']) # Pour la table des réponses
def api_reponses():
    """
    Fonction qui permet d'afficher des données spécifiques de la table ”reponses” en se basant sur l'ID de la réponse.
    
    :return: un dictionnaire JSON contenant la réponse dont l'utilisateur a spécifié l'ID.
    """

    query = 'SELECT * FROM reponses WHERE'
    to_filter = []

    query_parameters = request.args
    print(query_parameters)

    id = query_parameters.get('id')
        
    if id: 
        query += ' id=%s AND ' 
        to_filter.append(id)

    if not (id) :
        return page_not_found(404) # Redirection vers la page 404 si aucun paramètre n'est donné

    query = query[:-4] # Supression du dernier AND à la fin de la requête
    print(query, to_filter)
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query, to_filter)
        results = cursor.fetchall()

    return jsonify(results)






# Accès à l'ajout des données à la base :

@app.route('/api/v1/resources/questions/create_question', methods=['POST']) # Creation d'une question
def create_question():
    """
    Fonction qui permet d'ajouter des données dans la table ”reponses”
    
    :return: un JSON contenant la nouvelle question créée
    """

    nouvelle_question = json.loads(request.data)

    id = nouvelle_question.get('id', '')
    question = nouvelle_question.get('question', '')
    type_question = nouvelle_question.get('type_question', '')
    niveau = nouvelle_question.get('niveau', '')

    query = "INSERT INTO questions (id, question, type_question, niveau) VALUES (%s, %s, %s, %s)"

    with connection.cursor() as cursor:
        cursor.execute(query, (id, question, type_question, niveau))
        connection.commit()

        # Création des données de la nouvelle réponse :
        question = {
            'id': id,
            'question': question,
            'type_question': type_question,
            'niveau': niveau
        }

        return jsonify(question)


@app.route('/api/v1/resources/reponses/create_reponse', methods=['POST']) # Creation d'une réponse
def create_reponse():
    """
    Fonction qui permet d'ajouter des données dans la table ”reponses”
    
    :return: un JSON contenant la nouvelle reponse créée
    """

    nouvelle_reponse = json.loads(request.data)

    id = nouvelle_reponse.get('id', '')
    reponse = nouvelle_reponse.get('reponse', '')
    type_reponse = nouvelle_reponse.get('type_reponse', '')
    niveau = nouvelle_reponse.get('niveau', '')
    question_id = nouvelle_reponse.get('question_id', '')

    query = "INSERT INTO reponses (id, reponse, type_reponse, niveau, question_id) VALUES (%s, %s, %s, %s, %s)"

    with connection.cursor() as cursor:
        cursor.execute(query, (id, reponse, type_reponse, niveau, question_id))
        connection.commit()

        # Création des données de la nouvelle réponse :
        rep = {
            'id': id,
            'reponse': reponse,
            'type_reponse': type_reponse,
            'niveau': niveau,
            'question_id': question_id
        }

        return jsonify(rep)




# Accès à la mise à jour des données dans la base :

@app.route('/api/v1/resources/questions/update_question', methods=['PUT']) # Pour la table des questions
def update_question():
    """
    Fonction qui permet de mettre à jour des données de la table ”questions”
    
    :return: un JSON contenant la nouvelle version de la question
    """

    updated_question = json.loads(request.data)

    question_id = updated_question.get('id') # ID de la question qu'on veut modifier
    updated_texte = updated_question.get('question', '')
    updated_type = updated_question.get('type_question', '')
    updated_niveau = updated_question.get('niveau', '')

    query = "UPDATE questions SET question = %s, type_question = %s, niveau = %s WHERE id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, (updated_texte, updated_type, updated_niveau, question_id))
        connection.commit()

        cursor.execute("SELECT * FROM questions WHERE id = %s", (question_id,))
        updated_question = cursor.fetchone()

        return jsonify(updated_question)


@app.route('/api/v1/resources/reponses/update_reponse', methods=['PUT']) # Pour la table des réponses
def update_reponse():
    """
    Fonction qui permet de mettre à jour des données de la table ”reponses”
    
    :return: un JSON contenant la nouvelle version de la réponse
    """

    updated_reponse = json.loads(request.data)

    reponse_id = updated_reponse.get('id') # ID de la réponse qu'on veut modifier
    updated_texte = updated_reponse.get('reponse', '')
    updated_type = updated_reponse.get('type_reponse', '')
    updated_niveau = updated_reponse.get('niveau', '')
    updated_question_id = updated_reponse.get('question_id', '')

    query = "UPDATE reponses SET reponse = %s, type_reponse = %s, niveau = %s, question_id = %s WHERE id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, (updated_texte, updated_type, updated_niveau, updated_question_id, reponse_id))
        connection.commit()

        cursor.execute("SELECT * FROM reponses WHERE id = %s", (reponse_id,))
        updated_reponse = cursor.fetchone()

        return jsonify(updated_reponse)





# Accès à la suppression des données dans la base : 

@app.route('/api/v1/resources/questions/delete_question', methods=['DELETE']) # Suppression de la question et de sa réponse associée
def delete_question():
    """
    Fonction qui permet de supprimer des données de la table ”questions” ainsi que la réponse qui lui est associée
    
    :return: un JSON contenant l'ID de la question qui a été supprimée
    """

    deleted_question = json.loads(request.data)
    id = deleted_question.get('id')

    query = "DELETE FROM questions WHERE id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, (id,))
        connection.commit()

        return jsonify(deleted_question)




if __name__ == '__main__': 

   app.secret_key = 'secretkey'
   app.run(debug = True)