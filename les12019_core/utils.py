"""Mensagens de resposta para o usuário
"""
SUCESSO_ATUALIZAR_FUNCIONARIO = 'Os dados do(a) funcionário(a) {} foram atualizados com sucesso!'
SUCESSO_SALVAR_FUNCIONARIO_BD = 'O cadastro do(a) funcionário(a) {} foi salvo com sucesso!'
SUCESSO_EXCLUIR_FUNCIONARIO = 'O cadastro do funcionário(a) {} foi excluido com sucesso!'
SUCESSO_LISTAR_TODOS = 'Foi encontrado com sucesso! o total de {} registros de {}s - Ativos, Inativos e Excluidos.'
SUCESSO_SALVAR_ENDERECO_BD = 'O endereço {} foi salvo com sucesso!'
SUCESSO_FILTRO_PARAM_FUNCIONARIO = '{} funcionário(s) encontrado(s) com sucesso! para o filtro aplicado.'
SUCESSO_ATUALIZAR_ENDERECO = 'O endereço {} foi atualizado com sucesso!'
SUCESSO_EXCLUIR_ENDERECO = 'O endereço do cep:{} foi excluido com sucesso!'
SUCESSO_SALVAR_ENTIDADE_BD = 'O objeto {}, foi salvo com sucesso!'
SUCESSO_ATUALIZAR_ENTIDADE_BD = 'O objeto {} - foi atualizado com sucesso!'
SUCESSO_EXCLUIR_ENTIDADE = 'O objeto {}, foi excluido com sucesso!'


ERRO_ATUALIZAR_FUNCIONARIO = 'Os dados do funcionário(a) {} não foram atualizados, erro inesperado no banco de dados.'
ERRO_SALVAR_FUNCIONARIO_BD = 'O cadastro do funcionário(a) {} não foi salvo, devido a falha no Banco de Dados.'
ERRO_EXCLUIR_FUNCIONARIO = 'O cadastro do funcionário(a) {} nao fou foi excluido, devido a falha no Banco de Dados.'
ERRO_LISTAR_TODOS = '{} funcionário encontrados - não há registros no banco de dados!'
ERRO_SALVAR_FUNCIONARIO_RNS = 'Os dados do funcionáro(a) {} não foram cadastrado no sistema devido a não atender a seguinte regra: '
ERRO_ATUALIZAR_ENDERECO = 'Não foi possível cadastrar o endereço {}, devido a falha ocorrida no banco de dados.'
ERRO_SALVAR_ENDERECO_BD = 'O endereço {} não foi salvo, devido a uma falha no Banco de Dados.'
ERRO_FILTRO_PARAM_FUNCIONARIO = '{} Funcionario encontrado - nenhum registro encontrado para o filtro aplicado.'
ERRO_FILTRO_PARAM_FUNCIONARIO_NONE = '{} Funcionarios encontrados - não foi inserido nenhuma valor nos campos de filtragem'
ERRO_CONSULTAR_STATUS_ENTIDADE = '{} registro de status para {} -'
ERRO_CONSULTAR_TIPO_ENTIDADE = '{} registro de tipos para {} -'
ERRO_EXECUTAR_RNS = 'Falha ao executar a seguinte regra para {}: '
ERRO_SALVAR_ENTIDADE_RNS = 'A operação salvar não pode ser executada, porque não atendeu a seguinte regra: {}'
ERRO_PRE_OPERACAO_SALVAR = 'O objeto "{}" não foi instanciado!'
ERRO_CONSULTAR_LOGRADOURO = 'Não foi encontrado nenhum logradouro com o CEP:{}'
ERRO_EXCLUIR_ENDERECO = 'O endereco do cep:{} não pode ser excluido devido a falha inesperada!'
ERRO_CONSULTA_POR_ID_ENDERECO = 'O endereco com id:{} não foi encontrado!'
ERRO_SALVAR_ENDERECO_RNS = 'O endereço {} não pode ser salvo devido não cumprir a seguinte regra: '
ERRO_CONSULTAR_TIPO_LOGRADOURO = 'Não foi encontrado nenhum tipo de logradouro cadastrado:{}'
ERRO_CONSULTA_ENTIDADE = 'Não foi encontrado nenhum registro da entidade {} no banco de dados!'
ERRO_SALVAR_ENTIDADE_BD = 'Ocorreu um erro inesperado ao tentar salvar a entidade {}'
ERRO_CONSULTA_POR_ID_ENTIDADE = 'Não foi encontrado o registro da entidade {} no banco de dados!'
ERRO_ATUALIZAR_ENTIDADE_BD = 'Devido a um erro no banco de dados o objeto {} não foi atualizado!'
ERRO_EXCLUIR_ENTIDADE = 'O objeto {} não foi excluido devido a um erro de persitência de dados!'

def get_parameters_request(request):
    if request.method == 'GET':
            parameters = request.args
    else:
        parameters = request.form
    return parameters
