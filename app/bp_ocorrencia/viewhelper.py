from les12019_web.abstract_viewhelper import AbstractViewHelper, _verificar_msg
from les12019_core.aplicacao import Resultado, ConverteData, ConverteHora
from les12019_core.utils import get_parameters_request
from app.bp_ocorrencia.models import Ocorrencia, Pendencia, TipoPendencia, PeriodoOcorrencia, StatusOcorrencia, StatusPendencia
from app.bp_frequencia.models import EspelhoDiario
from app.bp_solicitacao.models import Solicitacao
from app.bp_funcionario.models import Funcionario
from flask import render_template, redirect, url_for, session, Request


class OcorrenciaViewHelper(AbstractViewHelper):

    def getEntidade(self, request):

        ocorrencia = Ocorrencia()
        ocorrencia.status = StatusOcorrencia(nome='PENDENTE')
        ocorrencia.periodo = PeriodoOcorrencia()
        ocorrencia.espelho_diario = EspelhoDiario()
        ocorrencia.pendencia = Pendencia()
        
        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            
            if operacao == 'PRE-SALVAR':

                # ocorrencia_id = parameters.get('txt_ocorrencia_id', '').strip()
                status_id = parameters.get('txt-ocorrencia-status', '').strip()
                periodo_id = parameters.get('txt-ocorrencia-periodo', '').strip()
                espelho_dia_id = parameters.get('txt_espelho_diario_id', '').strip()
                pendencia_id = parameters.get('txt-ocorrencia-pendencia', '').strip()

                ocorrencia_quantidade_horas = parameters.get('txt-ocorrencia-quantidade_horas', '').strip()
                ocorrencia_cobranca = parameters.get('txt-ocorrencia-cobranca', 0)
                ocorrencia_data_inicio = parameters.get('txt-ocorrencia-data_inicio', '').strip()
                ocorrencia_data_fim = parameters.get('txt-ocorrencia-data_fim', '').strip()
                ocorrencia_data_cadastro = parameters.get('txt-ocorrencia-data_cadastro', '').strip()
                ocorrencia_responsavel_cadastro = parameters.get('txt-ocorrencia-responsaval_cadastro', '').strip()
                ocorrencia_observacao = parameters.get('txt-ocorrencia-observacao', '').strip()

                # ocorrencia.id = ocorrencia_id
                ocorrencia.status.id = status_id
                ocorrencia.periodo.id = periodo_id
                ocorrencia.espelho_diario.id = espelho_dia_id
                ocorrencia.pendencia.id = pendencia_id

                ocorrencia.data_inicio = ConverteData.stringDate(ocorrencia_data_inicio)
                ocorrencia.data_fim = ConverteData.stringDate(ocorrencia_data_fim)
                ocorrencia.data_cadastro = ConverteData.stringDate(ocorrencia_data_cadastro)
                ocorrencia.responsavel_cadastro = ocorrencia_responsavel_cadastro
                ocorrencia.cobranca = ocorrencia_cobranca
                ocorrencia.quantidade_horas = ocorrencia_quantidade_horas
                ocorrencia.observacao = ocorrencia_observacao


            elif operacao == 'SALVAR':
                # ocorrencia_id = parameters.get('txt_ocorrencia_id', '').strip()
                status_id = parameters.get('txt-ocorrencia-status', '').strip()
                periodo_id = parameters.get('txt-ocorrencia-periodo', '').strip()
                espelho_dia_id = parameters.get('txt_espelho_diario_id', '').strip()
                pendencia_id = parameters.get('txt-ocorrencia-pendencia', '').strip()

                ocorrencia_quantidade_horas = parameters.get('txt-ocorrencia-quantidade_horas', '').strip()
                ocorrencia_cobranca = parameters.get('txt-ocorrencia-cobranca', 0)
                ocorrencia_data_inicio = parameters.get('txt-ocorrencia-data_inicio', '').strip()
                ocorrencia_data_fim = parameters.get('txt-ocorrencia-data_fim', '').strip()
                ocorrencia_data_cadastro = parameters.get('txt-ocorrencia-data_cadastro', '').strip()
                ocorrencia_responsavel_cadastro = parameters.get('txt-ocorrencia-responsaval_cadastro', '').strip()
                ocorrencia_observacao = parameters.get('txt-ocorrencia-observacao', '').strip()

                # ocorrencia.id = ocorrencia_id
                ocorrencia.status.id = status_id
                ocorrencia.periodo.id = periodo_id
                ocorrencia.espelho_diario.id = espelho_dia_id
                ocorrencia.pendencia.id = pendencia_id

                ocorrencia.data_inicio = ConverteData.stringDate(ocorrencia_data_inicio)
                ocorrencia.data_fim = ConverteData.stringDate(ocorrencia_data_fim)
                ocorrencia.data_cadastro = ConverteData.stringDate(ocorrencia_data_cadastro)
                ocorrencia.responsavel_cadastro = ocorrencia_responsavel_cadastro
                ocorrencia.cobranca = ocorrencia_cobranca == '1'
                ocorrencia.quantidade_horas = ocorrencia_quantidade_horas
                ocorrencia.observacao = ocorrencia_observacao
        
            if operacao == 'PRE-ATUALIZAR':
                ocorrencia_id = parameters.get('txt_ocorrencia_id', '').strip()
                status_id = parameters.get('txt-ocorrencia-status', '').strip()
                periodo_id = parameters.get('txt-ocorrencia-periodo', '').strip()
                espelho_dia_id = parameters.get('txt_espelho_diario_id', '').strip()
                pendencia_id = parameters.get('txt-ocorrencia-pendencia', '').strip()

                ocorrencia_quantidade_horas = parameters.get('txt-ocorrencia-quantidade_horas', '').strip()
                ocorrencia_cobranca = parameters.get('txt-ocorrencia-cobranca', 0)
                ocorrencia_data_inicio = parameters.get('txt-ocorrencia-data_inicio', '').strip()
                ocorrencia_data_fim = parameters.get('txt-ocorrencia-data_fim', '').strip()
                ocorrencia_data_cadastro = parameters.get('txt-ocorrencia-data_cadastro', '').strip()
                ocorrencia_responsavel_cadastro = parameters.get('txt-ocorrencia-responsaval_cadastro', '').strip()
                ocorrencia_observacao = parameters.get('txt-ocorrencia-observacao', '').strip()

                ocorrencia.id = ocorrencia_id
                ocorrencia.status.id = status_id
                ocorrencia.periodo.id = periodo_id
                ocorrencia.espelho_diario.id = espelho_dia_id
                ocorrencia.pendencia.id = pendencia_id

                ocorrencia.data_inicio = ConverteData.stringDate(ocorrencia_data_inicio)
                ocorrencia.data_fim = ConverteData.stringDate(ocorrencia_data_fim)
                ocorrencia.data_cadastro = ConverteData.stringDate(ocorrencia_data_cadastro)
                ocorrencia.responsavel_cadastro = ocorrencia_responsavel_cadastro
                ocorrencia.cobranca = ocorrencia_cobranca == '1'
                ocorrencia.quantidade_horas = ocorrencia_quantidade_horas
                ocorrencia.observacao = ocorrencia_observacao

            elif operacao == 'ATUALIZAR':
                ocorrencia_id = parameters.get('txt_ocorrencia_id', '').strip()
                status_id = parameters.get('txt-ocorrencia-status', '').strip()
                periodo_id = parameters.get('txt-ocorrencia-periodo', '').strip()
                espelho_dia_id = parameters.get('txt_espelho_diario_id', '').strip()
                pendencia_id = parameters.get('txt-ocorrencia-pendencia', '').strip()

                ocorrencia_quantidade_horas = parameters.get('txt-ocorrencia-quantidade_horas', '').strip()
                ocorrencia_cobranca = parameters.get('txt-ocorrencia-cobranca', 0)
                ocorrencia_data_inicio = parameters.get('txt-ocorrencia-data_inicio', '').strip()
                ocorrencia_data_fim = parameters.get('txt-ocorrencia-data_fim', '').strip()
                ocorrencia_data_cadastro = parameters.get('txt-ocorrencia-data_cadastro', '').strip()
                ocorrencia_responsavel_cadastro = parameters.get('txt-ocorrencia-responsaval_cadastro', '').strip()
                ocorrencia_observacao = parameters.get('txt-ocorrencia-observacao', '').strip()

                ocorrencia.id = ocorrencia_id
                ocorrencia.status.id = status_id
                ocorrencia.periodo.id = periodo_id
                ocorrencia.espelho_diario.id = espelho_dia_id
                ocorrencia.pendencia.id = pendencia_id

                ocorrencia.data_inicio = ConverteData.stringDate(ocorrencia_data_inicio)
                ocorrencia.data_fim = ConverteData.stringDate(ocorrencia_data_fim)
                ocorrencia.data_cadastro = ConverteData.stringDate(ocorrencia_data_cadastro)
                ocorrencia.responsavel_cadastro = ocorrencia_responsavel_cadastro
                ocorrencia.cobranca = ocorrencia_cobranca == '1'
                ocorrencia.quantidade_horas = ocorrencia_quantidade_horas
                ocorrencia.observacao = ocorrencia_observacao
        
            if operacao == 'PRE-EXCLUIR':
                ocorrencia_id = parameters.get('txt_ocorrencia_id', '').strip()
                status_id = parameters.get('txt-ocorrencia-status', '').strip()
                periodo_id = parameters.get('txt-ocorrencia-periodo', '').strip()
                espelho_dia_id = parameters.get('txt_espelho_diario_id', '').strip()
                pendencia_id = parameters.get('txt-ocorrencia-pendencia', '').strip()

                ocorrencia_quantidade_horas = parameters.get('txt-ocorrencia-quantidade_horas', '').strip()
                ocorrencia_cobranca = parameters.get('txt-ocorrencia-cobranca', 0)
                ocorrencia_data_inicio = parameters.get('txt-ocorrencia-data_inicio', '').strip()
                ocorrencia_data_fim = parameters.get('txt-ocorrencia-data_fim', '').strip()
                ocorrencia_data_cadastro = parameters.get('txt-ocorrencia-data_cadastro', '').strip()
                ocorrencia_responsavel_cadastro = parameters.get('txt-ocorrencia-responsaval_cadastro', '').strip()
                ocorrencia_observacao = parameters.get('txt-ocorrencia-observacao', '').strip()

                ocorrencia.id = ocorrencia_id
                ocorrencia.status.id = status_id
                ocorrencia.periodo.id = periodo_id
                ocorrencia.espelho_diario.id = espelho_dia_id
                ocorrencia.pendencia.id = pendencia_id

                ocorrencia.data_inicio = ConverteData.stringDate(ocorrencia_data_inicio)
                ocorrencia.data_fim = ConverteData.stringDate(ocorrencia_data_fim)
                ocorrencia.data_cadastro = ConverteData.stringDate(ocorrencia_data_cadastro)
                ocorrencia.responsavel_cadastro = ocorrencia_responsavel_cadastro
                ocorrencia.cobranca = ocorrencia_cobranca == '1'
                ocorrencia.quantidade_horas = ocorrencia_quantidade_horas
                ocorrencia.observacao = ocorrencia_observacao

            elif operacao == 'EXCLUIR':
                ocorrencia_id = parameters.get('txt_ocorrencia_id', '').strip()
                status_id = parameters.get('txt-ocorrencia-status', '').strip()
                periodo_id = parameters.get('txt-ocorrencia-periodo', '').strip()
                espelho_dia_id = parameters.get('txt_espelho_diario_id', '').strip()
                pendencia_id = parameters.get('txt-ocorrencia-pendencia', '').strip()

                ocorrencia_quantidade_horas = parameters.get('txt-ocorrencia-quantidade_horas', '').strip()
                ocorrencia_cobranca = parameters.get('txt-ocorrencia-cobranca', 0)
                ocorrencia_data_inicio = parameters.get('txt-ocorrencia-data_inicio', '').strip()
                ocorrencia_data_fim = parameters.get('txt-ocorrencia-data_fim', '').strip()
                ocorrencia_data_cadastro = parameters.get('txt-ocorrencia-data_cadastro', '').strip()
                ocorrencia_responsavel_cadastro = parameters.get('txt-ocorrencia-responsaval_cadastro', '').strip()
                ocorrencia_observacao = parameters.get('txt-ocorrencia-observacao', '').strip()

                ocorrencia.id = ocorrencia_id
                ocorrencia.status.id = status_id
                ocorrencia.periodo.id = periodo_id
                ocorrencia.espelho_diario.id = espelho_dia_id
                ocorrencia.pendencia.id = pendencia_id

                ocorrencia.data_inicio = ConverteData.stringDate(ocorrencia_data_inicio)
                ocorrencia.data_fim = ConverteData.stringDate(ocorrencia_data_fim)
                ocorrencia.data_cadastro = ConverteData.stringDate(ocorrencia_data_cadastro)
                ocorrencia.responsavel_cadastro = ocorrencia_responsavel_cadastro
                ocorrencia.cobranca = ocorrencia_cobranca == '1'
                ocorrencia.quantidade_horas = ocorrencia_quantidade_horas
                ocorrencia.observacao = ocorrencia_observacao
        
        return ocorrencia        



    def setView(self, resultado, request):

        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            if operacao == 'PRE-SALVAR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR'))
                else:
                    return render_template('ocorrencia/cadastrar_ocorrencia.html', resultado=resultado)

            elif operacao == 'SALVAR':
                if _verificar_msg(resultado):
                    return render_template('ocorrencia/cadastrar_ocorrencia.html', resultado=resultado)
                else:
                    return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR'))
        
            if operacao == 'PRE-ATUALIZAR':
                if _verificar_msg(resultado):
                    return render_template('ocorrencia/atualizar_ocorrencia.html', resultado=resultado)
                else:
                    return render_template('ocorrencia/atualizar_ocorrencia.html', resultado=resultado)

            elif operacao == 'ATUALIZAR':
                if _verificar_msg(resultado):
                    return render_template('ocorrencia/atualizar_ocorrencia.html', resultado=resultado)
                else:
                    return render_template('ocorrencia/atualizar_ocorrencia.html', resultado=resultado)
        
            if operacao == 'PRE-EXCLUIR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR'))
                else:
                    return render_template('ocorrencia/excluir_ocorrencia.html', resultado=resultado)

            elif operacao == 'EXCLUIR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR')+'#id-titulo-ocorrencias')
                else:
                    return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR')+'#id-titulo-ocorrencias')
        
        else:
            pass

        return f'OPERACAO:{operacao}, NOT IMPLEMENTED'



class PendenciaViewHelper(AbstractViewHelper):

    def getEntidade(self, request):

        pendencia = Pendencia(responsavel_cadastro='', data_cadastro='')
        pendencia.status = StatusPendencia()
        pendencia.tipo = TipoPendencia()
        
        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            if operacao == 'PRE-SALVAR':
                # pendencia_id = parameters.get('txt_pendencia_id', '').strip()
                tipo_id = parameters.get('txt-pendencia-tipo', '').strip()
                status_id = parameters.get('txt-pendencia-status', '').strip()

                pendencia_codigo = parameters.get('txt-pendencia-codigo','').strip()
                pendencia_sigla = parameters.get('txt-pendencia-sigla','').strip()
                pendencia_nome = parameters.get('txt-pendencia-nome','').strip()
                pendencia_descricao = parameters.get('txt-pendencia-descricao', '').strip()
                pendencia_limite_maximo_horas = parameters.get('txt-pendencia-limite_maximo_horas','').strip()
                pendencia_prazo_pagamento_dias = parameters.get('txt-pendencia-prazo_pagamento','').strip()
                pendencia_data_cadastro = parameters.get('txt-pendencia-data_cadastro','').strip()
                pendencia_responsavel_cadastro = parameters.get('txt-pendencia-responsavel_cadastro','').strip()

                # pendencia.id = pendencia_id
                pendencia.tipo.id = tipo_id
                pendencia.status.id = status_id

                pendencia.codigo = pendencia_codigo
                pendencia.sigla = pendencia_sigla
                pendencia.nome = pendencia_nome
                pendencia.descricao = pendencia_descricao
                pendencia.limite_maximo_horas = pendencia_limite_maximo_horas
                pendencia.prazo_pagamento_dias = pendencia_prazo_pagamento_dias
                pendencia.data_cadastro = ConverteData.stringDate(pendencia_data_cadastro)
                pendencia.responsavel_cadastro = pendencia_responsavel_cadastro

            elif operacao == 'SALVAR':
                # pendencia_id = parameters.get('txt_pendencia_id', '').strip()
                tipo_id = parameters.get('txt-pendencia-tipo', '').strip()
                status_id = parameters.get('txt-pendencia-status', '').strip()

                pendencia_codigo = parameters.get('txt-pendencia-codigo','').strip()
                pendencia_sigla = parameters.get('txt-pendencia-sigla','').strip()
                pendencia_nome = parameters.get('txt-pendencia-nome','').strip()
                pendencia_descricao = parameters.get('txt-pendencia-descricao', '').strip()
                pendencia_limite_maximo_horas = parameters.get('txt-pendencia-limite_maximo_horas','').strip()
                pendencia_prazo_pagamento_dias = parameters.get('txt-pendencia-prazo_pagamento','').strip()
                pendencia_data_cadastro = parameters.get('txt-pendencia-data_cadastro','').strip()
                pendencia_responsavel_cadastro = parameters.get('txt-pendencia-responsavel_cadastro','').strip()

                # pendencia.id = pendencia_id
                pendencia.tipo.id = tipo_id
                pendencia.status.id = status_id

                pendencia.codigo = pendencia_codigo
                pendencia.sigla = pendencia_sigla
                pendencia.nome = pendencia_nome
                pendencia.descricao = pendencia_descricao
                pendencia.limite_maximo_horas = pendencia_limite_maximo_horas
                pendencia.prazo_pagamento_dias = pendencia_prazo_pagamento_dias
                pendencia.data_cadastro = ConverteData.stringDate(pendencia_data_cadastro)
                pendencia.responsavel_cadastro = pendencia_responsavel_cadastro

            elif operacao == 'PRE-ATUALIZAR':
                pendencia_id = parameters.get('txt_pendencia_id', '').strip()
                tipo_id = parameters.get('txt-pendencia-tipo', '').strip()
                status_id = parameters.get('txt-pendencia-status', '').strip()

                pendencia_codigo = parameters.get('txt-pendencia-codigo','').strip()
                pendencia_sigla = parameters.get('txt-pendencia-sigla','').strip()
                pendencia_nome = parameters.get('txt-pendencia-nome','').strip()
                pendencia_descricao = parameters.get('txt-pendencia-descricao', '').strip()
                pendencia_limite_maximo_horas = parameters.get('txt-pendencia-limite_maximo_horas','').strip()
                pendencia_prazo_pagamento_dias = parameters.get('txt-pendencia-prazo_pagamento','').strip()
                pendencia_data_cadastro = parameters.get('txt-pendencia-data_cadastro','').strip()
                pendencia_responsavel_cadastro = parameters.get('txt-pendencia-responsavel_cadastro','').strip()

                pendencia.id = pendencia_id
                pendencia.tipo.id = tipo_id
                pendencia.status.id = status_id

                pendencia.codigo = pendencia_codigo
                pendencia.sigla = pendencia_sigla
                pendencia.nome = pendencia_nome
                pendencia.descricao = pendencia_descricao
                pendencia.limite_maximo_horas = pendencia_limite_maximo_horas
                pendencia.prazo_pagamento_dias = pendencia_prazo_pagamento_dias
                pendencia.data_cadastro = ConverteData.stringDate(pendencia_data_cadastro)
                pendencia.responsavel_cadastro = pendencia_responsavel_cadastro

            elif operacao == 'ATUALIZAR':
                pendencia_id = parameters.get('txt_pendencia_id', '').strip()
                tipo_id = parameters.get('txt-pendencia-tipo', '').strip()
                status_id = parameters.get('txt-pendencia-status', '').strip()

                pendencia_codigo = parameters.get('txt-pendencia-codigo','').strip()
                pendencia_sigla = parameters.get('txt-pendencia-sigla','').strip()
                pendencia_nome = parameters.get('txt-pendencia-nome','').strip()
                pendencia_descricao = parameters.get('txt-pendencia-descricao', '').strip()
                pendencia_limite_maximo_horas = parameters.get('txt-pendencia-limite_maximo_horas','').strip()
                pendencia_prazo_pagamento_dias = parameters.get('txt-pendencia-prazo_pagamento','').strip()
                pendencia_data_cadastro = parameters.get('txt-pendencia-data_cadastro','').strip()
                pendencia_responsavel_cadastro = parameters.get('txt-pendencia-responsavel_cadastro','').strip()

                pendencia.id = pendencia_id
                pendencia.tipo.id = tipo_id
                pendencia.status.id = status_id

                pendencia.codigo = pendencia_codigo
                pendencia.sigla = pendencia_sigla
                pendencia.nome = pendencia_nome
                pendencia.descricao = pendencia_descricao
                pendencia.limite_maximo_horas = pendencia_limite_maximo_horas
                pendencia.prazo_pagamento_dias = pendencia_prazo_pagamento_dias
                pendencia.data_cadastro = ConverteData.stringDate(pendencia_data_cadastro)
                pendencia.responsavel_cadastro = pendencia_responsavel_cadastro
            
            elif operacao == 'PRE-EXCLUIR':
                pendencia_id = parameters.get('txt_pendencia_id', '').strip()
                tipo_id = parameters.get('txt-pendencia-tipo', '').strip()
                status_id = parameters.get('txt-pendencia-status', '').strip()

                pendencia_codigo = parameters.get('txt-pendencia-codigo','').strip()
                pendencia_sigla = parameters.get('txt-pendencia-sigla','').strip()
                pendencia_nome = parameters.get('txt-pendencia-nome','').strip()
                pendencia_descricao = parameters.get('txt-pendencia-descricao', '').strip()
                pendencia_limite_maximo_horas = parameters.get('txt-pendencia-limite_maximo_horas','').strip()
                pendencia_prazo_pagamento_dias = parameters.get('txt-pendencia-prazo_pagamento','').strip()
                pendencia_data_cadastro = parameters.get('txt-pendencia-data_cadastro','').strip()
                pendencia_responsavel_cadastro = parameters.get('txt-pendencia-responsavel_cadastro','').strip()

                pendencia.id = pendencia_id
                pendencia.tipo.id = tipo_id
                pendencia.status.id = status_id

                pendencia.codigo = pendencia_codigo
                pendencia.sigla = pendencia_sigla
                pendencia.nome = pendencia_nome
                pendencia.descricao = pendencia_descricao
                pendencia.limite_maximo_horas = pendencia_limite_maximo_horas
                pendencia.prazo_pagamento_dias = pendencia_prazo_pagamento_dias
                pendencia.data_cadastro = ConverteData.stringDate(pendencia_data_cadastro)
                pendencia.responsavel_cadastro = pendencia_responsavel_cadastro
            
            elif operacao == 'EXCLUIR':
                pendencia_id = parameters.get('txt_pendencia_id', '').strip()
                tipo_id = parameters.get('txt-pendencia-tipo', '').strip()
                status_id = parameters.get('txt-pendencia-status', '').strip()

                pendencia_codigo = parameters.get('txt-pendencia-codigo','').strip()
                pendencia_sigla = parameters.get('txt-pendencia-sigla','').strip()
                pendencia_nome = parameters.get('txt-pendencia-nome','').strip()
                pendencia_descricao = parameters.get('txt-pendencia-descricao', '').strip()
                pendencia_limite_maximo_horas = parameters.get('txt-pendencia-limite_maximo_horas','').strip()
                pendencia_prazo_pagamento_dias = parameters.get('txt-pendencia-prazo_pagamento','').strip()
                pendencia_data_cadastro = parameters.get('txt-pendencia-data_cadastro','').strip()
                pendencia_responsavel_cadastro = parameters.get('txt-pendencia-responsavel_cadastro','').strip()

                pendencia.id = pendencia_id
                pendencia.tipo.id = tipo_id
                pendencia.status.id = status_id

                pendencia.codigo = pendencia_codigo
                pendencia.sigla = pendencia_sigla
                pendencia.nome = pendencia_nome
                pendencia.descricao = pendencia_descricao
                pendencia.limite_maximo_horas = pendencia_limite_maximo_horas
                pendencia.prazo_pagamento_dias = pendencia_prazo_pagamento_dias
                pendencia.data_cadastro = ConverteData.stringDate(pendencia_data_cadastro)
                pendencia.responsavel_cadastro = pendencia_responsavel_cadastro

        return pendencia        

    def setView(self, resultado, request):

        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            if operacao == 'PRE-SALVAR':
                if _verificar_msg(resultado):
                    return render_template('ocorrencia/cadastrar_pendencia.html', resultado=resultado)
                else:
                    return render_template('ocorrencia/cadastrar_pendencia.html', resultado=resultado)

            elif operacao == 'SALVAR':
                if _verificar_msg(resultado):
                    return render_template('ocorrencia/cadastrar_pendencia.html', resultado=resultado)
                else:
                    return redirect(url_for('bp_ocorrencia.pendencias'))

            elif operacao == 'PRE-ATUALIZAR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_ocorrencia.pendencias'))
                else:
                    return render_template('ocorrencia/atualizar_pendencia.html', resultado=resultado)
            
            elif operacao == 'ATUALIZAR':
                if _verificar_msg(resultado):
                    return render_template('ocorrencia/atualizar_pendencia.html', resultado=resultado)
                else:
                    return render_template('ocorrencia/atualizar_pendencia.html', resultado=resultado)

            elif operacao == 'PRE-EXCLUIR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_ocorrencia.pendencias'))
                else:
                    return render_template('ocorrencia/excluir_pendencia.html', resultado=resultado)
            
            elif operacao == 'EXCLUIR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_ocorrencia.pendencias'))
                else:
                    return redirect(url_for('bp_ocorrencia.pendencias'))

        else:
            _verificar_msg(resultado)
            return render_template('ocorrencia/pendencias.html', resultado=resultado)

        return f'OPERACAO:{operacao}, NOT IMPLEMENTED'
