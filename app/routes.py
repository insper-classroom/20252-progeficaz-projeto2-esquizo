from flask import Blueprint, jsonify
from .db import get_connection

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return jsonify({"message": "API Imobiliária rodando!"})

@bp.route('/imoveis')
def listar_imoveis():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM imoveis")
    rows = cursor.fetchall() #todas as linhas
    con.close()
    
    # Pega os nomes das colunas da tabela (id, logradouro, cidade, etc.)
    colunas = []
    for desc in cursor.description:
        colunas.append(desc[0]) #adiciona os nomes das colunas 

    # Agora cria a lista de imóveis como dicionários
    imoveis = []
    for row in rows:
        item = {}
        for i, valor in enumerate(row):
            nome_coluna = colunas[i]
            item[nome_coluna] = valor
        imoveis.append(item)
    return jsonify(imoveis) #retorna dados em formato json