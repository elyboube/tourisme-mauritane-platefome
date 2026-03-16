# 🌍 Mauritanie Tourisme — Plateforme Web Django & Oracle

Plateforme de tourisme complète pour la Mauritanie, développée avec **Django** (partie applicative) et **Oracle** (base de données).

---

## 📁 Structure du projet

```
tourisme_mauritanie/
├── manage.py
├── requirements.txt
├── oracle_setup.sql          ← Script SQL complet Oracle
├── db.sqlite3                ← Base SQLite (développement)
│
├── tourisme/                 ← Configuration Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── main/                     ← Application principale
│   ├── models.py             ← 10 modèles Django
│   ├── views.py              ← ~30 vues
│   ├── forms.py              ← 7 formulaires
│   ├── urls.py               ← Routes complètes
│   ├── admin.py              ← Interface admin Django
│   └── management/
│       └── commands/
│           └── populate_demo.py  ← Données de démonstration
│
├── templates/                ← 26 templates HTML
│   ├── base.html             ← Template de base
│   ├── home/                 ← Accueil, home, favoris
│   ├── registration/         ← Connexion, inscription, profil
│   ├── destinations/         ← Liste + détail
│   ├── guides/               ← Liste + détail
│   ├── hebergements/         ← Liste, détail, comparaison
│   ├── reservations/         ← Créer, mes réservations
│   └── admin_panel/          ← Dashboard + gestion CRUD
│
└── static/
    ├── css/style.css         ← CSS personnalisé (palette Mauritanie)
    └── js/main.js            ← JavaScript (favoris, comparaison, prix)
```

---

## 🚀 Installation et lancement

### 1. Créer l'environnement virtuel
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Migrer la base de données (SQLite pour dev)
```bash
python manage.py makemigrations main
python manage.py migrate
```

### 4. Créer les données de démonstration
```bash
python manage.py populate_demo
```
Cette commande crée :
- **Admin** : `admin` / `admin123`
- **Utilisateurs test** : `alice`, `omar`, `sofia` / `test123`
- 8 destinations mauritaniennes
- 7 hébergements avec prix et services
- 4 guides certifiés
- 4 réservations avec différents statuts
- 8 commentaires et notes

### 5. Lancer le serveur
```bash
python manage.py runserver
```

Accès : http://127.0.0.1:8000/

---

## 🗄️ Configuration Oracle (production)

### 1. Exécuter le script SQL
```sql
-- En tant que SYS dans SQL*Plus :
@oracle_setup.sql
```

### 2. Activer Oracle dans settings.py
```python
# Décommenter dans tourisme/settings.py :
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'localhost:1521/ORCL',
        'USER': 'tourisme_user',
        'PASSWORD': 'tourisme_pass123',
    }
}
```

### 3. Installer le driver Oracle
```bash
pip install cx_Oracle
```

---

## 🎨 Palette de couleurs (Mauritanie)

| Couleur    | Variable CSS    | Hex       | Usage               |
|------------|-----------------|-----------|---------------------|
| Sable      | `--sable`       | `#C8A96E` | Accents, badges     |
| Désert     | `--desert`      | `#D4874E` | Boutons primaires   |
| Océan      | `--ocean`       | `#1A6B8C` | Boutons secondaires |
| Vert       | `--vert`        | `#2D7D46` | Statuts positifs    |
| Nuit       | `--nuit`        | `#1A1A2E` | Navbar, fond dark   |
| Crème      | `--creme`       | `#FAF7F2` | Fond de page        |

---

## 👥 Rôles utilisateurs

| Rôle          | Accès                                                              |
|---------------|--------------------------------------------------------------------|
| **Visiteur**  | Voir destinations, guides, hébergements. Créer un compte.         |
| **Utilisateur** | + Réserver, commenter, noter, gérer favoris, voir ses réservations |
| **Admin**     | + Confirmer réservations, CRUD complet, gérer utilisateurs         |

---

## 🗃️ Base de données Oracle — Récapitulatif

### Tables (13)
`UTILISATEUR`, `REGION`, `DESTINATION`, `IMAGE_DESTINATION`,
`TYPE_HEBERGEMENT`, `HEBERGEMENT`, `IMAGE_HEBERGEMENT`,
`GUIDE`, `GUIDE_DESTINATION`, `RESERVATION`, `COMMENTAIRE`,
`FAVORI`, `NOTIFICATION`, `AUDIT_RESERVATION`

### Triggers (8)
1. Auto-incrément ID avec séquences (`trg_*_bi`)
2. Calcul automatique prix à l'INSERT réservation
3. Recalcul prix à l'UPDATE réservation
4. Notification à la création d'une réservation
5. Notification au changement de statut (confirmation/annulation)
6. Mise à jour automatique `note_moyenne` + `nb_commentaires`
7. Vérification disponibilité hébergement (chevauchement dates)
8. Vérification disponibilité guide (pas de double réservation)
9. Interdiction suppression réservation confirmée
10. Audit log des changements de statut

### Packages (2)
- **`PKG_RESERVATION`** : `calculer_prix()`, `creer_reservation()`, `confirmer_reservation()`, `annuler_reservation()`
- **`PKG_STATISTIQUES`** : `stats_globales()`, `top_destinations()`, `top_hebergements()`, `reservations_par_mois()`

---

## 🌐 URLs disponibles

| URL                              | Description                    |
|----------------------------------|-------------------------------|
| `/`                              | Page d'accueil publique        |
| `/home/`                         | Home après connexion           |
| `/inscription/`                  | Créer un compte                |
| `/connexion/`                    | Se connecter                   |
| `/deconnexion/`                  | Se déconnecter                 |
| `/profil/`                       | Mon profil                     |
| `/destinations/`                 | Liste des destinations         |
| `/destinations/<id>/`            | Détail destination             |
| `/guides/`                       | Liste des guides               |
| `/guides/<id>/`                  | Profil guide                   |
| `/hebergements/`                 | Liste hébergements             |
| `/hebergements/<id>/`            | Détail hébergement             |
| `/hebergements/comparer/`        | Comparaison côte à côte        |
| `/reserver/<dest_id>/`           | Créer une réservation          |
| `/mes-reservations/`             | Mes réservations               |
| `/favoris/`                      | Mes favoris                    |
| `/api/favori/`                   | Toggle favori (AJAX)           |
| `/administration/`               | Dashboard admin                |
| `/administration/reservations/`  | Gestion réservations           |
| `/administration/destinations/`  | Gestion destinations           |
| `/administration/guides/`        | Gestion guides                 |
| `/administration/hebergements/`  | Gestion hébergements           |
| `/administration/utilisateurs/`  | Gestion utilisateurs           |

---

## 📋 Fonctionnalités clés

- ✅ Page d'accueil avec **vidéo** de fond
- ✅ Inscription / Connexion / Déconnexion / Profil
- ✅ Exploration destinations, guides, hébergements (sans compte)
- ✅ **Réservation** hébergement + guide pour une destination
- ✅ **Commentaires et notes** (1-5 étoiles)
- ✅ **Favoris** avec toggle AJAX
- ✅ **Comparaison** hébergements côte à côte
- ✅ **Notifications** automatiques (création, confirmation, annulation)
- ✅ Dashboard admin avec statistiques
- ✅ Confirmation réservations par l'admin
- ✅ CRUD complet (destinations, guides, hébergements, utilisateurs)
- ✅ 8 triggers Oracle (automatisation métier)
- ✅ 2 packages Oracle (logique transactionnelle)
- ✅ Calcul prix automatique (Oracle ou fallback Python)
- ✅ Pagination sur toutes les listes
- ✅ Filtres avancés (prix, services, région, type)
- ✅ Design responsive mobile
