from flask import Flask, request, jsonify
from flask_cors import CORS
from argo_client import ArgoClient
import uuid

app = Flask(__name__)
CORS(app)

# Sessioni attive: token → ArgoClient
sessions = {}

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    codice_scuola = data.get("codice_scuola")
    utente = data.get("utente")
    password = data.get("password")

    client = ArgoClient(codice_scuola, utente, password)
    if client.login():
        token = str(uuid.uuid4())
        sessions[token] = client
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Credenziali errate"}), 401

@app.route("/api/voti", methods=["GET"])
def voti():
    token = request.args.get("token")
    materia = request.args.get("materia")
    client = sessions.get(token)

    if not client:
        return jsonify({"error": "Token non valido"}), 403

    voti = client.get_voti().get("dati", [])
    voti_materia = [v for v in voti if v.get("materia_descrizione") == materia] if materia else voti
    media = round(sum(float(v["valore"]) for v in voti_materia) / len(voti_materia), 2) if voti_materia else 0

    return jsonify({"voti": voti_materia, "media": media})

@app.route("/api/media-generale", methods=["GET"])
def media_generale():
    token = request.args.get("token")
    client = sessions.get(token)

    if not client:
        return jsonify({"error": "Token non valido"}), 403

    voti = client.get_voti().get("dati", [])
    materie = {}
    for v in voti:
        m = v["materia_descrizione"]
        materie.setdefault(m, []).append(float(v["valore"]))

    medie = [sum(vs)/len(vs) for vs in materie.values()]
    media_generale = round(sum(medie)/len(medie), 2) if medie else 0

    return jsonify({"media_generale": media_generale})

@app.route("/api/assenze", methods=["GET"])
def assenze():
    token = request.args.get("token")
    client = sessions.get(token)

    if not client:
        return jsonify({"error": "Token non valido"}), 403

    return jsonify(client.get_assenze())

@app.route("/api/compiti", methods=["GET"])
def compiti():
    token = request.args.get("token")
    client = sessions.get(token)

    if not client:
        return jsonify({"error": "Token non valido"}), 403

    return jsonify(client.get_compiti())

@app.route("/api/lezioni", methods=["GET"])
def lezioni():
    token = request.args.get("token")
    client = sessions.get(token)

    if not client:
        return jsonify({"error": "Token non valido"}), 403

    return jsonify(client.get_lezioni())

@app.route("/api/promemoria", methods=["GET"])
def promemoria():
    token = request.args.get("token")
    client = sessions.get(token)

    if not client:
        return jsonify({"error": "Token non valido"}), 403

    return jsonify(client.get_promemoria())

@app.route("/api/bacheca", methods=["GET"])
def bacheca():
    token = request.args.get("token")
    client = sessions.get(token)

    if not client:
        return jsonify({"error": "Token non valido"}), 403

    return jsonify(client.get_bacheca())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
