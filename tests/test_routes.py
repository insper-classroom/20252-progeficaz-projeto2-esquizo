import pytest
from app import create_app
from unittest.mock import patch, MagicMock
import flask


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
    
def test_update_imoveis(client):
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
    
    response = client.post('/update/1')
    assert response.status_code == 200
    data = response.get_json() 
    assert data['message'] == 'alguma Coisa aconteceu enquanto atualizava :0' 

def teste_lista_imoveis(client):
    response = client.get('/imoveis')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'id' in data[0] #verificar no primeiro se existir
    assert 'cidade' in data[0]
    
def teste_pega_imovel_por_id_existente(client):
    response = client.get('imoveis/1')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert len(data)>0
    assert 'id' in data 
    assert 'cidade' in data

def teste_pega_imovel_por_id_inexistente(client):
    response = client.get('imoveis/9999999999999')
    assert response.status_code == 404
    data = response.get_json()
    assert data == {"error":"Imovel nao encontrado!"}
    
