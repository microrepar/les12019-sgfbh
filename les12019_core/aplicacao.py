
"""Módulo aplicacao - contém a classe Resultado da aplicação
"""
from typing import List
from collections.abc import Sequence
import datetime


list_entidade = List[object]
list_str = List[str]

class Resultado():

    def __init__(self):
        self.__msg= list()
        self.__entidades: list_entidade = list()
        self.form = None
        
    @property
    def msg(self) -> list_str:
        return self.__msg

    @msg.setter
    def msg(self, mensagem: str):
        if isinstance(mensagem, str):
            self.__msg += list([mensagem])
        elif isinstance(mensagem, Sequence):
            self.__msg += list(mensagem)

    @property
    def entidades(self) -> list_entidade:
        return self.__entidades

    @entidades.setter
    def entidades(self, entidade):
        if isinstance(entidade, Sequence):
            self.__entidades += list(entidade)
        elif entidade is not None:
            self.__entidades += list([entidade])
    
    def qtde_entidades(self):
        return len(self.entidades)
    
    def qtde_msg(self):
        return len(self.msg)


class ConverteData:

    @classmethod
    def stringDate(cls, strData:str):
        if strData is None or strData.strip() == '':
            return None
        try:
            data = datetime.datetime.strptime(strData, '%d/%m/%Y')
        except Exception as e:
            str(e)
            return None
        else:
            return data

    @classmethod
    def dateString(cls, dtData):
        return dtData.strftime('%d/%m/%Y')


class ConverteHora:

    @classmethod
    def stringHora(cls, strDateTime: str):
        if strDateTime is None or strDateTime.strip() == '':
            return None
        try:
            hora = datetime.datetime.strptime(strDateTime, '%H:%M')
        except Exception as e:
            str(e)
            return None
        else:
            return hora
   
    @classmethod
    def stringDataHora(cls, strDate: str, strTime):
        if not all([strDate, strTime, strDate.strip(), strTime.strip()]):
            return None
        try:
            data = datetime.datetime.strptime(strDate, '%d/%m/%Y')
            hora = datetime.datetime.strptime(strTime, '%H:%M')
            data_hora = datetime.datetime.combine(data.date(), hora.time())
        except Exception as e:
            str(e)
            return None
        else:
            return data_hora

    @classmethod
    def datetimeStringHora(cls, dthString: datetime.datetime):

        try:
            hora = dthString.strftime('%H:%M')
        except Exception as e:
            str(e)
            return None
        else:
            return hora
