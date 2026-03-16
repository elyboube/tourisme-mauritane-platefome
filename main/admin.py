from django.contrib import admin
from .models import *


@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'est_actif', 'date_inscription')
    list_filter  = ('role', 'est_actif')
    search_fields = ('username', 'email')


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('nom',)


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'region', 'note_moyenne', 'nb_commentaires', 'est_active')
    list_filter  = ('est_active', 'region')
    search_fields = ('nom',)


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'prix_journee', 'est_disponible', 'est_verifie', 'note_moyenne')
    list_filter  = ('est_disponible', 'est_verifie')


@admin.register(TypeHebergement)
class TypeHebergementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'icone')


@admin.register(Hebergement)
class HebergementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'destination', 'type_hebergement', 'prix_nuit', 'est_actif', 'note_moyenne')
    list_filter  = ('est_actif', 'est_verifie', 'type_hebergement')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'utilisateur', 'destination', 'type_reservation', 'statut', 'prix_total', 'date_creation')
    list_filter  = ('statut', 'type_reservation')
    readonly_fields = ('prix_total', 'date_creation', 'date_modification')


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'note', 'est_approuve', 'date_creation')
    list_filter  = ('note', 'est_approuve')
    actions      = ['approuver_commentaires']

    def approuver_commentaires(self, request, queryset):
        queryset.update(est_approuve=True)
    approuver_commentaires.short_description = "Approuver les commentaires sélectionnés"


@admin.register(Favori)
class FavoriAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'destination', 'hebergement', 'guide', 'date_ajout')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'type_notif', 'titre', 'est_lu', 'date_creation')
    list_filter  = ('type_notif', 'est_lu')
