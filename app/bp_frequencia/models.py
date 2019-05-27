"""Módulo com os modelos - classe de domínio
"""
from app import db
from les12019_core.aplicacao import ConverteData
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Text, SmallInteger
from sqlalchemy.orm import relationship
import datetime


_dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']

class EspelhoMensal(db.Model):

    __tablename__ = 'tb_espelho_mensal'

    id = Column(Integer, primary_key=True)
    data_fechamento = Column(DateTime)
    mes_referencia = Column(SmallInteger)
    ano_referencia = Column(Integer)
    data_inicio = Column(DateTime)
    data_fim = Column(DateTime)
    data_cadastro = Column(DateTime)
    responsavel_cadastro = Column(String(200))
    observacao = Column(Text)
    
    funcionario_id = Column(Integer, ForeignKey('tb_funcionario.id'))
    status_id = Column(Integer, ForeignKey('tb_status_espelho.id'))
    # periodo_id = Column(Integer, ForeignKey('tb_periodo_espelho_mensal.id'))

    funcionario = relationship('Funcionario', back_populates='espelhos_mensais')
    espelhos_diarios = relationship('EspelhoDiario', back_populates='espelho_mensal')
    status = relationship('StatusEspelho', back_populates='espelhos_mensais')
    # periodo = relationship('PeriodoEspelhoMensal', back_populates='espelhos_mensais')

    @property
    def periodo_inicio_formatado(self):
        return ConverteData.dateString(self.data_inicio)
    
    @property
    def periodo_fim_formatado(self):
        return ConverteData.dateString(self.data_fim)

    @property
    def qtde_total_ocorrencias(self):
        return sum([len(dia.ocorrencias) for dia in self.espelhos_diarios], 0)

    def maior_numero_pontos(self):
        lista_num_marcacoes = [len(dia.pontos) for dia in self.espelhos_diarios]
        return max(lista_num_marcacoes)

    def __repr__(self):
        return f'<id={self.id}, mês={self.mes_referencia}, ano={self.ano_referencia}, funcionario={self.funcionario}>'
    

class EspelhoDiario(db.Model):

    __tablename__ = 'tb_espelho_diario' 

    id = Column(Integer, primary_key=True)
    data = Column(DateTime)                                                            
    dia_semana = Column(String(50))                                                            
    data_fechamento = Column(DateTime)
    dia_fechamento = Column(Integer)                                                
    dia_referencia = Column(SmallInteger)    
    mes_referencia = Column(SmallInteger)
    ano_referencia = Column(Integer)
    data_cadastro = Column(DateTime, default=datetime.datetime.utcnow)
    responsavel_cadastro = Column(String(200))
    observacao = Column(Text)

    status_id = Column(Integer, ForeignKey('tb_status_espelho.id'))
    tipo_id = Column(Integer, ForeignKey('tb_tipo_espelhodia.id'))                      # verificar a real necessidade deste campo - dia util/feriado/pontofacultativo
    espelho_mensal_id = Column(Integer, ForeignKey('tb_espelho_mensal.id'))
    funcionario_id = Column(Integer, ForeignKey('tb_funcionario.id'))

    tipo = relationship('TipoEspelhoDia', back_populates='espelhos_diarios')            # verificar a real necessidade deste campo - dia util/feriado/pontofacultativo
    espelho_mensal = relationship('EspelhoMensal', back_populates='espelhos_diarios')
    funcionario = relationship('Funcionario', back_populates='espelhos_diarios')
    status = relationship('StatusEspelho', back_populates='espelhos_diarios')
    pontos = relationship('Ponto', back_populates='espelho_diario')
    ocorrencias = relationship('Ocorrencia', back_populates='espelho_diario')

    @property
    def data_formatada(self):
        return ConverteData.dateString(self.data)
    
    @property
    def data_cadastro_formatada(self):
        return ConverteData.dateString(self.data_cadastro)

    @property
    def qtde_pontos_incluidos(self):
        return len([ponto for ponto in self.pontos if ponto.incluir])

    def funcionario_matricula(self):
        return self.funcionario.matricula

    def funcionario_nome(self):
        return self.funcionario.nome
    
    def funcionario_lotacao(self):
        return self.funcionario.lotacao

    def funcionario_unidade_trabalho(self):
        return self.funcionario.unidadeDeTrabalho
    
    def funcionario_cargo(self):
        return self.funcionario.cargo.nome
    
    def autopreencher_dados_data(self):
        if self.data is not None:
            data: datetime.datetime = self.data
            self.dia_semana = _dias_semana[data.weekday()]
            self.data_fechamento = data + datetime.timedelta(days=1)
            self.dia_fechamento = self.data_fechamento.day
            self.dia_referencia = data.day
            self.mes_referencia = data.month
            self.ano_referencia = data.year
            return True
        return False

    def __repr__(self):
        return f'<mes={self.mes_referencia}, ano={self.ano_referencia}, cadastro={self.data_cadastro}, espelho_mensal={self.espelho_mensal}>'


class StatusEspelho(db.Model):

    __tablename__ = 'tb_status_espelho'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(100))
    descricao = Column(Text)
    espelhos_diarios = relationship('EspelhoDiario', back_populates='status')
    espelhos_mensais = relationship('EspelhoMensal', back_populates='status')

    def __repr__(self):
        return f'<id={self.id}, nome={self.nome}, codigo={self.codigo}>'


class TipoEspelhoDia(db.Model):

    __tablename__ = 'tb_tipo_espelhodia'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(100))
    descricao = Column(Text)
    espelhos_diarios = relationship('EspelhoDiario', back_populates='tipo')

    def __repr__(self):
        return f'<id={self.id}, nome={self.nome}, codigo={self.codigo}>'


# class PeriodoEspelhoMensal(db.Model):

#     __tablename__ = 'tb_periodo_espelho_mensal'

#     id = Column(Integer, primary_key=True)
#     codigo = Column(Integer, index=True, unique=True)
#     mes = Column(SmallInteger)
#     data_inicio = Column(DateTime)
#     data_fim = Column(DateTime)
#     descricao = Column(Text)

#     espelhos_mensais = relationship('EspelhoMensal', back_populates='periodo')

#     def __repr__(self):
#         return f'<id={self.id}, mes={self.mes}, inicio={self.data_inicio}, fim={self.data_fim}>'
