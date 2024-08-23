import xml.dom.minidom
import json
from datetime import datetime, timezone, timedelta

# Fonction pour formater la date au format ISO 8601
def format_date(date_str):
    # Convertir la chaîne de date en objet datetime
    date_obj = datetime.strptime(date_str, "%Y%m%d %H:%M:%S.%f")

    # Ajouter le décalage horaire
    date_with_tz = date_obj.replace(tzinfo=timezone.utc) + timedelta(hours=1)  # Ajouter un décalage de +01:00

    # Formater la date au format ISO 8601
    return date_with_tz.isoformat()

# Chemin vers le fichier XML
xml_file = 'output.xml'

# Lire le fichier XML
tree = xml.dom.minidom.parse(xml_file)
test_elements = tree.getElementsByTagName("test")

# Initialiser une liste pour stocker les cas de test
test_cases = []

# Parcourir chaque élément <test> dans le fichier XML
for test_element in test_elements:
    test_case = {}
    # Récupérer le nom du cas de test
    test_case["name"] = test_element.getAttribute("name")

    # Récupérer la balise <status>
    status_element = test_element.getElementsByTagName('status')[0]

    # Récupérer le statut du cas de test
    test_case["status"] = status_element.getAttribute('status')

    # Récupérer les horodatages de début et de fin
    test_case["start_time"] = format_date(status_element.getAttribute('starttime'))
    test_case["end_time"] = format_date(status_element.getAttribute('endtime'))

    # Récupérer les mots-clés associés à chaque cas de test
    keywords = []
    keyword_elements = test_element.getElementsByTagName("kw")
    for keyword_element in keyword_elements:
        keyword = {}
        keyword["name"] = keyword_element.getAttribute("name")
        keyword["library"] = keyword_element.getAttribute("library")
        keyword_status_element = keyword_element.getElementsByTagName("status")[0]
        keyword["status"] = keyword_status_element.getAttribute("status")
        keyword["start_time"] = format_date(keyword_status_element.getAttribute("starttime"))
        keyword["end_time"] = format_date(keyword_status_element.getAttribute("endtime"))
        keywords.append(keyword)
    test_case["keywords"] = keywords

    # Récupérer les balises associées à ce cas de test
    tags = []
    tag_elements = test_element.getElementsByTagName("tag")
    for tag_element in tag_elements:
        tags.append(tag_element.firstChild.nodeValue.strip())
    test_case["tags"] = tags

    # Ajouter le cas de test à la liste des cas de test
    test_cases.append(test_case)

# Créer le dictionnaire JSON final
output_data = {"test_cases": test_cases}

# Convertir le dictionnaire en JSON
output_json = json.dumps(output_data, indent=4)

# Afficher le JSON résultant
print(output_json)

# Écrire le JSON résultant dans un fichier
with open('output.json', 'w') as f:
    json.dump(output_data, f)
