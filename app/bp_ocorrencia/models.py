"""Módulo com os modelos - classe de domínio
"""
from app import db
from les12019_core.aplicacao import ConverteData
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime



class Ocorrencia(db.Model):
    
    __tablename__ = 'tb_ocorrencia'

    id = Column(Integer, primary_key=True)
    data_inicio = Column(DateTime)
    data_fim = Column(DateTime)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    responsavel_cadastro = Column(String(200))
    cobranca = Column(Boolean)
    quantidade_horas = Column(Float)
    observacao = Column(Text)

    status_id = Column('StatusOcorrencia', ForeignKey('tb_status_ocorrencia.id'))
    espelho_diario_id = Column('EspelhoDiario', ForeignKey('tb_espelho_diario.id'))
    pendencia_id = Column('Pendencia', ForeignKey('tb_pendencia.id'))
    periodo_id = Column('PeriodoOcorrencia', ForeignKey('tb_periodo_ocorrencia.id'))

    status = relationship('StatusOcorrencia', back_populates='ocorrencias')
    pendencia = relationship('Pendencia', back_populates='ocorrencias')
    periodo = relationship('PeriodoOcorrencia', back_populates='ocorrencias')
    espelho_diario = relationship('EspelhoDiario', back_populates='ocorrencias')
    solicitacoes = relationship('Solicitacao', back_populates='ocorrencia')

    @property
    def data_inicio_formatada(self):
        return ConverteData.dateString(self.data_inicio)
    
    @property
    def data_fim_formatada(self):
        return ConverteData.dateString(self.data_fim)
    
    @property
    def data_cadastro_formatada(self):
        return ConverteData.dateString(self.data_cadastro)

    @property
    def funcionario(self):
        return self.espelho_diario.funcionario
    
    def funcionario_matricula(self):
        return self.espelho_diario.funcionario_matricula()

    def funcionario_nome(self):
        return self.espelho_diario.funcionario_nome()

    def funcionario_lotacao(self):
        return self.espelho_diario.funcionario_lotacao()

    def funcionario_unidade_trabalho(self):
        return self.espelho_diario.funcionario_unidade_trabalho()

    def funcionario_cargo(self):
        return self.espelho_diario.funcionario_cargo()
    
    

    @property
    def escala(self):
        for atribuicao in self.espelho_diario.funcionario.atribuicao_escala:
            if atribuicao.status_id == 1:
                return atribuicao.escala
        return None

    

    def __repr__(self):
        return f'<id={self.id}, data_cadastro={self.data_cadastro}, pendencia={self.pendencia}>'


class Pendencia(db.Model):
    
    __tablename__ = 'tb_pendencia'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    sigla = Column(String(50), unique=True)
    nome = Column(String(200))
    descricao = Column(Text)
    limite_maximo_horas = Column(Float, default=0.0)
    prazo_pagamento_dias = Column(Integer, default=0)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    responsavel_cadastro = Column(String(200))

    status_id = Column(Integer, ForeignKey('tb_status_pendencia.id'))
    tipo_id = Column(Integer, ForeignKey('tb_tipo_pendencia.id'))

    status = relationship('StatusPendencia', back_populates='pendencias')
    tipo = relationship('TipoPendencia', back_populates='pendencias')
    ocorrencias = relationship('Ocorrencia', back_populates='pendencia')
    
    @property
    def data_cadastro_formatada(self):
        return ConverteData.dateString(self.data_cadastro)

    def __repr__(self):
        return f'<id={self.id}, sigla={self.sigla}, nome={self.nome}>'


class PeriodoOcorrencia(db.Model):

    __tablename__ = 'tb_periodo_ocorrencia'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(100))
    momento = Column(String(100))
    descricao = Column(Text)

    ocorrencias = relationship('Ocorrencia', back_populates='periodo')

    def __repr__(self):
        return f'<id={self.id}, nome={self.nome}, momento={self.momento}>'


class StatusOcorrencia(db.Model):
    
    __tablename__ = 'tb_status_ocorrencia'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(100))
    descricao = Column(Text)

    ocorrencias = relationship('Ocorrencia', back_populates='status')

    def __repr__(self):
        return f'<id={self.id}, nome={self.nome}, codigo={self.codigo}>'



class StatusPendencia(db.Model):

    __tablename__ = 'tb_status_pendencia'
    
    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(100))
    descricao = Column(Text)

    pendencias = relationship('Pendencia', back_populates='status')

    def __repr__(self):
        return f'<id={self.id}, nome={self.nome}, codigo={self.codigo}>'



class TipoPendencia(db.Model):

    __tablename__ = 'tb_tipo_pendencia'
    
    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(100))
    descricao = Column(Text)

    pendencias = relationship('Pendencia', back_populates='tipo')

    def __repr__(self):
        return f'<id={self.id}, nome={self.nome}, codigo={self.codigo}>'


