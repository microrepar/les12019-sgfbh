import sys
import csv
import json
from pathlib import Path, PurePath
from shutil import copyfile, copytree, copy
from app import create_app, db
from app.bp_funcionario.models import Funcionario, StatusFuncionario, TipoVinculo, Cargo, PadraoSalario
from app.bp_endereco.models import Endereco, Logradouro, StatusEndereco, TipoEndereco
from app.bp_frequencia.models import EspelhoMensal, EspelhoDiario, StatusEspelho
from app.bp_escala.models import Jornada, Escala, Turno, HorarioDia, AtribuicaoEscala, StatusJornada, StatusEscala
from app.bp_ocorrencia.models import Ocorrencia, Pendencia, PeriodoOcorrencia, StatusOcorrencia, StatusPendencia, TipoPendencia
from app.bp_ponto.models import Ponto, StatusPonto, TipoPonto
from app.bp_solicitacao.models import Solicitacao, Despacho, Decisao, StatusSolicitacao, TipoSolicitacao, StatusDespacho
from les12019_core.aplicacao import ConverteData, ConverteHora
from les12019_core import utils
import datetime
from sqlalchemy import and_
from app import db


class NumberArgumentsError(Exception):
    pass

tablesnames = {
    Funcionario.__tablename__.upper(): Funcionario,
    StatusFuncionario.__tablename__.upper(): StatusFuncionario,
    TipoVinculo.__tablename__.upper(): TipoVinculo,    
    Cargo.__tablename__.upper(): Cargo,
    PadraoSalario.__tablename__.upper(): PadraoSalario,
    
    Endereco.__tablename__.upper(): Endereco,
    StatusEndereco.__tablename__.upper(): StatusEndereco,
    Logradouro.__tablename__.upper(): Logradouro,
    TipoEndereco.__tablename__.upper(): TipoEndereco,
    
    EspelhoMensal.__tablename__.upper(): EspelhoMensal,
    EspelhoDiario.__tablename__.upper(): EspelhoDiario,
    StatusEspelho.__tablename__.upper(): StatusEspelho,
    
    Jornada.__tablename__.upper(): Jornada,
    Escala.__tablename__.upper(): Escala,
    Turno.__tablename__.upper(): Turno,
    HorarioDia.__tablename__.upper(): HorarioDia,
    AtribuicaoEscala.__tablename__.upper(): AtribuicaoEscala,
    StatusJornada.__tablename__.upper(): StatusJornada,
    StatusEscala.__tablename__.upper(): StatusEscala,

    Ocorrencia.__tablename__.upper(): Ocorrencia,
    Pendencia.__tablename__.upper(): Pendencia,
    PeriodoOcorrencia.__tablename__.upper(): PeriodoOcorrencia,
    StatusOcorrencia.__tablename__.upper(): StatusOcorrencia,
    StatusPendencia.__tablename__.upper(): StatusPendencia,
    TipoPendencia.__tablename__.upper(): TipoPendencia,

    Ponto.__tablename__.upper(): Ponto,
    StatusPonto.__tablename__.upper(): StatusPonto,
    TipoPonto.__tablename__.upper(): TipoPonto,
       
    Solicitacao.__tablename__.upper(): Solicitacao,
    Despacho.__tablename__.upper(): Despacho,
    Decisao.__tablename__.upper(): Decisao,
    StatusSolicitacao.__tablename__.upper(): StatusSolicitacao,
    TipoSolicitacao.__tablename__.upper(): TipoSolicitacao,
    StatusDespacho.__tablename__.upper(): StatusDespacho,
}    


app = create_app()
app.app_context().push()


def _load_db(tablename, list_tables: list) -> list:
    
    if tablename == 'tb_logradouro':
        for table in list_tables:
            COLUMNS = dict()
            for i, row in enumerate(table):
                print('>>>>>>>>>', row)
            
                if i < 1:
                    COLUMNS = dict(zip(map(str.lower, row), range(len(row))))
                    print(COLUMNS)
                    continue 

                if i % 50000 == 0:
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        raise e

                nm_logradouro = row[COLUMNS.get('logradouro')]

                logradouro = Logradouro(
                    cep=row[COLUMNS.get('cep')],
                    uf=row[COLUMNS.get('uf')],
                    cidade=row[COLUMNS.get('cidade')],
                    bairro=row[COLUMNS.get('bairro')],
                    tipo_logradouro=nm_logradouro.split()[0],
                    logradouro=' '.join(nm_logradouro.split()[1:])
                )
                db.session.add(logradouro)
            db.session.commit()
        return len(Logradouro.query.all())
    
    elif tablename == 'tb_tipo_endereco':
        for table in list_tables:
            COLUMNS = dict()
            for i, row in enumerate(table):
                print('>>>>>>>>>', row)

                if i < 1:
                    COLUMNS = dict(zip(map(str.lower, row), range(len(row))))
                    print(COLUMNS)
                    continue

                if i == 3:
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        raise e

                tp_endereco = TipoEndereco(
                    nome=row[COLUMNS.get('nome')],
                    descricao=row[COLUMNS.get('descricao')],
                )
                db.session.add(tp_endereco)
            db.session.commit()
        return len(TipoEndereco.query.all())
    
    elif tablename == 'tb_status_endereco':
        for table in list_tables:
            COLUMNS = dict()
            for i, row in enumerate(table):
                print('>>>>>>>>>', row)

                if i < 1:
                    COLUMNS = dict(zip(map(str.lower, row), range(len(row))))
                    print(COLUMNS)
                    continue

                if i == 3:
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        raise e

                status_endereco = StatusEndereco(
                    nome=row[COLUMNS.get('nome')],
                    descricao=row[COLUMNS.get('descricao')],
                )
                db.session.add(status_endereco)
            db.session.commit()
        return len(StatusEndereco.query.all())
    
    elif tablename == 'tb_status_funcionario':
        for table in list_tables:
            COLUMNS = dict()
            for i, row in enumerate(table):
                print('>>>>>>>>>', row)

                if i < 1:
                    COLUMNS = dict(zip(map(str.lower, row), range(len(row))))
                    print(COLUMNS)
                    continue

                if i == 3:
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        raise e

                entidade = StatusFuncionario(
                    nome=row[COLUMNS.get('nome')],
                    codigo=row[COLUMNS.get('codigo')],
                    descricao=row[COLUMNS.get('descricao')],
                )
                db.session.add(entidade)
            db.session.commit()
        return len(StatusFuncionario.query.all())
    
    elif tablename == 'tb_tipo_vinculo':
        for table in list_tables:
            COLUMNS = dict()
            for i, row in enumerate(table):
                print('>>>>>>>>>', row)

                if i < 1:
                    COLUMNS = dict(zip(map(str.lower, row), range(len(row))))
                    print(COLUMNS)
                    continue

                if i == 3:
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        raise e

                entidade = TipoVinculo(
                    nome=row[COLUMNS.get('nome')],
                    codigo=row[COLUMNS.get('codigo')],
                    descricao=row[COLUMNS.get('descricao')],
                )
                db.session.add(entidade)
            db.session.commit()
        return len(TipoVinculo.query.all())
    
    elif tablename == 'tb_cargo':
        for table in list_tables:
            COLUMNS = dict()
            for i, row in enumerate(table):
                print('>>>>>>>>>', row)

                if i < 1:
                    COLUMNS = dict(zip(map(str.lower, row), range(len(row))))
                    print(COLUMNS)
                    continue

                if i == 3:
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        raise e

                entidade = Cargo(
                    nome=row[COLUMNS.get('nome')],
                    codigo=row[COLUMNS.get('codigo')],
                    atribuicoes=row[COLUMNS.get('atribuicoes')],
                )
                db.session.add(entidade)
            db.session.commit()
        return len(Cargo.query.all())

    elif tablename == 'tb_funcionario':
        for table in list_tables:
            COLUMNS = dict()
            for i, row in enumerate(table):
                print('>>>>>>>>>', row)

                if i< 1:
                    COLUMNS = dict(zip(row, range(len(row))))
                    print(COLUMNS)
                    continue

                funcionario = Funcionario(
                    id=row[COLUMNS.get('id')],
                    cpf=row[COLUMNS.get('cpf')],
                    rg=row[COLUMNS.get('rg')],
                    nome=row[COLUMNS.get('nome')],
                    sexo=row[COLUMNS.get('sexo')],
                    dataNascimento=datetime.datetime.strptime(row[COLUMNS.get('dataNascimento')], '%d/%m/%Y'),
                    pisPasep=row[COLUMNS.get('pisPasep')],
                    email=row[COLUMNS.get('email')],
                    responsavelCadastro=row[COLUMNS.get('responsavelCadastro')],
                    matricula=row[COLUMNS.get('matricula')],
                    dataAdmissao=datetime.datetime.strptime(row[COLUMNS.get('dataAdmissao')], '%d/%m/%Y'),
                    dataCadastro=datetime.datetime.strptime(row[COLUMNS.get('dataCadastro')], '%d/%m/%Y'),
                    lotacao=row[COLUMNS.get('lotacao')],
                    unidadeDeTrabalho=row[COLUMNS.get('unidadeDeTrabalho')],
                    numeroCTPS=row[COLUMNS.get('numeroCTPS')],
                    serieCTPS=row[COLUMNS.get('serieCTPS')],
                    ufCTPS=row[COLUMNS.get('ufCTPS')],
                    dataEmissaoCTPS=datetime.datetime.strptime(row[COLUMNS.get('dataEmissaoCTPS')], '%d/%m/%Y'),
                    nomeUsuario=row[COLUMNS.get('nomeUsuario')],
                    senha=row[COLUMNS.get('senha')],
                    status_id=row[COLUMNS.get('status_id')],
                    tipo_vinculo_id=row[COLUMNS.get('tipo_vinculo_id')],
                    cargo_id=row[COLUMNS.get('cargo_id')]
                )
                db.session.add(funcionario)
            try:
                db.session.commit()
                
            except Exception as e:
                print(str(e))
                db.session.rollback()
        return len(Funcionario.query.all())


    elif tablename == 'tb_ponto':
        start_time = datetime.datetime.now()
        _formato_data = '%d/%m/%Y'        

        for table in list_tables:

            pontos_visitados = [False] * len(table)
            COLUMNS = dict()

            status_ponto = StatusPonto.query.filter_by(id=2).first()
            if status_ponto is None:
                return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Status de ponto')

            status_espelho = StatusEspelho.query.filter_by(id=1).first()
            if status_espelho is None:
                return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Status de espelhos de ponto')

            for i, row in enumerate(table):

                if i < 1 :
                    COLUMNS = dict(zip(row, range(len(row))))
                    print(COLUMNS)
                    continue
                elif pontos_visitados[i]:
                    continue

                funcionario: Funcionario = Funcionario.query.filter(Funcionario.pisPasep == row[COLUMNS.get('pispasep')]).first()
                if funcionario is None:
                    print('funcionario do pispasep={} não encontrado!'.format(row[COLUMNS.get('pispasep')]))
                    pontos_visitados[i] = True
                    continue

                for j in range(i, len(table[i:]) + 1):

                    if table[j][COLUMNS.get('pispasep')] == funcionario.pisPasep:
                        
                        if pontos_visitados[j]:
                            continue    
                        else:                        
                            pontos_visitados[j] = True                    

                        print('>>>>table[j] PONTO {}>>>>>'.format(i), table[j])
                        ponto = Ponto(
                            numero_seq_ponto=table[j][COLUMNS.get('numero_seq_ponto')],
                            tipo_ponto=table[j][COLUMNS.get('tipo_ponto')],
                            data_hora= datetime.datetime.strptime(table[j][COLUMNS.get('data')]+' '+table[j][COLUMNS.get('hora')], '%d%m%Y %H%M'),
                            pispasep=table[j][COLUMNS.get('pispasep')],
                            digito_pispasep=table[j][COLUMNS.get('digito_pispasep')],
                            relogio='R156',
                            responsavel_cadastro='sistema',
                            observacao='teste popular banco a partir dos pontos.',
                            matricula=funcionario.matricula,
                            funcionario=funcionario,
                            status=status_ponto
                        )

                        espelho_diario = EspelhoDiario.query.filter(and_(
                            EspelhoDiario.dia_referencia == ponto.data_hora.day,
                            EspelhoDiario.mes_referencia == ponto.data_hora.month,
                            EspelhoDiario.ano_referencia == ponto.data_hora.year,
                            EspelhoDiario.funcionario_id == ponto.funcionario.id
                        )).first()

                        if espelho_diario is None:                        
                            um_dia = datetime.timedelta(days=1)
                            hoje = datetime.datetime.now()
                            mes_atual = ponto.data_hora.month
                            ano_atual = ponto.data_hora.year

                            mes_anterior = mes_atual - 1 if mes_atual > 1 else 12
                            ano_mes_anterior = ano_atual - 1 if mes_anterior == 12 else ano_atual

                            mes_posterior = mes_atual + 1 if mes_atual < 12 else 1
                            ano_mes_posterior = ano_atual + 1 if mes_posterior == 1 else ano_atual

                            if ponto.data_hora.day < 16:
                                data_inicio = datetime.datetime.strptime(f'16/{mes_anterior}/{ano_mes_anterior:0>2}', _formato_data)
                                data_fim = datetime.datetime.strptime(f'15/{mes_atual}/{ano_atual}', _formato_data)
                            else:
                                data_inicio = datetime.datetime.strptime(f'16/{mes_atual}/{ano_atual}', _formato_data)
                                data_fim = datetime.datetime.strptime(f'15/{mes_posterior}/{ano_mes_posterior:0>2}', _formato_data)                        

                            espelho_mensal = EspelhoMensal.query.filter(and_(
                                EspelhoMensal.data_inicio == data_inicio,
                                EspelhoMensal.data_fim == data_fim,
                                EspelhoMensal.funcionario_id == funcionario.id
                            )).first()

                            if espelho_mensal is None:
                                espelho_mensal = EspelhoMensal(responsavel_cadastro='sistema')
                                espelho_mensal.mes_referencia = data_inicio.month
                                espelho_mensal.ano_referencia = data_inicio.year
                                espelho_mensal.data_inicio = data_inicio
                                espelho_mensal.data_fim = data_fim
                                espelho_mensal.data_cadastro = hoje
                                espelho_mensal.observacao = 'teste popular banco a partir dos pontos.'
                                espelho_mensal.funcionario = funcionario
                                espelho_mensal.status = status_espelho

                                dia_frequencia_iterador: datetime.datetime = espelho_mensal.data_inicio

                                while dia_frequencia_iterador <= espelho_mensal.data_fim:
                                    print('>>>>>>>>>>>>>ESPELHO DIARIO>>>>>>>>>>>>>',dia_frequencia_iterador, espelho_mensal.data_fim)
                                    espelho_dia = EspelhoDiario(data_cadastro=hoje, responsavel_cadastro='sistema')
                                    espelho_dia.data = dia_frequencia_iterador
                                    espelho_dia.autopreencher_dados_data()
                                    espelho_dia.observacao = 'teste popular banco a partir dos pontos.'

                                    espelho_dia.status = status_espelho
                                    espelho_dia.funcionario = funcionario

                                    espelho_mensal.espelhos_diarios.append(espelho_dia)

                                    dia_frequencia_iterador += um_dia

                                db.session.add(espelho_mensal)
                                db.session.commit()

                                espelho_diario = EspelhoDiario.query.filter(and_(
                                    EspelhoDiario.dia_referencia == ponto.data_hora.day,
                                    EspelhoDiario.mes_referencia == ponto.data_hora.month,
                                    EspelhoDiario.ano_referencia == ponto.data_hora.year,
                                    EspelhoDiario.funcionario_id == ponto.funcionario.id
                                )).first()

                            if espelho_diario is not None:
                                ponto.espelho_diario = espelho_diario
                            else:
                                print('>>>>>>>ESPELHO DIARIO NONE>>>>>>>>', ponto, funcionario)
                                input('Para continuar <ENTER>')
                        else:
                            ponto.espelho_diario = espelho_diario

                try:
                    db.session.commit()
                except Exception as e:
                    print(str(e))
                    db.session.rollback()                
        end_time = datetime.datetime.now()
        tempo_total: datetime.timedelta = end_time - start_time
        print('TEMPO TOTAL CAD PONTOS', '{}minutos e {} segundos'.format(tempo_total.seconds // 60, tempo_total.seconds % 60) )
        return len(Ponto.query.all())


    # elif tablename == 'tb_ponto':

    #     _formato_data = '%d/%m/%Y'        

    #     for table in list_tables:
    #         COLUMNS = dict()
    #         for i, row in enumerate(table):
    #             print('>>>>>>>>>', row)

    #             if i < 1:
    #                 COLUMNS = dict(zip(row, range(len(row))))
    #                 print(COLUMNS)
    #                 continue
                
    #             ponto = Ponto(
    #                 numero_seq_ponto=row[COLUMNS.get('numero_seq_ponto')],
    #                 tipo_ponto=row[COLUMNS.get('tipo_ponto')],
    #                 data_hora= datetime.datetime.strptime(row[COLUMNS.get('data')]+' '+row[COLUMNS.get('hora')], '%d%m%Y %H%M'),
    #                 pispasep=row[COLUMNS.get('pispasep')],
    #                 digito_pispasep=row[COLUMNS.get('digito_pispasep')],
    #                 relogio='R156',
    #                 responsavel_cadastro='sistema',
    #                 observacao='teste popular banco a partir dos pontos.',
    #             )                

    #             funcionario = Funcionario.query.filter(Funcionario.pisPasep == ponto.pispasep).first()
    #             if funcionario is None:
    #                 print('funcionario do pispasep={} não encontrado!'.format(ponto.pispasep))
    #                 continue

    #             status_ponto = StatusPonto.query.filter_by(id=2).first()
    #             if status_ponto is None:
    #                 return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Status de ponto')

    #             ponto.matricula = funcionario.matricula
    #             ponto.funcionario = funcionario
    #             ponto.status = status_ponto

    #             db.session.add(ponto)
    #             if i % 1000 == 0:
    #                 db.session.commit()

    #     try:
    #         db.session.commit()
    #     except Exception as e:
    #         print(str(e))
    #         db.session.rollback()
    #     else:
    #         pontos = [p for p in Ponto.query.all() if ponto.espelho_diario_id is None]
    #         print('Total de pontos fora do espelho_diario: {}'.format(len(pontos)))
    #         contador = 0
            
    #         for i, ponto in enumerate(pontos):
    #             ponto: Ponto = ponto
    #             funcionario: Funcionario = ponto.funcionario

    #             print('>>>>>>>>PONTO>>>>>>>>', ponto)

    #             espelho_diario = EspelhoDiario.query.filter(and_(
    #                 EspelhoDiario.dia_referencia == ponto.data_hora.day,
    #                 EspelhoDiario.mes_referencia == ponto.data_hora.month,
    #                 EspelhoDiario.ano_referencia == ponto.data_hora.year,
    #                 EspelhoDiario.funcionario_id == ponto.funcionario.id
    #             )).first()

    #             if espelho_diario is not None:
    #                 ponto.espelho_diario = espelho_diario
    #                 contador += 1
    #             else:
    #                 um_dia = datetime.timedelta(days=1)
    #                 hoje = datetime.datetime.now()
    #                 mes_atual = ponto.data_hora.month
    #                 ano_atual = ponto.data_hora.year

    #                 mes_anterior = mes_atual - 1 if mes_atual > 1 else 12
    #                 ano_mes_anterior = ano_atual - 1 if mes_anterior == 12 else ano_atual

    #                 mes_posterior = mes_atual + 1 if mes_atual < 12 else 1
    #                 ano_mes_posterior = ano_atual + 1 if mes_posterior == 1 else ano_atual

    #                 if ponto.data_hora.day < 16:
    #                     data_inicio = datetime.datetime.strptime(f'16/{mes_anterior}/{ano_mes_anterior:0>2}', _formato_data)
    #                     data_fim = datetime.datetime.strptime(f'15/{mes_atual}/{ano_atual}', _formato_data)
    #                 else:
    #                     data_inicio = datetime.datetime.strptime(f'16/{mes_atual}/{ano_atual}', _formato_data)
    #                     data_fim = datetime.datetime.strptime(f'15/{mes_posterior}/{ano_mes_posterior:0>2}', _formato_data)

    #                 status = StatusEspelho.query.filter_by(id=1).first()
    #                 if status is None:
    #                     return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Status de espelhos de ponto')

    #                 espelho_mensal = EspelhoMensal.query.filter(and_(
    #                     EspelhoMensal.data_inicio == data_inicio,
    #                     EspelhoMensal.data_fim == data_fim,
    #                     EspelhoMensal.funcionario_id == funcionario.id
    #                 )).first()

    #                 if espelho_mensal is None:
    #                     espelho_mensal = EspelhoMensal(responsavel_cadastro='sistema')
    #                     espelho_mensal.mes_referencia = data_inicio.month
    #                     espelho_mensal.ano_referencia = data_inicio.year
    #                     espelho_mensal.data_inicio = data_inicio
    #                     espelho_mensal.data_fim = data_fim
    #                     espelho_mensal.data_cadastro = hoje
    #                     espelho_mensal.observacao = 'teste popular banco a partir dos pontos.'
    #                     espelho_mensal.funcionario = funcionario
    #                     espelho_mensal.status = status

    #                     dia_frequencia_iterador: datetime.datetime = espelho_mensal.data_inicio

    #                     while dia_frequencia_iterador <= espelho_mensal.data_fim:
    #                         print('>>>>>>>>>>>>>ESPELHO DIARIO>>>>>>>>>>>>>',dia_frequencia_iterador, espelho_mensal.data_fim)
    #                         espelho_dia = EspelhoDiario(data_cadastro=hoje, responsavel_cadastro='sistema')
    #                         espelho_dia.data = dia_frequencia_iterador
    #                         espelho_dia.autopreencher_dados_data()
    #                         espelho_dia.observacao = 'teste popular banco a partir dos pontos.'

    #                         espelho_dia.status = status
    #                         espelho_dia.funcionario = funcionario

    #                         espelho_mensal.espelhos_diarios.append(espelho_dia)

    #                         dia_frequencia_iterador += um_dia

    #                     db.session.add(espelho_mensal)
    #                     db.session.commit()

    #                 espelho_diario = EspelhoDiario.query.filter(and_(
    #                     EspelhoDiario.dia_referencia == ponto.data_hora.day,
    #                     EspelhoDiario.mes_referencia == ponto.data_hora.month,
    #                     EspelhoDiario.ano_referencia == ponto.data_hora.year,
    #                     EspelhoDiario.funcionario_id == ponto.funcionario.id
    #                 )).first()

    #                 if espelho_diario is not None:
    #                     contador += 1
    #                     ponto.espelho_diario = espelho_diario
    #                 else:                        
    #                     print('>>>>>>>ESPELHO DIARIO NONE>>>>>>>>', ponto, funcionario)
    #                     input('Para continuar <ENTER>')

    #             if i % 1000 == 0:
    #                 try:
    #                     db.session.commit()
    #                 except Exception as e:
    #                     print(str(e))
    #                     db.session.rollback()
    #         try:
    #             db.session.commit()
    #         except Exception as e:
    #             print(str(e))
    #             db.session.rollback()

    #         print('Total de pontos inseridos no espelho_diario: {}'.format(contador))
                


def _list_path_files(tablename, path_files: str) -> list:
    path = Path(path_files)
    list_path = [p for p in path.glob(f'{tablename}.csv')]
    return list_path


def _read_files(path: Path) -> list:
    with path.open(encoding='utf-8') as csvfile:
        filereader = csv.reader(csvfile, delimiter=';')
        return list(filereader)


def load(tablename, path):    
    path_files_csv = _list_path_files(tablename, path)
    print('>>>>>>>>>>>>>>LIST PATH', path_files_csv)

    list_rows_str = list(map(_read_files, path_files_csv))
    
    return _load_db(tablename, list_rows_str)


if __name__ == "__main__":
    
    if len(sys.argv) == 3:
        tablename = sys.argv[1]
        path  = sys.argv[2]        
        if tablename.upper() in tablesnames:
            print(load(tablename, path), f'registros na tabela {tablename}')
    else:
        tablename = 'tb_ponto'
        path = r"E:\04-FATEC-1_SEM_2019\Profº. Rodrigo\LES_1SEM_2019\PROJETO_LES12019_SGFBH\DIAGRAMAS_MODELOS\BANCO_DE_DADOS"
        load(tablename, path)
        raise NumberArgumentsError(str('A quantidade de argumentos é diferente de 2... Por favor informe o NOME da tabela e o ENDEREÇO do arquivo separados por espaço' ))
    

