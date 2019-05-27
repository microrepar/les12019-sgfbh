"""Módulo viewhelper - contém a classe AbstractViewHelper e as classes concretas
"""

from les12019_web.abstract_viewhelper import AbstractViewHelper, _verificar_msg
from datetime import datetime
from les12019_core.aplicacao import Resultado
from les12019_core.aplicacao import ConverteData

from app.bp_funcionario.models import Funcionario
from app.bp_endereco.models import Endereco, Logradouro

from flask import render_template, redirect, url_for, Request, flash

################### AbstractViewHelper de Endereço #############################
class EnderecoViewHelper(AbstractViewHelper):

    def getEntidade(self, request):
        endereco = Endereco(responsavel_cadastro='')

        if request.method == 'GET':
            parameters = request.args
        else:
            parameters = request.form

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:

            if operacao == 'PRE-SALVAR':
                cep = parameters.get('txt-endereco-cep', '')
                numero = parameters.get('txt-endereco-numero', '')
                complemento_endereco = parameters.get('txt-endereco-complemento','')
                observacoes = parameters.get('txt-endereco-observacao', '')
                
                funcionario_id = parameters.get('funcionario_id','')
                tipo_endereco_id = parameters.get('txt-endereco-tipo_endereco_id','')
                status_id = parameters.get('txt-endereco-status_endereco_id')

                endereco.cep = cep
                endereco.numero = numero
                endereco.complemento_endereco = complemento_endereco
                endereco.observacoes = observacoes
                
                endereco.funcionario_id = funcionario_id
                endereco.tipo_endereco_id = tipo_endereco_id
                endereco.status_id = status_id


            elif operacao == 'SALVAR':
                cep = parameters.get('txt-endereco-cep', '')
                numero = parameters.get('txt-endereco-numero', '')
                complemento_endereco = parameters.get('txt-endereco-complemento','')
                observacoes = parameters.get('txt-endereco-observacao', '')
                funcionario_id = parameters.get('funcionario_id','')
                tipo_endereco_id = parameters.get('txt-endereco-tipo_endereco_id','')
                status_id = parameters.get('txt-endereco-status_endereco_id')
                logradouro_id = parameters.get('txt-logradouro-id', '')
                
                endereco.cep = cep
                endereco.numero = numero
                endereco.complemento_endereco = complemento_endereco
                endereco.observacoes = observacoes
                endereco.funcionario_id = funcionario_id
                endereco.tipo_endereco_id = tipo_endereco_id
                endereco.status_id = status_id
                endereco.logradouro_id = logradouro_id

                logradouro = Logradouro()

                tipo_logradouro = parameters.get('txt-logradouro-tipo_logradouro', '')
                _logradouro = parameters.get('txt-logradouro-logradouro', '')
                bairro = parameters.get('txt-logradouro-bairro', '')
                cidade = parameters.get('txt-logradouro-cidade', '')
                uf = parameters.get('txt-logradouro-estado', '')

                logradouro.cep = cep
                logradouro.tipo_logradouro = tipo_logradouro
                logradouro.logradouro = _logradouro
                logradouro.bairro = bairro
                logradouro.cidade = cidade
                logradouro.uf = uf

                endereco._logradouro = logradouro


            elif operacao == 'PRE-ATUALIZAR':
                endereco.id = parameters.get('endereco_id')
                cep = parameters.get('txt-endereco-cep', None)
                numero = parameters.get('txt-endereco-numero', '')
                complemento_endereco = parameters.get('txt-endereco-complemento','')
                observacoes = parameters.get('txt-endereco-observacao', '')
                
                endereco.cep = cep
                endereco.numero = numero
                endereco.complemento_endereco = complemento_endereco
                endereco.observacoes = observacoes
                
                funcionario_id = parameters.get('funcionario_id', '')
                tipo_endereco_id = parameters.get('txt-endereco-tipo_endereco_id','')
                status_id = parameters.get('txt-endereco-status_endereco_id')
                logradouro_id = parameters.get('txt-logradouro-id', '')
                                
                endereco.funcionario_id = funcionario_id
                endereco.tipo_endereco_id = tipo_endereco_id
                endereco.status_id = status_id
                endereco.logradouro_id = logradouro_id
                

            elif operacao == 'ATUALIZAR':
                endereco.id = parameters.get('endereco_id')
                cep = parameters.get('txt-endereco-cep', '')
                numero = parameters.get('txt-endereco-numero', '')
                complemento_endereco = parameters.get('txt-endereco-complemento','')
                observacoes = parameters.get('txt-endereco-observacao', '')
                funcionario_id = parameters.get('funcionario_id','')
                tipo_endereco_id = parameters.get('txt-endereco-tipo_endereco_id','')
                status_id = parameters.get('txt-endereco-status_endereco_id')
                logradouro_id = parameters.get('txt-logradouro-id', '')
                
                endereco.cep = cep
                endereco.numero = numero
                endereco.complemento_endereco = complemento_endereco
                endereco.observacoes = observacoes
                endereco.funcionario_id = funcionario_id
                endereco.tipo_endereco_id = tipo_endereco_id
                endereco.status_id = status_id
                endereco.logradouro_id = logradouro_id

                logradouro = Logradouro()

                tipo_logradouro = parameters.get('txt-logradouro-tipo_logradouro', '')
                _logradouro = parameters.get('txt-logradouro-logradouro', '')
                bairro = parameters.get('txt-logradouro-bairro', '')
                cidade = parameters.get('txt-logradouro-cidade', '')
                uf = parameters.get('txt-logradouro-estado', '')

                logradouro.cep = cep
                logradouro.tipo_logradouro = tipo_logradouro
                logradouro.logradouro = _logradouro
                logradouro.bairro = bairro
                logradouro.cidade = cidade
                logradouro.uf = uf

                logradouro._enderecos_moradores.append(endereco)


            elif operacao == 'PRE-EXCLUIR':
                endereco.id = parameters.get('endereco_id')


            elif operacao == 'EXCLUIR':
                endereco.id = parameters.get('endereco_id')
                endereco.funcionario_id = parameters.get('funcionario_id')
                
        return endereco


    def setView(self, resultado, request):

        if request.method == 'GET':
            parameters = request.args
        else:
            parameters = request.form

        operacao = parameters.get('operacao')

        if operacao == 'PRE-SALVAR':
            return render_template('endereco/enderecoCadastrar.html', resultado=resultado)
        
        elif operacao == 'SALVAR':
            if _verificar_msg(resultado):
                return render_template('endereco/enderecoCadastrar.html', resultado=resultado)
            else:
                return redirect(url_for('bp_funcionario.alterar_funcionario', funcionario_id=resultado.entidades[-1].funcionario_id, operacao='PRE-ATUALIZAR')+'#id-titulo-enderecos')

        elif operacao == 'PRE-ATUALIZAR':
            return render_template('endereco/enderecoAlterar.html', resultado=resultado)

        elif operacao == 'BUSCAR-CEP':
            return render_template('endereco/enderecoAlterar.html', resultado=resultado)

        elif operacao == 'ATUALIZAR':
            if _verificar_msg(resultado):
                return render_template('endereco/enderecoAlterar.html', resultado=resultado)
            else:
                return redirect(url_for('bp_endereco.alterar_endereco', endereco_id=resultado.entidades[-1].id, operacao='PRE-ATUALIZAR'))

        elif operacao == 'PRE-EXCLUIR':
            if _verificar_msg(resultado):
                return redirect(url_for('bp_funcionario.alterar_funcionario', funcionario_id=resultado.entidades[-1].funcionario_id, operacao='PRE-ATUALIZAR'))
            else:
                return render_template('endereco/enderecoExcluir.html', resultado=resultado)

        elif operacao == 'EXCLUIR':
            if _verificar_msg(resultado):
                return redirect(url_for('bp_funcionario.alterar_funcionario', funcionario_id=resultado.entidades[-1].funcionario_id, operacao='PRE-ATUALIZAR'))
                # return redirect(url_for('bp_funcionario.funcionarios'))
            else:
                return redirect(url_for('bp_funcionario.alterar_funcionario', funcionario_id=resultado.entidades[-1].funcionario_id, operacao='PRE-ATUALIZAR'))
