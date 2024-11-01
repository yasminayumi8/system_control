from models import Categoria, db_session, Produto, Funcionario, Movimentacao
from sqlalchemy import select

#def chamar_func(tabela):
   # inserir_tabela()

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def inserir_categorias():
    categorias = Categoria(nome_cat=str(input('Nome da categoria: '))
                           )
    print(categorias)
    categorias.save()


def consultar_categorias():
    var_cat = select(Categoria)
    var_cat = db_session.execute(var_cat).all()
    print(var_cat)


def atualizar_categorias():
    var_pessoa = select(Categoria).where(str(input('Nome da categoria: ')) == Categoria.nome_cat)
    var_pessoa = db_session.execute(var_pessoa).scalar()
    print(var_pessoa)
    var_pessoa.nome = str(input('Novo Nome: '))
    var_pessoa.save()


def deletar_categorias():
    var_cat = select(Categoria).where(str(input('Novo Nome: ')) == Categoria.nome_cat)
    var_cat = db_session.execute(var_cat).scalar()
    var_cat.delete()

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def inserir_produtos():

    produtos = Produto(nome_produto=str(input('Nome do produto: ')),
                       ID_produto=int(input('id Produto: ')),
                       quantidade=int(input('Quantidade: ')),
                       valor=float(input('Valor: ')),
                       fornecedor=str(input('Fornecedor: ')),
                       categoria=str(input('Categoria: ')),
                       data=str(input('Data: ')),
                       Descricao=str(input('Descricao: '))
                       )
    print(produtos)
    produtos.save()


def consultar_produtos():
    var_cat = select(Produto)
    var_cat = db_session.execute(var_cat).all()
    print(var_cat)


def atualizar_produtos():
    var_pessoa = select(Produto).where(str(input('Nome: ')) == Produto.nome_produto)
    var_pessoa = db_session.execute(var_pessoa).scalar()
    print(var_pessoa)
    var_pessoa.nome = str(input('Novo Nome: '))
    var_pessoa.save()


def deletar_produtos():
    var_cat = select(Produto).where(str(input('Novo Nome: ')) == Produto.nome_produto)
    var_cat = db_session.execute(var_cat).scalar()
    var_cat.delete()

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------


def inserir_funcionarios():
    categorias = Funcionario(nome_funcionario=str(input('Nome do funcionario: ')),
                             ID_funcionario=int(input('Funcionario: ')),
                             CPF=str(input('CPF: ')),
                             salario=float(input('Salario: ')),
                             )
    print(categorias)
    categorias.save()


def consultar_funcionarios():
    var_cat = select(Funcionario)
    var_cat = db_session.execute(var_cat).all()
    print(var_cat)


def atualizar_funcionarios():
    var_pessoa = select(Funcionario).where(str(input('Nome: ')) == Funcionario.nome_funcionario)
    var_pessoa = db_session.execute(var_pessoa).scalar()
    print(var_pessoa)
    var_pessoa.nome = str(input('Novo Nome: '))
    var_pessoa.save()


def deletar_funcionarios():
    var_cat = select(Funcionario).where(str(input('Novo Nome: ')) == Funcionario.nome_funcionario)
    var_cat = db_session.execute(var_cat).scalar()
    var_cat.delete()

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------


def inserir_movimentacao():
    categorias = Movimentacao(produto=str(input('Produto: ')),
                              ID_movimentacao=int(input('Movimentacao: ')),
                              quantidade=int(input('Quantidade: ')),
                              data1=str(input('Data: ')),
                              status=str(input('Status: '))
                              )
    print(categorias)
    categorias.save()


def consultar_movimentacao():
    var_cat = select(Movimentacao)
    var_cat = db_session.execute(var_cat).all()
    print(var_cat)


def atualizar_movimentacao():
    var_pessoa = select(Movimentacao).where(str(input('Nome: ')) == Movimentacao.produto)
    var_pessoa = db_session.execute(var_pessoa).scalar()
    print(var_pessoa)
    var_pessoa.nome = str(input('Novo Nome: '))
    var_pessoa.save()


def deletar_movimentacao():
    var_cat = select(Movimentacao).where(str(input('Novo Nome: ')) == Movimentacao.produto)
    var_cat = db_session.execute(var_cat).scalar()
    var_cat.delete()


if __name__ == '__main__':

    while True:
        print('Oque você deseja fazer?')
        print('1.  categoria')
        print('2.  produto')
        print('3.  funcionario')
        print('4.  movimentacao')
        print('5. Sair')
        numero = input("Escolha: ")

        if numero == '1':
           print("MENU")
           print("1 -Inserir categoria")
           print("2 -Consultar categoria")
           print("3 -Atualizar categoria")
           print("4 -Deletar categoria")
           print("5 -Sair")
           escolha = input("escolha: ")
           if escolha == "1":
               inserir_categorias()
           elif escolha == "2":
               consultar_categorias()
           elif escolha == "3":
               atualizar_categorias()
           elif escolha == "4":
               deletar_categorias()
           elif escolha == "5":
               break

        elif numero == '2':
            print("MENU")
            print("1 -Inserir produto")
            print("2 -Consultar produto")
            print("3 -Atualizar produto")
            print("4 -Deletar produto")
            print("5 -Sair")
            escolha = input("escolha: ")
            if escolha == "1":
                inserir_produtos()
            elif escolha == "2":
                consultar_produtos()
            elif escolha == "3":
                atualizar_produtos()
            elif escolha == "4":
                 deletar_produtos()
            elif escolha == "5":
                break

        elif numero == '3':
            print("MENU")
            print("1 -inserir funcionario")
            print("2 -Consultar funcionario")
            print("3 -Atualizar funcionario")
            print("4 -Deletar funcionario")
            print("5 -Sair")
            escolha = input("escolha: ")
            if escolha == "1":
                inserir_funcionarios()
            elif escolha == "2":
                consultar_funcionarios()
            elif escolha == "3":
                atualizar_funcionarios()
            elif escolha == "4":
                deletar_funcionarios()
            elif escolha == "5":
                break

        elif numero == '4':
            print("MENU")
            print("1 -inserir movimentacao")
            print("2 -Consultar movimentacao")
            print("3 -Atualizar movimentacao")
            print("4 -Deletar movimentacao")
            print("5 -Sair")
            escolha = input("escolha: ")
            if escolha == "1":
               inserir_movimentacao()
            elif escolha == "2":
                consultar_movimentacao()
            elif escolha == "3":
                atualizar_movimentacao()
            elif escolha == "4":
                deletar_movimentacao()
            elif escolha == "5":
                break





