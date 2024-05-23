from django.shortcuts import render
from .forms import SatisfactionForm
import requests
from dotenv import load_dotenv
import os
load_dotenv()


def main_view(request):
    result = None
    if request.method == 'POST':
        form = SatisfactionForm(request.POST)
        if form.is_valid():
            produit_recu = form.cleaned_data['produit_recu']
            temps_livraison = form.cleaned_data['temps_livraison']
            # Requête à l'API
            url = 'http://apimodeletemplate.francecentral.azurecontainer.io:8000/predict'  # Remplacez par l'URL de votre API
            api_token = os.getenv("TOKEN")
            headers = {'Authorization': f'Bearer {api_token}'}
            print(headers)
            params = {'produit_recu': produit_recu, 'temps_livraison': temps_livraison}
            response = requests.post(url, headers=headers, json=params)
            if response.status_code == 200:
                result = response.json()
            else:
                result = {'error': 'API request failed'}
    else:
        form = SatisfactionForm()

    return render(request, 'query_app/form_template.html', {'form': form, 'result': result})