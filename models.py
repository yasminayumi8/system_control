#importar biblioteca.
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float

#importar session e sessionmaker.
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship

#configurar a conexão de banco.
engine = create_engine('sqlite:///banco.sqlite3')

#gerenciar sessao com banco de dados.
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Categoria(Base):
    __tablename__ = 'categorias'
    ID_categoria = Column(Integer, primary_key=True)
    nome_cat = Column(String(40), nullable=False, index=True)


    def __repr__(self):
        return '<categorias: {} {}>'.format(self.nome_cat, self.ID_categoria)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_categoria(self):
        dados_categoria = {
            'id_categoria': self.ID_categoria,
            'nome_cat': self.nome_cat,
        }
        return dados_categoria


class Produto(Base):
    __tablename__ = 'produtos'
    ID_produto = Column(Integer, primary_key=True)
    categoria_id = Column(Integer, ForeignKey('categorias.ID_categoria'))
    nome_produto = Column(String(40), nullable=False, index =True)
    quantidade = Column(Integer, nullable=False, index=True)
    valor = Column(Float, nullable=False, index=True)
    categoria = Column(String(40), nullable=False, index=True)
    fornecedor = Column(String(40), nullable=False, index=True)
    data = Column(String(11), nullable=False, index =True)
    Descricao = Column(String(40), nullable=False, index=True)
    Produto = relationship('Categoria')

    def __repr__(self):
        return '<produtos: {} {}>'.format(self.nome_produto, self.ID_produto, self.categoria, self.fornecedor, self.data, self.valor, self.Descricao)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_produto(self):
        dados_produto = {
            'id_produto': self.ID_produto,
            'nome': self.nome_produto,
            'quantidade': self.quantidade,
            'valor': self.valor,
            'categoria': self.categoria,
            'fornecedor': self.fornecedor,
            'data': self.data,
            'descricao': self.Descricao,
        }
        return dados_produto


class Funcionario(Base):
    __tablename__ = 'funcionarios'
    ID_funcionario = Column(Integer, primary_key=True)
    categoria_id = Column(Integer, ForeignKey('categorias.ID_categoria'))
    nome_funcionario = Column(String(40), nullable=False, index=True)
    CPF = Column(String(11), nullable=False, index=True, unique=True)
    salario = Column(Float, nullable=False, index=True)
    Funcionario = relationship('Categoria')

    def __repr__(self):
        return '<funcionarios: {} {}>'.format(self.nome_funcionario, self.ID_funcionario, self.salario)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_funcionario(self):
        dados_funcionario = {
            'id_funcionario': self.ID_funcionario,
            'nome': self.nome_funcionario,
            'CPF': self.CPF,
            'salario': self.salario,
        }
        return dados_funcionario


class Movimentacao(Base):
    __tablename__ = 'movimentacao'
    quantidade = Column(Integer, nullable=False, index=True)
    produto = Column(String(40), nullable=False, index=True)
    ID_movimentacao = Column(Integer,primary_key=True)
    produto_id = Column(Integer, ForeignKey('produtos.ID_produto'))
    funcionario_id = Column(Integer, ForeignKey('funcionarios.ID_funcionario'))
    data1 = Column(String(11), nullable=False, index=True)
    status = Column(String(3), nullable=False, index=True)
    produto_relacao = relationship('Produto')
    funcionario_relacao = relationship('Funcionario')

    def __repr__(self):
        return '<funcionarios: {} {}>'.format(self.quantidade, self.ID_movimentacao, self.data1, self.status, self.produto)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_movimentacao(self):
        dados_movimentacao = {
            'id_movimentacao': self.ID_movimentacao,
            'data1': self.data1,
            'status': self.status,
            'quantidade': self.quantidade,
            'produto': self.produto,
        }
        return dados_movimentacao


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
