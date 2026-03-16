"""
Commande Django pour peupler la base de données avec des données de démonstration.
Usage : python manage.py populate_demo
"""

import os
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from main.models import (
    Utilisateur, Region, Destination, TypeHebergement,
    Hebergement, Guide, Reservation, Commentaire, Notification
)
from datetime import date, timedelta
from decimal import Decimal


class Command(BaseCommand):
    help = 'Peuple la base de données avec des données de démonstration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🌍 Peuplement de la base de données...'))

        # ── SUPERUSER / ADMIN ──────────────────────────
        if not Utilisateur.objects.filter(username='admin').exists():
            admin = Utilisateur.objects.create(
                username='admin',
                email='admin@mauritanie-tourisme.mr',
                first_name='Admin',
                last_name='Système',
                role='admin',
                is_staff=True,
                is_superuser=True,
                password=make_password('admin123'),
                pays='Mauritanie',
            )
            self.stdout.write(self.style.SUCCESS('✓ Admin créé  (login: admin / mdp: admin123)'))
        else:
            admin = Utilisateur.objects.get(username='admin')

        # ── UTILISATEURS DE TEST ───────────────────────
        users_data = [
            ('alice', 'alice@test.mr', 'Alice', 'Diallo', 'Mauritanie', 'utilisateur'),
            ('omar', 'omar@test.mr', 'Omar', 'Ba', 'Mauritanie', 'utilisateur'),
            ('sofia', 'sofia@test.mr', 'Sofia', 'Lebrun', 'France', 'utilisateur'),
        ]
        users = {}
        for username, email, fn, ln, pays, role in users_data:
            u, created = Utilisateur.objects.get_or_create(
                username=username,
                defaults=dict(email=email, first_name=fn, last_name=ln,
                              pays=pays, role=role, password=make_password('test123'))
            )
            users[username] = u
            if created:
                self.stdout.write(f'  ✓ Utilisateur {username} créé')

        # ── RÉGIONS ────────────────────────────────────
        regions_data = [
            ('Adrar',            'Région désertique au nord, connue pour ses ksour historiques et ses majestueuses dunes de sable.'),
            ('Tagant',           'Plateau rocheux parsemé d\'oasis, villes caravanières et falaises spectaculaires.'),
            ('Dakhlet Nouadhibou','Région côtière autour de Nouadhibou, capitale économique et porte vers la pêche atlantique.'),
            ('Trarza',           'Région du fleuve Sénégal et de la capitale Nouakchott, entre désert et savane.'),
            ('Hodh el Chargui',  'Grande région orientale, porte du Sahara avec ses nomades et son architecture de terre.'),
            ('Assaba',           'Région centrale avec le massif de l\'Assaba et ses plateaux granitiques.'),
        ]
        regions = {}
        for nom, desc in regions_data:
            r, _ = Region.objects.get_or_create(nom=nom, defaults={'description': desc})
            regions[nom] = r
        self.stdout.write(self.style.SUCCESS(f'✓ {len(regions)} régions créées'))

        # ── DESTINATIONS ───────────────────────────────
        destinations_data = [
            {
                'nom': 'Chinguetti',
                'region': 'Adrar',
                'description': 'Cité caravanière légendaire, 7ème ville sainte de l\'Islam et ancienne capitale intellectuelle du monde arabo-berbère. Ses bibliothèques manuscrites et ses ksour de pierre rouge en font un trésor classé au patrimoine mondial de l\'UNESCO.',
                'prix_entree': Decimal('500'),
                'note_moyenne': Decimal('4.8'),
                'nb_commentaires': 47,
                'lat': 20.4536, 'lon': -12.3683,
            },
            {
                'nom': 'Ouadane',
                'region': 'Adrar',
                'description': 'Fondée au XIIe siècle, Ouadane fut un carrefour commercial majeur entre le Maghreb et l\'Afrique subsaharienne. Ses ruines millénaires et l\'ancienne ville fortifiée dominent l\'erg Ouarane.',
                'prix_entree': Decimal('300'),
                'note_moyenne': Decimal('4.6'),
                'nb_commentaires': 31,
                'lat': 20.9297, 'lon': -11.6239,
            },
            {
                'nom': 'Atar',
                'region': 'Adrar',
                'description': 'Capitale de la région Adrar, Atar est le point de départ idéal pour explorer les dunes de l\'Erg Chebbi mauritanien, les gorges de Terjit et les villes caravanières du désert.',
                'prix_entree': Decimal('0'),
                'note_moyenne': Decimal('4.3'),
                'nb_commentaires': 22,
                'lat': 20.5143, 'lon': -13.0498,
            },
            {
                'nom': 'Oasis de Terjit',
                'region': 'Adrar',
                'description': 'Véritable joyau caché au fond d\'une gorge rocheuse, l\'oasis de Terjit offre des sources d\'eau fraîche, des palmiers et une végétation luxuriante en plein cœur du Sahara.',
                'prix_entree': Decimal('200'),
                'note_moyenne': Decimal('4.9'),
                'nb_commentaires': 58,
                'lat': 20.2167, 'lon': -13.1333,
            },
            {
                'nom': 'Banc d\'Arguin',
                'region': 'Dakhlet Nouadhibou',
                'description': 'Parc national classé au patrimoine mondial, le Banc d\'Arguin est l\'un des plus grands parcs naturels d\'Afrique. Il abrite d\'immenses colonies d\'oiseaux migrateurs et les villages de pêcheurs imraguen.',
                'prix_entree': Decimal('1000'),
                'note_moyenne': Decimal('4.7'),
                'nb_commentaires': 39,
                'lat': 20.0000, 'lon': -16.5000,
            },
            {
                'nom': 'Nouakchott',
                'region': 'Trarza',
                'description': 'Capitale de la Mauritanie, Nouakchott est une ville moderne née du désert. Son marché central, ses mosquées, la plage des pêcheurs et le musée national en font une étape incontournable.',
                'prix_entree': Decimal('0'),
                'note_moyenne': Decimal('3.9'),
                'nb_commentaires': 66,
                'lat': 18.0735, 'lon': -15.9582,
            },
            {
                'nom': 'Nouadhibou',
                'region': 'Dakhlet Nouadhibou',
                'description': 'Deuxième ville de Mauritanie et capitale économique, Nouadhibou est célèbre pour son port, sa plage des épaves et son accès à la Réserve du Cap Blanc et aux phoques moines.',
                'prix_entree': Decimal('0'),
                'note_moyenne': Decimal('4.1'),
                'nb_commentaires': 19,
                'lat': 20.9333, 'lon': -17.0333,
            },
            {
                'nom': 'Tichitt',
                'region': 'Tagant',
                'description': 'L\'une des quatre anciennes villes caravanières classées par l\'UNESCO. Tichitt était un centre d\'apprentissage islamique réputé. Ses mosquées en pisé et ses puits anciens témoignent d\'une splendeur passée.',
                'prix_entree': Decimal('400'),
                'note_moyenne': Decimal('4.5'),
                'nb_commentaires': 14,
                'lat': 18.4667, 'lon': -9.5167,
            },
        ]

        destinations = {}
        for d in destinations_data:
            obj, created = Destination.objects.get_or_create(
                nom=d['nom'],
                defaults={
                    'region': regions[d['region']],
                    'description': d['description'],
                    'prix_entree': d['prix_entree'],
                    'note_moyenne': d['note_moyenne'],
                    'nb_commentaires': d['nb_commentaires'],
                    'latitude': d['lat'],
                    'longitude': d['lon'],
                    'est_active': True,
                }
            )
            destinations[d['nom']] = obj
        self.stdout.write(self.style.SUCCESS(f'✓ {len(destinations)} destinations créées'))

        # ── TYPES D'HÉBERGEMENT ─────────────────────────
        types_data = [
            ('Hôtel', 'fa-hotel'),
            ('Auberge', 'fa-bed'),
            ('Campement désert', 'fa-campground'),
            ('Maison d\'hôtes', 'fa-home'),
            ('Lodge éco', 'fa-tree'),
        ]
        types = {}
        for nom, icone in types_data:
            t, _ = TypeHebergement.objects.get_or_create(nom=nom, defaults={'icone': icone})
            types[nom] = t

        # ── HÉBERGEMENTS ────────────────────────────────
        hebergements_data = [
            {
                'nom': 'Hôtel Chinguetti Étoile',
                'type': 'Hôtel',
                'destination': 'Chinguetti',
                'description': 'Hôtel de charme au cœur de la vieille ville, construit en pierres traditionnelles. Toutes les chambres donnent sur la palmeraie avec vue sur les dunes.',
                'adresse': 'Vieille ville de Chinguetti, Adrar',
                'prix_nuit': Decimal('4500'),
                'capacite': 20,
                'nb_chambres': 10,
                'wifi': True, 'piscine': False, 'climatisation': True, 'parking': True, 'restaurant': True,
                'note_moyenne': Decimal('4.7'),
            },
            {
                'nom': 'Campement Sahara Dream',
                'type': 'Campement désert',
                'destination': 'Chinguetti',
                'description': 'Campement de luxe dans les dunes, avec tentes berbères décorées, feux de camp sous les étoiles et repas traditionnels préparés par des cuisiniers locaux.',
                'adresse': 'Erg de Chinguetti, 8km de la ville',
                'prix_nuit': Decimal('7500'),
                'capacite': 16,
                'nb_chambres': 8,
                'wifi': False, 'piscine': False, 'climatisation': False, 'parking': True, 'restaurant': True,
                'note_moyenne': Decimal('4.9'),
            },
            {
                'nom': 'Auberge Caravane d\'Or',
                'type': 'Auberge',
                'destination': 'Atar',
                'description': 'Auberge familiale tenue par une famille locale depuis trois générations. Point de départ idéal pour les excursions dans la région de l\'Adrar. Terrasse avec vue panoramique.',
                'adresse': 'Centre-ville d\'Atar, Adrar',
                'prix_nuit': Decimal('2800'),
                'capacite': 30,
                'nb_chambres': 15,
                'wifi': True, 'piscine': False, 'climatisation': True, 'parking': True, 'restaurant': True,
                'note_moyenne': Decimal('4.4'),
            },
            {
                'nom': 'Maison d\'Hôtes Oasis Terjit',
                'type': 'Maison d\'hôtes',
                'destination': 'Oasis de Terjit',
                'description': 'Maison d\'hôtes lovée dans l\'oasis, construite en harmonie avec la nature. Piscine naturelle, jardin de palmiers et cuisine traditionnelle mauritanienne bio.',
                'adresse': 'Gorge de Terjit, Adrar',
                'prix_nuit': Decimal('5500'),
                'capacite': 12,
                'nb_chambres': 6,
                'wifi': False, 'piscine': True, 'climatisation': False, 'parking': True, 'restaurant': True,
                'note_moyenne': Decimal('4.8'),
            },
            {
                'nom': 'Hôtel Atlantique Nouadhibou',
                'type': 'Hôtel',
                'destination': 'Nouadhibou',
                'description': 'Hôtel moderne face à l\'océan Atlantique. Idéal pour les voyageurs d\'affaires et les amateurs de pêche. Piscine extérieure, spa et restaurant de fruits de mer.',
                'adresse': 'Boulevard de l\'Atlantique, Nouadhibou',
                'prix_nuit': Decimal('8500'),
                'capacite': 60,
                'nb_chambres': 30,
                'wifi': True, 'piscine': True, 'climatisation': True, 'parking': True, 'restaurant': True,
                'note_moyenne': Decimal('4.2'),
            },
            {
                'nom': 'Lodge Banc d\'Arguin',
                'type': 'Lodge éco',
                'destination': 'Banc d\'Arguin',
                'description': 'Lodge écologique en bord de mer, certifié éco-tourisme. Observation des oiseaux, sorties en pirogue imraguen et nuitées en bungalows sur pilotis.',
                'adresse': 'Parc National du Banc d\'Arguin',
                'prix_nuit': Decimal('9000'),
                'capacite': 20,
                'nb_chambres': 10,
                'wifi': False, 'piscine': False, 'climatisation': True, 'parking': True, 'restaurant': True,
                'note_moyenne': Decimal('4.6'),
            },
            {
                'nom': 'Hôtel Marhaba Nouakchott',
                'type': 'Hôtel',
                'destination': 'Nouakchott',
                'description': 'Hôtel 4 étoiles au centre de Nouakchott, à proximité du marché central et des ministères. Business center, salle de conférence et navette aéroport.',
                'adresse': 'Avenue Gamal Abdel Nasser, Nouakchott',
                'prix_nuit': Decimal('6500'),
                'capacite': 80,
                'nb_chambres': 40,
                'wifi': True, 'piscine': True, 'climatisation': True, 'parking': True, 'restaurant': True,
                'note_moyenne': Decimal('4.1'),
            },
        ]

        hebergements = {}
        for h in hebergements_data:
            obj, created = Hebergement.objects.get_or_create(
                nom=h['nom'],
                defaults={
                    'type_hebergement': types[h['type']],
                    'destination': destinations[h['destination']],
                    'description': h['description'],
                    'adresse': h['adresse'],
                    'prix_nuit': h['prix_nuit'],
                    'capacite': h['capacite'],
                    'nb_chambres': h['nb_chambres'],
                    'wifi': h['wifi'],
                    'piscine': h['piscine'],
                    'climatisation': h['climatisation'],
                    'parking': h['parking'],
                    'restaurant': h['restaurant'],
                    'note_moyenne': h['note_moyenne'],
                    'est_actif': True,
                    'est_verifie': True,
                }
            )
            hebergements[h['nom']] = obj
        self.stdout.write(self.style.SUCCESS(f'✓ {len(hebergements)} hébergements créés'))

        # ── GUIDES ─────────────────────────────────────
        guides_data = [
            {
                'nom': 'Ould Ahmed', 'prenom': 'Mohamed',
                'email': 'mohamed.guide@mauritanie.mr',
                'telephone': '+222 22 11 00 01',
                'biographie': 'Guide certifié avec 15 ans d\'expérience dans la région de l\'Adrar. Né à Chinguetti, Mohamed connaît chaque dune et chaque manuscrit de la région. Il parle couramment arabe, français et anglais.',
                'langues': 'Arabe, Français, Anglais',
                'specialites': 'Désert Adrar, Manuscrits de Chinguetti, Treks dunes, Culture hassaniya',
                'prix_journee': Decimal('3500'),
                'dests': ['Chinguetti', 'Ouadane', 'Atar', 'Oasis de Terjit'],
                'note': Decimal('4.9'),
            },
            {
                'nom': 'Mint Sidi', 'prenom': 'Fatima',
                'email': 'fatima.guide@mauritanie.mr',
                'telephone': '+222 22 11 00 02',
                'biographie': 'Première femme guide certifiée de Mauritanie, Fatima est spécialisée dans l\'éco-tourisme et l\'ornithologie du Banc d\'Arguin. Auteure d\'un guide de terrain sur les oiseaux côtiers.',
                'langues': 'Arabe, Français, Espagnol',
                'specialites': 'Éco-tourisme, Ornithologie, Banc d\'Arguin, Villages Imraguen',
                'prix_journee': Decimal('4000'),
                'dests': ['Banc d\'Arguin', 'Nouadhibou'],
                'note': Decimal('4.8'),
            },
            {
                'nom': 'Diallo', 'prenom': 'Ibrahima',
                'email': 'ibrahima.guide@mauritanie.mr',
                'telephone': '+222 22 11 00 03',
                'biographie': 'Originaire du Trarza, Ibrahima est spécialisé dans les circuits culturels de Nouakchott et la région du fleuve Sénégal. Expert en gastronomie mauritanienne et artisanat local.',
                'langues': 'Français, Wolof, Pulaar',
                'specialites': 'Nouakchott, Fleuve Sénégal, Gastronomie, Artisanat',
                'prix_journee': Decimal('2500'),
                'dests': ['Nouakchott'],
                'note': Decimal('4.5'),
            },
            {
                'nom': 'Ould Dah', 'prenom': 'Brahim',
                'email': 'brahim.guide@mauritanie.mr',
                'telephone': '+222 22 11 00 04',
                'biographie': 'Chamelier et guide de trekking depuis 20 ans, Brahim organise des traversées du Sahara à dos de dromadaire. Il connaît les pistes ancestrales que seuls les nomades empruntent.',
                'langues': 'Arabe, Français',
                'specialites': 'Trekking chameau, Navigation désert, Survie Sahara, Astronomie',
                'prix_journee': Decimal('5000'),
                'dests': ['Chinguetti', 'Ouadane', 'Oasis de Terjit', 'Atar'],
                'note': Decimal('4.7'),
            },
        ]

        guides = {}
        for g in guides_data:
            obj, created = Guide.objects.get_or_create(
                email=g['email'],
                defaults={
                    'nom': g['nom'],
                    'prenom': g['prenom'],
                    'telephone': g['telephone'],
                    'biographie': g['biographie'],
                    'langues': g['langues'],
                    'specialites': g['specialites'],
                    'prix_journee': g['prix_journee'],
                    'note_moyenne': g['note'],
                    'est_disponible': True,
                    'est_verifie': True,
                }
            )
            for dnom in g['dests']:
                if dnom in destinations:
                    obj.destinations.add(destinations[dnom])
            guides[g['prenom']] = obj
        self.stdout.write(self.style.SUCCESS(f'✓ {len(guides)} guides créés'))

        # ── RÉSERVATIONS ───────────────────────────────
        today = date.today()
        resa_data = [
            {
                'user': users['alice'],
                'dest': destinations['Chinguetti'],
                'type': 'package',
                'heb': hebergements['Hôtel Chinguetti Étoile'],
                'guide': guides['Mohamed'],
                'debut': today + timedelta(days=15),
                'fin': today + timedelta(days=22),
                'nb': 2,
                'statut': 'confirmee',
                'prix': Decimal('63000'),
            },
            {
                'user': users['omar'],
                'dest': destinations['Banc d\'Arguin'],
                'type': 'hebergement',
                'heb': hebergements['Lodge Banc d\'Arguin'],
                'guide': None,
                'debut': today + timedelta(days=5),
                'fin': today + timedelta(days=8),
                'nb': 1,
                'statut': 'en_attente',
                'prix': Decimal('27000'),
            },
            {
                'user': users['sofia'],
                'dest': destinations['Oasis de Terjit'],
                'type': 'package',
                'heb': hebergements['Maison d\'Hôtes Oasis Terjit'],
                'guide': guides['Brahim'],
                'debut': today + timedelta(days=30),
                'fin': today + timedelta(days=35),
                'nb': 2,
                'statut': 'en_attente',
                'prix': Decimal('77500'),
            },
            {
                'user': users['alice'],
                'dest': destinations['Nouakchott'],
                'type': 'guide',
                'heb': None,
                'guide': guides['Ibrahima'],
                'debut': today - timedelta(days=30),
                'fin': today - timedelta(days=27),
                'nb': 3,
                'statut': 'terminee',
                'prix': Decimal('22500'),
            },
        ]

        for r in resa_data:
            if not Reservation.objects.filter(utilisateur=r['user'], destination=r['dest'], date_debut=r['debut']).exists():
                Reservation.objects.create(
                    utilisateur=r['user'],
                    destination=r['dest'],
                    type_reservation=r['type'],
                    hebergement=r['heb'],
                    guide=r['guide'],
                    date_debut=r['debut'],
                    date_fin=r['fin'],
                    nb_personnes=r['nb'],
                    statut=r['statut'],
                    prix_total=r['prix'],
                    confirme_par=admin if r['statut'] == 'confirmee' else None,
                )
        self.stdout.write(self.style.SUCCESS(f'✓ {len(resa_data)} réservations créées'))

        # ── COMMENTAIRES ───────────────────────────────
        commentaires_data = [
            (users['alice'],  'destination', 'Chinguetti',     5, 'Un voyage inoubliable ! Les dunes au coucher du soleil sont magiques. Les manuscrits de la bibliothèque sont époustouflants.'),
            (users['omar'],   'destination', 'Banc d\'Arguin', 5, 'La nature y est préservée et les oiseaux en nombre incroyable. Les pêcheurs imraguen sont très accueillants.'),
            (users['sofia'],  'destination', 'Oasis de Terjit',5, 'L\'eau fraîche dans le désert, c\'est presque irréel. Une halte de paradis après les dunes brûlantes.'),
            (users['alice'],  'hebergement', 'Campement Sahara Dream', 5, 'Nuit magique sous les étoiles du Sahara. Le personnel est aux petits soins et le couscous traditionnel est délicieux.'),
            (users['omar'],   'hebergement', 'Hôtel Chinguetti Étoile', 4, 'Très bel hôtel, architecture en harmonie avec la vieille ville. La vue sur les dunes depuis la terrasse est magnifique.'),
            (users['sofia'],  'guide',       'Mohamed',        5, 'Mohamed est un guide exceptionnel ! Sa connaissance de l\'histoire de Chinguetti est encyclopédique. Très patient et passionné.'),
            (users['alice'],  'guide',       'Brahim',         5, 'Le trek à dos de dromadaire organisé par Brahim est une expérience de vie. Il connaît le désert comme sa poche.'),
            (users['omar'],   'destination', 'Atar',           4, 'Bonne base pour explorer l\'Adrar. Marché animé et habitants très sympathiques.'),
        ]

        for user, ctype, nom, note, texte in commentaires_data:
            kwargs = {'utilisateur': user, 'note': note}
            if ctype == 'destination':
                kwargs['destination'] = destinations.get(nom)
            elif ctype == 'hebergement':
                kwargs['hebergement'] = hebergements.get(nom)
            elif ctype == 'guide':
                kwargs['guide'] = guides.get(nom)

            if not Commentaire.objects.filter(utilisateur=user, **{ctype: kwargs.get(ctype)}).exists():
                Commentaire.objects.create(texte=texte, est_approuve=True, **kwargs)

        self.stdout.write(self.style.SUCCESS(f'✓ {len(commentaires_data)} commentaires créés'))

        # ── NOTIFICATIONS ──────────────────────────────
        for username, u in users.items():
            Notification.objects.get_or_create(
                utilisateur=u,
                titre='Bienvenue sur MauritanieTourisme !',
                defaults={
                    'type_notif': 'info',
                    'message': f'Bonjour {u.first_name}, bienvenue sur la plateforme de tourisme de référence en Mauritanie. Explorez nos destinations et réservez votre aventure !',
                    'est_lu': False,
                }
            )

        self.stdout.write(self.style.SUCCESS('\n✅ Base de données peuplée avec succès !'))
        self.stdout.write(self.style.WARNING(
            '\n📋 Comptes de test :\n'
            '  Admin   → admin / admin123\n'
            '  Alice   → alice / test123\n'
            '  Omar    → omar  / test123\n'
            '  Sofia   → sofia / test123\n'
        ))
