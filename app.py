import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select

from models import Categoria, Produto, db_session, Funcionario, Movimentacao


def dicionario_colunas_movimentacao():
    dicion = {
        "ID_movimentacao": "ID Movimentacao",
        "quantidade": "Quantidade",
        "data": "Valor Consulta",
        "status": "Entrada/Saída",

        "ID_produto": "Produto ID",
        "nome_produto": "Produto nome",
        "fornecedor": "Fabricante do Produto",

        "ID_categoria": "Categoria ID",
        "nome_cat": "Categoria nome",

        "ID_funcionario": "Funcionario ID",
        "nome_funcionario": "Funcionario nome"

    }
    return dicion


def dicionario_colunas_funcionario():
    dicion = {
        "ID_funcionario": "ID Funcionario",
        "nome_funcionario": "Nome Funcionario",
        "CPF": "CPF",
        "salario": "Salário"
    }
    return dicion


def dicionario_colunas_categoria():
    dicion = {
        "ID_categoria": "ID Categoria",
        "nome_cat": "Nome Categoria"
    }
    return dicion


def dicionario_colunas_produto():
    dicion = {
        "ID_produto": "ID Produto",
        "nome_produto": "Nome Produto",
        "fornecedor": "Fabricante",
        "nome_cat": "Nome Categoria"
    }
    return dicion


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return redirect('home')


@app.route('/home', methods=['GET'])
def home():
    return render_template('templates.html', modo_escuro=False)


@app.route('/cadastro', methods=['GET'])
def pagina_cadastro_func():
    return render_template('pagina-cadastro.html')


@app.route('/categoria', methods=['GET', 'POST'])
def categorias_func():
    lista_categoria = select(Categoria).select_from(Categoria)
    lista_categoria = db_session.execute(lista_categoria).scalars()
    resultado = []
    print(lista_categoria)
    for cat in lista_categoria:
        resultado.append(cat.serialize_categoria())
    dicion = dicionario_colunas_categoria()
    return render_template('lista_categoria.html',
                           var_categoria=resultado,
                           class_=Categoria,
                           pesquisa=False,
                           numero_resultados=len(resultado),
                           dicio=dicion)


@app.route('/funcionario', methods=['GET', 'POST'])
def funcionarios_func():
    lista_funcionarios = select(Funcionario).select_from(Funcionario)
    lista_funcionarios = db_session.execute(lista_funcionarios).scalars()
    resultado = []
    print(lista_funcionarios)
    for func in lista_funcionarios:
        resultado.append(func.serialize_funcionario())
    dicion = dicionario_colunas_funcionario()
    # numero_resultados = len(resultado)
    return render_template('lista_funcionario.html',
                           var_funcionario=resultado,
                           class_=Funcionario,
                           pesquisa=False,
                           numero_resultados=len(resultado),
                           dicio=dicion)


@app.route('/produto', methods=['GET', 'POST'])
def produtos_func():
    lista_produtos = select(Produto, Categoria).join(Categoria,
                                                     Produto.categoria_id == Categoria.ID_categoria)
    lista_produtos = db_session.execute(lista_produtos).fetchall()
    dicion = dicionario_colunas_produto()
    # dicion = dicionario_colunas_cliente()
    # numero_resultados = len(resultado)
    return render_template('lista_produto.html',
                           var_produto=lista_produtos,
                           class_=Produto,
                           pesquisa=False,
                           numero_resultados=len(lista_produtos),
                           dicio=dicion)


@app.route('/produto_<id_produto>')
def produto_detalhes_func(id_produto):
    lista_produtos = select(Produto, Categoria).join(
        Categoria, Produto.categoria_id == Categoria.ID_categoria).where(
        Produto.ID_produto == id_produto
    )
    lista_produtos = db_session.execute(lista_produtos).fetchone()
    return render_template('produto-detalhes.html', var_produto=lista_produtos)


@app.route('/movimentacao', methods=['GET', 'POST'])
def movimentacao_func():
    lista_movimentacao = select(Movimentacao, Produto, Funcionario, Categoria).join(
        Produto, Produto.ID_produto == Movimentacao.produto_id).join(
        Funcionario, Movimentacao.funcionario_id == Funcionario.ID_funcionario).join(
        Categoria, Produto.categoria_id == Categoria.ID_categoria)
    lista_movimentacao = db_session.execute(lista_movimentacao).fetchall()

    dicion = dicionario_colunas_movimentacao()
    # numero_resultados = len(resultado)
    return render_template('lista_movimentacao.html',
                           var_movimentacao=lista_movimentacao,
                           class_=Movimentacao,
                           pesquisa=False,
                           numero_resultados=len(lista_movimentacao),
                           dicio=dicion)


@app.route('/cadastro/categoria', methods=['GET', 'POST'])
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


@app.route('/cadastro/funcionario', methods=['GET', 'POST'])
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


@app.route('/cadastro/produtos', methods=['GET', 'POST'])
def cadastro_produtos_func():
    lista_cat = select(Categoria)
    lista_categoria = db_session.execute(lista_cat).scalars()
    resultado = []
    print(lista_categoria)
    for cat in lista_categoria:
        resultado.append(cat.serialize_categoria())
    if request.method == "POST":
        nome_form = request.form['form_nome_produto']
        # qtde = request.form['form_quantidade']
        id_categoria = request.form['form_id_categoria']
        fornecedor = request.form['form_fornecedor']
        descricao = request.form['form_descricao']

        if not nome_form or not id_categoria or not fornecedor:
            flash('Todos os campos devem estar preenchidos!', 'error')
        else:
            # id_categoria_ = select(Categoria).where(Categoria.ID_categoria == id_categoria)
            # id_categoria_ = db_session.execute(id_categoria_).scalar()
            # if not id_categoria_:
            #     flash('Não existe uma categoria com esse ID cadastrado', 'error')
            # else:
            form_add = Produto(nome_produto=nome_form,
                               quantidade=0,
                               descricao=descricao,
                               fornecedor=fornecedor,
                               categoria_id=int(id_categoria)
                               )
            form_add.save()
            db_session.close()
            flash('Produto cadastrado com sucesso!', 'success')

    return render_template('cadastro_produto.html', categorias=resultado)


@app.route('/cadastro/movimentacao', methods=['GET', 'POST'])
def cadastro_movimentacao_func():
    lista_funcionarios = select(Funcionario).select_from(Funcionario)
    lista_funcionarios = db_session.execute(lista_funcionarios).scalars()
    resultado_funcionario = []
    print(lista_funcionarios)
    for func in lista_funcionarios:
        resultado_funcionario.append(func.serialize_funcionario())

    lista_produtos = select(Produto).select_from(Produto)
    lista_produtos = db_session.execute(lista_produtos).scalars()
    resultado_produto = []
    for produto in lista_produtos:
        resultado_produto.append(produto.serialize_produto())

    if request.method == "POST":
        qtde = request.form['form_quantidade']
        id_produto = request.form['form_produto']
        id_funcionario = request.form['form_funcionario']
        data = request.form['form_data1']
        tipo_movimentacao = request.form['tipo_movimentacao']
        print(tipo_movimentacao)
        data_replace = data.replace('-', '')
        if not qtde or not id_produto or not data or not tipo_movimentacao:
            flash('Todos os campos devem estar preenchidos!', 'error')
        else:
            id_produto_sql = select(Produto).where(Produto.ID_produto == id_produto)
            id_produto_ = db_session.execute(id_produto_sql).scalar()
            if not id_produto_:
                flash('Não existe um produto com esse ID cadastrado', 'error')
            else:
                id_funcionario_sql = select(Funcionario).where(Funcionario.ID_funcionario == id_funcionario)
                id_funcionario_ = db_session.execute(id_funcionario_sql).scalar()
                if not id_funcionario_:
                    flash('Não existe um funcionario com esse ID cadastrado', 'error')
                else:
                    if tipo_movimentacao == '0' and id_produto_.quantidade - int(qtde) < 0:
                        print('primeiro iff')
                        flash('Não existe essa quantidade em estoque', 'error')
                    else:
                        data_f = '{}/{}/{}'.format(data_replace[6:], data_replace[4:6], data_replace[:4])
                        form_add = Movimentacao(quantidade=int(qtde),
                                                funcionario_id=int(id_funcionario),
                                                produto_id=int(id_produto),
                                                data1=data_f,
                                                status=bool(int(tipo_movimentacao))
                                                )
                        form_add.save()
                        # Salvar a movimentação no banco de dados
                        form_add.save()  # Aqui você adiciona a movimentação ao banco.

                        # Atualizar a quantidade do produto
                        try:
                            # Se o tipo de movimentação for entrada (tipo_movimentacao == "1"), somamos
                            if tipo_movimentacao == "1":  # Entrada
                                id_produto_.quantidade = (id_produto_.quantidade or 0) + int(qtde)
                            # Se o tipo de movimentação for saída (tipo_movimentacao == "0"), subtraímos
                            elif tipo_movimentacao == "0":  # Saída
                                id_produto_.quantidade = (id_produto_.quantidade or 0) - int(qtde)

                            # Salvar as alterações no banco
                            db_session.commit()

                            # Mensagem de sucesso ao usuário
                            flash('Movimentação cadastrada e quantidade do produto atualizada com sucesso!', 'success')
                        except Exception as e:
                            # Desfazer alterações se ocorrer um erro
                            db_session.rollback()
                            flash(f'Erro ao atualizar a quantidade do produto: {e}', 'error')

                            db_session.close()

    return render_template('cadastro_movimentacao.html', funcionarios=resultado_funcionario, produtos=resultado_produto)


dicionario_classes = {
    "<class 'models.Produto'>": Produto,
    "<class 'models.Funcionario'>": Funcionario,
    "<class 'models.Movimentacao'>": Movimentacao,
    "<class 'models.Categoria'>": Categoria,
}


# adicionar classes


@app.route('/pesquisar/<class_>', methods=['GET', 'POST'])
def pesquisar_func(class_):
    if request.method == 'POST':
        campo = request.form['campo']
        print(f'campo : {campo}')
        classe = dicionario_classes[class_]
        print(f'class : {classe}')
        termo_pesquisa = request.form.get('form-pesquisa')
        print(f'termo : {termo_pesquisa}')
        if not campo or not termo_pesquisa:
            flash('Por favor, selecione um campo e insira um termo de pesquisa.')
        #         tabelas que recebem FK precisam de um if específico (produto, movimentacao
        #         diferente de tabelas como categoria e funcionario
        if classe in [Categoria, Funcionario]:
            print('CATEGORIA / FUNCIONARIO')
            if 'ID' not in campo:
                print('geral')
                consulta = select(classe).where(getattr(classe, campo).like(f"%{termo_pesquisa}%"))
                lista_resultados = db_session.execute(consulta).scalars()
            else:
                print('exata')
                consulta = select(classe).where(getattr(classe, campo) == termo_pesquisa)
                lista_resultados = db_session.execute(consulta).scalars()
            resultado = []
            if classe == Categoria:
                print('CATEGORIAaaaaaaaa')

                for result in lista_resultados:
                    resultado.append(result.serialize_categoria())
                dicion = dicionario_colunas_categoria()
                return render_template('lista_categoria.html',
                                       var_categoria=resultado,
                                       numero_resultados=len(resultado),
                                       dicio=dicion,
                                       class_=class_,
                                       pesquisa=True)
            else:
                for result in lista_resultados:
                    resultado.append(result.serialize_funcionario())
                dicion = dicionario_colunas_funcionario()
                return render_template('lista_funcionario.html',
                                       var_funcionario=resultado,
                                       numero_resultados=len(resultado),
                                       dicio=dicion,
                                       class_=class_,
                                       pesquisa=True)
        elif classe == Produto:
            if campo == 'nome_cat':
                classe = Categoria
            if 'id' not in campo:
                consulta = select(Produto, Categoria).join(
                    Categoria, Produto.categoria_id == Categoria.ID_categoria).where(
                    getattr(classe, campo).like(f"%{termo_pesquisa}%")
                )
            else:
                consulta = select(Produto, Categoria).join(
                    Categoria, Produto.categoria_id == Categoria.ID_categoria).where(
                    getattr(classe, campo) == termo_pesquisa)

            resultado = db_session.execute(consulta).fetchall()
            dicion = dicionario_colunas_produto()
            return render_template('lista_produto.html',
                                   var_produto=resultado,
                                   numero_resultados=len(resultado),
                                   dicio=dicion,
                                   class_=class_,
                                   pesquisa=True)
        elif classe == Movimentacao:
            if campo in ['ID_produto', 'nome_produto', "fornecedor"]:
                classe = Produto
            elif campo in ['ID_categoria', 'nome_cat']:
                classe = Categoria
            elif campo in ['ID_funcionario', 'nome_funcionario']:
                classe = Funcionario
            print(classe)
            if 'ID' not in campo:
                if campo == 'status' and termo_pesquisa.lower() in lista_saida:
                    termo_pesquisa = '0'
                elif campo == 'status' and termo_pesquisa.lower() in lista_entrada:
                    termo_pesquisa = '1'
                print('geral')
                consulta = select(Movimentacao, Produto, Funcionario, Categoria).join(
                    Produto, Movimentacao.produto_id == Produto.ID_produto).join(
                    Funcionario, Movimentacao.funcionario_id == Funcionario.ID_funcionario
                ).join(Categoria, Produto.categoria_id == Categoria.ID_categoria).where(
                    getattr(classe, campo).like(f"%{termo_pesquisa}%")
                )
            else:
                print('exata')
                consulta = select(Movimentacao, Produto, Funcionario, Categoria).join(
                    Produto, Movimentacao.produto_id == Produto.ID_produto).join(
                    Funcionario, Movimentacao.funcionario_id == Funcionario.ID_funcionario
                ).join(Categoria, Produto.categoria_id == Categoria.ID_categoria).where(
                    getattr(classe, campo) == termo_pesquisa)

            dicion = dicionario_colunas_movimentacao()
            resultado = db_session.execute(consulta).fetchall()
            return render_template('lista_movimentacao.html',
                                   var_movimentacao=resultado,
                                   numero_resultados=len(resultado),
                                   dicio=dicion,
                                   class_=class_,
                                   pesquisa=True)


lista_saida = ['saida', 's', 'sa', 'sai', 'said']
lista_entrada = ['entrada', 'e', 'en', 'entr', 'entra', 'entrad']


@app.route('/editar-categoria<int:id_categoria>', methods=['GET', 'POST'])
def editar_categoria(id_categoria):
    print(f'ID categoria:{id_categoria}')
    edit_categoria = select(Categoria).where(Categoria.ID_categoria == id_categoria)
    edit_categoria = db_session.execute(edit_categoria).scalar()
    if request.method == 'POST':
        nome = request.form['form_nome_cat']

        if not nome:
            flash('Todos os campos devem estar preenchidos!', 'error')
        else:
            edit_categoria.nome_cat = nome
            edit_categoria.save()
            flash('Categoria editada com sucesso!', 'success')
            return redirect(url_for('categorias_func'))
    print(f'edit categoria id:{edit_categoria.ID_categoria}')
    return render_template('editar_categoria.html', edit_categoria=edit_categoria)


@app.route('/editar-funcionario<int:id_funcionario>', methods=['GET', 'POST'])
def editar_funcionario(id_funcionario):
    print(f'ID categoria:{id_funcionario}')
    edit_funcionario = select(Funcionario).where(Funcionario.ID_funcionario == id_funcionario)
    edit_funcionario = db_session.execute(edit_funcionario).scalar()




    if request.method == 'POST':
        nome = request.form['form_nome_funcionario']
        CPF = request.form['form_CPF']
        salario = request.form['form_salario']
        if not nome or not CPF or not salario:
            flash('Todos os campos devem estar preenchidos!', 'error')
        else:
            cpf_ = str(CPF)
            if len(cpf_) != 11:
                flash('Os campos estão preenchidos incorretamente!', 'error')
            else:
                cpf_f = '{0}.{1}.{2}-{3}'.format(cpf_[:3], cpf_[3:6], cpf_[6:9], cpf_[9:])
                if not nome:
                    flash('Todos os campos devem estar preenchidos!', 'error')
                else:
                    edit_funcionario.nome_funcionario = nome
                    edit_funcionario.CPF = cpf_f
                    edit_funcionario.salario = salario

                    edit_funcionario.save()
                    flash('Funcionário editado com sucesso!', 'success')
                    return redirect(url_for('funcionarios_func'))
    # print(f'edit categoria id:{edit_funcionario.ID_funcionario}')
    return render_template('editar_funcionario.html', edit_funcionario=edit_funcionario, cpf=int(edit_funcionario.CPF.replace('.', '').replace('-', '')))


@app.route('/home_', methods=['GET', 'POST'])
def modo_escuro_func():
    checkbox = request.form['form-checkbox']
    print(checkbox)
    return render_template('templates.html', modo_escuro=bool(int(checkbox)))


if __name__ == '__main__':
    app.run(debug=True)
