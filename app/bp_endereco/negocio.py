from les12019_core.abstract_strategy import AbstractStrategy
from app.bp_endereco.models import Endereco, StatusEndereco, TipoEndereco, Logradouro
from les12019_core import utils
from flask import flash
from app import db
from sqlalchemy import and_, func


class ApensadorDependeciasPreOperacaoSalvarEndereco(AbstractStrategy):
    def processar(self, entidade):
        if entidade is not None:
            if isinstance(entidade, Endereco):
                endereco: Endereco=entidade

                status_endereco = StatusEndereco.query.all()
                tipo_endereco = TipoEndereco.query.all()
                tipo_logradouro = db.session.query(func.count(Logradouro.tipo_logradouro), Logradouro.tipo_logradouro).group_by(Logradouro.tipo_logradouro).all()
                
                if len(status_endereco) < 1:
                    flash(utils.ERRO_CONSULTAR_STATUS_ENTIDADE.format('0', '"Status do Enderço"') + ' Por favor cadastre primeiro os status para endereço.')
                
                if len(tipo_endereco) < 1:
                    flash(utils.ERRO_CONSULTAR_TIPO_ENTIDADE.format('0', '"Tipo de Endereço"') + ' Por favor cadastre primeiro os tipos para endereço.')
                
                if len(tipo_logradouro) < 1:
                    flash(utils.ERRO_CONSULTAR_TIPO_LOGRADOURO.format(' Por favor, entre em contado com um administrador.'))
                
                endereco._status_endereco_aux = status_endereco
                endereco._tipo_endereco_aux = tipo_endereco
                endereco._tipo_logradouro = tipo_logradouro
                
                if endereco.cep:
                    logradouro = Logradouro.query.filter(Logradouro.cep==endereco.cep.strip()).first()
                    if logradouro is not None:
                        endereco._logradouro = logradouro
                    else:
                        flash(utils.ERRO_CONSULTAR_LOGRADOURO.format(endereco.cep.strip()))
                        endereco._logradouro = Logradouro(cep='', tipo_logradouro='', logradouro='', bairro='', 
                                                          uf='', cidade='', id=None)
                else:
                    endereco._logradouro = Logradouro(cep='', tipo_logradouro='', logradouro='', bairro='', 
                                                      uf='', cidade='', id=None)
            else:
                return utils.ERRO_EXECUTAR_RNS.format('cadastro de endereço') + 'Não é possível executar, pois a entidade não é um endereço'
        else:
            return utils.ERRO_PRE_OPERACAO_SALVAR.format('Endereço')
        return None


class ValidadorCep(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Endereco):
            endereco: Endereco = entidade
            if endereco.cep is not None:
                if len(endereco.cep) != 8:
                    if endereco.cep.strip():
                        return utils.ERRO_SALVAR_ENDERECO_RNS.format('com o CEP: '+ endereco.cep) + " CEP deve conter 8 digitos!"
                    else:
                        return utils.ERRO_SALVAR_ENDERECO_RNS.format('') + " CEP deve conter 8 digitos!"
                else:
                    try:
                        int(endereco.cep.strip())
                    except:
                        return utils.ERRO_SALVAR_ENDERECO_RNS.format('com cep: ' + endereco.cep) + " Deve conter apenas números inteiros!"
        else:
            return 'CEP não pode ser válidado, pois a entidade não é um endereço!'

        return None


class ValidadorTipoLogradouro(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Endereco):
            endereco: Endereco = entidade
            if endereco._logradouro is not None:
                tipo: str= endereco._logradouro.tipo_logradouro
                count_tipo_logradouro = db.session.query(func.count(Logradouro.tipo_logradouro), Logradouro.tipo_logradouro).group_by(Logradouro.tipo_logradouro).all()
                tipos_logradouros = [t for _, t in count_tipo_logradouro]
                if endereco._logradouro.tipo_logradouro not in tipos_logradouros:
                    return utils.ERRO_SALVAR_ENDERECO_RNS.format(endereco._logradouro.tipo_logradouro) + "O tipo de logradouro informado não existe no cadastro, por favor contate um administrador"
        else:
            return 'Tipo de logradouro não pode ser válidado, pois a entidade não é um endereço!'

        return None


class ValidadorNumeroEndereco(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Endereco):
            endereco: Endereco = entidade
            if endereco.numero is None:
                return utils.ERRO_SALVAR_ENDERECO_RNS.format('com número '+ endereco.numero) + " Não pode ser nula!"
                if endereco.numero.strip() == '':
                    return utils.ERRO_SALVAR_ENDERECO_RNS.format('com número '+ endereco.numero) + "deve ser preenchido!"

            try:
                int(entidade.numero)
            except Exception:
                return utils.ERRO_SALVAR_ENDERECO_RNS.format('com número '+ endereco.numero) + " Deve conter apenas números inteiros!"

            if int(endereco.numero) < 0:
                return utils.ERRO_SALVAR_ENDERECO_RNS.format('com número ' + endereco.numero) + "Não é permitido números negativos!"

        else:
            return 'CPF não pode ser válidado, pois a entidade não é um funcionário!'

        return None


class PreencherResponsavelCadastroEndereco(AbstractStrategy):

    def processar(self, entidade: Endereco):
        if entidade is not None:
            entidade.responsavel_cadastro = 'mc_siva'  # inserir o usuário logado aqui
        else:
            return f'Entidade: {entidade.__class__.__name__.upper()} nula!'

        return None


class ValidadorDadosObrigatoriosEndereco(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Endereco):
            endereco: Endereco = entidade

            # print('>>>>>>>>>>>>>CAMPOS OBRIGATORIOS>>>>>>>>>>>>>>>>>', [endereco.cep, endereco.numero, 
            # endereco._logradouro.tipo_logradouro, endereco._logradouro.logradouro, endereco.tipo_endereco_id, endereco.status_id,
            # endereco._logradouro.bairro, endereco._logradouro.cidade, endereco._logradouro.uf])

            if not all([endereco.cep, endereco.numero, endereco._logradouro.logradouro, endereco.tipo_endereco_id, 
                        endereco._logradouro.tipo_logradouro, endereco.status_id, endereco._logradouro.bairro, 
                        endereco._logradouro.cidade, endereco._logradouro.uf]):
                return utils.ERRO_SALVAR_ENDERECO_RNS.format(endereco._logradouro.tipo_logradouro +' '+ endereco._logradouro.logradouro) + 'Todos os campos com (*) são obrigatórios e devem ser preenchidos'
        else:
            return utils.ERRO_SALVAR_ENDERECO_RNS.format(endereco._logradouro.tipo_logradouro + ' '+ endereco._logradouro.logradouro) + " Deve ser registrado um endereço!"
        return None


class VerificadorExistenciaEnderecoDuplicadoSalvar(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Endereco):
            endereco: Endereco= entidade
            if endereco.cep is not None and endereco.numero is not None:
                _endereco = Endereco.query.filter(and_(Endereco.status_id!=3 , Endereco.cep == entidade.cep.strip(), Endereco.numero == endereco.numero, Endereco.funcionario_id==entidade.funcionario_id)).first()
                if _endereco is not None:
                    return utils.ERRO_SALVAR_ENDERECO_RNS.format(endereco._logradouro.tipo_logradouro + ' ' +\
                        endereco._logradouro.logradouro) + f'O endereço com o cep:{endereco.cep} e número: {endereco.numero} já cadastrado para o funcionário {_endereco._morador.nome}'
                
        return None


class VerificadorExistenciaEnderecoDuplicadoAtualizar(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Endereco):
            endereco: Endereco= entidade
            if endereco.cep is not None and endereco.numero is not None:
                _endereco = Endereco.query.filter(and_(Endereco.status_id!=3 , Endereco.cep == entidade.cep, Endereco.numero == endereco.numero, Endereco.funcionario_id==entidade.funcionario_id)).first()
                if _endereco is not None:
                    # print('>>>>>>>>>>>>>>ATUALIZAR ENDERECO>>>>>>>>>>>>>>', type(_endereco.id), type(endereco.id))
                    if int(endereco.id) != _endereco.id:
                        return utils.ERRO_SALVAR_ENDERECO_RNS.format(endereco._logradouro.tipo_logradouro + ' ' +\
                            endereco._logradouro.logradouro) + f'O endereço com o cep:{endereco.cep} e número: {endereco.numero} já cadastrado para o funcionário {_endereco._morador.nome}'
                
        return None


class VerificadorExitenciaEndereco(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Endereco):
            endereco: Endereco= entidade
            if endereco.id is not None:
                _endereco = Endereco.query.filter(Endereco.id==endereco.id).first()
                if _endereco is None:
                    return f'O endereço com id:{endereco.id} não foi encontrado.'
                elif _endereco._status.nome == 'EXCLUIDO':                    
                    return f'O endereço { _endereco._logradouro.tipo_logradouro} { _endereco._logradouro.logradouro  }, do funcionário {_endereco._morador.nome} já foi excluido!'
                
            return None
        else:
            return f'Entidade: {entidade.__class__.__name__.upper()} nula!'
