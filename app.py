import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, flash
from models import Categoria, Produto, db_session, Funcionario, Movimentacao
from sqlalchemy import select

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return redirect('home')


@app.route('/home', methods=['GET'])
def home():
    return render_template('templates.html')


@app.route('/categoria', methods=['GET', 'POST'])
def categorias_func():
    lista_categoria = select(Categoria).select_from(Categoria)
    lista_categoria = db_session.execute(lista_categoria).scalars()
    resultado = []
    print(lista_categoria)
    for cat in lista_categoria:
        resultado.append(cat.serialize_categoria())
    # dicion = dicionario_colunas_cliente()
    # numero_resultados = len(resultado)
    return render_template('lista_categoria.html', var_categoria=resultado)


@app.route('/funcionario', methods=['GET', 'POST'])
def funcionarios_func():
    lista_funcionarios = select(Funcionario).select_from(Funcionario)
    lista_funcionarios = db_session.execute(lista_funcionarios).scalars()
    resultado = []
    print(lista_funcionarios)
    for func in lista_funcionarios:
        resultado.append(func.serialize_funcionario())
    # dicion = dicionario_colunas_cliente()
    # numero_resultados = len(resultado)
    return render_template('lista_funcionario.html', var_funcionario=resultado)


@app.route('/produto', methods=['GET', 'POST'])
def produtos_func():
    lista_produtos = select(Produto, Categoria).join(Categoria,
                                                     Produto.categoria_id == Categoria.ID_categoria)
    lista_produtos = db_session.execute(lista_produtos).fetchall()

    # dicion = dicionario_colunas_cliente()
    # numero_resultados = len(resultado)
    return render_template('lista_produto.html', var_funcionario=lista_produtos)


@app.route('/movimentacao', methods=['GET', 'POST'])
def movimentacao_func():
    lista_movimentacao = ((select(Movimentacao, Produto, Funcionario).
                          join(Produto, Produto.ID_produto == Movimentacao.produto_id)).
                          join(Funcionario, Movimentacao.funcionario_id == Funcionario.ID_funcionario))
    lista_movimentacao = db_session.execute(lista_movimentacao).fetchall()

    # dicion = dicionario_colunas_cliente()
    # numero_resultados = len(resultado)
    return render_template('lista_movimentacao.html', var_movimentacao=lista_movimentacao)


@app.route('/categoria/cadastro', methods=['GET', 'POST'])
def cadastro_categorias_func():
    if request.method == "POST":
        nome = request.form['form_nome_cat']

        if not nome:
            flash('Todos os campos devem estar preenchidos!', 'error')
        else:
            form_add = Categoria(nome_cat=nome)
            form_add.save()
            db_session.close()
            flash('Categoria cadastrada com sucesso!', 'success')

    return render_template('cadastro_categoria.html')


@app.route('/funcionario/cadastro', methods=['GET', 'POST'])
def cadastro_funcionarios_func():
    if request.method == "POST":
        nome = request.form['form_nome_funcionario']
        cpf = request.form['form_CPF']
        salario = request.form['form_salario']
        if not nome or not cpf or not salario:
            flash('Todos os campos devem estar preenchidos!', 'error')
        else:
            cpf_ = str(cpf)
            if len(cpf_) != 11:
                flash('Os campos estão preenchidos incorretamente!', 'error')
            else:
                cpf_f = '{0}.{1}.{2}-{3}'.format(cpf_[:3], cpf_[3:6], cpf_[6:9], cpf_[9:])
                try:
                    form_add = Funcionario(nome_funcionario=nome,
                                           CPF=cpf_f,
                                           salario=float(salario)
                                           )
                    form_add.save()
                    db_session.close()
                    flash('Funcionário cadastrado com sucesso!', 'success')
                except sqlalchemy.exc.IntegrityError:
                    flash('Algo ocorreu errado! Verifique se os campos estão corretos')
    return render_template('cadastro_funcionario.html')


if __name__ == '__main__':
    app.run(debug=True)



