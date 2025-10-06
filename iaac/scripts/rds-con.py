import boto3
import json
import psycopg2

def get_secret(secret_name, region_name="us-east-1"):
    """
    Retrieve secret from AWS Secrets Manager.
    """
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response["SecretString"]
        return json.loads(secret)
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None

def test_postgres_connection(secret_name, region_name="us-east-1"):
    """
    Test connection to PostgreSQL using credentials from AWS Secrets Manager.
    """
    secret = get_secret(secret_name, region_name)
    
    if not secret:
        print("❌ Failed to retrieve database credentials.")
        return False

    try:
        conn = psycopg2.connect(
            dbname=secret["db_name"],
            user=secret["username"],
            password=secret["password"],
            host="rds-prod.cmt2mu288c4s.us-east-1.rds.amazonaws.com"
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")  # Simple query to test connection
        db_version = cur.fetchone()
        print(f"✅ Connected to PostgreSQL: {db_version[0]}")
        
        # Close resources
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        return False

# Example usage:
test_postgres_connection("rds-secret")

