import psycopg2

params = {
    "dbname": "jobard_leaderboard",
    "user": "jobard_user",
    "password": "Motdepasse72!",
    "host": "localhost",
    "port": "5432"
}

print("Params:", params)

try:
    conn = psycopg2.connect(**params)
    print("✅ Connexion réussie !")
    conn.close()
except Exception as e:
    print("❌ Erreur de connexion :")
    print(repr(e))