from flask import Flask, request, jsonify
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv('.cred')


# tudo q tiver com #✅ eh q o codigo parece com o do professor
# e tudo que tiver #VERIFICAR vou colocar uma explicacao do que faz o codigo

# Configurações para conexão com o banco de dados usando variáveis de ambiente
config = {
    'host': os.getenv('DB_HOST', 'localhost'),  # Obtém o host do banco de dados da variável de ambiente
    'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
    'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
    'database': os.getenv('DB_NAME', 'db_escola'),  # Obtém o nome do banco de dados da variável de ambiente
    'port': int(os.getenv('DB_PORT', 3306)),  # Obtém a porta do banco de dados da variável de ambiente
    'ssl_ca': os.getenv('SSL_CA_PATH')  # Caminho para o certificado SSL
}

# Função para conectar ao banco de dados
def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        # Tenta estabelecer a conexão com o banco de dados usando mysql-connector-python
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Erro: {err}")
        return None


app = Flask(__name__)

@app.route('/')
def home():#✅
    return jsonify({"message": "API Imobiliária rodando!"})


@app.route('/add', methods=['POST'])
def add_imoveis():#✅
    # conectar com a base de dados
    conn = connect_db()
    
    data = request.get_json() # VERIFICAR
    cursor = conn.cursor()

    logradouro = data.get("logradouro") #pega informacoes futuras que entram nas condicoes do post 
    tipo_logradouro = data.get("tipo_logradouro")
    bairro = data.get("bairro")
    cidade = data.get("cidade")
    cep = data.get("cep")
    tipo = data.get("tipo")
    valor = data.get("valor")
    data_aquisicao = data.get("data_aquisicao")
    
    cursor.execute("""
        INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)) #o que cada incognita representa
    conn.commit()

    return jsonify({"message": "Imóvel adicionado com sucesso"}), 201   

@app.route('/imoveis')
def listar_imoveis():#✅
    con = connect_db()
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

@app.route('/imoveis/<int:id>', methods=['GET'])
def pega_imovel_por_id(id):#✅
    con = connect_db()
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
    
@app.route('/update/<int:id>', methods=['PUT'])
def update_imoveis(id):#✅
    data = request.get_json()
    conn = connect_db()

    logradouro = data.get("logradouro") #pega informacoes futuras que entram nas condicoes do post 
    tipo_logradouro = data.get("tipo_logradouro")
    bairro = data.get("bairro")
    cidade = data.get("cidade")
    cep = data.get("cep")
    tipo = data.get("tipo")
    valor = data.get("valor")
    data_aquisicao = data.get("data_aquisicao")
    with conn as con:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE imoveis
            SET logradouro = %s, 
                tipo_logradouro = %s, 
                bairro = %s, 
                cidade = %s, 
                cep = %s, 
                tipo = %s, 
                valor = %s, 
                data_aquisicao = %s
            WHERE id = %s
        """, (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao, id)) #o que cada incognita representa
        con.commit()
    
    if cursor.rowcount == 0: #nenhuma linha foi editada entao o banco de dados  recebe um id nulo
        return jsonify({"message": "nao eh possivel realizar alguma alteracao"}), 404
        
    return jsonify({"message": "Imóvel alterado com sucesso"}), 200   

@app.route('/imoveis/cidade=<cidade>', methods=['GET'])
def list_cidades(cidade):#✅
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE cidade = %s", (cidade,)) #VERIFICAR
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

if __name__ == '__main__': #roda o flask
    app.run(debug=True)
    
@app.route('/imoveis/<int:id>', methods=['DELETE'])
def deleta_imovel(id):
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id = %s", (id,))
    con.commit()
    linha_afetada = cursor.rowcount
    con.close()

    if linha_afetada == 0:
        return jsonify({"error": "Imovel nao encontrado!"}), 404

    return jsonify({"message": "Imovel deletado com sucesso!"}), 200

