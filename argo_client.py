import requests

class ArgoClient:
    BASE_URL = "https://www.portaleargo.it/famiglia/api/rest"

    def __init__(self, codice_scuola, utente, password):
        self.codice_scuola = codice_scuola
        self.utente = utente
        self.password = password
        self.token = None
        self.headers = {}

    def login(self):
        url = f"{self.BASE_URL}/login"
        payload = {
            "user": self.utente,
            "password": self.password,
            "codice_scuola": self.codice_scuola
        }

        response = requests.post(url, json=payload)
        if response.status_code == 200:
            self.token = response.json().get("token")
            self.headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            return True
        else:
            return False

    def get_voti(self):
        return requests.get(f"{self.BASE_URL}/votigiornalieri", headers=self.headers).json()

    def get_assenze(self):
        return requests.get(f"{self.BASE_URL}/assenze", headers=self.headers).json()

    def get_compiti(self):
        return requests.get(f"{self.BASE_URL}/compiti", headers=self.headers).json()

    def get_lezioni(self):
        return requests.get(f"{self.BASE_URL}/lezioni", headers=self.headers).json()

    def get_promemoria(self):
        return requests.get(f"{self.BASE_URL}/promemoria", headers=self.headers).json()

    def get_bacheca(self):
        return requests.get(f"{self.BASE_URL}/bacheca", headers=self.headers).json()
