from les12019_web.abstract_viewhelper import AbstractViewHelper, _verificar_msg
from les12019_core.aplicacao import Resultado, ConverteData, ConverteHora
from les12019_core.utils import get_parameters_request
from app.bp_ponto.models import Ponto, StatusPonto
from app.bp_funcionario.models import Funcionario, Cargo
from app.bp_frequencia.models import EspelhoDiario, StatusEspelho

from flask import Request, render_template, url_for, redirect, session
import datetime


################################################# PONTO #############################################
class PontoViewHelper(AbstractViewHelper):

    def getEntidade(self, request):

        ponto = Ponto(data_cadastro='', responsavel_cadastro='', observacao='')
        ponto.funcionario = Funcionario()
        ponto.funcionario.cargo = Cargo()
        ponto.espelho_diario = EspelhoDiario()
        ponto.status = StatusPonto()

        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:

            if operacao == 'PRE-SALVAR':                
                espelho_dia_id = parameters.get('txt_espelho_diario_id', '').strip()
                funcionario_id = parameters.get('txt_funcionario_id', '').strip()
                status_id = parameters.get('txt-ponto-status_id', '').strip()

                funcionario_matricula = parameters.get('txt-funcionario-matricula', '').strip()
                funcionario_nome = parameters.get('txt-funcionario-nome', '').strip()
                funcionario_cargo_nome = parameters.get('txt-funcionario-cargo-nome', '').strip()
                espelho_diario_data = parameters.get('txt-espelho-diario-data', '').strip()
                ponto_data_cadastro = parameters.get('txt-ponto-data_cadastro', '').strip()
                ponto_responsavel_cadastro = parameters.get('txt-ponto-responsavel-cadastro', '').strip()                
                ponto_data_hora = parameters.get('txt-ponto-data_hora', '').strip()
                ponto_observacao = parameters.get('txt-horario-trabalho-descricao', '').strip()

                ponto.espelho_diario.id = espelho_dia_id
                ponto.funcionario.id = funcionario_id
                ponto.status.id = status_id

                ponto.funcionario.matricula = funcionario_matricula
                ponto.funcionario.nome = funcionario_nome
                ponto.funcionario.cargo.nome = funcionario_cargo_nome
                ponto.espelho_diario.data = ConverteData.stringDate(espelho_diario_data)
                ponto.data_cadastro = ponto_data_cadastro
                ponto.responsavel_cadastro = ponto_responsavel_cadastro
                ponto.data_hora = ConverteHora.stringDataHora(espelho_diario_data, ponto_data_hora)
                ponto.observacao = ponto_observacao
                

            elif operacao == 'SALVAR':
                espelho_dia_id = parameters.get('txt_espelho_diario_id', '').strip()
                funcionario_id = parameters.get('txt_funcionario_id', '').strip()
                status_id = parameters.get('txt-ponto-status_id', '').strip()

                funcionario_matricula = parameters.get('txt-funcionario-matricula', '').strip()
                funcionario_nome = parameters.get('txt-funcionario-nome', '').strip()
                funcionario_cargo_nome = parameters.get('txt-funcionario-cargo-nome', '').strip()
                espelho_diario_data = parameters.get('txt-espelho-diario-data', '').strip()
                ponto_data_cadastro = parameters.get('txt-ponto-data_cadastro', '').strip()
                ponto_responsavel_cadastro = parameters.get('txt-ponto-responsavel-cadastro', '').strip()                
                ponto_data_hora = parameters.get('txt-ponto-data_hora', '').strip()
                ponto_observacao = parameters.get('txt-horario-trabalho-descricao', '').strip()

                ponto.espelho_diario.id = espelho_dia_id
                ponto.funcionario.id = funcionario_id
                ponto.status.id = status_id

                ponto.funcionario.matricula = funcionario_matricula
                ponto.funcionario.nome = funcionario_nome
                ponto.funcionario.cargo.nome = funcionario_cargo_nome
                ponto.espelho_diario.data = ConverteData.stringDate(espelho_diario_data)
                ponto.data_cadastro = ponto_data_cadastro
                ponto.responsavel_cadastro = ponto_responsavel_cadastro
                ponto.data_hora = ConverteHora.stringDataHora(espelho_diario_data, ponto_data_hora)
                ponto.observacao = ponto_observacao

            elif operacao == 'PRE-ATUALIZAR':
                ponto_id = parameters.get('txt_ponto_id', '').strip()
                espelho_dia_id = parameters.get('txt_espelho_diario_id', '').strip()
                funcionario_id = parameters.get('txt_funcionario_id', '').strip()
                status_id = parameters.get('txt-ponto-status_id', '').strip()

                funcionario_matricula = parameters.get('txt-funcionario-matricula', '').strip()
                funcionario_nome = parameters.get('txt-funcionario-nome', '').strip()
                funcionario_cargo_nome = parameters.get('txt-funcionario-cargo-nome', '').strip()
                espelho_diario_data = parameters.get('txt-espelho-diario-data', '').strip()
                ponto_data_cadastro = parameters.get('txt-ponto-data_cadastro', '').strip()
                ponto_responsavel_cadastro = parameters.get('txt-ponto-responsavel-cadastro', '').strip()                
                ponto_data_hora = parameters.get('txt-ponto-data_hora', '').strip()
                ponto_observacao = parameters.get('txt-horario-trabalho-descricao', '').strip()

                ponto.id = ponto_id
                ponto.espelho_diario.id = espelho_dia_id
                ponto.funcionario.id = funcionario_id
                ponto.status.id = status_id

                ponto.funcionario.matricula = funcionario_matricula
                ponto.funcionario.nome = funcionario_nome
                ponto.funcionario.cargo.nome = funcionario_cargo_nome
                ponto.espelho_diario.data = ConverteData.stringDate(espelho_diario_data)
                ponto.data_cadastro = ponto_data_cadastro
                ponto.responsavel_cadastro = ponto_responsavel_cadastro
                ponto.data_hora = ConverteHora.stringDataHora(espelho_diario_data, ponto_data_hora)
                ponto.observacao = ponto_observacao

            elif operacao == 'ATUALIZAR':
                ponto_id = parameters.get('txt_ponto_id', '').strip()
                espelho_dia_id = parameters.get('txt_espelho_diario_id', '').strip()
                funcionario_id = parameters.get('txt_funcionario_id', '').strip()
                status_id = parameters.get('txt-ponto-status_id', '').strip()

                funcionario_matricula = parameters.get('txt-funcionario-matricula', '').strip()
                funcionario_nome = parameters.get('txt-funcionario-nome', '').strip()
                funcionario_cargo_nome = parameters.get('txt-funcionario-cargo-nome', '').strip()
                espelho_diario_data = parameters.get('txt-espelho-diario-data', '').strip()
                ponto_data_cadastro = parameters.get('txt-ponto-data_cadastro', '').strip()
                ponto_responsavel_cadastro = parameters.get('txt-ponto-responsavel-cadastro', '').strip()                
                ponto_data_hora = parameters.get('txt-ponto-data_hora', '').strip()
                ponto_observacao = parameters.get('txt-horario-trabalho-descricao', '').strip()

                ponto.id = ponto_id
                ponto.espelho_diario.id = espelho_dia_id
                ponto.funcionario.id = funcionario_id
                ponto.status.id = status_id

                ponto.funcionario.matricula = funcionario_matricula
                ponto.funcionario.nome = funcionario_nome
                ponto.funcionario.cargo.nome = funcionario_cargo_nome
                ponto.espelho_diario.data = ConverteData.stringDate(espelho_diario_data)
                ponto.data_cadastro = ponto_data_cadastro
                ponto.responsavel_cadastro = ponto_responsavel_cadastro
                ponto.data_hora = ConverteHora.stringDataHora(espelho_diario_data, ponto_data_hora)
                ponto.observacao = ponto_observacao

            if operacao == 'INCLUIR':
                ponto_id = parameters.get('txt_ponto_id', '').strip()
                espelho_dia_id = parameters.get('txt_espelho_diario_id', '').strip()
                funcionario_id = parameters.get('txt_funcionario_id', '').strip()
                status_id = parameters.get('txt-ponto-status_id', '').strip()

                funcionario_matricula = parameters.get('txt-funcionario-matricula', '').strip()
                funcionario_nome = parameters.get('txt-funcionario-nome', '').strip()
                funcionario_cargo_nome = parameters.get('txt-funcionario-cargo-nome', '').strip()
                espelho_diario_data = parameters.get('txt-espelho-diario-data', '').strip()
                ponto_data_cadastro = parameters.get('txt-ponto-data_cadastro', '').strip()
                ponto_responsavel_cadastro = parameters.get('txt-ponto-responsavel-cadastro', '').strip()                
                ponto_data_hora = parameters.get('txt-ponto-data_hora', '').strip()
                ponto_observacao = parameters.get('txt-horario-trabalho-descricao', '').strip()

                ponto.id = ponto_id
                ponto.espelho_diario.id = espelho_dia_id
                ponto.funcionario.id = funcionario_id
                ponto.status.id = status_id

                ponto.funcionario.matricula = funcionario_matricula
                ponto.funcionario.nome = funcionario_nome
                ponto.funcionario.cargo.nome = funcionario_cargo_nome
                ponto.espelho_diario.data = ConverteData.stringDate(espelho_diario_data)
                ponto.data_cadastro = ponto_data_cadastro
                ponto.responsavel_cadastro = ponto_responsavel_cadastro
                ponto.data_hora = ConverteHora.stringDataHora(espelho_diario_data, ponto_data_hora)
                ponto.observacao = ponto_observacao
            
            elif operacao == 'PRE-EXCLUIR':
                ponto_id = parameters.get('txt_ponto_id', '').strip()
                espelho_dia_id = parameters.get('txt_espelho_diario_id', '').strip()
                ponto.id = ponto_id
                ponto.espelho_diario.id = espelho_dia_id
            
            elif operacao == 'EXCLUIR':
                ponto_id = parameters.get('txt_ponto_id', '').strip()
                espelho_dia_id = parameters.get('txt_espelho_diario_id', '').strip()
                ponto.id = ponto_id
                ponto.espelho_diario.id = espelho_dia_id

        return ponto



    def setView(self, resultado, request):

        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:

            if operacao == 'PRE-SALVAR':
                if _verificar_msg(resultado):
                    return render_template('ponto/cadastrar_ponto.html', resultado=resultado)
                else:
                    return render_template('ponto/cadastrar_ponto.html', resultado=resultado)

            elif operacao == 'SALVAR':
                if _verificar_msg(resultado):
                    return render_template('ponto/cadastrar_ponto.html', resultado=resultado)
                else:
                    return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR')+'#id-titulo-pontos')

            elif operacao == 'PRE-ATUALIZAR':
                if _verificar_msg(resultado):
                    return render_template('ponto/atualizar_ponto.html', resultado=resultado)
                else:
                    return render_template('ponto/atualizar_ponto.html', resultado=resultado)

            elif operacao == 'ATUALIZAR':
                if _verificar_msg(resultado):
                    return render_template('ponto/atualizar_ponto.html', resultado=resultado)
                else:
                    return render_template('ponto/atualizar_ponto.html', resultado=resultado)

            elif operacao == 'INCLUIR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR')+'#id-titulo-pontos')
                else:
                    return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR')+'#id-titulo-pontos')
            
            elif operacao == 'PRE-EXCLUIR':
                if _verificar_msg(resultado):
                    return render_template('ponto/excluir_ponto.html', resultado=resultado)
                else:
                    return render_template('ponto/excluir_ponto.html', resultado=resultado)

            elif operacao == 'EXCLUIR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR')+'#id-titulo-pontos')
                else:
                    return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR')+'#id-titulo-pontos')
        else:
            pass
            # _verificar_msg(resultado)
            # return render_template('ponto/cadastrar_ponto.html', resultado=resultado)

        return f'OPERACAO:{operacao}, NOT IMPLEMENTED'




# modelo para implementação das viewhelpers
class _ViewHelper(AbstractViewHelper):

    def getEntidade(self, request):
        pass

    def setView(self, resultado, request):
        pass
