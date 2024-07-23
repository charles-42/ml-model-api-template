from django.shortcuts import render
from .forms import SatisfactionForm
import requests
import logging
from dotenv import load_dotenv
import os
from app_web.opentelemetry_setup import prediction_counter_per_minute, logger, tracer
load_dotenv()

def main_view(request):
    
    with tracer.start_as_current_span("main_view_span"):
        result = None
        if request.method == 'POST':
            form = SatisfactionForm(request.POST)
            if form.is_valid():
                with tracer.start_as_current_span("form"):
                    produit_recu = form.cleaned_data['produit_recu']
                    temps_livraison = form.cleaned_data['temps_livraison']
                    
                    # Log the produit_recu value
                    logger.info(f"Produit reçu: {produit_recu}")
                    logger.info(f"Temps livraison: {temps_livraison}")
                    
                    app_name = os.getenv("APP_NAME")
                    # API Request
                    url = f'http://{app_name}.francecentral.azurecontainer.io:8000/predict'
                    api_token = os.getenv("TOKEN")
                    headers = {'Authorization': f'Bearer {api_token}'}
                    params = {'produit_recu': produit_recu, 'temps_livraison': temps_livraison}
                with tracer.start_as_current_span("external_api_request"):
                    response = requests.post(url, headers=headers, json=params)
                    if response.status_code == 200:
                        result = response.json()
                        prediction_value = result.get('prediction', 0)
                        logger.info(f"Prediction: {prediction_value}")
                        # Record prediction metrics
                        prediction_counter_per_minute.add(1)
                    
                    
                    else:
                        result = {'error': 'API request failed'}
        else:
            form = SatisfactionForm()

        return render(request, 'query_app/form_template.html', {'form': form, 'result': result})