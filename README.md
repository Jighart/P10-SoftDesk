## Initialisation du projet

### Windows :

#### • Récupération du projet

```
git clone https://github.com/Jighart/P10-SoftDesk.git
```

#### • Activer l'environnement virtuel

```
cd P10-SoftDesk
python -m venv venv 
venv\Scripts\activate.bat
```

#### • Installer les paquets requis

```
pip install -r requirements.txt
```


### MacOS et Linux :

#### • Récupération du projet
```
git clone https://github.com/Jighart/P10-SoftDesk.git
```

#### • Activer l'environnement virtuel
```
cd P10-SoftDesk 
python3 -m venv venv 
source venv/bin/activate
```

#### • Installer les paquets requis
```
pip install -r requirements.txt
```

## Utilisation

### Faire les migrations (si nécessaire) :

```
python manage.py migrate
```

### Lancer le serveur Django :

```
python manage.py runserver
```

Il est possible de naviguer dans l'API avec différents outils :

- la plateforme [Postman](https://www.postman.com/) ;
- l'outil de commandes [cURL](https://curl.se) ;
- l'interface intégrée Django REST framework à l'adresse http://127.0.0.1:8000/ (adresse par défaut, cf. points de terminaison ci-dessous).

La documentation est disponible sur [Postman](https://documenter.getpostman.com/view/26832348/2s93Y3w289).

### Liste des utilisateurs existants :

| *ID* | *Identifiant* | *Mot de passe*  |
|------|---------------|-----------------|
| 1    | TestUser1     | SoftDesk1234    |
| 2    | TestUser2     | SoftDesk1234    |
| 3    | TestUser3     | SoftDesk1234    |
| 4    | admin         | SoftDesk1234    |



### Liste des points de terminaison de l'API :

| #   | *Point de terminaison d'API*                                              | *Méthode HTTP* | *URL (base: http://127.0.0.1:8000)*       |
|-----|---------------------------------------------------------------------------|----------------|-------------------------------------------|
| 1   | Inscription de l'utilisateur                                              | POST           | /signup/                                  |
| 2   | Connexion de l'utilisateur                                                | POST           | /login/                                   |
| 3   | Récupérer la liste de tous les projets rattachés à l'utilisateur connecté | GET            | /projects/                                |
| 4   | Créer un projet                                                           | POST           | /projects/                                |
| 5   | Récupérer les détails d'un projet via son id                              | GET            | /projects/{id}/                           |
| 6   | Mettre à jour un projet                                                   | PUT            | /projects/{id}/                           |
| 7   | Supprimer un projet et ses problèmes                                      | DELETE         | /projects/{id}/                           |
| 8   | Ajouter un utilisateur (collaborateur) à un projet                        | POST           | /projects/{id}/users/                     |
| 9   | Récupérer la liste de tous les utilisateurs attachés à un projet          | GET            | /projects/{id}/users/                     |
| 10  | Supprimer un utilisateur d'un projet                                      | DELETE         | /projects/{id}/users/{id}/                |
| 11  | Récupérer la liste des problèmes liés à un projet                         | GET            | /projects/{id}/issues/                    |
| 12  | Créer un problème dans un projet                                          | POST           | /projects/{id}/issues/                    |
| 13  | Mettre à jour un problème dans un projet                                  | PUT            | /projects/{id}/issues/{id}/               |
| 14  | Supprimer un problème d'un projet                                         | DELETE         | /projects/{id}/issues/{id}/               |
| 15  | Créer des commentaires sur un problème                                    | POST           | /projects/{id}/issues/{id}/comments/      |
| 16  | Récupérer la liste de tous les commentaires liés à un problème            | GET            | /projects/{id}/issues/{id}/comments/      |
| 17  | Modifier un commentaire                                                   | PUT            | /projects/{id}/issues/{id}/comments/{id}/ |
| 18  | Supprimer un commentaire                                                  | DELETE         | /projects/{id}/issues/{id}/comments/{id}/ |
| 19  | Récupérer un commentaire via son id                                       | GET            | /projects/{id}/issues/{id}/comments/{id}/ |