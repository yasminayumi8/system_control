#importar biblioteca.
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Boolean, DateTime

#importar session e sessionmaker.
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship

#configurar a conexão de banco.
engine = create_engine('sqlite:///base_estoque.sqlite3')

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
            'ID_categoria': self.ID_categoria,
            'nome_cat': self.nome_cat,
        }
        return dados_categoria


class Produto(Base):
    __tablename__ = 'produtos'
    ID_produto = Column(Integer, primary_key=True)
    categoria_id = Column(Integer, ForeignKey('categorias.ID_categoria'))
    nome_produto = Column(String(40), nullable=False, index =True)
    quantidade = Column(Integer, nullable=True, index=True)
    # valor = Column(Float, nullable=False, index=True)
    # categoria = Column(String(40), nullable=False, index=True)
    fornecedor = Column(String(40), nullable=False, index=True)
    # data = Column(String(11), nullable=False, index =True)
    descricao = Column(String(40))
    categoria_produto = relationship('Categoria')

    def __repr__(self):
        return '<produtos: {} #{}>'.format(self.nome_produto, self.ID_produto)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_produto(self):
        dados_produto = {
            'ID_produto': self.ID_produto,
            'nome_produto': self.nome_produto,
            'quantidade': self.quantidade,
            'valor': self.valor,
            'fornecedor': self.fornecedor,
            'descricao': self.descricao,
        }
        return dados_produto


class Funcionario(Base):
    __tablename__ = 'funcionarios'
    ID_funcionario = Column(Integer, primary_key=True)
    nome_funcionario = Column(String(40), nullable=False, index=True)
    CPF = Column(String(11), nullable=False, index=True, unique=True)
    salario = Column(Float, nullable=False, index=True)

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
            'ID_funcionario': self.ID_funcionario,
            'nome_funcionario': self.nome_funcionario,
            'CPF': self.CPF,
            'salario': self.salario,
        }
        return dados_funcionario

class Movimentacao(Base):
    __tablename__ = 'movimentacao'
    quantidade = Column(Integer, nullable=False, index=True)
    ID_movimentacao = Column(Integer,primary_key=True)
    produto_id = Column(Integer, ForeignKey('produtos.ID_produto'))
    funcionario_id = Column(Integer, ForeignKey('funcionarios.ID_funcionario'))
    data1 = Column(String(11), nullable=False, index=True)
    status = Column(Boolean, nullable=False, index=True, default=False)
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
            'ID_movimentacao': self.ID_movimentacao,
            'data1': self.data1,
            'status': self.status,
            'quantidade': self.quantidade,
            'funcionario_id': self.funcionario_id,
            'produto_id': self.produto_id,
        }
        return dados_movimentacao


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
