import sqlite3
from sys import exit
from time import sleep
from tkinter import *
from tkinter import ttk

from tkcalendar import *

from funcoes import contador_maior, contador_menor, data_tratado
from main import Browser

conexao = sqlite3.connect('contador.db')
cursor = conexao.cursor()


class Interface:
    def __init__(self):
        self.popupBonusWindow = None
        self.impressora = None
        self.ip = None
        self.date_atual = None
        self.janela = None
        self.date_anterior = None

    def inicio(self):
        sleep(0.5)
        janela = Tk()
        # Centralizar janela no monitor
        janela.eval('tk::PlaceWindow . center')
        self.janela = janela
        janela.title("Consulta OKI")
        # janela.geometry("500x300")

        D_anterior = Label(janela, text="Data anterior")
        D_anterior.grid(row=0, column=0, padx=10, pady=10)

        date_anterior = DateEntry(janela, selectmode="day", date_pattern='dd/mm/yy')
        date_anterior.grid(row=1, column=0, padx=10, pady=10)
        self.date_anterior = date_anterior

        D_atual = Label(janela, text="Data atual")
        D_atual.grid(row=0, column=1, padx=10, pady=10)

        date_atual = DateEntry(janela, selectmode="day", date_pattern='dd/mm/yy')
        date_atual.grid(row=1, column=1, padx=10, pady=10)
        self.date_atual = date_atual

        # Botoes
        botao_UC = Button(
            janela, text="Unidade Centro", command=self.consulta_uc)
        botao_UC.grid(row=3, column=0, padx=10,
                      pady=10, )
        botao_UJ = Button(
            janela, text="Unidade Juçara", command=self.consulta_uj)
        botao_UJ.grid(row=3, column=1, padx=10,
                      pady=10,)

        botao_atualizar = Button(
            janela, text="Atualizar Banco", command=self.atualizar_banco)
        botao_atualizar.grid(row=4, column=0, padx=10,
                             pady=10, ipadx=80, columnspan=2)

        botao_fechar = Button(
            janela, text="Fechar", command=exit)
        botao_fechar.grid(row=5, column=0, padx=10,
                          pady=10, ipadx=105, columnspan=2)

        janela.mainloop()

    def consulta_uc(self):
        self.ip = 101
        self.impressora = "UC"
        self.valida_data()

    def consulta_uj(self):
        self.impressora = "UJ"
        self.ip = 102
        self.valida_data()

    def valida_data(self):
        self.date_anterior = self.date_anterior.get_date()
        self.date_atual = self.date_atual.get_date()

        if self.date_anterior == self.date_atual:
            try:
                self.janela.destroy()
                menor_hora = contador_menor(
                    self.impressora, self.date_anterior)
                maior_hora = contador_maior(self.impressora, self.date_atual)

                contador_hora = maior_hora - menor_hora
                self.date_atual = data_tratado(str(self.date_atual))
                self.popup_info(
                    f"Impressões de hoje", text_info=f"Total de impressões realizadas: {contador_hora}\n Data: {self.date_atual}")
                self.inicio()
            except IndexError as error_text:
                self.popup_info(
                    "Erro", f"Dados não encontrados! \n\n\n {error_text}")
                self.inicio()
            except AttributeError as error_text:
                self.popup_info(
                    "Erro", f"Você não selecionou nenhuma impressora! \n\n\n {error_text}")
                self.inicio()
        else:
            try:
                self.janela.destroy()
                contador_anterior = contador_maior(
                    self.impressora, self.date_anterior)
                contador_atual = contador_maior(
                    self.impressora, self.date_atual)
                contador_mes = contador_atual - contador_anterior
                self.date_atual = data_tratado(str(self.date_atual))
                self.date_anterior = data_tratado(str(self.date_anterior))
                self.popup_info(
                    f"Impressões do mês", f"Total de impressões realizadas: {contador_mes}\n De {self.date_anterior} a {self.date_atual}")
                self.inicio()
            except IndexError as error_text:
                self.popup_info(
                    "Erro", f"Dados não encontrados! \n Verifique as datas \n {error_text}")
                self.inicio()

    def popup_info(self, title_info, text_info):
        popupBonusWindow = Tk()
        self.popupBonusWindow = popupBonusWindow
        popupBonusWindow.wm_title(title_info)
        labelBonus = Label(
            popupBonusWindow, text=text_info, justify=CENTER)
        labelBonus.grid(row=0, column=0, padx=10)
        B1 = ttk.Button(popupBonusWindow, text="Okay",
                        command=self.foco_janela)
        B1.grid(row=1, column=0, pady=10)

    def foco_janela(self):
        self.janela.focus_force()
        self.popupBonusWindow.destroy()

    @staticmethod
    def atualizar_banco():
        Browser("101", "UC")
        Browser("102", "UJ")
        popupBonusWindow = Tk()
        popupBonusWindow.wm_title("Atualizado")
        labelBonus = Label(
            popupBonusWindow, text="Dados do banco atualizados com sucesso!", justify=CENTER)
        labelBonus.grid(row=0, column=0, padx=10)
        B1 = ttk.Button(popupBonusWindow, text="Okay",
                        command=popupBonusWindow.destroy)
        B1.grid(row=1, column=0, pady=10)


interface = Interface()
interface.inicio()
