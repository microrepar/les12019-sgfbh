"""Módulo com os modelos - classe de domínio
"""
from app import db
from les12019_core.aplicacao import ConverteData
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, BigInteger, Sequence
from sqlalchemy.orm import relationship
from datetime import datetime


class Solicitacao(db.Model):

    __tablename__ = 'tb_solicitacao'

    id = Column(Integer, primary_key=True)
    numero = Column(BigInteger) 
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    responsavel_cadastro = Column(String(100))
    email = Column(String(200))
    descricao = Column(Text)

    tipo_id = Column('TipoSolicitacao', ForeignKey('tb_tipo_solicitacao.id'))
    status_id = Column('StatusSolicitacao', ForeignKey('tb_status_solicitacao.id'))
    despacho_id = Column('Despacho', ForeignKey('tb_despacho.id'))
    ocorrencia_id = Column('Ocorrencia', ForeignKey('tb_ocorrencia.id'))

    status = db.relationship('StatusSolicitacao', back_populates='solicitacoes')
    tipo = db.relationship('TipoSolicitacao', back_populates='solicitacoes')
    despacho = db.relationship('Despacho', back_populates='solicitacao')
    ocorrencia = db.relationship('Ocorrencia', back_populates='solicitacoes')

    @property
    def data_cadastro_formatada(self):
        return ConverteData.dateString(self.data_cadastro)
    
    @property
    def espelho_diario(self):
        return self.ocorrencia.espelho_diario

    @property
    def funcionario(self):
        return self.ocorrencia.funcionario

    def funcionario_matricula(self):
        return self.ocorrencia.funcionario_matricula()

    def funcionario_nome(self):
        return self.ocorrencia.funcionario_nome()
    
    def funcionario_lotacao(self):
        return self.ocorrencia.funcionario_lotacao()

    def funcionario_unidade_trabalho(self):
        return self.ocorrencia.funcionario_unidade_trabalho()
    
    def funcionario_cargo(self):
        return self.ocorrencia.funcionario_cargo()
    
    def __repr__(self):
        return f'<id={self.id}, data={self.data_cadastro}, ocorrencia={self.ocorrencia}>'

    def concluir(self, decisao):
        if decisao != 'DEVOLVER':
            self.ocorrencia.status_id = 2
        else:
            self.ocorrencia.status_id = 3

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return str(e)
        else:
            return None


class Despacho(db.Model):
    
    __tablename__ = 'tb_despacho'
    
    id = Column(Integer, primary_key=True)
    data_cadastro = Column(DateTime)
    responsavel_cadastro = Column(String(100))
    descricao = Column(Text)

    decisao_id = Column(Integer, ForeignKey('tb_decisao.id'))

    solicitacao = db.relationship('Solicitacao', uselist=False, back_populates='despacho')
    decisao = db.relationship('Decisao', back_populates='despachos')

    def __repr__(self):
        return f'<id={self.id}, data={self.data_cadastro}, decisão={self.decisao}>'
    
    @property
    def data_cadastro_formatada(self):
        return ConverteData.dateString(self.data_cadastro)

    def concluir(self):
        if self.decisao.nome != 'DEVOLVER':
            self.solicitacao.status_id = 2
        else:
            self.solicitacao.status_id = 3
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return str(e)
        else:
            return self.solicitacao.concluir(self.decisao.nome)
            
    


class Decisao(db.Model):
    
    __tablename__ = 'tb_decisao'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(100))
    descricao = Column(Text)

    despachos = db.relationship('Despacho', back_populates='decisao')    

    def __repr__(self):
        return f'<id={self.id}, nome={self.nome}, codigo={self.codigo}>'


class StatusSolicitacao(db.Model):

    __tablename__ = 'tb_status_solicitacao'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(50))
    descricao = Column(Text)

    solicitacoes = db.relationship('Solicitacao', back_populates='status')

    def __repr__(self):
        return f'<id={self.id}, status={self.nome}>'


class TipoSolicitacao(db.Model):

    __tablename__ = 'tb_tipo_solicitacao'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(50))
    descricao = Column(Text)

    solicitacoes = db.relationship('Solicitacao', back_populates='tipo')

    def __repr__(self):
        return f'<id={self.id}, status={self.nome}>'


class StatusDespacho(db.Model):

    __tablename__ = 'tb_status_depachos'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(50))
    descricao = Column(Text)

    def __repr__(self):
        return f'<id={self.id}, status={self.nome}>'
