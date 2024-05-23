from django import forms
# Définir le formulaire
class SatisfactionForm(forms.Form):
    produit_recu = forms.IntegerField(label='Produit Recu')
    temps_livraison = forms.IntegerField(label='Nombre de jours de livraisonc')
