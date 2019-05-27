from les12019_core.abstract_dao import AbstractDAO
from app.bp_escala.models import (
    Escala, StatusEscala, StatusJornada, Jornada, HorarioDia, AtribuicaoEscala, Turno, StatusHorarioDiario, StatusAtribuicao)
from les12019_core.aplicacao import ConverteData
from les12019_core import utils
from app import db
from flask import flash


########################### Classe Concreta - EscalaDAO ##################################
class EscalaDAO(AbstractDAO):

    def salvar(self, entidade: Escala):
        
        cont_msg = 0

        with db.session.no_autoflush:
            status: StatusEscala = StatusEscala.query.filter(StatusEscala.nome == entidade.status.nome).first()
            jornada: Jornada = Jornada.query.filter(Jornada.nome == entidade.jornada.nome).first()
            turno: Turno = Turno.query.filter(Turno.nome == entidade.turno.nome).first()

            if status is None:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('"Status"'))
                cont_msg += 1
            if jornada is None:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('"jornada"'))
                cont_msg += 1
            if turno is None:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('"turno"'))
                cont_msg += 1

            if cont_msg != 0:
                return 'Selecione os itens com *.' 

            escala = Escala()

            escala.codigo = entidade.codigo
            escala.nome = entidade.nome
            escala.responsavel_cadastro = entidade.responsavel_cadastro
            escala.descricao = entidade.descricao

            escala.jornada = jornada
            escala.status = status
            escala.turno = turno

        try:
            db.session.add(escala)
            db.session.commit()
            flash(utils.SUCESSO_SALVAR_ENTIDADE_BD.format(f'Escala {escala.nome}'))
            flash('Atenção! Agora cadastre os dias da semana e os horários para esta escala')
            return escala
        except:
            db.session.rollback()
            return utils.ERRO_SALVAR_ENTIDADE_BD.format('Escala!')



    def listar(self, entidade: Escala):
        return super().listar(entidade)

    def alterar(self, entidade: Escala):
        cont_msg = 0    

        escala: Escala = super().consultarPorId(entidade)

        if escala is None:
            return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format(f'Escala {entidade.nome}')

        escala.codigo = entidade.codigo
        escala.nome = entidade.nome            
        escala.descricao = entidade.descricao

        if escala.turno_id != entidade.turno_id:
            turno: Turno = Turno.query.filter(Turno.id == entidade.turno_id).first()
            if turno is not None:
                escala.turno = turno
            else:
                flash('Atenção! O turno deve ser selecionado.')
                cont_msg += 1

        if escala.jornada_id != entidade.jornada_id:
            jornada: Jornada = Jornada.query.filter(Jornada.id == entidade.jornada_id).first()
            if jornada is not None:
                escala.jornada = jornada
            else:
                flash('Atenção! A jornada deve ser selecionada.')
                cont_msg += 1

        if escala.status_id != entidade.status_id:
            status: StatusEscala = StatusEscala.query.filter(StatusEscala.id == entidade.status_id).first()
            if status is not None:
                escala.status = status
            else:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('"Status"'))
                cont_msg += 1

        if cont_msg != 0:
                return 'Selecione os itens com *.'

        try:
            db.session.commit()
            flash(utils.SUCESSO_ATUALIZAR_ENTIDADE_BD.format(f'Escala {escala.nome}'))
            return escala
        except:
            db.session.rollback()           
            return utils.ERRO_ATUALIZAR_ENTIDADE_BD.format(f'Escala {escala.nome}')


    def consultarPorId(self, entidade: Escala):
        escala: Escala = super().consultarPorId(entidade)
        return escala

    def consultarPorParametro(self, entidade: Escala):
        pass

    def consultar(self, entidade: Escala):
        escalas = Escala.query.filter(Escala.status_id != '3').all()
        return escalas        

    def excluir(self, entidade: Escala):
        escala: Escala = super().consultarPorId(entidade)       

        if escala is not None:
            nome_escala = escala.nome
            foi_excluido = super().excluir(escala)
            if foi_excluido:
                flash(utils.SUCESSO_EXCLUIR_ENTIDADE.format(f'Escala {nome_escala}'))
                return foi_excluido
            else:
                flash(utils.ERRO_EXCLUIR_ENTIDADE.format(f'Escala {nome_escala}'))
                return foi_excluido
        else:
            return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format(f'Escala {nome_escala}')



########################### Classe Concreta - StatusEscalaDAO ##################################
class StatusEscalaDAO(AbstractDAO):

    def salvar(self, entidade: StatusEscala):
        pass

    def listar(self, entidade: StatusEscala):
        status_escala = super().listar(entidade)
        return status_escala

    def alterar(self, entidade: StatusEscala):
        pass

    def consultarPorId(self, entidade: StatusEscala):
        pass

    def consultarPorParametro(self, entidade: StatusEscala):
        pass

    def consultar(self, entidade: StatusEscala):
        pass

    def excluir(self, entidade: StatusEscala):
        pass


########################### Classe Concreta - DAO de Jornada ##################################
class JornadaDAO(AbstractDAO):

    def salvar(self, entidade: Jornada):
        
        jornada: Jornada = entidade

        status: StatusJornada = super().consultarPorId(entidade.status)

        if status is not None:
            del jornada.status
            jornada.status = status
        else:
            return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Status de jornada')

        try:
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return utils.ERRO_SALVAR_ENTIDADE_BD.format('Jornada')
        else:
            flash(utils.SUCESSO_SALVAR_ENTIDADE_BD.format(f'Jornada {jornada.nome}'))
            return jornada
        


    def listar(self, entidade: Jornada):
        jornadas = super().listar(entidade)
        return jornadas

    def alterar(self, entidade: Jornada):
        
        mensagens = []

        jornada: Jornada = Jornada.query.filter_by(id=entidade.id).first()

        if jornada.status.id != int(entidade.status.id):
            status = super().consultarPorId(entidade.status)
            if status is not None:
                jornada.status = status
            else:
                return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Status de jornada')

            
        jornada.codigo = entidade.codigo
        jornada.nome = entidade.nome
        jornada.carga_horaria = entidade.carga_horaria
        jornada.quantidade_minima_mpto = entidade.quantidade_minima_mpto
        jornada.quantidade_maxima_dias = entidade.quantidade_maxima_dias
        jornada.intervalo_minimo = entidade.intervalo_minimo
        jornada.limite_max_horas_periodo = entidade.limite_max_horas_periodo
        jornada.descricao = entidade.descricao


        try:
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return utils.ERRO_SALVAR_ENTIDADE_BD.format('Jornada')
        else:
            flash(utils.SUCESSO_ATUALIZAR_ENTIDADE_BD.format(f'jornada {jornada.nome}'))
            return jornada

        
        

    def consultarPorId(self, entidade: Jornada):
        jornada = super().consultarPorId(entidade)
        return jornada

    def consultarPorParametro(self, entidade: Jornada):
        pass

    def consultar(self, entidade: Jornada):
        jornadas = Jornada.query.filter(Jornada.status_id!=3).all()
        return jornadas

    def excluir(self, entidade: Jornada):
        
        jornada: Jornada = super().consultarPorId(entidade)

        if jornada is not None:
            foi_excluido = super().excluir(jornada)
            if foi_excluido:
                flash(utils.SUCESSO_EXCLUIR_ENTIDADE.format(f'Pendência {entidade.nome}'))
                return foi_excluido
            else:
                return utils.ERRO_EXCLUIR_ENTIDADE.format(f'Pendência {entidade.nome}')
        else:
            return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format(f'jornada de código={entidade.codigo} nome={entidade.nome}')



########################### Classe Concreta - DAO de Turno ##################################
class TurnoDAO(AbstractDAO):

    def salvar(self, entidade: Turno):
        pass

    def listar(self, entidade: Turno):
        turnos = super().listar(entidade)
        return turnos

    def alterar(self, entidade: Turno):
        pass

    def consultarPorId(self, entidade: Turno):
        pass

    def consultarPorParametro(self, entidade: Turno):
        pass

    def consultar(self, entidade: Turno):
        pass

    def excluir(self, entidade: Turno):
        pass


########################### Classe Concreta - DAO de HorarioDia ##################################
class HorarioDiaDAO(AbstractDAO):

    def salvar(self, entidade: HorarioDia):
        
        cont_msg = 0        
    
        status = super().consultarPorId(entidade.status)
        escala = super().consultarPorId(entidade.escala)

        if status is None:
            flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Status"'))
            cont_msg += 1

        if escala is None:
            flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Escala"'))
            cont_msg += 1

        if cont_msg != 0:
            return 'Verifique com atenção os erros apresentados!'

        horario_dia = HorarioDia()
        horario_dia.dia_semana = entidade.dia_semana
        horario_dia.hora_ponto1 = entidade.hora_ponto1
        horario_dia.hora_ponto2 = entidade.hora_ponto2
        horario_dia.hora_ponto3 = entidade.hora_ponto3
        horario_dia.hora_ponto4 = entidade.hora_ponto4
        horario_dia.descricao = entidade.descricao
        horario_dia.responsavel_cadastro = entidade.responsavel_cadastro
        
        horario_dia.escala = escala
        horario_dia.status = status
        
        try:
            db.session.add(horario_dia)
            db.session.commit()
            flash(utils.SUCESSO_SALVAR_ENTIDADE_BD.format(f'"Horario de trabalho diário" de {horario_dia.dia_semana} da escala {horario_dia.escala.nome}'))            
            return horario_dia.escala
        except Exception as e:
            print(str(e))
            db.session.rollback()

            return utils.ERRO_SALVAR_ENTIDADE_BD.format('"Horario de trabalho diário"')


    def listar(self, entidade: HorarioDia):
        HorariosDias = super().listar(entidade)
        return HorariosDias

    def alterar(self, entidade: HorarioDia):
        cont_msg = 0
        
        status = super().consultarPorId(entidade.status)
        escala = super().consultarPorId(entidade.escala)

        with db.session.no_autoflush:

            if status is None:
                flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Status"'))
                cont_msg += 1

            if escala is None:
                flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Escala"'))
                cont_msg += 1

            if cont_msg != 0:
                return 'Verifique com atenção os erros apresentados!'

        horario_dia: HorarioDia = super().consultarPorId(entidade)
        horario_dia.dia_semana = entidade.dia_semana
        horario_dia.hora_ponto1 = entidade.hora_ponto1
        horario_dia.hora_ponto2 = entidade.hora_ponto2
        horario_dia.hora_ponto3 = entidade.hora_ponto3
        horario_dia.hora_ponto4 = entidade.hora_ponto4
        horario_dia.descricao = entidade.descricao

        horario_dia.escala = escala
        horario_dia.status = status

        try:
            db.session.commit()
            flash(utils.SUCESSO_ATUALIZAR_ENTIDADE_BD.format(
                f'"Horario de trabalho diário" de {horario_dia.dia_semana} da escala {horario_dia.escala.nome}'))
            return horario_dia
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return utils.ERRO_SALVAR_ENTIDADE_BD.format('"Horario de trabalho diário"')

            

    def consultarPorId(self, entidade: HorarioDia):
        horario_dia = super().consultarPorId(entidade)
        return horario_dia

    def consultarPorParametro(self, entidade: HorarioDia):
        pass

    def consultar(self, entidade: HorarioDia):
        pass

    def excluir(self, entidade: HorarioDia):
        horario_dia: HorarioDia = super().consultarPorId(entidade)
        escala: Escala = super().consultarPorId(entidade.escala)

        if horario_dia is not None:
            dia_semana = horario_dia.dia_semana
            foi_excluido = super().excluir(horario_dia)
            if foi_excluido:
                flash(utils.SUCESSO_EXCLUIR_ENTIDADE.format(f'Horarios do dia da semana {dia_semana} da escala {escala.nome}'))
                return escala
            else:
                flash(utils.ERRO_EXCLUIR_ENTIDADE.format(f'Horários do dia {dia_semana}'))
                return utils.ERRO_EXCLUIR_ENTIDADE.format(f'{dia_semana} da Escala {escala.nome}')
        else:
            return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format(f'Horarios do dia da semana {dia_semana} da escala {escala.nome}')



class StatusHorarioDiarioDAO(AbstractDAO):

    def salvar(self, entidade: HorarioDia):
        pass

    def listar(self, entidade: HorarioDia):
        HorariosDias = super().listar(entidade)
        return HorariosDias

    def alterar(self, entidade: HorarioDia):
        pass

    def consultarPorId(self, entidade: HorarioDia):
        pass

    def consultarPorParametro(self, entidade: HorarioDia):
        pass

    def consultar(self, entidade: HorarioDia):
        pass

    def excluir(self, entidade: HorarioDia):
        pass


########################### Classe Concreta - AtribuicaoEscalaDAO ##################################
class AtribuicaoEscalaDAO(AbstractDAO):

    def salvar(self, entidade: AtribuicaoEscala):
        
        atribuicao_escala = AtribuicaoEscala()
        
        status = super().consultarPorId(entidade.status)
        escala = super().consultarPorId(entidade.escala)
        funcionario = super().consultarPorId(entidade.funcionario)
        
        count_msg = 0

        if all([status, escala, funcionario]):
            atribuicao_escala.funcionario = funcionario
            atribuicao_escala.escala = escala
            atribuicao_escala.status = status            
            atribuicao_escala.data_inicio = entidade.data_inicio
            atribuicao_escala.data_fim = entidade.data_fim
            atribuicao_escala.responsavel_cadastro = entidade.responsavel_cadastro
            atribuicao_escala.observacao = entidade.observacao
        else:
            if status is None:
                flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"status da atribuição"'))
                count_msg += 1
            if escala is None:
                flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format(f'escala - {entidade.escala.nome}'))
                count_msg += 1
            if funcionario is None:
                flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format(f'funcionario - {entidade.funcionario.nome}'))

        if count_msg != 0:
            return 'Os dados descritos não foram encontrados na base de dados!'

        try:
            db.session.add(atribuicao_escala)
            db.session.commit()
            flash(utils.SUCESSO_SALVAR_ENTIDADE_BD.format(f'atribuição da escala: {atribuicao_escala.escala.nome}'))
            return atribuicao_escala.funcionario
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return utils.ERRO_SALVAR_ENTIDADE_BD.format('Atribuicão de Escala')



    def listar(self, entidade: AtribuicaoEscala):
        pass

    def alterar(self, entidade: AtribuicaoEscala):
        pass

    def consultarPorId(self, entidade: AtribuicaoEscala):
        atribuicao = super().consultarPorId(entidade)
        return atribuicao

    def consultarPorParametro(self, entidade: AtribuicaoEscala):
        pass

    def consultar(self, entidade: AtribuicaoEscala):
        pass

    def excluir(self, entidade: AtribuicaoEscala):
        pass


########################### Classe Concreta - StatusAtribuicaoEscalaDAO ##################################
class StatusAtribuicaoDAO(AbstractDAO):

    def salvar(self, entidade: StatusAtribuicao):
        pass

    def listar(self, entidade: StatusAtribuicao):
        status = super().listar(entidade)
        return status

    def alterar(self, entidade: StatusAtribuicao):
        pass

    def consultarPorId(self, entidade: StatusAtribuicao):
        pass

    def consultarPorParametro(self, entidade: StatusAtribuicao):
        pass

    def consultar(self, entidade: StatusAtribuicao):
        pass

    def excluir(self, entidade: StatusAtribuicao):
        pass
