from flask import Flask, request, jsonify
import json

app = Flask(__name__)

ARQUIVO = "chamados.json"


def ler_dados():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def salvar_dados(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as file:
        json.dump(dados, file, indent=4, ensure_ascii=False)


def gerar_novo_id(dados):
    if not dados:
        return 1
    return max(chamado["id"] for chamado in dados) + 1


# GET → listar chamados
@app.route("/chamados", methods=["GET"])
def listar_chamados():
    return jsonify(ler_dados())


# POST → criar chamado
@app.route("/chamados", methods=["POST"])
def criar_chamado():
    dados = ler_dados()
    corpo = request.json

    if not corpo or "nome" not in corpo or "setor" not in corpo or "descricao" not in corpo:
        return jsonify({"erro": "Dados inválidos"}), 400

    novo_chamado = {
        "id": gerar_novo_id(dados),
        "nome": corpo["nome"],
        "setor": corpo["setor"],
        "descricao": corpo["descricao"],
        "status": "Aberto"
    }

    dados.append(novo_chamado)
    salvar_dados(dados)

    return jsonify(novo_chamado), 201


# PUT → atualizar status
@app.route("/chamados/<int:id>", methods=["PUT"])
def atualizar_chamado(id):
    dados = ler_dados()
    corpo = request.json

    for chamado in dados:
        if chamado["id"] == id:
            novo_status = corpo.get("status")
            if novo_status not in ["Aberto", "Em andamento", "Fechado"]:
                return jsonify({"erro": "Status inválido"}), 400

            chamado["status"] = novo_status
            salvar_dados(dados)
            return jsonify(chamado)

    return jsonify({"erro": "Chamado não encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)
