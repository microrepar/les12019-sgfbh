"""Módulo com os modelos - classe de domínio
"""

from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime


class Endereco(db.Model):

    __tablename__ = 'tb_endereco'

    id = Column(Integer, primary_key=True)
    cep = Column(String(8))    
    numero = Column(Integer)
    complemento_endereco = Column(String(200))
    responsavel_cadastro = Column(String(200))
    dataCadastro = Column(DateTime(), default=datetime.utcnow)
    observacoes = Column(Text())
    funcionario_id = Column(Integer, ForeignKey('tb_funcionario.id'))
    tipo_endereco_id = Column(Integer, ForeignKey('tb_tipo_endereco.id'))
    status_id = Column(Integer, ForeignKey('tb_status_endereco.id'))
    logradouro_id = Column(Integer, ForeignKey('tb_logradouro.id'))

    def __repr__(self):
        return f'<Endereco={self._logradouro}, Nº={self.numero}>'


class TipoEndereco(db.Model):
    
    __tablename__ = 'tb_tipo_endereco'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    descricao = Column(Text)
    _enderecos_moradores = db.relationship('Endereco', backref='_tipo_endereco', lazy='dynamic')

    def __repr__(self):
        return f'<tipo={self.nome}, id={self.id}>'


class StatusEndereco(db.Model):

    __tablename__ = 'tb_status_endereco'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    descricao = Column(Text)
    _enderecos_moradores = db.relationship('Endereco', backref='_status', lazy='dynamic')

    def __repr__(self):
        return f'<tipo={self.nome}, id={self.id}>'

        
class Logradouro(db.Model):

    __tablename__ = 'tb_logradouro'

    id = Column(Integer, primary_key=True)
    cep = Column(String(8), index=True, unique=True)
    uf = Column(String(2))
    cidade = Column(String(150))
    bairro = Column(String(250))
    tipo_logradouro = Column(String(100))
    logradouro = Column(String(250))        # TODO: verificar se precisa ser unique, com ou sem formatação
    data_cadastro = Column(DateTime(), default=datetime.utcnow)
    responsavel_cadastro = Column(String(200))
    _enderecos_moradores = db.relationship('Endereco', backref='_logradouro', lazy='dynamic')

    def __repr__(self):
        return f'<Logradouro={self.tipo_logradouro} {self.logradouro}, cep={self.cep}, cidade={self.cidade}, uf={self.uf}>'


