import psycopg2

def purge_table():
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(
            host="localhost",
            database="test",
            user="postgres",
            password="123456"
        )

        # Création d'un curseur pour exécuter des requêtes SQL
        cur = conn.cursor()

        # Requête de suppression des données de la table spécifiée
        #cur.execute("DELETE FROM nom_de_votre_table WHERE condition_pour_purger")

        # Valider la transaction
        conn.commit()

        # Fermer le curseur et la connexion
        cur.close()
        conn.close()

        print("Purge des données de la table terminée avec succès.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Erreur lors de la purge des données :", error)

# Appel de la fonction pour purger la table
purge_table()
