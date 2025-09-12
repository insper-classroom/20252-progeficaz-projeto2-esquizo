from flask import Blueprint, jsonify, request
import sqlite3

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