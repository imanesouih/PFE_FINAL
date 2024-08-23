import xml.dom.minidom
import requests
 
 

def read_xml_file(xml_file):
    try:
        with open(xml_file, 'r') as file:
            xml_data = file.read()
        return xml_data
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier XML : {e}")
        return None
 

def get_new_token():
    try:
        # URL et identifiant    s
        auth_url = 'https://xray.cloud.getxray.app/api/v1/authenticate'
        client_id = 'BE8F3D9AA5BE4B8690FB5D6CC0073B03'
        client_secret = '9596834558827ddc637a46b337b828dfb5b1ed062e432045f42ec05b58882e31'
 
       
        auth_data = {'client_id': client_id, 'client_secret': client_secret}
 
        
        response = requests.post(auth_url, data=auth_data)
 
       
        if response.status_code == 200:
            token = response.text.strip('"')  
            print("Token récupéré avec succès:", token)
            return token
        else:
            print(f"Échec de l'obtention du nouveau token. Code d'erreur : {response.status_code}")
            print(f"Contenu de la réponse en cas d'erreur : {response.text}")
            return None
 
    except Exception as e:
        print(f"Erreur lors de la récupération du nouveau token : {e}")
        return None
 
def import_test_results(xml_data, project_key): 
    try:
 
        token = get_new_token()
           
        if not token:
            print("Impossible d'obtenir un nouveau token. Vérifiez vos informations d'authentification.")
            return
       
       
       
        xray_api_url = f'https://xray.cloud.getxray.app/api/v1/import/execution/robot?projectKey={project_key}'
        headers = {
            'Content-Type': 'application/xml',
            'Authorization': 'Bearer '+token
        }
       
        response = requests.post(xray_api_url, headers=headers, data=xml_data)
        if response.status_code == 200:
            print(f"Les résultats des tests ont été importés avec succès !: {response.text}")
        else:
            print(f"Échec de l'importation des résultats des tests. Erreur :{response.status_code}")
    except Exception as e:
        print(f"Erreur lors de l'importation des résultats des tests : {e}")
 
 
# Fonction pour parser le fichier XML et extraire les informations sur les tests
def parse_xml_tests(xml_data):
    try:
        doc = xml.dom.minidom.parseString(xml_data)
        tests = doc.getElementsByTagName('test')
        test_data = []
        for test in tests:
            test_info = {
                "id": test.getAttribute("id"),
                "name": test.getAttribute("name"),
                "tags": [tag.firstChild.nodeValue for tag in test.getElementsByTagName('tag')],
                "status": test.getElementsByTagName('status')[0].getAttribute("status")
            }
            test_data.append(test_info)
        return test_data
    except Exception as e:
        print(f"Erreur lors de l'analyse du fichier XML : {e}")
        return None
 
# Fonction principale
def main():
    xml_file_path = 'C:/Users/Imane.SOUIH/OneDrive - Akkodis/Bureau/Test/output.xml'
    project_key = 'FT'  
 
    xml_data = read_xml_file(xml_file_path)
    if xml_data:
        parsed_tests = parse_xml_tests(xml_data)
        if parsed_tests:
            imported_tests = []
            tagless_test_imported = False
            for test in parsed_tests:
                if not test['tags']:
                    if not tagless_test_imported:
                        print(f"Le test {test['name']} n'a pas de tag.")
                        tagless_test_imported = True
                else:
                    if test not in imported_tests:
                        print(f"Test ID: {test['id']}, Nom: {test['name']}, Tags: {test['tags']}, Statut: {test['status']}")
                        imported_tests.append(test)
 
            import_test_results(xml_data, project_key) #token)
        else:
            print("Aucun test trouvé dans le fichier XML.")
    else:
        print("Le fichier XML est vide ou n'a pas pu être lu.")
 
if __name__ == "__main__":
    main()
 