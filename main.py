from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import datetime
import time

# Placeholder per argo (sostituibile con argo-api-python reale)
# from argo import ArgoClient

app = Flask(__name__)
CORS(app)

# In-memory session store
sessions = {}

# Simulazione login e accesso Argo
def fake_login(codice_scuola, utente, password):
    if codice_scuola and utente and password:
        return {
            "id": str(uuid.uuid4()),
            "nome": "Mario",
            "cognome": "Rossi",
            "data": int(time.time()),
            "voti": {
                "italiano": [
                    {"tipo": "Orale", "voto": 7.5, "descrizione": "Interrogazione Manzoni", "data": "2024-04-10"},
                    {"tipo": "Scritto", "voto": 6.0, "descrizione": "Tema sull'Illuminismo", "data": "2024-04-15"}
                ],
                "storia": [
                    {"tipo": "Orale", "voto": 8.0, "descrizione": "La Prima Guerra Mondiale", "data": "2024-04-05"}
                ]
            }
        }
    return None

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    session = fake_login(data['codice_scuola'], data['utente'], data['password'])
    if session:
        token = str(uuid.uuid4())
        sessions[token] = session
        return jsonify({"token": token})
    return jsonify({"error": "Credenziali non valide"}), 401

@app.route('/api/voti', methods=['GET'])
def voti():
    token = request.args.get('token')
    materia = request.args.get('materia')
    session = sessions.get(token)
    if not session or materia not in session['voti']:
        return jsonify({"voti": [], "media": 0.0})
    voti = session['voti'][materia]
    media = sum(v['voto'] for v in voti) / len(voti)
    return jsonify({"voti": voti, "media": round(media, 2)})

@app.route('/api/media-generale', methods=['GET'])
def media_generale():
    token = request.args.get('token')
    session = sessions.get(token)
    if not session:
        return jsonify({"media_generale": 0.0})
    medie = [sum(v['voto'] for v in voti) / len(voti) for voti in session['voti'].values()]
    return jsonify({"media_generale": round(sum(medie) / len(medie), 2)})

@app.route('/api/assenze', methods=['GET'])
def assenze():
    token = request.args.get('token')
    session = sessions.get(token)
    if not session:
        return jsonify({"assenze": []})
    return jsonify({
        "assenze": [
            {"data": "2024-04-12", "giustificata": False},
            {"data": "2024-03-30", "giustificata": True}
        ]
    })

@app.route('/api/compiti', methods=['GET'])
def compiti():
    token = request.args.get('token')
    session = sessions.get(token)
    if not session:
        return jsonify({"compiti": []})
    return jsonify({
        "compiti": [
            {
                "materia": "italiano",
                "descrizione": "Tema su Pirandello",
                "data_assegnazione": "2024-04-10",
                "data_consegna": "2024-04-20"
            }
        ]
    })

@app.route('/api/lezioni', methods=['GET'])
def lezioni():
    token = request.args.get('token')
    session = sessions.get(token)
    if not session:
        return jsonify({"lezioni": []})
    return jsonify({
        "lezioni": [
            {"data": "2024-04-15", "materia": "storia", "argomento": "La crisi del '29"},
            {"data": "2024-04-12", "materia": "italiano", "argomento": "Il Decadentismo"}
        ]
    })

@app.route('/api/promemoria', methods=['GET'])
def promemoria():
    token = request.args.get('token')
    session = sessions.get(token)
    if not session:
        return jsonify({"promemoria": []})
    return jsonify({
        "promemoria": [
            {"titolo": "Compito di storia", "testo": "Capitolo 4 da studiare", "data_pubblicazione": "2024-04-14"}
        ]
    })

@app.route('/api/bacheca', methods=['GET'])
def bacheca():
    token = request.args.get('token')
    session = sessions.get(token)
    if not session:
        return jsonify({"circolari": []})
    return jsonify({
        "circolari": [
            {"oggetto": "Colloqui genitori", "contenuto": "Disponibili da lunedì", "data_pubblicazione": "2024-04-10"}
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
