from django.urls import path
from . import views

urlpatterns = [
    # Pages publiques
    path('',                        views.page_accueil,         name='accueil'),
    path('home/',                   views.home,                 name='home'),

    # Authentification
    path('inscription/',            views.inscription,          name='inscription'),
    path('connexion/',              views.connexion,            name='connexion'),
    path('deconnexion/',            views.deconnexion,          name='deconnexion'),
    path('profil/',                 views.profil,               name='profil'),

    # Destinations
    path('destinations/',                       views.liste_destinations,       name='destinations'),
    path('destinations/<int:pk>/',              views.detail_destination,       name='destination_detail'),

    # Guides
    path('guides/',                             views.liste_guides,             name='guides'),
    path('guides/<int:pk>/',                    views.detail_guide,             name='guide_detail'),

    # Hébergements
    path('hebergements/',                       views.liste_hebergements,       name='hebergements'),
    path('hebergements/<int:pk>/',              views.detail_hebergement,       name='hebergement_detail'),
    path('hebergements/comparer/',              views.comparer_hebergements,    name='comparer_hebergements'),

    # Réservations
    path('reserver/<int:dest_id>/',             views.creer_reservation,        name='creer_reservation'),
    path('mes-reservations/',                   views.mes_reservations,         name='mes_reservations'),
    path('mes-reservations/<int:pk>/annuler/',  views.annuler_reservation,      name='annuler_reservation'),

    # Favoris
    path('favoris/',                            views.mes_favoris,              name='mes_favoris'),
    path('api/favori/',                         views.toggle_favori,            name='toggle_favori'),

    # Notifications
    path('api/notifications/lire/',             views.marquer_notifications_lues, name='notif_lire'),

    # Administration
    path('administration/',                     views.admin_dashboard,          name='admin_dashboard'),
    path('administration/reservations/',        views.admin_reservations,       name='admin_reservations'),
    path('administration/reservations/<int:pk>/confirmer/', views.admin_confirmer_reservation, name='admin_confirmer'),
    path('administration/destinations/',        views.admin_destinations,       name='admin_destinations'),
    path('administration/destinations/ajouter/', views.admin_ajouter_destination, name='admin_dest_ajouter'),
    path('administration/destinations/<int:pk>/modifier/', views.admin_modifier_destination, name='admin_dest_modifier'),
    path('administration/destinations/<int:pk>/supprimer/', views.admin_supprimer_destination, name='admin_dest_supprimer'),
    path('administration/guides/',              views.admin_guides,             name='admin_guides'),
    path('administration/guides/ajouter/',      views.admin_ajouter_guide,      name='admin_guide_ajouter'),
    path('administration/hebergements/',        views.admin_hebergements,       name='admin_hebergements'),
    path('administration/hebergements/ajouter/', views.admin_ajouter_hebergement, name='admin_heb_ajouter'),
    path('administration/utilisateurs/',        views.admin_utilisateurs,       name='admin_utilisateurs'),
    path('administration/utilisateurs/<int:pk>/toggle/', views.admin_toggle_utilisateur, name='admin_user_toggle'),
]
