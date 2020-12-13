from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from typing import Optional
import sqlite3

banco = 'data.db'

#variaveis
app = FastAPI()

#rota raiz
@app.get("/")
def raiz():
    return {'Olá': 'Mundo'}

#criar modelo de base
class Achados(BaseModel):
    id: Optional[int]
    item: str
    peso: str
    cor: str
    categoria: str
    data: str

#rota get_All
@app.get("/achados")
def get_todos_achados(response: Response):
    list_all = []
    conn = sqlite3.connect(banco)
    c = conn.cursor()
    c.execute('SELECT * FROM tb_achados ORDER BY Id')
    for linha in c.fetchall():
        list_all.append(linha)
    conn.commit()
    conn.close()
    return list_all

#rota inserir
@app.post('/achados')
def inserir_achados(achado: Achados):
    conn = sqlite3.connect(banco)
    c = conn.cursor()
    c.execute("insert into tb_achados (item, peso, cor, categoria, data) values ('"+achado.item+"', '"+achado.peso+"','"+achado.cor+"', '"+achado.categoria+"', '"+achado.data+"');")
    conn.commit()
    conn.close()
    return achado

#rota deletar
@app.delete('/achados')
def apagar_achados(id):
    conn = sqlite3.connect(banco)
    c = conn.cursor()
    c.execute("DELETE from tb_achados WHERE id = ?", (id))
    conn.commit()
    conn.close()
    return {'CADASTRO DELETADO COM SUCESSO'}


#rota filtro categoria
@app.get('/achados/{categoria}')
def get_achados_pela_categoria(categoria: str):
    list_cat = []
    conn = sqlite3.connect(banco)
    c = conn.cursor()
    c.execute("SELECT * FROM tb_achados WHERE categoria = ?", (categoria,))
    for cat in c.fetchall():
        list_cat.append(cat)
    conn.commit()
    conn.close()
    return list_cat