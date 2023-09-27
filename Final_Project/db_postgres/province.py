import json
import urllib3
import psycopg2

conn = psycopg2.connect(database="covid_jabar", user="postgres", password="postgres", host="127.0.0.1", port="5432")
cur = conn.cursor()

http = urllib3.PoolManager()
url = "http://103.150.197.96:5005/api/v1/rekapitulasi_v2/jabar/harian?level=kab"

try:
    response = http.request('GET', url)
    data = json.loads(response.data.decode('utf-8'))
    index = 0 #I'm using index as an id_key

    for i in data:
        province_Id = None
        province_Name = None

        province_Id = ['kode_prov']
        province_Name = ['nama_prov']

        cur.execute("""
            INSERT INTO province_table
            VALUES (%s, %s, %s); 
            """,
            (index, province_Id('kode_prov'), province_Name ('nama_prov')))
        conn.commit()
        index += 1 
    cur.close()
except IOError as io:
    print("ERROR!")