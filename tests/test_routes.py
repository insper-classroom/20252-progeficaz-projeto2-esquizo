import pytest
from app import create_app
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

def teste_lista_imoveis(client):
    response = client.get('/imoveis')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'id' in data[0] #verificar no primeiro se existir
    assert 'cidade' in data[0]
    
def teste_pega_imovel_por_id_existente(client):
    response = client.get('/imoveis/28')
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
    
def teste_deleta_imovel_existente(client):
    lista = client.get("/imoveis").get_json()
    id_existente = lista[0]["id"]
    response = client.delete(f"/imoveis/{id_existente}")
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"message": "Imovel deletado!"}


def teste_deleta_imovel_inexistente(client):
    response = client.delete("/imoveis/999999999")
    assert response.status_code == 404
    data = response.get_json()
    assert data == {"error": "Imovel ja removido!"}
