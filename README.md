# FlaskProject
Application web utilisant Flask. User authentication, Crud.

# Manuel d'utilisation

Pour pouvoir exécuter ce code sur votre machine, vous devez installer python et l’ajouter comme variable d’environnement.

Ouvrir le CMD et passer cette commande pour installer Flask
``` bash
pip install flask
```

Ouvrir le CMD dans le dossier principal et passer cette commande
``` bash
pip install -r requirements.txt
```

Pour réinitialiser la base de données SQLite, veuillez entrer python comme commande dans la CMD et ensuite entrer le code suivant et exécuter

```
from projetflask import db
db.drop_all()
db.create_all()
from projetflask.models import Utilisateur, Enseignant, Etudiant, Admin, Note, Module, Matiere
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
pp = bcrypt.generate_password_hash('password').decode('utf-8')
ad = Admin(email='admin@checkit.com', password=pp, role="admin")
db.session.add(ad)
db.session.commit()
exit()
```

Pour lancer l’application passer la commande suivante
```
python run.py
```

Pour vous connecter à la base de données en tant qu’admin, veuillez entrer le login suivant :  
	Email = admin@checkit.com  
	Mot de passe = password  
Vous pourrez ensuite modifier ce login

# Demo

https://youtu.be/fY-qKvKurCo
