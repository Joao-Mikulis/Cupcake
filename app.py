from flask import Flask, render_template, request, jsonify
import os
import mysql.connector

app = Flask(__name__, template_folder='frontend/telas')

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'loja'
}

# Conecta ao banco de dados
db = mysql.connector.connect(**db_config)
cursor = db.cursor()

@app.route('/testar_conexao_banco')
def testar_conexao_banco():
    try:
        cursor.execute('SELECT 1')  # Executa uma query simples para testar a conexão
        return jsonify({'mensagem': 'Conexão com o banco de dados bem-sucedida!'})
    except mysql.connector.Error as e:
        return jsonify({'mensagem': f'Erro ao conectar ao banco de dados: {str(e)}'})

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('cadastrocliente.html')

# Rota para o formulário de cadastro
@app.route('/cadastro', methods=['POST'])
def cadastro():
    try:
        if request.method == 'POST':
            # Obtenha os dados do formulário
            dados_formulario = request.form

            # Execute a query para inserir os dados no banco
            query = "INSERT INTO clientes (nome, telefone, cep, cidade, endereco, numeroCasa, complemento) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (
                dados_formulario['nome'],
                dados_formulario['telefone'],
                dados_formulario['cep'],
                dados_formulario['cidade'],
                dados_formulario['endereco'],
                dados_formulario['numero_casa'],
                dados_formulario['complemento']
            )

            cursor.execute(query, values)
            db.commit()
            db.close()

            return jsonify({'mensagem': 'Cadastro realizado com sucesso!'})

    except Exception as e:
        return jsonify({'mensagem': f'Erro ao cadastrar cliente: {str(e)}'})

#Rota cadastro produto
@app.route('/cadastro_produto', methods=['GET', 'POST'])
def cadastro_produto():
    if request.method == 'POST':
        try:
            # Obtenha os dados do formulário
            dados_formulario = request.form

            # Salve a imagem em um diretório
            imagem = request.files['imagem']
            caminho_imagem = os.path.join(app.root_path, 'static', imagem.filename)
            imagem.save(caminho_imagem)

            # Execute a query para inserir os dados no banco
            query = "INSERT INTO produtos (nome, especificacao, valor, imagem, quantidade) VALUES (%s, %s, %s, %s, %s)"
            values = (
                dados_formulario['nome'],
                dados_formulario['especificacao'],
                dados_formulario['valor'],
                imagem.filename,
                dados_formulario['quantidade']
            )

            cursor.execute(query, values)
            db.commit()

            return jsonify({'mensagem': 'Cadastro de produto realizado com sucesso!'})
        except Exception as e:
            return jsonify({'mensagem': f'Erro ao cadastrar produto: {str(e)}'})
    else:
        return render_template('cadastroproduto.html')
    

if __name__ == '__main__':
    app.run(debug=True)
