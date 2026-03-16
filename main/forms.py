from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *


class InscriptionForm(UserCreationForm):
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True, label='Prénom')
    last_name  = forms.CharField(max_length=150, required=True, label='Nom')
    telephone  = forms.CharField(max_length=20, required=False)
    pays       = forms.CharField(max_length=100, required=False)

    class Meta:
        model  = Utilisateur
        fields = ('username', 'email', 'first_name', 'last_name',
                  'telephone', 'pays', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ConnexionForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ProfilForm(forms.ModelForm):
    class Meta:
        model  = Utilisateur
        fields = ('first_name', 'last_name', 'email', 'telephone', 'adresse', 'pays', 'photo_profil')
        widgets = {f: forms.TextInput(attrs={'class': 'form-control'})
                   for f in ('first_name', 'last_name', 'email', 'telephone', 'adresse', 'pays')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CommentaireForm(forms.ModelForm):
    class Meta:
        model  = Commentaire
        fields = ('note', 'texte')
        widgets = {
            'note':  forms.Select(choices=[(i, f'{i} étoile{"s" if i>1 else ""}') for i in range(1, 6)],
                                  attrs={'class': 'form-select'}),
            'texte': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                           'placeholder': 'Partagez votre expérience...'}),
        }


class ReservationForm(forms.ModelForm):
    class Meta:
        model  = Reservation
        fields = ('type_reservation', 'hebergement', 'guide',
                  'date_debut', 'date_fin', 'nb_personnes', 'notes')
        widgets = {
            'type_reservation': forms.Select(attrs={'class': 'form-select'}),
            'hebergement':      forms.Select(attrs={'class': 'form-select'}),
            'guide':            forms.Select(attrs={'class': 'form-select'}),
            'date_debut':       forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin':         forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nb_personnes':     forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'notes':            forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, destination=None, **kwargs):
        super().__init__(*args, **kwargs)
        if destination:
            self.fields['hebergement'].queryset = Hebergement.objects.filter(
                destination=destination, est_actif=True)
            self.fields['guide'].queryset = destination.guides.filter(est_disponible=True)
        self.fields['hebergement'].required = False
        self.fields['guide'].required = False


class DestinationForm(forms.ModelForm):
    class Meta:
        model  = Destination
        fields = ('nom', 'description', 'region', 'latitude', 'longitude',
                  'image_principale', 'video_url', 'prix_entree', 'est_active')
        widgets = {
            'nom':              forms.TextInput(attrs={'class': 'form-control'}),
            'description':      forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'region':           forms.Select(attrs={'class': 'form-select'}),
            'latitude':         forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude':        forms.NumberInput(attrs={'class': 'form-control'}),
            'video_url':        forms.URLInput(attrs={'class': 'form-control'}),
            'prix_entree':      forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'est_active':       forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class GuideForm(forms.ModelForm):
    class Meta:
        model  = Guide
        fields = ('nom', 'prenom', 'email', 'telephone', 'photo', 'biographie',
                  'langues', 'specialites', 'prix_journee', 'est_disponible', 'destinations')
        widgets = {
            'nom':           forms.TextInput(attrs={'class': 'form-control'}),
            'prenom':        forms.TextInput(attrs={'class': 'form-control'}),
            'email':         forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone':     forms.TextInput(attrs={'class': 'form-control'}),
            'biographie':    forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'langues':       forms.TextInput(attrs={'class': 'form-control'}),
            'specialites':   forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prix_journee':  forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'destinations':  forms.SelectMultiple(attrs={'class': 'form-select'}),
        }


class HebergementForm(forms.ModelForm):
    class Meta:
        model  = Hebergement
        fields = ('nom', 'type_hebergement', 'destination', 'description', 'adresse',
                  'telephone', 'email', 'site_web', 'image_principale',
                  'prix_nuit', 'capacite', 'nb_chambres',
                  'wifi', 'piscine', 'climatisation', 'parking', 'restaurant', 'est_actif')
        widgets = {
            'nom':              forms.TextInput(attrs={'class': 'form-control'}),
            'type_hebergement': forms.Select(attrs={'class': 'form-select'}),
            'destination':      forms.Select(attrs={'class': 'form-select'}),
            'description':      forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'adresse':          forms.TextInput(attrs={'class': 'form-control'}),
            'telephone':        forms.TextInput(attrs={'class': 'form-control'}),
            'email':            forms.EmailInput(attrs={'class': 'form-control'}),
            'site_web':         forms.URLInput(attrs={'class': 'form-control'}),
            'prix_nuit':        forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'capacite':         forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'nb_chambres':      forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
