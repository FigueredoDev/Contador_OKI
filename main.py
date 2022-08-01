import sqlite3
from datetime import datetime

from bs4 import BeautifulSoup
from requests import get


class Browser:
    def __init__(self, ip, impressora):
        self.data_hora = None
        self.A4 = None
        self.A3 = None
        self.contador = None
        self.modelo_impressora = None
        conexao = sqlite3.connect("contador.db")
        cursor = conexao.cursor()
        self.conexao = conexao
        self.cursor = cursor

        URL = f"http://192.168.1.{ip}/countsum.htm"
        page = get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        dados = soup.find_all(class_="sub_item_color")

        mptray = dados[0].text.split("y")[-1]
        tray = dados[1].text.split("y")[-1][1:]
        data = datetime.now().strftime('%Y-%m-%d %H:%M')
        contador = int(mptray) + int(tray)

        self.inserir_dados(mptray, tray, contador, data, impressora)

    def inserir_dados(self, A4, A3, contador, data_hora, modelo_impressora):
        self.A4 = A4
        self.A3 = A3
        self.contador = contador
        self.data_hora = data_hora
        self.modelo_impressora = modelo_impressora

        self.cursor.execute("""
            INSERT INTO contador (A4, A3, contador, datahora, ID)
            VALUES (?,?,?,?,?)""", (self.A4, self.A3, self.contador, self.data_hora, self.modelo_impressora))
        self.conexao.commit()
        self.conexao.close()
