"""Módulo com os modelos - classe de domínio
"""
from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, SmallInteger
from sqlalchemy.orm import relationship
from les12019_core.aplicacao import ConverteData, ConverteHora
from datetime import datetime


class Ponto(db.Model):

    __tablename__ = 'tb_ponto'

    id = Column(Integer, primary_key=True)
    numero_seq_ponto = Column(Integer)
    ordem = Column(SmallInteger)                                 # incluir na entidade na proxima atualiza
    tipo_ponto = Column(SmallInteger)
    data_hora = Column(DateTime)                                 # horário da marcação de ponto
    relogio = Column(String(100))                                # deverár ser retirado, quando for implementado a classe RelogioPonto
    incluir = Column(Boolean, default=False)
    matricula = Column(Integer)
    pispasep = Column(String(11))
    digito_pispasep = Column(Integer)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    responsavel_cadastro = Column(String(100))
    observacao = Column(Text)
   

    tipo_id = Column(Integer, ForeignKey('tb_tipo_ponto.id'))
    status_id = Column(Integer, ForeignKey('tb_status_ponto.id'))
    espelho_diario_id = Column(Integer, ForeignKey('tb_espelho_diario.id'))
    funcionario_id = Column(Integer, ForeignKey('tb_funcionario.id'))    
    # relogio_id = Column(Integer, ForeignKey('precisa ser definido a classe Relogio'))     # incluir após implementação de bp_relogioponto

    status = relationship('StatusPonto', back_populates='pontos')
    tipo = relationship('TipoPonto', back_populates='pontos')
    espelho_diario = relationship('EspelhoDiario', back_populates='pontos')
    funcionario = relationship('Funcionario', back_populates='pontos')

    def carregar_dados_funcionario(self):
        if self.funcionario is not None:
            self.matricula = self.funcionario.matricula
            self.pispasep = self.funcionario.pisPasep
            return True
        else:
            return False

    @property
    def hora_formatada(self):
        return ConverteHora.datetimeStringHora(self.data_hora)
    
    @property
    def data_formatada(self):
        return ConverteData.dateString(self.data_hora)

    @property
    def data_cadastro_formatada(self):
        return ConverteData.dateString(self.data_cadastro)

    

    def __repr__(self):
        return f'<matricula={self.matricula}, data={self.data_hora}, incluir={self.incluir}>'



class StatusPonto(db.Model):

    __tablename__ = 'tb_status_ponto'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(100))
    descricao = Column(Text)
    pontos = relationship('Ponto', back_populates='status')

    def __repr__(self):
        return f'<id={self.id}, nome={self.nome}, codigo={self.codigo}>'



class TipoPonto(db.Model):

    __tablename__ = 'tb_tipo_ponto'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(100))
    descricao = Column(Text)
    pontos = relationship('Ponto', back_populates='tipo')

    def __repr__(self):
        return f'<id={self.id}, nome={self.nome}, codigo={self.codigo}>'
