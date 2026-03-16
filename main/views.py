from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import connection
from .models import *
from .forms import *
import json


# ─────────────────────────────────────────────
#  AUTHENTIFICATION
# ─────────────────────────────────────────────

def page_accueil(request):
    """Page d'accueil publique avec vidéo et highlights"""
    destinations = Destination.objects.filter(est_active=True).order_by('-note_moyenne')[:6]
    hebergements = Hebergement.objects.filter(est_actif=True).order_by('-note_moyenne')[:4]
    guides       = Guide.objects.filter(est_disponible=True).order_by('-note_moyenne')[:4]
    return render(request, 'home/accueil.html', {
        'destinations': destinations,
        'hebergements': hebergements,
        'guides': guides,
    })


def inscription(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'utilisateur'
            user.save()
            login(request, user)
            messages.success(request, f'Bienvenue {user.first_name} ! Votre compte a été créé.')
            return redirect('home')
    else:
        form = InscriptionForm()
    return render(request, 'registration/inscription.html', {'form': form})


def connexion(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = ConnexionForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenue {user.first_name or user.username} !')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Identifiants incorrects.')
    else:
        form = ConnexionForm()
    return render(request, 'registration/connexion.html', {'form': form})


@login_required
def deconnexion(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('accueil')


@login_required
def profil(request):
    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('profil')
    else:
        form = ProfilForm(instance=request.user)
    reservations = request.user.reservations.order_by('-date_creation')[:5]
    favoris      = request.user.favoris.select_related('destination', 'hebergement', 'guide')
    return render(request, 'registration/profil.html', {
        'form': form,
        'reservations': reservations,
        'favoris': favoris,
    })


def home(request):
    """Page home après connexion"""
    destinations = Destination.objects.filter(est_active=True).order_by('-note_moyenne')[:8]
    hebergements = Hebergement.objects.filter(est_actif=True).order_by('-note_moyenne')[:6]
    if request.user.is_authenticated:
        notifications = request.user.notifications.filter(est_lu=False)[:5]
    else:
        notifications = []
    return render(request, 'home/home.html', {
        'destinations': destinations,
        'hebergements': hebergements,
        'notifications': notifications,
    })


# ─────────────────────────────────────────────
#  DESTINATIONS
# ─────────────────────────────────────────────

def liste_destinations(request):
    qs = Destination.objects.filter(est_active=True).select_related('region')
    # Filtres
    q       = request.GET.get('q', '')
    region  = request.GET.get('region', '')
    tri     = request.GET.get('tri', 'note')

    if q:
        qs = qs.filter(Q(nom__icontains=q) | Q(description__icontains=q))
    if region:
        qs = qs.filter(region_id=region)
    if tri == 'note':
        qs = qs.order_by('-note_moyenne')
    elif tri == 'nom':
        qs = qs.order_by('nom')
    elif tri == 'prix':
        qs = qs.order_by('prix_entree')

    paginator   = Paginator(qs, 9)
    page_obj    = paginator.get_page(request.GET.get('page'))
    regions     = Region.objects.all()
    return render(request, 'destinations/liste.html', {
        'page_obj': page_obj,
        'regions': regions,
        'q': q,
        'region_sel': region,
        'tri': tri,
    })


def detail_destination(request, pk):
    destination  = get_object_or_404(Destination, pk=pk, est_active=True)
    commentaires = destination.commentaires.filter(est_approuve=True).select_related('utilisateur').order_by('-date_creation')
    hebergements = destination.hebergements.filter(est_actif=True)
    guides       = destination.guides.filter(est_disponible=True)
    is_favori    = False
    if request.user.is_authenticated:
        is_favori = Favori.objects.filter(utilisateur=request.user, destination=destination).exists()
    # Commentaire form
    form_comment = CommentaireForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form_comment = CommentaireForm(request.POST)
        if form_comment.is_valid():
            c = form_comment.save(commit=False)
            c.utilisateur  = request.user
            c.destination  = destination
            c.save()
            messages.success(request, 'Commentaire ajouté !')
            return redirect('destination_detail', pk=pk)
    return render(request, 'destinations/detail.html', {
        'destination': destination,
        'commentaires': commentaires,
        'hebergements': hebergements,
        'guides': guides,
        'is_favori': is_favori,
        'form_comment': form_comment,
    })


# ─────────────────────────────────────────────
#  GUIDES
# ─────────────────────────────────────────────

def liste_guides(request):
    qs = Guide.objects.filter(est_disponible=True)
    q  = request.GET.get('q', '')
    if q:
        qs = qs.filter(
            Q(nom__icontains=q) | Q(prenom__icontains=q) |
            Q(langues__icontains=q) | Q(specialites__icontains=q)
        )
    qs = qs.order_by('-note_moyenne')
    paginator = Paginator(qs, 9)
    page_obj  = paginator.get_page(request.GET.get('page'))
    return render(request, 'guides/liste.html', {'page_obj': page_obj, 'q': q})


def detail_guide(request, pk):
    guide        = get_object_or_404(Guide, pk=pk)
    commentaires = guide.commentaires.filter(est_approuve=True).select_related('utilisateur')
    destinations = guide.destinations.filter(est_active=True)
    is_favori    = False
    if request.user.is_authenticated:
        is_favori = Favori.objects.filter(utilisateur=request.user, guide=guide).exists()
    form_comment = CommentaireForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form_comment = CommentaireForm(request.POST)
        if form_comment.is_valid():
            c = form_comment.save(commit=False)
            c.utilisateur = request.user
            c.guide = guide
            c.save()
            messages.success(request, 'Commentaire ajouté !')
            return redirect('guide_detail', pk=pk)
    return render(request, 'guides/detail.html', {
        'guide': guide,
        'commentaires': commentaires,
        'destinations': destinations,
        'is_favori': is_favori,
        'form_comment': form_comment,
    })


# ─────────────────────────────────────────────
#  HÉBERGEMENTS
# ─────────────────────────────────────────────

def liste_hebergements(request):
    qs = Hebergement.objects.filter(est_actif=True).select_related('destination', 'type_hebergement')
    q          = request.GET.get('q', '')
    dest_id    = request.GET.get('destination', '')
    type_id    = request.GET.get('type', '')
    prix_max   = request.GET.get('prix_max', '')
    services   = request.GET.getlist('services')
    tri        = request.GET.get('tri', 'note')

    if q:
        qs = qs.filter(Q(nom__icontains=q) | Q(description__icontains=q))
    if dest_id:
        qs = qs.filter(destination_id=dest_id)
    if type_id:
        qs = qs.filter(type_hebergement_id=type_id)
    if prix_max:
        qs = qs.filter(prix_nuit__lte=prix_max)
    if 'wifi' in services:
        qs = qs.filter(wifi=True)
    if 'piscine' in services:
        qs = qs.filter(piscine=True)
    if 'parking' in services:
        qs = qs.filter(parking=True)
    if 'restaurant' in services:
        qs = qs.filter(restaurant=True)

    if tri == 'prix_asc':
        qs = qs.order_by('prix_nuit')
    elif tri == 'prix_desc':
        qs = qs.order_by('-prix_nuit')
    else:
        qs = qs.order_by('-note_moyenne')

    paginator    = Paginator(qs, 9)
    page_obj     = paginator.get_page(request.GET.get('page'))
    destinations = Destination.objects.filter(est_active=True)
    types        = TypeHebergement.objects.all()
    return render(request, 'hebergements/liste.html', {
        'page_obj': page_obj,
        'destinations': destinations,
        'types': types,
        'q': q,
        'dest_sel': dest_id,
        'type_sel': type_id,
        'prix_max': prix_max,
        'tri': tri,
    })


def detail_hebergement(request, pk):
    heb          = get_object_or_404(Hebergement, pk=pk, est_actif=True)
    commentaires = heb.commentaires.filter(est_approuve=True).select_related('utilisateur')
    is_favori    = False
    if request.user.is_authenticated:
        is_favori = Favori.objects.filter(utilisateur=request.user, hebergement=heb).exists()
    form_comment = CommentaireForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form_comment = CommentaireForm(request.POST)
        if form_comment.is_valid():
            c = form_comment.save(commit=False)
            c.utilisateur  = request.user
            c.hebergement  = heb
            c.save()
            messages.success(request, 'Commentaire ajouté !')
            return redirect('hebergement_detail', pk=pk)
    return render(request, 'hebergements/detail.html', {
        'heb': heb,
        'commentaires': commentaires,
        'is_favori': is_favori,
        'form_comment': form_comment,
    })


def comparer_hebergements(request):
    """Compare 2 à 3 hébergements côte à côte"""
    ids = request.GET.getlist('ids')
    hebs = []
    if ids:
        hebs = Hebergement.objects.filter(pk__in=ids[:3], est_actif=True)
    return render(request, 'hebergements/comparer.html', {'hebs': hebs})


# ─────────────────────────────────────────────
#  RÉSERVATIONS
# ─────────────────────────────────────────────

@login_required
def creer_reservation(request, dest_id):
    destination = get_object_or_404(Destination, pk=dest_id, est_active=True)
    hebergements = destination.hebergements.filter(est_actif=True)
    guides       = destination.guides.filter(est_disponible=True)

    if request.method == 'POST':
        form = ReservationForm(request.POST, destination=destination)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.utilisateur  = request.user
            reservation.destination  = destination
            # Calcul prix via Oracle ou Python fallback
            try:
                with connection.cursor() as cursor:
                    cursor.callproc('PKG_RESERVATION.creer_reservation', [
                        request.user.id,
                        destination.id,
                        reservation.type_reservation,
                        reservation.hebergement_id,
                        reservation.guide_id,
                        reservation.date_debut,
                        reservation.date_fin,
                        reservation.nb_personnes,
                        reservation.notes,
                        None, None
                    ])
            except Exception:
                # Fallback si Oracle non disponible
                nb_nuits = (reservation.date_fin - reservation.date_debut).days
                prix = 0
                if reservation.hebergement:
                    prix += reservation.hebergement.prix_nuit * nb_nuits
                if reservation.guide:
                    prix += reservation.guide.prix_journee * nb_nuits * reservation.nb_personnes
                reservation.prix_total = prix
                reservation.save()

            messages.success(request, 'Réservation créée ! Elle sera confirmée par notre équipe.')
            return redirect('mes_reservations')
    else:
        form = ReservationForm(destination=destination)

    return render(request, 'reservations/creer.html', {
        'form': form,
        'destination': destination,
        'hebergements': hebergements,
        'guides': guides,
    })


@login_required
def mes_reservations(request):
    reservations = request.user.reservations.select_related(
        'destination', 'hebergement', 'guide'
    ).order_by('-date_creation')
    return render(request, 'reservations/mes_reservations.html', {
        'reservations': reservations
    })


@login_required
def annuler_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, utilisateur=request.user)
    if reservation.statut in ['en_attente', 'confirmee']:
        reservation.statut = 'annulee'
        reservation.save()
        messages.success(request, 'Réservation annulée.')
    else:
        messages.error(request, 'Cette réservation ne peut pas être annulée.')
    return redirect('mes_reservations')


# ─────────────────────────────────────────────
#  FAVORIS (AJAX)
# ─────────────────────────────────────────────

@login_required
def toggle_favori(request):
    if request.method == 'POST':
        data     = json.loads(request.body)
        type_obj = data.get('type')
        obj_id   = data.get('id')
        kwargs   = {'utilisateur': request.user}
        if type_obj == 'destination':
            kwargs['destination_id'] = obj_id
        elif type_obj == 'hebergement':
            kwargs['hebergement_id'] = obj_id
        elif type_obj == 'guide':
            kwargs['guide_id'] = obj_id

        fav, created = Favori.objects.get_or_create(**kwargs)
        if not created:
            fav.delete()
            return JsonResponse({'status': 'removed'})
        return JsonResponse({'status': 'added'})
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


@login_required
def mes_favoris(request):
    favoris = request.user.favoris.select_related('destination', 'hebergement', 'guide')
    return render(request, 'home/favoris.html', {'favoris': favoris})


# ─────────────────────────────────────────────
#  NOTIFICATIONS
# ─────────────────────────────────────────────

@login_required
def marquer_notifications_lues(request):
    request.user.notifications.filter(est_lu=False).update(est_lu=True)
    return JsonResponse({'status': 'ok'})


# ─────────────────────────────────────────────
#  ADMINISTRATION
# ─────────────────────────────────────────────

def admin_required(view_func):
    """Décorateur : accès réservé aux administrateurs"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            messages.error(request, 'Accès réservé aux administrateurs.')
            return redirect('connexion')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    stats = {
        'nb_utilisateurs':  Utilisateur.objects.filter(est_actif=True).count(),
        'nb_reservations':  Reservation.objects.exclude(statut='annulee').count(),
        'nb_en_attente':    Reservation.objects.filter(statut='en_attente').count(),
        'nb_destinations':  Destination.objects.filter(est_active=True).count(),
        'nb_hebergements':  Hebergement.objects.filter(est_actif=True).count(),
        'nb_guides':        Guide.objects.filter(est_disponible=True).count(),
        'revenu_total':     Reservation.objects.filter(statut='confirmee').aggregate(
                                total=models.Sum('prix_total'))['total'] or 0,
    }
    reservations_recentes = Reservation.objects.select_related(
        'utilisateur', 'destination'
    ).order_by('-date_creation')[:10]
    return render(request, 'admin_panel/dashboard.html', {
        'stats': stats,
        'reservations_recentes': reservations_recentes,
    })


@admin_required
def admin_reservations(request):
    statut = request.GET.get('statut', '')
    qs = Reservation.objects.select_related('utilisateur', 'destination', 'hebergement', 'guide')
    if statut:
        qs = qs.filter(statut=statut)
    qs = qs.order_by('-date_creation')
    paginator = Paginator(qs, 20)
    page_obj  = paginator.get_page(request.GET.get('page'))
    return render(request, 'admin_panel/reservations.html', {
        'page_obj': page_obj,
        'statut_sel': statut,
    })


@admin_required
def admin_confirmer_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if reservation.statut == 'en_attente':
        reservation.statut      = 'confirmee'
        reservation.confirme_par = request.user
        reservation.save()
        messages.success(request, f'Réservation #{pk} confirmée.')
    else:
        messages.warning(request, 'Cette réservation ne peut pas être confirmée.')
    return redirect('admin_reservations')


@admin_required
def admin_destinations(request):
    destinations = Destination.objects.select_related('region').order_by('-date_creation')
    return render(request, 'admin_panel/destinations.html', {'destinations': destinations})


@admin_required
def admin_ajouter_destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Destination ajoutée.')
            return redirect('admin_destinations')
    else:
        form = DestinationForm()
    return render(request, 'admin_panel/form_destination.html', {'form': form, 'action': 'Ajouter'})


@admin_required
def admin_modifier_destination(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            messages.success(request, 'Destination modifiée.')
            return redirect('admin_destinations')
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'admin_panel/form_destination.html', {'form': form, 'action': 'Modifier'})


@admin_required
def admin_supprimer_destination(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.delete()
        messages.success(request, 'Destination supprimée.')
        return redirect('admin_destinations')
    return render(request, 'admin_panel/confirmer_suppression.html', {'obj': destination, 'type': 'destination'})


@admin_required
def admin_guides(request):
    guides = Guide.objects.order_by('-date_creation')
    return render(request, 'admin_panel/guides.html', {'guides': guides})


@admin_required
def admin_ajouter_guide(request):
    if request.method == 'POST':
        form = GuideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Guide ajouté.')
            return redirect('admin_guides')
    else:
        form = GuideForm()
    return render(request, 'admin_panel/form_guide.html', {'form': form, 'action': 'Ajouter'})


@admin_required
def admin_hebergements(request):
    hebs = Hebergement.objects.select_related('destination', 'type_hebergement').order_by('-date_creation')
    return render(request, 'admin_panel/hebergements.html', {'hebs': hebs})


@admin_required
def admin_ajouter_hebergement(request):
    if request.method == 'POST':
        form = HebergementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hébergement ajouté.')
            return redirect('admin_hebergements')
    else:
        form = HebergementForm()
    return render(request, 'admin_panel/form_hebergement.html', {'form': form, 'action': 'Ajouter'})


@admin_required
def admin_utilisateurs(request):
    utilisateurs = Utilisateur.objects.order_by('-date_inscription')
    return render(request, 'admin_panel/utilisateurs.html', {'utilisateurs': utilisateurs})


@admin_required
def admin_toggle_utilisateur(request, pk):
    user = get_object_or_404(Utilisateur, pk=pk)
    user.est_actif = not user.est_actif
    user.save()
    etat = 'activé' if user.est_actif else 'désactivé'
    messages.success(request, f'Compte de {user.username} {etat}.')
    return redirect('admin_utilisateurs')
