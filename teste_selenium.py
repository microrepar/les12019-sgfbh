import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
import time


funcionarios = [
    ('111.222.333-45', 'maria das dores',   '50001',  'feminino'), 
    ('211.222.333-45', 'josé das coves',    '50002',  'masculino'), 
    ('311.222.333-45', 'Sandro Heleno',     '50003',  'masculino'),
    ('411.222.333-45', 'chuck norris',      '50004',  'masculino')
]

class CrudFuncionarioTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()
        # limparteste.limpar_funcionarios_test()
        

    def test_cadastrar_funcionario(self):
        driver = self.driver
        driver.get(r'http://localhost:5000/cadastroDeFuncionario')
        for cpf, nome, matricula, genero in funcionarios[0:1]:
            self.assertIn('SGF - Banco de Horas', driver.title)
            bt_adicionar = self.driver.find_element_by_id('id_novo_funcionario')
            bt_adicionar.click()
            assert 'Cadastro de Funcionário' in driver.page_source
            driver.find_element_by_id('id-matricula-func').send_keys(matricula)
            Select(driver.find_element_by_id('txt-funcionario-status')).select_by_value('ATIVO')
            driver.find_element_by_id('id-cpf-funcionario').send_keys(cpf)
            driver.find_element_by_id('id-nome-funcionario').send_keys(nome)
            sgenero = Select(driver.find_element_by_id('id-sexo-func'))
            sgenero.select_by_value(genero)
            driver.find_element_by_id('id-data-nasc-func').send_keys('22/5/1985')
            driver.find_element_by_id('id-pis-func').send_keys('33311122244')
            driver.find_element_by_id('rg-func').send_keys('32.654.987-1')
            driver.find_element_by_id('id-email-func').send_keys('exemplo@email.com.br')
            driver.find_element_by_id('id-cargo-func').send_keys('engenheiro de software')
            driver.find_element_by_id('id-data-admissao-func').send_keys('10/01/2019')
            driver.find_element_by_id('id-lotacao-func').send_keys('departamento de ti')
            driver.find_element_by_id('id-unidade-trabalho-func').send_keys('laboratório de engenharia de software')
            driver.find_element_by_id('id-numero-ctps-func').send_keys('12345')
            driver.find_element_by_id('serie-ctps-func').send_keys('123')
            driver.find_element_by_id('id-uf-ctps-func').send_keys('sp')
            driver.find_element_by_id('id-data-emissao-ctps-func').send_keys('05/3/2017')
            stipo_vinculo = Select(driver.find_element_by_id('txt-funcionario-tipo_vinvulo'))
            stipo_vinculo.select_by_value('CELETISTA')
            driver.find_element_by_id('id-nome-usuario-func').send_keys('g_jones')
            driver.find_element_by_id('id-senha-usuario-func').send_keys('123fatec')
            btn_salvar = driver.find_element_by_id('id-salvar-func')
            btn_salvar.click()
            time.sleep(2)
            for i in range(0,600,1):
                driver.execute_script(f'window.scrollTo(0, {i});')
                # time.sleep(1)
            time.sleep(3)
            assert f'{nome.upper()} foi salvo com sucesso!' in driver.page_source

    def test_consultar_funcionario(self):
        driver = self.driver
        driver.get(r'http://localhost:5000/funcionarios')
        for cpf, nome, matricula, genero in funcionarios[1:2]:
            self.assertIn('SGF - Banco de Horas', driver.title)
            bt_adicionar = self.driver.find_element_by_id('id_novo_funcionario')
            bt_adicionar.click()
            assert 'Cadastro de Funcionário' in driver.page_source
            driver.find_element_by_id('id-matricula-func').send_keys(matricula)
            Select(driver.find_element_by_id('txt-funcionario-status')).select_by_value('ATIVO')
            driver.find_element_by_id('id-cpf-funcionario').send_keys(cpf)
            driver.find_element_by_id('id-nome-funcionario').send_keys(nome)
            sgenero = Select(driver.find_element_by_id('id-sexo-func'))
            sgenero.select_by_value(genero)
            driver.find_element_by_id('id-data-nasc-func').send_keys('22/5/1985')
            driver.find_element_by_id('id-pis-func').send_keys('33311122244')
            driver.find_element_by_id('rg-func').send_keys('32.654.987-1')
            driver.find_element_by_id('id-email-func').send_keys('exemplo@email.com.br')
            driver.find_element_by_id('id-cargo-func').send_keys('engenheiro de software')
            driver.find_element_by_id('id-data-admissao-func').send_keys('10/01/2019')
            driver.find_element_by_id('id-lotacao-func').send_keys('departamento de ti')
            driver.find_element_by_id('id-unidade-trabalho-func').send_keys('laboratório de engenharia de software')
            driver.find_element_by_id('id-numero-ctps-func').send_keys('12345')
            driver.find_element_by_id('serie-ctps-func').send_keys('123')
            driver.find_element_by_id('id-uf-ctps-func').send_keys('sp')
            driver.find_element_by_id('id-data-emissao-ctps-func').send_keys('05/3/2017')
            stipo_vinculo = Select(driver.find_element_by_id('txt-funcionario-tipo_vinvulo'))
            stipo_vinculo.select_by_value('CELETISTA')
            driver.find_element_by_id('id-nome-usuario-func').send_keys('g_jones')
            driver.find_element_by_id('id-senha-usuario-func').send_keys('123fatec')
            btn_salvar = driver.find_element_by_id('id-salvar-func')
            btn_salvar.click()
            assert f'{nome.upper()} foi salvo com sucesso!' in driver.page_source
        time.sleep(3)
        for i in range(0, 600, 1):
            driver.execute_script(f'window.scrollTo(0, {i});')
            # time.sleep(1)
        time.sleep(3)        
        driver.find_element_by_id('id-numero-matricula').send_keys(matricula)
        time.sleep(2)
        driver.find_element_by_id('id-btn-filtrar').click()
        time.sleep(1)
        assert '1 funcionário(s) encontrado(s) com sucesso! para o filtro aplicado.' in driver.page_source
        for i in range(0,600,1):
            driver.execute_script(f'window.scrollTo(0, {i});')
            # time.sleep(1)
        time.sleep(4)
        driver.find_element_by_id('limpar-filtros').click()
        time.sleep(2)

    
    def test_atualizar_funcionario(self):
        driver = self.driver
        driver.get(r'http://localhost:5000/funcionarios')
        for cpf, nome, matricula, genero in funcionarios[2:3]:
            self.assertIn('SGF - Banco de Horas', driver.title)
            bt_adicionar = self.driver.find_element_by_id('id_novo_funcionario')
            bt_adicionar.click()
            assert 'Cadastro de Funcionário' in driver.page_source
            driver.find_element_by_id('id-matricula-func').send_keys(matricula)
            Select(driver.find_element_by_id('txt-funcionario-status')).select_by_value('ATIVO')
            driver.find_element_by_id('id-cpf-funcionario').send_keys(cpf)
            driver.find_element_by_id('id-nome-funcionario').send_keys(nome)
            sgenero = Select(driver.find_element_by_id('id-sexo-func'))
            sgenero.select_by_value(genero)
            driver.find_element_by_id('id-data-nasc-func').send_keys('22/5/1985')
            driver.find_element_by_id('id-pis-func').send_keys('33311122244')
            driver.find_element_by_id('rg-func').send_keys('32.654.987-1')
            driver.find_element_by_id('id-email-func').send_keys('exemplo@email.com.br')
            driver.find_element_by_id('id-cargo-func').send_keys('engenheiro de software')
            driver.find_element_by_id('id-data-admissao-func').send_keys('10/01/2019')
            driver.find_element_by_id('id-lotacao-func').send_keys('departamento de ti')
            driver.find_element_by_id('id-unidade-trabalho-func').send_keys('laboratório de engenharia de software')
            driver.find_element_by_id('id-numero-ctps-func').send_keys('12345')
            driver.find_element_by_id('serie-ctps-func').send_keys('123')
            driver.find_element_by_id('id-uf-ctps-func').send_keys('sp')
            driver.find_element_by_id('id-data-emissao-ctps-func').send_keys('05/3/2017')
            stipo_vinculo = Select(driver.find_element_by_id('txt-funcionario-tipo_vinvulo'))
            stipo_vinculo.select_by_value('CELETISTA')
            driver.find_element_by_id('id-nome-usuario-func').send_keys('g_jones')
            driver.find_element_by_id('id-senha-usuario-func').send_keys('123fatec')
            btn_salvar = driver.find_element_by_id('id-salvar-func')
            btn_salvar.click()
            assert f'{nome.upper()} foi salvo com sucesso!' in driver.page_source
            time.sleep(3)
            for i in range(0, 600, 1):
                driver.execute_script(f'window.scrollTo(0, {i});')
                # time.sleep(1)
            time.sleep(3)
            btn_atualizar = driver.find_element_by_id(f'id-btn-pre-alterar-{matricula}')
            btn_atualizar.click()
            driver.find_element_by_id('id-nome-funcionario').clear()
            driver.find_element_by_id('id-nome-funcionario').send_keys('GLADSTONE JONES')
            driver.find_element_by_id('id-atualizar').click()
            time.sleep(3)
            assert 'Os dados do(a) funcionário(a) GLADSTONE JONES foram atualizados com sucesso!' in driver.page_source
            driver.find_element_by_id('id-voltar').click()
            for i in range(0, 600, 1):
                driver.execute_script(f'window.scrollTo(0, {i});')
                # time.sleep(1)
            time.sleep(5)
    
    def test_excluir_funcionario(self):
        driver = self.driver
        driver.get(r'http://localhost:5000/funcionarios')
        for cpf, nome, matricula, genero in funcionarios[3:4]:
            self.assertIn('SGF - Banco de Horas', driver.title)
            bt_adicionar = self.driver.find_element_by_id('id_novo_funcionario')
            bt_adicionar.click()
            assert 'Cadastro de Funcionário' in driver.page_source
            driver.find_element_by_id('id-matricula-func').send_keys(matricula)
            Select(driver.find_element_by_id('txt-funcionario-status')).select_by_value('ATIVO')
            driver.find_element_by_id('id-cpf-funcionario').send_keys(cpf)
            driver.find_element_by_id('id-nome-funcionario').send_keys(nome)
            sgenero = Select(driver.find_element_by_id('id-sexo-func'))
            sgenero.select_by_value(genero)
            driver.find_element_by_id('id-data-nasc-func').send_keys('22/5/1985')
            driver.find_element_by_id('id-pis-func').send_keys('33311122244')
            driver.find_element_by_id('rg-func').send_keys('32.654.987-1')
            driver.find_element_by_id('id-email-func').send_keys('exemplo@email.com.br')
            driver.find_element_by_id('id-cargo-func').send_keys('engenheiro de software')
            driver.find_element_by_id('id-data-admissao-func').send_keys('10/01/2019')
            driver.find_element_by_id('id-lotacao-func').send_keys('departamento de ti')
            driver.find_element_by_id('id-unidade-trabalho-func').send_keys('laboratório de engenharia de software')
            driver.find_element_by_id('id-numero-ctps-func').send_keys('12345')
            driver.find_element_by_id('serie-ctps-func').send_keys('123')
            driver.find_element_by_id('id-uf-ctps-func').send_keys('sp')
            driver.find_element_by_id('id-data-emissao-ctps-func').send_keys('05/3/2017')
            stipo_vinculo = Select(driver.find_element_by_id('txt-funcionario-tipo_vinvulo'))
            stipo_vinculo.select_by_value('CELETISTA')
            driver.find_element_by_id('id-nome-usuario-func').send_keys('g_jones')
            driver.find_element_by_id('id-senha-usuario-func').send_keys('123fatec')
            btn_salvar = driver.find_element_by_id('id-salvar-func')
            btn_salvar.click()
            time.sleep(3)
            for i in range(0, 600, 1):
                driver.execute_script(f'window.scrollTo(0, {i});')
                # time.sleep(1)
            time.sleep(3)
            assert f'{nome.upper()} foi salvo com sucesso!' in driver.page_source
            btn_exluir = driver.find_element_by_id(f'id-btn-pre-excluir-{matricula}')
            btn_exluir.click()
            time.sleep(3)
            driver.find_element_by_id('id-excluir').click()
            time.sleep(2)
            for i in range(0, 600, 1):
                driver.execute_script(f'window.scrollTo(0, {i});')
                # time.sleep(1)
            time.sleep(3)
            assert f'O cadastro do funcionário(a) {nome.upper()} foi excluido com sucesso!' in driver.page_source
            driver.find_element_by_id('id-listar-tudo').click()
            time.sleep(0)
            for i in range(0, 600, 1):
                driver.execute_script(f'window.scrollTo(0, {i});')
                # time.sleep(1)
            time.sleep(5)
            driver.find_element_by_id('limpar-filtros').click()
            time.sleep(3)
            
       

if __name__ == "__main__":
    
    unittest.main()
