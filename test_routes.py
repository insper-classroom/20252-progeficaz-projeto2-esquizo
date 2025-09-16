import pytest
from unittest.mock import patch, MagicMock
from servidor import app, connect_db  # Importamos a aplicação Flask e a função de conexão

#TO COLOCANDO #✅ NA FRENTE DE TODOS OS CODIGOS Q DEVERIAM ESTAR FUNCIONANDO

@pytest.fixture
def client():
    """Cria um cliente de teste para a servidor."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("servidor.connect_db")
def test_home(mock_connect_db, client):#✅
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": "API Imobiliária rodando!"}

@patch("servidor.connect_db")
def test_add_imoveis(mock_connect_db, client):#✅
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
    
    mock_connect_db.return_value = mock_conn
    response = client.post('/add', json=novo_imovel)
    assert response.status_code == 201
    data = response.get_json() #pega a resposta de json do programa(mensagem q voltara)
    assert data['message'] == "Imóvel adicionado com sucesso" #faz a mensagem voltar desse jeito
 
@patch("servidor.connect_db")   #✅
def test_update_imoveis(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

        
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
    mock_connect_db.return_value = mock_conn
    response = client.put('/update/1', json=novo_imovel) #converter novo imovel como json como faria no codigo original
    assert response.status_code == 200
    data = response.get_json() 
    assert data['message'] == "Imóvel alterado com sucesso" 

@patch("servidor.connect_db")
def teste_lista_imoveis(mock_connect_db, client):#✅
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    
    mock_cursor.description = [
        ("id",), ("logradouro",), ("cidade",)
    ]
    mock_cursor.fetchall.return_value = [
        (1, "Rua das Flores", "São Paulo"),
        (2, "Av. Paulista", "São Paulo")
    ]
    
    response = client.get('/imoveis')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'id' in data[0] #verificar no primeiro se existir
    assert 'cidade' in data[0]
    
@patch("servidor.connect_db")
def teste_pega_imovel_por_id_existente(mock_connect_db, client): #✅
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    
    mock_cursor.description = [
        ("id",), ("logradouro",), ("cidade",), ("valor",)
    ]

    # Simula um registro encontrado
    mock_cursor.fetchone.return_value = (
        1, "Rua das Flores", "São Paulo", 500000.00
    )
    
    response = client.get('/imoveis/1')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert len(data)>0
    assert 'id' in data 
    assert 'cidade' in data

@patch("servidor.connect_db")
def teste_pega_imovel_por_id_inexistente(mock_connect_db, client):#✅
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    # Simula que não encontrou nenhum registro
    mock_cursor.fetchone.return_value = None
    response = client.get('/imoveis/9999999999999')
    assert response.status_code == 404
    data = response.get_json()
    assert data == {"error":"Imovel nao encontrado!"}
    
@patch("servidor.connect_db")#✅
def test_list_cidades(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor #falsifica movimentos futuramente reais

    # Resultado fictício que o banco retornaria
    mock_cursor.fetchall.return_value = [
        (
            1,
            "Rua das Flores",
            "Rua",
            "Centro",
            "São Paulo",
            "01000-000",
            "Apartamento",
            500000.00,
            "2023-05-10"
        ),
        (
            2,
            "Av. Paulista",
            "Avenida",
            "Bela Vista",
            "São Paulo",
            "01310-100",
            "Comercial",
            2000000.00,
            "2021-11-15"
        )
    ]
    
    mock_cursor.description = [
        ("id",), ("logradouro",), ("tipo_logradouro",), ("bairro",),
        ("cidade",), ("cep",), ("tipo",), ("valor",), ("data_aquisicao",)
    ]

    mock_connect_db.return_value = mock_conn #retornar mock no lugar da conexao real
    
    # Faz a requisição GET para listar imóveis em São Paulo
    response = client.get('/imoveis/cidade=São Paulo')
    
    assert response.status_code == 200
    
    data = response.get_json()
    
    # Verifica se todos os imóveis vieram na resposta
    assert isinstance(data, list)
    assert len(data) == 2
    

    assert data[0]['logradouro'] == "Rua das Flores"
    assert data[0]['bairro'] == "Centro"
    assert data[0]['cidade'] == "São Paulo"
    assert data[0]['tipo'] == "Apartamento"
    assert data[0]['valor'] == 500000.00
    
    assert data[1]['logradouro'] == "Av. Paulista"
    assert data[1]['tipo_logradouro'] == "Avenida"
    assert data[1]['tipo'] == "Comercial"
    assert data[1]['valor'] == 2000000.00

@patch("servidor.connect_db")
def teste_deleta_imovel_existente(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    mock_cursor.rowcount = 1

    response = client.delete("/imoveis/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"message": "Imovel deletado com sucesso!"}

@patch("servidor.connect_db")
def teste_deleta_imovel_inexistente(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    mock_cursor.rowcount = 0

    response = client.delete("/imoveis/999999999")
    assert response.status_code == 404
    data = response.get_json()
    assert data == {"error": "Imovel nao encontrado!"}

@patch("servidor.connect_db")#✅
def test_list_tipos(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor #falsifica movimentos futuramente reais

    # Resultado fictício que o banco retornaria
    mock_cursor.fetchall.return_value = [
        (
            1,
            "Rua A",
            "Rua",
            "Centro",
            "São Paulo",
            "01000-000",
            "Casa",
            350000.00,
            "2022-01-10"
        ),
        (
            2,
            "Rua B",
            "Rua",
            "Jardins",
            "São Paulo",
            "01410-100",
            "Casa",
            750000.00,
            "2021-07-20"
        )
    ]
    
    mock_cursor.description = [
        ("id",), ("logradouro",), ("tipo_logradouro",), ("bairro",),
        ("cidade",), ("cep",), ("tipo",), ("valor",), ("data_aquisicao",)
    ]

    mock_connect_db.return_value = mock_conn #retornar mock no lugar da conexao real
    
    # Faz a requisição GET para listar imóveis em São Paulo
    response = client.get('/imoveis/tipo=Casa')
    
    assert response.status_code == 200
    
    data = response.get_json()
    
    # Verifica se todos os imóveis vieram na resposta
    assert isinstance(data, list)
    assert len(data) == 2
    

    assert data[0]['logradouro'] == "Rua A"
    assert data[0]['bairro'] == "Centro"
    assert data[0]['cidade'] == "São Paulo"
    assert data[0]['tipo'] == "Casa"
    assert data[0]['valor'] == 350000.00

    assert data[1]['logradouro'] == "Rua B"
    assert data[1]['bairro'] == "Jardins"
    assert data[1]['cidade'] == "São Paulo"
    assert data[1]['tipo'] == "Casa"
    assert data[1]['valor'] == 750000.00