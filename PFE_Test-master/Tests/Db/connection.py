import psycopg2

def retrieve_user_credentials():
    # Informations de connexion à la base de données
    dbname = 'verceldb'
    user = 'default'
    password = '7axBzIu0bVng'
    host = 'ep-odd-mouse-a4br12y4-pooler.us-east-1.aws.neon.tech'
    port = '5432'

    # Connexion à la base de données
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # Récupération des informations utilisateur depuis la table 'users'
    cur = conn.cursor()
    cur.execute("SELECT username, email, password FROM users;")
    rows = cur.fetchall()

    # Fermeture de la connexion à la base de données
    cur.close()
    conn.close()

    return rows

if __name__ == '__main__':
    # Exemple d'utilisation : récupération des informations utilisateur
    users = retrieve_user_credentials()
    if users:
        for user in users:
            print(f"Username: {user[0]}, Email: {user[1]}, Password: {user[2]}")
    else:
        print("Aucun utilisateur trouvé dans la base de données.")
