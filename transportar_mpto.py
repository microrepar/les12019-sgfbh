

    elif tablename == 'tb_ponto':

        _formato_data = '%d/%m/%Y'        

        for table in list_tables:

            pontos_visitados = [None] * len(table)
            COLUMNS = dict()

            status_ponto = StatusPonto.query.filter_by(id=2).first()
            if status_ponto is None:
                return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Status de ponto')

            status_espelho = StatusEspelho.query.filter_by(id=1).first()
            if status is None:
                return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Status de espelhos de ponto')

            for i, row in enumerate(table):
                print('>>>>ROW>>>>>', row)

                if i < 1 :
                    pontos_visitados = True
                    COLUMNS = dict(zip(row, range(len(row))))
                    print(COLUMNS)
                    continue
                
                if pontos_visitados[i]:
                    continue

                funcionario = Funcionario.query.filter(Funcionario.pisPasep == row[COLUMNS.get('pispasep')]).first()
                if funcionario is not None:
                    print('funcionario do pispasep={} não encontrado!'.format(ponto.pispasep))
                    continue

                for row_ponto in table[i:]:

                    if pontos_visitados:
                        continue
                    
                    elif row_ponto[COLUMNS.get('pispasep')] != funcionario.pisPasep:
                        continue
                    else:
                        pontos_visitados = True
                    
                    ponto = Ponto(
                        numero_seq_ponto=row_ponto[COLUMNS.get('numero_seq_ponto')],
                        tipo_ponto=row_ponto[COLUMNS.get('tipo_ponto')],
                        data_hora= datetime.datetime.strptime(row_ponto[COLUMNS.get('data')]+' '+row_ponto[COLUMNS.get('hora')], '%d%m%Y %H%M'),
                        pispasep=row_ponto[COLUMNS.get('pispasep')],
                        digito_pispasep=row_ponto[COLUMNS.get('digito_pispasep')],
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

                    if espelho_diario is not None:
                        ponto.espelho_diario = espelho_diario
                        # contador += 1
                    else:
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
                            # contador += 1
                            ponto.espelho_diario = espelho_diario
                        else:
                            print('>>>>>>>ESPELHO DIARIO NONE>>>>>>>>', ponto, funcionario)
                            input('Para continuar <ENTER>')

                try:
                    db.session.commit()
                except Exception as e:
                    print(str(e))
                    db.session.rollback()

                


