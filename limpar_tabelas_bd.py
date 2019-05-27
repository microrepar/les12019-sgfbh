from app import create_app, db
from app.bp_funcionario.models import Funcionario, StatusFuncionario, TipoVinculo
from app.bp_endereco.models import Endereco, TipoEndereco, StatusEndereco, Logradouro
from app.bp_frequencia.models import EspelhoMensal, EspelhoDiario, StatusEspelho
from app.bp_ponto.models import Ponto

import sys

tablesnames = {
    Funcionario.__tablename__.upper(): Funcionario,
    StatusFuncionario.__tablename__.upper(): StatusFuncionario,
    TipoVinculo.__tablename__.upper(): TipoVinculo,
    Endereco.__tablename__.upper(): Endereco,
    TipoEndereco.__tablename__.upper(): TipoEndereco,
    StatusEndereco.__tablename__.upper(): StatusEndereco,
    Logradouro.__tablename__.upper(): Logradouro,
    EspelhoMensal.__tablename__.upper(): EspelhoMensal,
    EspelhoDiario.__tablename__.upper(): EspelhoDiario,
    StatusEspelho.__tablename__.upper(): StatusEspelho,
    Ponto.__tablename__.upper(): Ponto,
}

app = create_app()
app.app_context().push()

def limpar_funcionarios_test(matricula=1):
    funcionarios = Funcionario.query.filter(Funcionario.status_id == '3').all()
    count = 0
    for f in funcionarios:
        if f.matricula >= matricula:
            db.session.delete(f)
            count += 1
    db.session.commit()
    print(f'{count} registros excluidos permanentemente!')


def limpar_tudo_funcionarios_test(tablename_list):
    for tablename in tablename_list:
        repositorio = tablesnames.get(tablename.upper())
        if repositorio is not None:
            registros = repositorio.query.all()
            count = 0
            for registro in registros:
                db.session.delete(registro)
                count += 1
            db.session.commit()
            print(f'{count} registros da tabela {repositorio.__tablename__} foram excluidos permanentemente!')
        

    
if __name__ == "__main__":

    if len(sys.argv) > 1:
        try:            
            matricula = int(sys.argv[1])
            limpar_funcionarios_test(matricula)
        except Exception:
            tablename_list = sys.argv[1:]
            limpar_tudo_funcionarios_test(tablename_list)
    else:
        limpar_funcionarios_test()


    
