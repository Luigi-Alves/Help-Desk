from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)



BANCO = r"C:\Users\luigi\OneDrive\Área de Trabalho\Help Desk\instance\helpdesk.db"


# CONEXÃO COM BANCO
def conectar():
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row
    return conn


# CRIAR TABELA
def criar_tabela():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chamados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        setor TEXT NOT NULL,
        descricao TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# EXECUTA AO INICIAR API
criar_tabela()


# GET → LISTAR CHAMADOS
@app.route("/chamados", methods=["GET"])
def listar_chamados():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM chamados")

    chamados = cursor.fetchall()

    conn.close()

    resultado = []

    for chamado in chamados:
        resultado.append({
            "id": chamado["id"],
            "usuario_id": chamado["usuario_id"],
            "nome_solicitante": chamado["nome_solicitante"],
            "setor": chamado["setor"],
            "descricao": chamado["descricao"],
            "status": chamado["status"],
            "tecnico_id": chamado["tecnico_id"],
            "criado_em": chamado["criado_em"],
            "atualizado_em": chamado["atualizado_em"],
            "fechado_em": chamado["fechado_em"]
        })

    return jsonify(resultado)


# POST → CRIAR CHAMADO
@app.route("/chamados", methods=["POST"])
def criar_chamado():

    corpo = request.json

    if not corpo:
        return jsonify({"erro": "JSON inválido"}), 400

    if "nome" not in corpo:
        return jsonify({"erro": "Nome obrigatório"}), 400

    if "setor" not in corpo:
        return jsonify({"erro": "Setor obrigatório"}), 400

    if "descricao" not in corpo:
        return jsonify({"erro": "Descrição obrigatória"}), 400

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chamados (
                   nome_solicitante,
                   setor,
                   descricao,
                   status
        )
        VALUES (?, ?, ?, ?)
    """, (
        corpo["nome_solicitante"],
        corpo["setor"],
        corpo["descricao"],
        "Aberto"
    ))

    conn.commit()

    novo_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "id": novo_id,
        "nome": corpo["nome"],
        "setor": corpo["setor"],
        "descricao": corpo["descricao"],
        "status": "Aberto"
    }), 201


# PUT → ATUALIZAR STATUS
@app.route("/chamados/<int:id>", methods=["PUT"])
def atualizar_chamado(id):

    corpo = request.json

    if not corpo or "status" not in corpo:
        return jsonify({"erro": "Status obrigatório"}), 400

    novo_status = corpo["status"]

    if novo_status not in ["Aberto", "Em andamento", "Fechado"]:
        return jsonify({"erro": "Status inválido"}), 400

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE chamados
        SET status = ?
        WHERE id = ?
    """, (novo_status, id))

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"erro": "Chamado não encontrado"}), 404

    conn.close()

    return jsonify({
        "mensagem": "Status atualizado com sucesso"
    })


# INICIAR API
if __name__ == "__main__":
    app.run(debug=True)