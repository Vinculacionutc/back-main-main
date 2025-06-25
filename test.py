import pymysql

try:
    conn = pymysql.connect(
        host='68.233.122.231',
        user='root',
        password='Cappa100..',
        database='new',
        port=3306,
        connect_timeout=10
    )
    print("✅ Conexión exitosa")
    
    # Opcional: hacer una consulta de prueba
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"✅ Versión MySQL: {version[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")