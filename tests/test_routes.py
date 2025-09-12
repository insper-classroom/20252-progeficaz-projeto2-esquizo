import pytest
from app import create_app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": "API Imobiliária rodando!"}

def test_add_imoveis(client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
        
    novo_imovel = {
        "logradouro": "Rua das Flores",
        "tipo_logradouro": "Rua",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "cep": "01000-000",
        "tipo": "Apartamento",
        "valor": 500000.00,
        "data_aquisicao": "2023-05-10"
    }
    
    response = client.post('/add')
    assert response.status_code == 201
    data = response.get_json() #pega a resposta de json do programa(mensagem q voltara)
    assert data['message'] == 'alguma Coisa aconteceu' #faz a mensagem voltar desse jeito
    
