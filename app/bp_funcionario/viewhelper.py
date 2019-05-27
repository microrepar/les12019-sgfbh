"""Módulo viewhelper - contém a classe AbstractViewHelper e as classes concretas
"""

from les12019_web.abstract_viewhelper import AbstractViewHelper, _verificar_msg
from datetime import datetime
from les12019_core.aplicacao import Resultado
from les12019_core.aplicacao import ConverteData

from app.bp_funcionario.models import Funcionario, StatusFuncionario, TipoVinculo, Cargo

from flask import render_template, redirect, url_for, Request, flash, session
from flask_login import current_user


########################## ViewHelper de Funcionario ##############################
class FuncionarioViewHelper(AbstractViewHelper):
    
    def getEntidade(self, request):        
        funcionario = Funcionario()
        status = StatusFuncionario()
        vinculo = TipoVinculo()
        cargo = Cargo()
        
        funcionario._status = status
        funcionario._tipo_vinculo = vinculo
        funcionario.cargo = cargo

        if request.method == 'GET':
            parameters = request.args
        else:
            parameters = request.form


        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:

            if operacao == 'PRE-ATUALIZAR':
                funcionario.id = parameters.get('funcionario_id', session.get('funcionario_id','')).strip()
                session['funcionario_id'] = funcionario.id            
            
            elif operacao == 'ATUALIZAR':
                id_ = parameters.get('funcionario_id','').strip()
                status_nome = parameters.get('txt-funcionario-status', '').strip()
                # foto = parameters.get('foto-func', '').strip()
                cpf = parameters.get('cpf-func', '').strip()
                nome = parameters.get('nome-func', '').strip()
                sexo = parameters.get('sexo-func', '').strip()
                pisPasep = parameters.get('pis-pasep-func', '').strip()
                rg = parameters.get('rg-func', '').strip()
                email = parameters.get('email-func', '').strip()
                responsavelCadastro = parameters.get('reponsavel-cad-func', '').strip()
                matricula = parameters.get('matricula-func', '').strip()
                cargo_nome = parameters.get('cargo-func', '').strip()
                lotacao = parameters.get('lotacao-func', '').strip()
                unidadeDeTrabalho = parameters.get('unidade-trabalho-func', '').strip()
                numeroCTPS = parameters.get('numero-ctps-func', '').strip()
                serieCTPS = parameters.get('serie-ctps-func', '').strip()
                uf = parameters.get('uf-ctps-func', '').strip()
                tipo_vinculo_nome = parameters.get('txt-funcionario-tipo_vinvulo', '').strip()
                nomeUsuario = parameters.get('nome-usuario-func', '').strip()
                senha = parameters.get('senha-usuario-func', '').strip()
                
                funcionario.id = id_
                funcionario._status.nome = status_nome
                funcionario.cpf = cpf
                funcionario.nome = nome
                funcionario.sexo = sexo
                funcionario.pisPasep = pisPasep
                funcionario.rg = rg
                funcionario.email = email
                funcionario.responsavelCadastro = responsavelCadastro
                funcionario.matricula = matricula
                funcionario.cargo.nome = cargo_nome
                funcionario.lotacao = lotacao
                funcionario.unidadeDeTrabalho = unidadeDeTrabalho
                funcionario.numeroCTPS = numeroCTPS
                funcionario.serieCTPS = serieCTPS
                funcionario.ufCTPS = uf
                funcionario._tipo_vinculo.nome = tipo_vinculo_nome
                funcionario.nomeUsuario = nomeUsuario
                funcionario.senha = senha

                dataCadastro = parameters.get('data-cadastro-func').strip()
                dataAdmissao = parameters.get('data-admissao-func').strip()
                dataNascimento = parameters.get('data-nasc-func').strip()
                dataEmissaoCTPS = parameters.get('data-emissao-ctps-func').strip()

                if dataCadastro is not None:
                    funcionario.dataCadastro = ConverteData.stringDate(dataCadastro)
                if dataAdmissao is not None:
                    funcionario.dataAdmissao = ConverteData.stringDate(dataAdmissao)
                if dataNascimento is not None:
                    funcionario.dataNascimento = ConverteData.stringDate(dataNascimento)
                if dataEmissaoCTPS is not None:
                    funcionario.dataEmissaoCTPS = ConverteData.stringDate(dataEmissaoCTPS)
            

            elif operacao == 'PRE-SALVAR':                 # Atribui string vazia para não exibir a palavra None no formulário
                funcionario._status.nome = ''                    # status
                funcionario.cpf = ''                       # cpf
                funcionario.nome = ''                      # nome
                funcionario.sexo = ''                      # sexo
                funcionario.pisPasep = ''                  # pisPasep
                funcionario.rg = ''                        # rg
                funcionario.email = ''                     # email
                funcionario.responsavelCadastro = ''       # responsavelCadastro
                funcionario.matricula = ''                 # matricula
                funcionario.lotacao = ''                   # lotacao
                funcionario.unidadeDeTrabalho = ''         # unidadeDeTrabalho
                funcionario.numeroCTPS = ''                # numeroCTPS
                funcionario.serieCTPS = ''                 # serieCTPS
                funcionario.ufCTPS = ''                    # uf
                funcionario._tipo_vinculo.nome = ''        # tipo_vinculo_nome
                funcionario.nomeUsuario = ''               # nomeUsuario
                funcionario.senha = ''                     # senha
                

            elif operacao == 'SALVAR':
                status_nome = parameters.get('txt-funcionario-status', '').strip()
                # foto = parameters.get('foto-func', '').strip()
                cpf = parameters.get('cpf-func', '').strip()
                nome = parameters.get('nome-func', '').strip()
                sexo = parameters.get('sexo-func', '').strip()
                pisPasep = parameters.get('pis-pasep-func', '').strip()
                rg = parameters.get('rg-func', '').strip()
                email = parameters.get('email-func', '').strip()
                responsavelCadastro = parameters.get('reponsavel-cad-func', '').strip()
                matricula = parameters.get('matricula-func', '').strip()
                cargo_nome = parameters.get('cargo-func', '').strip()
                lotacao = parameters.get('lotacao-func', '').strip()
                unidadeDeTrabalho = parameters.get('unidade-trabalho-func', '').strip()
                numeroCTPS = parameters.get('numero-ctps-func', '').strip()
                serieCTPS = parameters.get('serie-ctps-func', '').strip()
                uf = parameters.get('uf-ctps-func', '').strip()
                tipo_vinculo_nome = parameters.get('txt-funcionario-tipo_vinvulo', '').strip()
                nomeUsuario = parameters.get('nome-usuario-func', '').strip()
                senha = parameters.get('senha-usuario-func', '').strip()
                
                funcionario._status.nome = status_nome
                funcionario.cpf = cpf
                funcionario.nome = nome
                funcionario.sexo = sexo
                funcionario.pisPasep = pisPasep
                funcionario.rg = rg
                funcionario.email = email
                funcionario.matricula = matricula
                funcionario.cargo.nome = cargo_nome
                funcionario.lotacao = lotacao
                funcionario.unidadeDeTrabalho = unidadeDeTrabalho
                funcionario.numeroCTPS = numeroCTPS
                funcionario.serieCTPS = serieCTPS
                funcionario.ufCTPS = uf
                funcionario._tipo_vinculo.nome = tipo_vinculo_nome
                funcionario.nomeUsuario = nomeUsuario
                funcionario.senha = senha

                dataAdmissao = parameters.get('data-admissao-func')
                dataNascimento = parameters.get('data-nasc-func')
                dataEmissaoCTPS = parameters.get('data-emissao-ctps-func')

                if dataAdmissao is not None:
                    funcionario.dataAdmissao = ConverteData.stringDate(dataAdmissao)
                if dataNascimento is not None:
                    funcionario.dataNascimento = ConverteData.stringDate(dataNascimento)
                if dataEmissaoCTPS is not None:
                    funcionario.dataEmissaoCTPS = ConverteData.stringDate(dataEmissaoCTPS)


            elif operacao == 'PRE-EXCLUIR':
                funcionario.id = parameters.get('funcionario_id')
            

            elif operacao == 'EXCLUIR':
                funcionario.id = parameters.get('funcionario_id')


            elif operacao == 'FILTRAR':
                funcionario_id = parameters.get('txt_funcionario_id', '').strip()
                cpf = parameters.get('cpf-func', '').strip()
                nome = parameters.get('nome-func', '').strip()
                matricula = parameters.get('matricula-func', '').strip()

                funcionario.id = funcionario_id
                funcionario.cpf = cpf
                funcionario.nome = nome
                funcionario.matricula = matricula
            
            elif operacao == 'APONTAR':
                pass
            
            elif operacao == 'CONSULTAR_ID':
                funcionario_id = parameters.get('txt_funcionario_id', '').strip()
                funcionario.id = funcionario_id

        return funcionario



    def setView(self, resultado: Resultado, request):

        if request.method == 'GET':
            parameters = request.args
        else:
            parameters = request.form

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            if operacao == 'FILTRAR':
                if current_user.is_authenticated:
                    if _verificar_msg(resultado):
                        return render_template('funcionario/funcionarios.html', resultado=resultado)
                    else:
                        return render_template('funcionario/funcionarios.html', resultado=resultado)
                else:
                    if _verificar_msg(resultado):
                        return render_template('ocorrencia/ocorrencias_funcionario.html', resultado=resultado)
                    else:
                        return render_template('ocorrencia/ocorrencias_funcionario.html', resultado=resultado)

            elif operacao == 'PRE-ATUALIZAR':
                return render_template('funcionario/funcionarioAlterar.html', resultado=resultado )
            

            elif operacao == 'ATUALIZAR':
                if _verificar_msg(resultado):
                    return render_template('funcionario/funcionarioAlterar.html', resultado=resultado)
                else: 
                    return redirect(url_for('bp_funcionario.alterar_funcionario', funcionario_id=parameters.get('funcionario_id'), operacao='PRE-ATUALIZAR'))
            

            elif operacao == 'PRE-SALVAR':
                return render_template('funcionario/funcionarioCadastrar.html', resultado=resultado)


            elif operacao == 'SALVAR':
                if _verificar_msg(resultado):
                    return render_template('funcionario/funcionarioCadastrar.html', resultado=resultado)
                return redirect(url_for('bp_funcionario.funcionarios'))
            

            elif operacao == 'PRE-EXCLUIR':
                return render_template('funcionario/funcionarioExcluir.html', resultado=resultado)
            

            elif operacao == 'EXCLUIR':
                _verificar_msg(resultado)
                return redirect(url_for('bp_funcionario.funcionarios') + '#resultado')

            elif operacao == 'APONTAR':
                if _verificar_msg(resultado):
                    return render_template('frequencia/frequencias.html', resultado=resultado)
                else:
                    return render_template('frequencia/frequencias.html', resultado=resultado)

            elif operacao == 'CONSULTAR_ID':                
                _verificar_msg(resultado)
                return render_template('solicitacao/consultar_solicitacoes.html', resultado=resultado)
        
        else:
            _verificar_msg(resultado)
            return render_template('funcionario/funcionarios.html', resultado=resultado)
