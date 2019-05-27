"""Módulo com os modelos - classe de domínio
"""
from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime


# class Relogio():
#     id
#     numero
#     nome
#     apelido
#     local
#     descricao
#     status_id
#     local_id


# class LocalRelogio():
#     id 
#     nome 
#     contato
#     descricao
#     endereco_id
#     _endereco
    


# class StatusRelogio():
#     id
#     nome
#     descricao
#     _relogios