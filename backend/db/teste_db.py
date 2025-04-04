import psycopg2

DATABASE_URL = "postgresql://2222120009_Marley:2222120009_Marley@dataiesb.iesbtech.com.br:5432/2222120009_Marley"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    cur.execute("SELECT version();")
    version = cur.fetchone()

    print("Conexão bem-sucedida!")
    print("Versão do PostgreSQL:", version[0])

    cur.close()
    conn.close()

except Exception as e:
    print("Erro na conexão com o banco de dados:")
    print(e)
