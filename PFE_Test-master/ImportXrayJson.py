import json
import requests

# Variables globales
PROJECT_KEY = 'FT'
XRAY_API_URL = 'https://xray.cloud.getxray.app/api/v1/import/execution'


# Fonction pour lire le contenu du fichier JSON
def read_json_file(json_file):
    try:
        with open(json_file, 'r') as file:
            json_data = json.load(file)
        return json_data
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier JSON : {e}")
        return None


# Fonction pour régénérer le token
def regenerate_token():
    try:
        token_url = 'https://xray.cloud.getxray.app/api/v1/authenticate'
        client_id = 'BE8F3D9AA5BE4B8690FB5D6CC0073B03'
        client_secret = '9596834558827ddc637a46b337b828dfb5b1ed062e432045f42ec05b58882e31'

        data = {
            'client_id': client_id,
            'client_secret': client_secret
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(token_url, json=data, headers=headers)
        if response.status_code == 200:
            new_token = response.text.strip('"')
            print("Token défini avec succès !", response.text)
            return new_token

    except Exception as e:
        print(f"Erreur lors de la régénération du token : {e}")
        return None


# Fonction pour importer les résultats des tests dans Xray via l'API Xray
def import_test_results(json_data, project_key):
    new_token = regenerate_token()
    if not new_token:
        print("Impossible d'obtenir un nouveau Token")
        return

    try:
        xray_api_url = f'{XRAY_API_URL}?projectKey={project_key}'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {new_token}'
        }
        response = requests.post(xray_api_url, headers=headers, json=json_data)
        if response.status_code == 200:
            print("Importation réussie !", response.text)
        else:
            print("Échec de l'importation !")
    except Exception as e:
        print(f"Erreur lors de l'importation des résultats des tests : {e}")


# Fonction principale
def main():
    json_file_path = 'C:/Users/Imane.SOUIH/OneDrive - Akkodis/Bureau/Test/data.json'
    project_key = 'FT'
    json_data = read_json_file(json_file_path)
    if json_data:
        json_data =read_json_file('data.json')
        import_test_results(json_data, project_key)
    print("l'importation est terminé !")
if __name__ == "__main__":
    main()
