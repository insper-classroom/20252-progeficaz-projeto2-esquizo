
from flask import Blueprint, jsonify, request, redirect, url_for
import sqlite3
from .db import get_connection
from app.models import *

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return jsonify({"message": "API Imobiliária rodando!"})


@bp.route('/add', methods=['POST'])
def add_imoveis():
    data = request.get_json()
    con = sqlite3.connect('banco.db') #conexao com banco de dados
    con.row_factory = sqlite3.Row #linhas retornadas do bd

    logradouro = data.get("logradouro") #pega informacoes futuras que entram nas condicoes do post 
    tipo_logradouro = data.get("tipo_logradouro")
    bairro = data.get("bairro")
    cidade = data.get("cidade")
    cep = data.get("cep")
    tipo = data.get("tipo")
    valor = data.get("valor")
    data_aquisicao = data.get("data_aquisicao")
    
    con.execute("""
        INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)) #o que cada incognita representa
    con.commit()

    return jsonify({"message": "Imóvel adicionado com sucesso"}), 201   

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
    
@bp.route('/update/<int:id>', methods=['PUT'])
def update_imoveis(id):
    data = request.get_json()


    logradouro = data.get("logradouro") #pega informacoes futuras que entram nas condicoes do post 
    tipo_logradouro = data.get("tipo_logradouro")
    bairro = data.get("bairro")
    cidade = data.get("cidade")
    cep = data.get("cep")
    tipo = data.get("tipo")
    valor = data.get("valor")
    data_aquisicao = data.get("data_aquisicao")
    with sqlite3.connect('banco.db') as con:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE imoveis
            SET logradouro = ?, 
                tipo_logradouro = ?, 
                bairro = ?, 
                cidade = ?, 
                cep = ?, 
                tipo = ?, 
                valor = ?, 
                data_aquisicao = ?
            WHERE id = ?
        """, (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao, id)) #o que cada incognita representa
        con.commit()
    
    if cursor.rowcount == 0: #nenhuma linha foi editada entao o banco de dados  recebe um id nulo
        return jsonify({"message": "nao eh possivel realizar alguma alteracao"}), 404
        
    return jsonify({"message": "Imóvel alterado com sucesso"}), 200   

@bp.route('/imoveis/cidade=<cidade>', methods=['GET'])
def list_cidades():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE cidade = %s")
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