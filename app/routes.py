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

@bp.route('/imoveis/<int:id>', methods=['GET'])
def pega_imovel_por_id(id):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id=%s", (id,))
    row = cursor.fetchone() #pega de linha em linha
    con.close()
    
    if row is None:
        return jsonify({"error":"Imovel nao encontrado!"}), 404
    
    colunas = [desc[0] for desc in cursor.description]
    imovel={}
    for i, valor in enumerate(row):
        imovel[colunas[i]] = valor
    
    return jsonify(imovel), 200
@bp.route('/imoveis/<int:id>', methods=['DELETE'])
def deleta_imovel(id):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id=%s", (id,))
    con.commit()
    linha_afetada = cursor.rowcount
    con.close()
    
    if linha_afetada == 0:
        return jsonify({"error":"Imovel ja removido!"}), 404
    return jsonify({"message":"Imovel deletado!"}), 200
    
   