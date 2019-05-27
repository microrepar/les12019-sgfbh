"""Módulo com os modelos - classe de domínio
"""
from app import db
from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, Date, DateTime, Text, Boolean, Float, Time
from sqlalchemy.orm import relationship
from datetime import datetime
from les12019_core.aplicacao import ConverteData

_dias_semana = dict([(None, 0), ('Segunda', 1), ('Terça', 2), ('Quarta', 3),
                     ('Quinta', 4), ('Sexta', 5), ('Sábado', 6), ('Domingo', 7)])


class Jornada(db.Model):
    
    __tablename__ = 'tb_jornada'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(200))
    carga_horaria = Column(Float)
    quantidade_minima_mpto = Column(Integer)
    quantidade_maxima_dias = Column(Integer)
    intervalo_minimo = Column(Float)
    limite_max_horas_periodo = Column(Float)
    descricao = Column(Text)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    responsavel_cadastro = Column(String(50))

    status_id = Column(Integer, ForeignKey('tb_status_jornada.id'))

    status = db.relationship('StatusJornada', back_populates='jornadas')
    cargos = db.relationship('Cargo', back_populates='jornada')
    escalas = db.relationship('Escala', back_populates='jornada')

    @property
    def data_cadastro_formatada(self):
        return ConverteData.dateString(self.data_cadastro)

    def __repr__(self):
        return f'<id={self.id}, nome={self.nome}, carga_horaria={self.carga_horaria}>'


class Escala(db.Model):

    __tablename__ = 'tb_escala'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(200))
    descricao = Column(Text)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    responsavel_cadastro = Column(String(100))


    status_id = Column(Integer, ForeignKey('tb_status_escala.id'))
    turno_id = Column(Integer, ForeignKey('tb_turno.id'))
    jornada_id = Column(Integer, ForeignKey('tb_jornada.id'))

    status = db.relationship('StatusEscala', back_populates='escalas')
    jornada = db.relationship('Jornada', back_populates='escalas')
    turno = db.relationship('Turno', back_populates='escalas')

    horarios_dia = db.relationship('HorarioDia', back_populates='escala', cascade="all, delete-orphan")
    atribuicao_escala = db.relationship('AtribuicaoEscala', back_populates='escala')

    @property
    def horarios_ordenados(self):
        return sorted(self.horarios_dia, key=lambda x: x.ordem_semana)
    
    @property
    def data_cadastro_formatada(self):
        return ConverteData.dateString(self.data_cadastro)

    @property
    def qtde_horario_dia_ativo(self):
        return len([h for h in self.horarios_dia if h.status.nome == 'ATIVO'])

    def __repr__(self):
        return f'<id={self.id}, nome={self.nome}, turno={self.turno}, jornada={self.jornada}>'


class Turno(db.Model):

    __tablename__ = 'tb_turno'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(100))
    limite_hora_entrada = Column(String(5))
    limite_hora_saida = Column(String(5))
    descricao = Column(Text)

    escalas = db.relationship('Escala', back_populates='turno')

    def __repr__(self):
        return f'<id={self.id}, nome={self.nome}>'


class HorarioDia(db.Model):

    __tablename__ = 'tb_horario_diario'

    id = Column(Integer, primary_key=True)    
    dia_semana = Column(String(50))
    hora_ponto1 = Column(String(5))
    hora_ponto2 = Column(String(5))
    hora_ponto3 = Column(String(5))
    hora_ponto4 = Column(String(5))
    descricao = Column(Text)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    responsavel_cadastro = Column(String(100))

    escala_id = Column(Integer, ForeignKey('tb_escala.id'))
    status_id = Column(Integer, ForeignKey('tb_status_horario_diario.id'))

    status = db.relationship('StatusHorarioDiario', back_populates='horarios_dia')
    escala = db.relationship('Escala', back_populates='horarios_dia')

    @property
    def data_cadastro_formatada(self):
        return ConverteData.dateString(self.data_cadastro) 

    @property
    def ordem_semana(self):
        return _dias_semana.get(self.dia_semana, 0)

    def __repr__(self):
        return f'<id={self.id}, dia_semana={self.dia_semana}>'


class AtribuicaoEscala(db.Model):
    
    __tablename__ = 'tb_atribuicao_escala'

    id = Column(Integer, primary_key=True)
    data_inicio = Column(DateTime)
    data_fim = Column(DateTime)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    responsavel_cadastro = Column(String(100))
    observacao = Column(Text)

    escala_id = Column(Integer, ForeignKey('tb_escala.id'), nullable=False)
    funcionario_id = Column(Integer, ForeignKey('tb_funcionario.id'))
    status_id = Column(Integer, ForeignKey('tb_status_atribuicao.id'))

    funcionario = db.relationship('Funcionario', back_populates='atribuicao_escala')
    escala = db.relationship('Escala', back_populates='atribuicao_escala')
    status = db.relationship('StatusAtribuicao', back_populates='atribuicoes_escalas')

    @property
    def data_cadastro_formatada(self):        
        if self.data_cadastro is None or self.data_cadastro == '':
            return 'indefinida'
        return ConverteData.dateString(self.data_cadastro)

    @property
    def data_inicio_formatada(self):
        if self.data_inicio is None or self.data_inicio == '':
            return 'indefinida'
        return ConverteData.dateString(self.data_inicio)

    @property
    def data_fim_formatada(self):
        if self.data_fim is None or self.data_fim == '':
            return 'indefinida'
        return ConverteData.dateString(self.data_fim)

    def __repr__(self):
        return f'<id={self.id}, inicio={self.data_inicio}, fim={self.data_fim}, escala={self.escala}, funcionario={self.funcionario}>'


class StatusJornada(db.Model):
    
    __tablename__ = 'tb_status_jornada'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(50))
    descricao = Column(Text)

    jornadas = db.relationship('Jornada', back_populates='status')

    def __repr__(self):
        return f'<codigo={self.codigo}, nome={self.nome}>'


class StatusEscala(db.Model):

    __tablename__ = 'tb_status_escala'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(50))
    descricao = Column(Text)

    escalas = db.relationship('Escala', back_populates='status')

    def __repr__(self):
        return f'<codigo={self.codigo}, nome={self.nome}>'


class StatusHorarioDiario(db.Model):

    __tablename__ = 'tb_status_horario_diario'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(50))
    descricao = Column(Text)

    horarios_dia = db.relationship('HorarioDia', back_populates='status')

    def __repr__(self):
        return f'<codigo={self.codigo}, nome={self.nome}>'


class StatusAtribuicao(db.Model):

    __tablename__ = 'tb_status_atribuicao'

    id = Column(Integer, primary_key=True)
    codigo = Column(Integer, index=True, unique=True)
    nome = Column(String(50))
    descricao = Column(Text)

    atribuicoes_escalas = db.relationship('AtribuicaoEscala', back_populates='status')

    def __repr__(self):
        return f'<codigo={self.codigo}, nome={self.nome}>'
