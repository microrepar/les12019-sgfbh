"""Módulo com os modelos - classe de domínio
"""
from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime


class Funcionario(db.Model):

    __tablename__ = 'tb_funcionario'

    id = Column(Integer, primary_key=True)
    cpf = Column(String(14), index=True)        # TODO: verificar se precisa ser unique, com ou sem formatação
    rg = Column(String(12))                     # TODO: verificar se precisa ser unique, com ou sem formatação
    nome = Column(String(250))                  # TODO: tamanho necessário para o campo
    sexo = Column(String(20))
    dataNascimento = Column(Date)
    pisPasep = Column(String(11))
    email = Column(String(150))
    responsavelCadastro = Column(String(200))
    matricula = Column(Integer, index=True, unique=True)
    # cargo = Column(String(200))                 # TODO: tamanho necessário para o campo
    dataAdmissao = Column(DateTime)
    dataCadastro = Column(DateTime, default=datetime.utcnow)
    lotacao = Column(String(200))               # TODO: tamanho necessário para o campo
    unidadeDeTrabalho = Column(String(200))     # TODO: tamanho necessário para o campo
    numeroCTPS = Column(String(10))             # TODO: tamanho necessário para o campo
    serieCTPS = Column(String(10))
    ufCTPS = Column(String(2))
    dataEmissaoCTPS = Column(Date)
    nomeUsuario = Column(String(200))           # TODO: tamanho necessário para o campo
    senha = Column(String(100))                 # TODO: tamanho necessário para o campo

    status_id = Column(Integer, ForeignKey('tb_status_funcionario.id'))
    tipo_vinculo_id = Column(Integer, ForeignKey('tb_tipo_vinculo.id'))
    cargo_id = Column(Integer, ForeignKey('tb_cargo.id'))

    _enderecos = relationship('Endereco', backref='_morador', lazy='dynamic', cascade="all, delete-orphan")
    pontos = relationship('Ponto', back_populates='funcionario')
    cargo = relationship('Cargo', back_populates='funcionarios')
    espelhos_mensais = relationship('EspelhoMensal', back_populates='funcionario')
    espelhos_diarios = relationship('EspelhoDiario', back_populates='funcionario')
    atribuicao_escala = relationship('AtribuicaoEscala', back_populates='funcionario', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<matricula={self.matricula}, nome={self.nome}, cargo={self.cargo} >'

    
class StatusFuncionario(db.Model):

    __tablename__ = 'tb_status_funcionario'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(50))
    descricao = Column(Text)
    _funcionarios = relationship('Funcionario', backref='_status', lazy='dynamic')

    def __repr__(self):
        return f'<codigo={self.codigo}, nome={self.nome}>'


class TipoVinculo(db.Model):

    __tablename__ = 'tb_tipo_vinculo'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(50))
    descricao = Column(Text)
    _funcionarios = relationship('Funcionario', backref='_tipo_vinculo', lazy='dynamic')

    def __repr__(self):
        return f'<codigo={self.codigo}, nome={self.nome}>'


class Cargo(db.Model):

    __tablename__ = 'tb_cargo'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(200))
    descricao = Column(Text)
    atribuicoes = Column(Text)
    
    padrao_salario_id = Column(Integer, ForeignKey('tb_padrao_salario.id'))
    jornada_id = Column(Integer, ForeignKey('tb_jornada.id'))
    
    padrao_salario = relationship('PadraoSalario', back_populates='cargos')
    jornada = relationship('Jornada', back_populates='cargos')
    funcionarios = relationship('Funcionario', back_populates='cargo')

    def __repr__(self):
        return f'<id={self.id}, nome={self.nome}, codigo={self.codigo}>'


class PadraoSalario(db.Model):
    
    __tablename__ = 'tb_padrao_salario'

    id = Column(Integer, primary_key=True)
    codigo = Column(String(20), index=True, unique=True)
    valor = Column(Float)
    descricao = Column(Text)

    cargos = relationship('Cargo', back_populates='padrao_salario')

    def __repr__(self):
        return f'<id={self.id}, codigo={self.codigo}, valor={self.valor}>'
