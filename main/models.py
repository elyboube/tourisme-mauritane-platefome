from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# ─────────────────────────────────────────────
#  UTILISATEUR PERSONNALISÉ
# ─────────────────────────────────────────────
class Utilisateur(AbstractUser):
    ROLES = [
        ('visiteur', 'Visiteur'),
        ('utilisateur', 'Utilisateur'),
        ('admin', 'Administrateur'),
    ]
    role = models.CharField(max_length=20, choices=ROLES, default='visiteur')
    telephone = models.CharField(max_length=20, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    pays = models.CharField(max_length=100, blank=True, null=True)
    photo_profil = models.ImageField(upload_to='profils/', blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    est_actif = models.BooleanField(default=True)

    class Meta:
        db_table = 'UTILISATEUR'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def est_admin(self):
        return self.role == 'admin'

    def est_utilisateur_connecte(self):
        return self.role in ['utilisateur', 'admin']


# ─────────────────────────────────────────────
#  RÉGION
# ─────────────────────────────────────────────
class Region(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'REGION'

    def __str__(self):
        return self.nom


# ─────────────────────────────────────────────
#  DESTINATION
# ─────────────────────────────────────────────
class Destination(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='destinations')
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    image_principale = models.ImageField(upload_to='destinations/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="URL YouTube ou autre")
    prix_entree = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    est_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    # Champ calculé par trigger Oracle
    note_moyenne = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    nb_commentaires = models.IntegerField(default=0)

    class Meta:
        db_table = 'DESTINATION'
        verbose_name = 'Destination'
        verbose_name_plural = 'Destinations'

    def __str__(self):
        return self.nom


class ImageDestination(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='destinations/galerie/')
    legende = models.CharField(max_length=200, blank=True)
    ordre = models.IntegerField(default=0)

    class Meta:
        db_table = 'IMAGE_DESTINATION'
        ordering = ['ordre']


# ─────────────────────────────────────────────
#  GUIDE TOURISTIQUE
# ─────────────────────────────────────────────
class Guide(models.Model):
    LANGUES = [
        ('ar', 'Arabe'),
        ('fr', 'Français'),
        ('en', 'Anglais'),
        ('es', 'Espagnol'),
        ('wolof', 'Wolof'),
    ]
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='guides/', blank=True, null=True)
    biographie = models.TextField()
    langues = models.CharField(max_length=200, help_text="Langues séparées par virgule")
    specialites = models.TextField(blank=True, help_text="Zones / thèmes maîtrisés")
    prix_journee = models.DecimalField(max_digits=10, decimal_places=2)
    destinations = models.ManyToManyField(Destination, related_name='guides', blank=True)
    est_disponible = models.BooleanField(default=True)
    est_verifie = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    note_moyenne = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    class Meta:
        db_table = 'GUIDE'
        verbose_name = 'Guide'
        verbose_name_plural = 'Guides'

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


# ─────────────────────────────────────────────
#  HÉBERGEMENT
# ─────────────────────────────────────────────
class TypeHebergement(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    icone = models.CharField(max_length=50, default='fa-hotel')

    class Meta:
        db_table = 'TYPE_HEBERGEMENT'

    def __str__(self):
        return self.nom


class Hebergement(models.Model):
    nom = models.CharField(max_length=200)
    type_hebergement = models.ForeignKey(TypeHebergement, on_delete=models.SET_NULL, null=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='hebergements')
    description = models.TextField()
    adresse = models.CharField(max_length=300)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    site_web = models.URLField(blank=True)
    image_principale = models.ImageField(upload_to='hebergements/', blank=True, null=True)
    prix_nuit = models.DecimalField(max_digits=10, decimal_places=2)
    capacite = models.IntegerField(default=1)
    nb_chambres = models.IntegerField(default=1)
    est_actif = models.BooleanField(default=True)
    est_verifie = models.BooleanField(default=False)
    # Services
    wifi = models.BooleanField(default=False)
    piscine = models.BooleanField(default=False)
    climatisation = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    restaurant = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    note_moyenne = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    class Meta:
        db_table = 'HEBERGEMENT'
        verbose_name = 'Hébergement'
        verbose_name_plural = 'Hébergements'

    def __str__(self):
        return f"{self.nom} - {self.destination.nom}"


class ImageHebergement(models.Model):
    hebergement = models.ForeignKey(Hebergement, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hebergements/galerie/')
    legende = models.CharField(max_length=200, blank=True)
    ordre = models.IntegerField(default=0)

    class Meta:
        db_table = 'IMAGE_HEBERGEMENT'
        ordering = ['ordre']


# ─────────────────────────────────────────────
#  RÉSERVATION
# ─────────────────────────────────────────────
class Reservation(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée'),
        ('terminee', 'Terminée'),
    ]
    TYPE_RESERVATION = [
        ('hebergement', 'Hébergement'),
        ('guide', 'Guide'),
        ('package', 'Package complet'),
    ]

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='reservations')
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, related_name='reservations')
    type_reservation = models.CharField(max_length=20, choices=TYPE_RESERVATION)
    hebergement = models.ForeignKey(Hebergement, on_delete=models.SET_NULL, null=True, blank=True)
    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, null=True, blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    nb_personnes = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    # Prix calculé par Oracle (procédure stockée)
    prix_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    confirme_par = models.ForeignKey(
        Utilisateur, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reservations_confirmees'
    )

    class Meta:
        db_table = 'RESERVATION'
        verbose_name = 'Réservation'
        verbose_name_plural = 'Réservations'
        constraints = [
            models.CheckConstraint(
                check=models.Q(date_fin__gte=models.F('date_debut')),
                name='chk_dates_reservation'
            )
        ]

    def __str__(self):
        return f"Réservation #{self.pk} - {self.utilisateur.username}"

    def nb_nuits(self):
        return (self.date_fin - self.date_debut).days


# ─────────────────────────────────────────────
#  COMMENTAIRE & NOTE
# ─────────────────────────────────────────────
class Commentaire(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='commentaires')
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, null=True, blank=True, related_name='commentaires'
    )
    hebergement = models.ForeignKey(
        Hebergement, on_delete=models.CASCADE, null=True, blank=True, related_name='commentaires'
    )
    guide = models.ForeignKey(
        Guide, on_delete=models.CASCADE, null=True, blank=True, related_name='commentaires'
    )
    note = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Note de 1 à 5 étoiles"
    )
    texte = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    est_approuve = models.BooleanField(default=True)

    class Meta:
        db_table = 'COMMENTAIRE'
        verbose_name = 'Commentaire'
        verbose_name_plural = 'Commentaires'
        constraints = [
            models.CheckConstraint(
                check=models.Q(note__gte=1) & models.Q(note__lte=5),
                name='chk_note_valide'
            )
        ]

    def __str__(self):
        return f"Commentaire de {self.utilisateur.username} - {self.note}★"


# ─────────────────────────────────────────────
#  FAVORI
# ─────────────────────────────────────────────
class Favori(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='favoris')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True)
    hebergement = models.ForeignKey(Hebergement, on_delete=models.CASCADE, null=True, blank=True)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, null=True, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'FAVORI'
        verbose_name = 'Favori'
        verbose_name_plural = 'Favoris'

    def __str__(self):
        return f"Favori de {self.utilisateur.username}"


# ─────────────────────────────────────────────
#  NOTIFICATION
# ─────────────────────────────────────────────
class Notification(models.Model):
    TYPES = [
        ('reservation', 'Réservation'),
        ('confirmation', 'Confirmation'),
        ('annulation', 'Annulation'),
        ('info', 'Information'),
    ]
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    type_notif = models.CharField(max_length=20, choices=TYPES)
    titre = models.CharField(max_length=200)
    message = models.TextField()
    est_lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'NOTIFICATION'
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} → {self.utilisateur.username}"
