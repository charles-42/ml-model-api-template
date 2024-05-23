import os
import pytest
from unittest.mock import patch
from django.urls import reverse
from django.test import Client
from query_app.forms import SatisfactionForm
from query_app.views import main_view

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def valid_post_data():
    return {
        'produit_recu': 1,
        'temps_livraison': 0
    }

@pytest.fixture
def invalid_post_data():
    return {
        'produit_recu': 'some_product',
        'temps_livraison': ''
    }

@patch('query_app.views.os.getenv')
@patch('query_app.views.requests.post')
def test_main_view_valid_form(mock_requests_post, mock_getenv, client, valid_post_data):
    # Mock environment variables
    mock_getenv.side_effect = lambda key: {
        'APP_NAME': 'test_app',
        'TOKEN': 'test_token'
    }.get(key)

    # Mock API response
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {'prediction': 'success'}

    # Make POST request with valid data
    response = client.post(reverse('form'), valid_post_data)

    # Check the response
    assert response.status_code == 200
    assert 'result' in response.context
    assert response.context['result'] == {'prediction': 'success'}
    assert isinstance(response.context['form'], SatisfactionForm)

@patch('query_app.views.os.getenv')
@patch('query_app.views.requests.post')
def test_main_view_invalid_form(mock_requests_post, mock_getenv, client, invalid_post_data):
    # Mock environment variables
    mock_getenv.side_effect = lambda key: {
        'APP_NAME': 'test_app',
        'TOKEN': 'test_token'
    }.get(key)

    # Mock API response (should not be called in this case)
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {'prediction': 'success'}

    # Make POST request with invalid data
    response = client.post(reverse('form'), invalid_post_data)

    # Check the response
    assert response.status_code == 200
    assert 'result' not in response.context or response.context['result'] is None
    assert isinstance(response.context['form'], SatisfactionForm)
    assert response.context['form'].is_valid() is False

@patch('query_app.views.os.getenv')
def test_main_view_get_request(mock_getenv, client):
    # Mock environment variables
    mock_getenv.side_effect = lambda key: {
        'APP_NAME': 'test_app',
        'TOKEN': 'test_token'
    }.get(key)

    # Make GET request
    response = client.get(reverse('form'))

    # Check the response
    assert response.status_code == 200
    assert 'result' not in response.context or response.context['result'] is None
    assert isinstance(response.context['form'], SatisfactionForm)
