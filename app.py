from flask import Flask, request, jsonify
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity

)
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Altere para uma chave secreta mais segura
jwt = JWTManager(app)

# Lista que armazena todos os chamados

def carregar_dados():
    try:
        with open("usuarios.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    
    except FileNotFoundError:
        return []
    
def salvar_dados(usuarios):
    with open("usuarios.json", "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

def carregar_chamados():
    try:
        with open("chamados.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    
    except FileNotFoundError:
        return []

def salvar_chamados(chamados):
    with open("chamados.json", "w", encoding="utf-8") as arquivo:
        json.dump(chamados, arquivo, indent=4, ensure_ascii=False)

#Autenticação

@app.post('/register')
def register():
    data = request.json
    usuarios = carregar_dados()

    if any(u['email'] == data['email'] for u in usuarios):
        return jsonify({"msg": "Usuário já existe!"}), 400
    
    novo = {
        "id": len(usuarios) + 1,
        "nome": data['nome'],
        "email": data['email'],
        "senha": generate_password_hash(data['senha']),
        "tipo": data['tipo']
    }

    usuarios.append(novo)
    salvar_dados(usuarios)

    return jsonify({"msg": "Usuário registrado com sucesso!"}), 201

@app.post('/login')
def login():
    data = request.json
    usuarios = carregar_dados()

    usuario = next((u for u in usuarios if u['email'] == data['email']), None)

    if not usuario or not check_password_hash(usuario['senha'], data['senha']):
        return jsonify({"msg": "Credenciais inválidas!"}), 401
    
    access_token = create_access_token(identity={"email": usuario['email'], "tipo": usuario['tipo']})
    
    return jsonify(access_token=access_token), 200

#chamados
@app.post('/chamados')
@jwt_required()
def abrir_chamado():
    identidade = get_jwt_identity()
    chamados = carregar_chamados()

    novo = {
        "id": len(chamados) + 1,
        "titulo": request.json["titulo"],
        "descricao": request.json["descricao"],
        "status": "Aberto",
        "criador": identidade["email"],
        "tecnico": None
    }

    chamados.append(novo)
    salvar_chamados(chamados)

    return jsonify({"msg": "Chamado criado"}), 201


@app.get("/chamados")
@jwt_required()
def listar_chamados():
    identidade = get_jwt_identity()
    chamados = carregar_chamados()

    if identidade["tipo"] == "admin":
        return jsonify(chamados)

    if identidade["tipo"] == "tecnico":
        return jsonify([c for c in chamados if c["tecnico"] == identidade["email"]])

    return jsonify([c for c in chamados if c["criador"] == identidade["email"]])


# --------------------

if __name__ == "__main__":
    app.run(debug=True)