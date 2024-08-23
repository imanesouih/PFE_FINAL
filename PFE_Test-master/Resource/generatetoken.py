import requests

def generate_token(username, email, password):
    url = "https://testing-auto-git-main-pfe2024s-projects.vercel.app/tasks/auth"
    payload = {
        "username": username,
        "email": email,
        "password": password
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        print("Response JSON:", response_json)  # Affiche la réponse JSON complète pour inspection

        access_token = response_json.get("access_token")  # Utilise la clé 'access_token'
        if access_token:
            print(f"Token generated: {access_token}")
            with open("token.txt", "w") as file:
                file.write(access_token)
            return access_token
        else:
            print("Access token not found in response JSON")
            return None
    else:
        print(f"Failed to generate token. Status code: {response.status_code}")
        return None

# Appel de la fonction pour tester
token = generate_token("imane", "imane@example.com", "motdepasse123")
print(token)  # Affiche le token généré ou None si la génération a échoué
