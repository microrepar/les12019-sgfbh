from app.bp_funcionario.models import Funcionario

class BancosDeHoras():
    
    def __init__(self):
        self.funcionarios = Funcionario.query.all()
    
    
class BancoDeHorasFuncionario():
    
    def __init__(self, funcionario_id):
        self.funcionario = Funcionario.query.filter_by(id=funcionario_id).first()
