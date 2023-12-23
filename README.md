# Devoir maison : Génie logiciel

## Explication du projet :  

Ce devoir maison met en relation les connaissances acquises lors du semestre 9 du Master TAL et notre mémoire de recherche.  
Ainsi, nous utilisons des données issues du corpus créé pour notre mémoire qui s'intitule *Correction automatique de réponses textuelles contenant des énumérations : application aux examens théoriques des Galops 1 à 7*, encadré par Iana Atanassova.  

## Exercice 1 :  

Dans le premier exercice, nous devons créer une base de données MySQL via un script Python *(cf. le fichier Ex1_MarinePotier.ipynb)*.  
Cette base de données "questionsreponses" est composées de deux tables : "questions" et "reponses".  
La table "questions" est composée de :
- id : l'id des questions (clé primaire)
- question : les questions issues de notre corpus de mémoire
- type_question : le type de la question (si la réponse doit être rédigée dans un certain ordre ou non)
- niveau : le Galop auquel la question appartient (1 à 7)

La table "reponses" est composée de :
- id : l'id des réponses (clé primaire)
- reponse : les réponses issues de notre corpus de mémoire
- type_reponse : le type de la réponse (si elle doit être rédigée dans un certain ordre ou non)
- niveau : le Galop auquel la question associée appartient (1 à 7)
- question_id : l'id de la question à laquelle la réponse est liée (clé étrangère qui permet de joindre les tables)

Dans la première table, nous injectons 20 questions issues de notre corpus.  
Dans la seconde table, nous injectons 30 questions issues de notre corpus.  
Chaque question peut avoir plusieurs réponses possibles.  


## Exercice 2 :  

Dans le deuxième exercice, nous devons créer une API permettant de manipuler notre base de données créée dans l'exerice 1.  
Dans le fichier *Ex2_MarinePotier.ipynb*, chaque cellule permet respectivement les requêtes suivantes :
- L'accès à toutes les données de la table ”questions”
- L'accès à toutes les données de la table ”reponses”
- L'accès à toutes les données de la base de données
- L'accès à des questions spécifiques en se basant sur l'ID précisé
- L'accès à des réponses spécifiques en sa basant sur l'ID précisé
- L'accès à l'ajout d'une question à la base de données
- L'accès à l'ajout d'une réponse à la base de données (et à quelle question elle est jointe)
- L'accès à la mise à jour d'une question
- L'accès à la mise à jour d'une réponse
- L'accès à la suppression d'une question et de la réponse qui lui est associée

## Exercice 3 :

Dans le troisième exercice, nous devons créer une interface web permettant l'interaction et la manipulation des données de la base.  
Le but est de créer une page HTML et un élément de visualisation.  
Devant les difficultés rencontrées, le choix a été fait de ne pas réaliser cet exercice, à l'exception de la création d'une simple page HTML avec un bouton intéractif qui permet d'afficher les données de la base dans un tableau.
