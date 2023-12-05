from flask import Flask, render_template, request, redirect, url_for
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
        resultado = cursor.fetchone()  # Consumir o resultado da consulta
        if resultado:
            return jsonify({'mensagem': 'Conexão com o banco de dados bem-sucedida!'})
        else:
            return jsonify({'mensagem': 'Nenhum resultado encontrado na consulta.'})
    except mysql.connector.Error as e:
        return jsonify({'mensagem': f'Erro ao conectar ao banco de dados: {str(e)}'})

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/novidades')
def novidades():
    return render_template('novidades.html')



@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/obrigado')
def obrigado():
    return render_template('obrigado.html')

@app.route('/clientes')
def clientes():
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    return render_template('clientes.html', clientes=clientes)

# Rota para o formulário de cadastro
@app.route('/cadastrocliente', methods=['POST', 'GET'])
def cadastro():
    mensagem = None

    if request.method == 'POST':
        try:
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

            mensagem = 'Cadastro realizado com sucesso!'
        except Exception as e:
            mensagem = f'Erro ao cadastrar cliente: {str(e)}'

    return render_template('cadastrocliente.html', mensagem=mensagem)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    mensagem = None

    if request.method == 'POST':
        try:
            # Obtenha os dados do formulário
            dados_formulario = request.form

                 # Execute a query para atualizar os dados no banco
            query = "UPDATE clientes SET nome = %s, telefone = %s, cep = %s, cidade = %s, endereco = %s, numeroCasa = %s, complemento = %s WHERE id = %s"
            values = (
                dados_formulario['nome'],
                dados_formulario['telefone'],
                dados_formulario['cep'],
                dados_formulario['cidade'],
                dados_formulario['endereco'],
                dados_formulario['numero_casa'],
                dados_formulario['complemento'],
                id
            )

            cursor.execute(query, values)
            db.commit()

            mensagem = 'Cliente atualizado com sucesso!'
            
            # Redirecionar para a página de clientes após atualização
            return redirect(url_for('clientes'))
        except Exception as e:
            mensagem = f'Erro ao atualizar cliente: {str(e)}'

    # Se o método for GET, busque os detalhes do cliente pelo ID
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    cliente = cursor.fetchone()

    # Renderizar o formulário de edição com os detalhes do cliente
    return render_template('edit.html', mensagem=mensagem, cliente=cliente)

# Rota para excluir clientes
@app.route('/delete/<int:id>')
def delete(id):
    mensagem = None

    try:
        cursor.execute("DELETE FROM clientes WHERE id=%s", (id,))
        db.commit()
        mensagem = 'Cliente excluído com sucesso!'
    except Exception as e:
        mensagem = f'Erro ao excluir cliente: {str(e)}'

    return redirect(url_for('clientes'))

#Exibir produtos
@app.route('/produtos')
def produtos():
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    return render_template('produtos.html', produtos=produtos)


#Rota cadastro de produtos
@app.route('/cadastroproduto', methods=['GET', 'POST'])
def cadastro_produto():
    mensagem = None

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

            mensagem = 'Cadastro de produto realizado com sucesso!'
        except Exception as e:
            mensagem = f'Erro ao cadastrar produto: {str(e)}'

    return render_template('cadastroproduto.html', mensagem=mensagem)

@app.route('/editproduto/<int:id>', methods=['GET', 'POST'])
def editproduto(id):
    mensagem = None

    if request.method == 'POST':
        try:
            # Obtenha os dados do formulário
            dados_formulario = request.form
            nova_imagem = request.files['nova_imagem']

            # Verifique se uma nova imagem foi enviada
            if nova_imagem:
                caminho_nova_imagem = os.path.join(app.root_path, 'static', nova_imagem.filename)
                nova_imagem.save(caminho_nova_imagem)
                imagem = nova_imagem.filename
            else:
                # Se nenhuma nova imagem foi enviada, mantenha a imagem existente
                imagem = dados_formulario['imagem_existente']  # Esse campo deve ser incluído no seu formulário HTML

            # Execute a query para atualizar os dados no banco
            query = "UPDATE produtos SET nome = %s, especificacao = %s, valor = %s, imagem = %s, quantidade = %s WHERE id = %s"
            values = (
                dados_formulario['nome'],
                dados_formulario['especificacao'],
                dados_formulario['valor'],
                imagem,  # Use a variável da imagem aqui
                dados_formulario['quantidade'],
                id
            )

            cursor.execute(query, values)
            db.commit()

            mensagem = 'Produto atualizado com sucesso!'
            
            # Redirecionar para a página principal após atualização
            return redirect(url_for('produtos'))
        except Exception as e:
            mensagem = f'Erro ao atualizar produto: {str(e)}'

    # Se o método for GET, busque os detalhes do produto pelo ID
    cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
    produto = cursor.fetchone()

    # Renderizar o formulário de edição com os detalhes do produto
    return render_template('editproduto.html', mensagem=mensagem, produto=produto)


@app.route('/deleteproduto/<int:id>')
def deleteproduto(id):
    try:
        # Execute a query para excluir o produto pelo ID
        query = "DELETE FROM produtos WHERE id = %s"
        cursor.execute(query, (id,))
        db.commit()

        return redirect(url_for('produto'))
    except Exception as e:
        return f'Erro ao excluir produto: {str(e)}'
    

if __name__ == '__main__':
    app.run(debug=True)
