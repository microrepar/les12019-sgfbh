from app import create_app, db
from app.bp_funcionario.models import Funcionario, StatusFuncionario, TipoVinculo, Cargo
from app.bp_endereco.models import Endereco, StatusEndereco, TipoEndereco, Logradouro
from app.bp_frequencia.models import EspelhoMensal, EspelhoDiario, StatusEspelho
from app.bp_escala.models import Jornada, StatusEscala, StatusJornada, Escala, Turno, AtribuicaoEscala, HorarioDia
from app.bp_ocorrencia.models import Ocorrencia, Pendencia, PeriodoOcorrencia, StatusOcorrencia, StatusPendencia, TipoPendencia
from app.bp_ponto.models import Ponto, StatusPonto, TipoPonto
from app.bp_solicitacao.models import Solicitacao, Despacho, Decisao, StatusSolicitacao, TipoSolicitacao, StatusDespacho
from app.bp_autenticacao.models import User

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Funcionario': Funcionario, 'Endereco': Endereco, 'StatusEndereco': StatusEndereco, 'TipoEndereco': TipoEndereco,
            'Logradouro': Logradouro, 'StatusFuncionario': StatusFuncionario, 'TipoVinculo': TipoVinculo, 'Cargo': Cargo, 'Jornada': Jornada, 
            'StatusEscala': StatusEscala, 'StatusJornada': StatusJornada, 'Escala': Escala, 'Turno': Turno, 'AtribuicaoEscala': AtribuicaoEscala,
            'HorarioDia': HorarioDia, 'EspelhoMensal': EspelhoMensal, 'EspelhoDiario': EspelhoDiario, 'StatusEspelho': StatusEspelho, 
            'Ocorrencia': Ocorrencia, 'Pendencia': Pendencia, 'PeriodoOcorrencia': PeriodoOcorrencia, 'StatusOcorrencia': StatusOcorrencia, 
            'StatusPendencia': StatusPendencia, 'TipoPendencia': TipoPendencia, 'Ponto': Ponto, 'StatusPonto': StatusPonto, 'TipoPonto': TipoPonto,
            'Solicitacao': Solicitacao, 'Despacho': Despacho, 'Decisao': Decisao, 'StatusSolicitacao': StatusSolicitacao, 'TipoSolicitacao': TipoSolicitacao, 
            'StatusDespacho': StatusDespacho, 'User': User,}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    
