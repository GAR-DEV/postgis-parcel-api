import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import geojson
import psycopg2
from shapely import wkb
from waitress import serve

load_dotenv()

def requestGeometry(sbl, swis):
    database=os.environ["DB_NAME"]
    host=os.environ["DB_HOST"]
    user=os.environ["DB_USER"]
    port=os.environ["DB_PORT"]
    password=os.environ["PGPASSWORD"]
    conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
    cur = conn.cursor()
    query = "SELECT geometry \
    FROM alldata \
    where print_key = %s AND swis = %s \
    LIMIT 1;"

    cur.execute(query, (sbl, swis))
    
    try:
        g = cur.fetchall()[0][0]
        shp = wkb.loads(g, hex=True)
        geoj = geojson.Feature(geometry=shp)
        return geoj
    except:
        return None

app = Flask(__name__)
CORS(app)
def create_app():
   return app.wsgi_app

limiter = Limiter(
   get_remote_address,
   app=app,
   default_limits=["25 per minute"],
   storage_uri="memory://",)


@app.route("/parcel", methods=['GET'])
def root():
    printkey = request.args.get('printkey',None,type=str)
    swis = request.args.get('swis',None,type=str)
    if not printkey:
        return jsonify(error="Asset not found."), 404
    if not swis:
        return jsonify(error="Asset not found."), 404
    result = requestGeometry(printkey, swis)
    if not result:
        return jsonify(error="Asset not found."), 404
    else:
        return result

@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify(error="Asset not found."), 404

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=80, url_scheme='http', threads=4)