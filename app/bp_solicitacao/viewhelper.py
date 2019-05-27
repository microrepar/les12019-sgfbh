from les12019_web.abstract_viewhelper import AbstractViewHelper, _verificar_msg
from les12019_core.utils import get_parameters_request
from les12019_core.aplicacao import ConverteData, Resultado
from app.bp_solicitacao.models import Solicitacao, Despacho, Decisao, StatusSolicitacao, StatusDespacho, TipoSolicitacao
from app.bp_ocorrencia.models import Ocorrencia
from app.bp_frequencia.models import EspelhoDiario
from flask_login import current_user
from flask import render_template, redirect, url_for, Request


class SolicitacaoViewHelper(AbstractViewHelper):

    def getEntidade(self, request):

        solicitacao = Solicitacao(email='')
        solicitacao.ocorrencia = Ocorrencia()
        solicitacao.tipo = TipoSolicitacao()
        solicitacao.status = StatusSolicitacao(nome='')
        solicitacao.despacho = Despacho()

        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            if operacao == 'PRE-SALVAR':
                # solicitacao_id = parameters.get('txt_solicitacao_id', '').strip()
                ocorrencia_id = parameters.get('txt_ocorrencia_id', '').strip()
                despacho_id = parameters.get('txt_despacho_id', '').strip()
                tipo_id = parameters.get('txt-solicitacao-tipo', '').strip()
                status_id = parameters.get('txt-solicitacao-status', '').strip()

                solicitacao_numero = parameters.get('txt-solicitacao-numero', '').strip()
                solicitacao_data_cadastro = parameters.get('txt-solicitacao-data_cadastro', '').strip()
                solicitacao_responsavel_cadastro = parameters.get('txt-solicitacao-responsavel_cadastro', '').strip()
                solicitacao_email = parameters.get('txt-solicitacao-email_reposponsavel_inclusao', '').strip()
                solicitacao_descricao = parameters.get('txt-solicitacao-descricao', '').strip()

                # solicitacao.id = solicitacao_id
                solicitacao.ocorrencia.id = ocorrencia_id
                solicitacao.tipo.id = tipo_id
                solicitacao.status.id = status_id
                solicitacao.despacho.id = despacho_id

                solicitacao.numero = solicitacao_numero
                solicitacao.data_cadastro = ConverteData.stringDate(solicitacao_data_cadastro)
                solicitacao.responsavel_cadastro = solicitacao_responsavel_cadastro
                solicitacao.email = solicitacao_email
                solicitacao.descricao = solicitacao_descricao

            elif operacao == 'SALVAR':
                # solicitacao_id = parameters.get('txt_solicitacao_id', '').strip()
                ocorrencia_id = parameters.get('txt_ocorrencia_id', '').strip()
                despacho_id = parameters.get('txt_despacho_id', '').strip()
                tipo_id = parameters.get('txt-solicitacao-tipo', '').strip()
                status_id = parameters.get('txt-solicitacao-status', '').strip()

                solicitacao_numero = parameters.get('txt-solicitacao-numero', '').strip()
                solicitacao_data_cadastro = parameters.get('txt-solicitacao-data_cadastro', '').strip()
                solicitacao_responsavel_cadastro = parameters.get('txt-solicitacao-responsavel_cadastro', '').strip()
                solicitacao_email = parameters.get('txt-solicitacao-email_reposponsavel_inclusao', '').strip()
                solicitacao_descricao = parameters.get('txt-solicitacao-descricao', '').strip()

                # solicitacao.id = solicitacao_id
                solicitacao.ocorrencia.id = ocorrencia_id
                solicitacao.tipo.id = tipo_id
                solicitacao.status.id = status_id
                solicitacao.despacho.id = despacho_id

                solicitacao.numero = solicitacao_numero
                solicitacao.data_cadastro = ConverteData.stringDate(solicitacao_data_cadastro)
                solicitacao.responsavel_cadastro = solicitacao_responsavel_cadastro
                solicitacao.email = solicitacao_email
                solicitacao.descricao = solicitacao_descricao

            elif operacao == 'PRE-ATUALIZAR':
                solicitacao_id = parameters.get('txt_solicitacao_id', '').strip()
                ocorrencia_id = parameters.get('txt_ocorrencia_id', '').strip()
                despacho_id = parameters.get('txt_despacho_id', '').strip()
                tipo_id = parameters.get('txt-solicitacao-tipo', '').strip()
                status_id = parameters.get('txt-solicitacao-status', '').strip()

                solicitacao_numero = parameters.get('txt-solicitacao-numero', '').strip()
                solicitacao_data_cadastro = parameters.get('txt-solicitacao-data_cadastro', '').strip()
                solicitacao_responsavel_cadastro = parameters.get('txt-solicitacao-responsavel_cadastro', '').strip()
                solicitacao_email = parameters.get('txt-solicitacao-email_reposponsavel_inclusao', '').strip()
                solicitacao_descricao = parameters.get('txt-solicitacao-descricao', '').strip()

                solicitacao.id = solicitacao_id
                solicitacao.ocorrencia.id = ocorrencia_id
                solicitacao.tipo.id = tipo_id
                solicitacao.status.id = status_id
                solicitacao.despacho.id = despacho_id

                solicitacao.numero = solicitacao_numero
                solicitacao.data_cadastro = ConverteData.stringDate(solicitacao_data_cadastro)
                solicitacao.responsavel_cadastro = solicitacao_responsavel_cadastro
                solicitacao.email = solicitacao_email
                solicitacao.descricao = solicitacao_descricao

            elif operacao == 'ATUALIZAR':
                solicitacao_id = parameters.get('txt_solicitacao_id', '').strip()
                ocorrencia_id = parameters.get('txt_ocorrencia_id', '').strip()
                despacho_id = parameters.get('txt_despacho_id', '').strip()
                tipo_id = parameters.get('txt-solicitacao-tipo', '').strip()
                status_id = parameters.get('txt-solicitacao-status', '').strip()

                solicitacao_numero = parameters.get('txt-solicitacao-numero', '').strip()
                solicitacao_data_cadastro = parameters.get('txt-solicitacao-data_cadastro', '').strip()
                solicitacao_responsavel_cadastro = parameters.get('txt-solicitacao-responsavel_cadastro', '').strip()
                solicitacao_email = parameters.get('txt-solicitacao-email_reposponsavel_inclusao', '').strip()
                solicitacao_descricao = parameters.get('txt-solicitacao-descricao', '').strip()

                solicitacao.id = solicitacao_id
                solicitacao.ocorrencia.id = ocorrencia_id
                solicitacao.tipo.id = tipo_id
                solicitacao.status.id = status_id
                solicitacao.despacho.id = despacho_id

                solicitacao.numero = solicitacao_numero
                solicitacao.data_cadastro = ConverteData.stringDate(solicitacao_data_cadastro)
                solicitacao.responsavel_cadastro = solicitacao_responsavel_cadastro
                solicitacao.email = solicitacao_email
                solicitacao.descricao = solicitacao_descricao
            
            elif operacao == 'PRE-EXCLUIR':
                solicitacao_id = parameters.get('txt_solicitacao_id', '').strip()
                ocorrencia_id = parameters.get('txt_ocorrencia_id', '').strip()
                despacho_id = parameters.get('txt_despacho_id', '').strip()
                tipo_id = parameters.get('txt-solicitacao-tipo', '').strip()
                status_id = parameters.get('txt-solicitacao-status', '').strip()

                solicitacao_numero = parameters.get('txt-solicitacao-numero', '').strip()
                solicitacao_data_cadastro = parameters.get('txt-solicitacao-data_cadastro', '').strip()
                solicitacao_responsavel_cadastro = parameters.get('txt-solicitacao-responsavel_cadastro', '').strip()
                solicitacao_email = parameters.get('txt-solicitacao-email_reposponsavel_inclusao', '').strip()
                solicitacao_descricao = parameters.get('txt-solicitacao-descricao', '').strip()

                solicitacao.id = solicitacao_id
                solicitacao.ocorrencia.id = ocorrencia_id
                solicitacao.tipo.id = tipo_id
                solicitacao.status.id = status_id
                solicitacao.despacho.id = despacho_id

                solicitacao.numero = solicitacao_numero
                solicitacao.data_cadastro = ConverteData.stringDate(solicitacao_data_cadastro)
                solicitacao.responsavel_cadastro = solicitacao_responsavel_cadastro
                solicitacao.email = solicitacao_email
                solicitacao.descricao = solicitacao_descricao

            elif operacao == 'EXCLUIR':
                espelho_diario_id = parameters.get('txt_espelho_diario_id', '').strip()
                solicitacao_id = parameters.get('txt_solicitacao_id', '').strip()
                ocorrencia_id = parameters.get('txt_ocorrencia_id', '').strip()
                despacho_id = parameters.get('txt_despacho_id', '').strip()
                tipo_id = parameters.get('txt-solicitacao-tipo', '').strip()
                status_id = parameters.get('txt-solicitacao-status', '').strip()

                solicitacao_numero = parameters.get('txt-solicitacao-numero', '').strip()
                solicitacao_data_cadastro = parameters.get('txt-solicitacao-data_cadastro', '').strip()
                solicitacao_responsavel_cadastro = parameters.get('txt-solicitacao-responsavel_cadastro', '').strip()
                solicitacao_email = parameters.get('txt-solicitacao-email_reposponsavel_inclusao', '').strip()
                solicitacao_descricao = parameters.get('txt-solicitacao-descricao', '').strip()

                solicitacao.ocorrencia.espelho_diario = EspelhoDiario(id=espelho_diario_id) 
                solicitacao.id = solicitacao_id
                solicitacao.ocorrencia.id = ocorrencia_id
                solicitacao.tipo.id = tipo_id
                solicitacao.status.id = status_id
                solicitacao.despacho.id = despacho_id

                solicitacao.numero = solicitacao_numero
                solicitacao.data_cadastro = ConverteData.stringDate(solicitacao_data_cadastro)
                solicitacao.responsavel_cadastro = solicitacao_responsavel_cadastro
                solicitacao.email = solicitacao_email
                solicitacao.descricao = solicitacao_descricao
                
        return solicitacao


    def setView(self, resultado, request):
        
        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            if operacao == 'PRE-SALVAR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR')+'#id-titulo-ocorrencias')
                else:
                    return render_template('solicitacao/cadastrar_solicitacao.html', resultado=resultado)
            
            elif operacao == 'SALVAR':
                if _verificar_msg(resultado):
                    return render_template('solicitacao/cadastrar_solicitacao.html', resultado=resultado)
                else:
                    return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR')+'#id-titulo-ocorrencias')
            
            elif operacao == 'PRE-ATUALIZAR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR')+'#id-titulo-ocorrencias')
                else:
                    return render_template('solicitacao/atualizar_solicitacao.html', resultado=resultado)
            
            elif operacao == 'ATUALIZAR':
                if _verificar_msg(resultado):
                    return render_template('solicitacao/atualizar_solicitacao.html', resultado=resultado)
                else:
                    return render_template('solicitacao/atualizar_solicitacao.html', resultado=resultado)

            elif operacao == 'PRE-EXCLUIR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR')+'#id-titulo-ocorrencias')
                else:
                    return render_template('solicitacao/excluir_solicitacao.html', resultado=resultado)
            
            elif operacao == 'EXCLUIR':
                if current_user.is_authenticated:
                    if _verificar_msg(resultado):
                        return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR')+'#id-titulo-ocorrencias')
                    else:
                        return redirect(url_for('bp_frequencia.frequencia_diaria', txt_espelho_diario_id=resultado.entidades[-1].espelho_diario.id, operacao='AVALIAR')+'#id-titulo-ocorrencias')
                else:
                    if _verificar_msg(resultado):
                        return redirect(url_for('bp_solicitacao.consultar_solicitacoes', txt_funcionario_id=28, operacao='CONSULTAR_ID') + '#id-titulo-pendencias')
                    else:
                        return redirect(url_for('bp_solicitacao.consultar_solicitacoes', txt_funcionario_id=28, operacao='CONSULTAR_ID') + '#id-titulo-pendencias')

        else:
            _verificar_msg(resultado)
            return render_template('solicitacao/cadastrar_solicitacao.html', resultado=resultado)

        return f'OPERACAO:{operacao}, NOT IMPLEMENTED'


###############################################################################################
class DespachoViewHelper(AbstractViewHelper):

    def getEntidade(self, request):
        despacho = Despacho()
        despacho.solicitacao = Solicitacao()
        despacho.solicitacao.ocorrencia = Ocorrencia()
        despacho.solicitacao.ocorrencia.espelho_diario = EspelhoDiario()
        despacho.status = StatusDespacho()        
        despacho.decisao = Decisao()


        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            if operacao == 'PRE-SALVAR':
                # despacho_id = parameters.get('txt_despacho_id', '').strip()
                solicitacao_id = parameters.get('txt_solicitacao_id', '').strip()
                espelho_diario_id = parameters.get('txt_espelho_diario_id', '').strip()
                ocorrencia_id = parameters.get('txt_ocorrencia_id', '').strip()

                despacho_decisao_id = parameters.get('txt-despacho-tipo_decisao', '').strip()
                despacho_data_cadastro = parameters.get('txt-despacho-data_cadastro', '').strip()
                despacho_responsavel_cadastro = parameters.get('txt-despacho-responsavel_cadastro', '').strip()
                despacho_descricao = parameters.get('txt-despacho-descricao', '').strip()

                # despacho.id = despacho_id
                despacho.solicitacao.id = solicitacao_id
                despacho.solicitacao.ocorrencia.id = ocorrencia_id
                despacho.solicitacao.ocorrencia.espelho_diario.id = espelho_diario_id

                despacho.decisao.id = despacho_decisao_id
                despacho.data_cadastro = ConverteData.stringDate(despacho_data_cadastro)
                despacho.responsavel_cadastro = despacho_responsavel_cadastro
                despacho.descricao = despacho_descricao                
            
            if operacao == 'SALVAR':
                # despacho_id = parameters.get('txt_despacho_id', '').strip()
                solicitacao_id = parameters.get('txt_solicitacao_id', '').strip()
                espelho_diario_id = parameters.get('txt_espelho_diario_id', '').strip()
                ocorrencia_id = parameters.get('txt_ocorrencia_id', '').strip()

                despacho_decisao_id = parameters.get('txt-despacho-tipo_decisao', '').strip()
                despacho_data_cadastro = parameters.get('txt-despacho-data_cadastro', '').strip()
                despacho_responsavel_cadastro = parameters.get('txt-despacho-responsavel_cadastro', '').strip()
                despacho_descricao = parameters.get('txt-despacho-descricao', '').strip()

                # despacho.id = despacho_id
                despacho.solicitacao.id = solicitacao_id
                despacho.solicitacao.ocorrencia.id = ocorrencia_id
                despacho.solicitacao.ocorrencia.espelho_diario.id = espelho_diario_id

                despacho.decisao.id = despacho_decisao_id
                despacho.data_cadastro = ConverteData.stringDate(despacho_data_cadastro)
                despacho.responsavel_cadastro = despacho_responsavel_cadastro
                despacho.descricao = despacho_descricao                
            
            elif operacao == 'PRE-ATUALIZAR':
                pass

            elif operacao == 'ATUALIZAR':
                pass

            elif operacao == 'PRE-EXCLUIR':
                pass

            elif operacao == 'EXCLUIR':
                pass


        return despacho

    def setView(self, resultado, request):

        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            if operacao == 'PRE-SALVAR':
                if _verificar_msg(resultado):
                    return render_template('solicitacao/cadastrar_despacho.html', resultado=resultado)
                else:
                    return render_template('solicitacao/cadastrar_despacho.html', resultado=resultado)
            
            elif operacao == 'SALVAR':
                if _verificar_msg(resultado):
                    return render_template('solicitacao/cadastrar_despacho.html', resultado=resultado)
                else:
                    return render_template('solicitacao/cadastrar_despacho.html', resultado=resultado)
            
            elif operacao == 'PRE-ATUALIZAR':
                if _verificar_msg(resultado):
                    pass
                else:
                    pass
            
            elif operacao == 'ATUALIZAR':
                if _verificar_msg(resultado):
                    pass
                else:
                    pass

            elif operacao == 'PRE-EXCLUIR':
                if _verificar_msg(resultado):
                    pass
                else:
                    pass
            
            elif operacao == 'EXCLUIR':
                if _verificar_msg(resultado):
                    pass
                else:
                    pass


        else:
            _verificar_msg(resultado)
            return render_template('solicitacao/cadastrar_despacho.html', resultado=resultado)

        return f'OPERACAO:{operacao}, NOT IMPLEMENTED'
