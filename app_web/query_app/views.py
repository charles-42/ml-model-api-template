from django.shortcuts import render
from .forms import SatisfactionForm
import requests
from dotenv import load_dotenv
import os
from opentelemetry import trace
from app_web.opentelemetry_setup import product_received_counter, delivery_time_counter, prediction_counter, prediction_sum, prediction_count
tracer = trace.get_tracer(__name__)

load_dotenv()

def main_view(request):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("main_view_span"):
        result = None
        if request.method == 'POST':
            form = SatisfactionForm(request.POST)
            if form.is_valid():
                produit_recu = form.cleaned_data['produit_recu']
                temps_livraison = form.cleaned_data['temps_livraison']
                
                # Record metrics for received values
                product_received_counter.add(produit_recu)
                delivery_time_counter.add(temps_livraison)
                
                app_name = os.getenv("APP_NAME")
                # API Request
                url = f'http://{app_name}.francecentral.azurecontainer.io:8000/predict'
                api_token = os.getenv("TOKEN")
                headers = {'Authorization': f'Bearer {api_token}'}
                params = {'produit_recu': produit_recu, 'temps_livraison': temps_livraison}
                response = requests.post(url, headers=headers, json=params)
                if response.status_code == 200:
                    result = response.json()
                    prediction_value = result.get('prediction', 0)
                    # Record prediction metrics
                    prediction_counter.add(1)
                    prediction_sum.add(prediction_value)
                    prediction_count.add(1)
                else:
                    result = {'error': 'API request failed'}
        else:
            form = SatisfactionForm()

        return render(request, 'query_app/form_template.html', {'form': form, 'result': result})



# def main_view(request):
#     with tracer.start_as_current_span("my_view_span"):
#         result = None
#         if request.method == 'POST':
#             form = SatisfactionForm(request.POST)
#             if form.is_valid():
#                 produit_recu = form.cleaned_data['produit_recu']
#                 temps_livraison = form.cleaned_data['temps_livraison']
#                 app_name = os.getenv("APP_NAME")
#                 # Requête à l'API
#                 url = f'http://{app_name}.francecentral.azurecontainer.io:8000/predict'  # Remplacez par l'URL de votre API
#                 api_token = os.getenv("TOKEN")
#                 headers = {'Authorization': f'Bearer {api_token}'}
#                 params = {'produit_recu': produit_recu, 'temps_livraison': temps_livraison}
#                 response = requests.post(url, headers=headers, json=params)
#                 if response.status_code == 200:
#                     result = response.json()
#                 else:
#                     result = {'error': 'API request failed'}
#         else:
#             form = SatisfactionForm()

#         return render(request, 'query_app/form_template.html', {'form': form, 'result': result})