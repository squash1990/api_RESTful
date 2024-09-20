from flask import jsonify, request, Flask, make_response
from catalog import get_products, create_product, get_product
from flask_cors import CORS
import os
import redis

app = Flask(__name__)
CORS(app)

# Obtenemos la información de las variables de entorno para después chequear que estan correctos.
redis_host = os.environ.get('REDIS_HOST', None)
redis_port = os.environ.get('REDIS_PORT', None)

# Una vez chequeados los importamos al conector de redis para después hacer las peticiones y dejarlas en cache
if redis_host and redis_port:
    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST'), # Importamos las variables de entorno que estan en el docker-compose o en los ficheros
        port=os.getenv('REDIS_PORT'), # Importamos el puerto
        db=0, decode_responses=True
    )
else:
    redis_client = None


@app.route('/product/<sku>', methods=['GET', ])
def get_product_by_sku(sku):
    product = redis_client.hgetall(sku) if redis_client else None
    if not product:
        product = get_product(sku)
        if not product:
        	return make_response(jsonify({"error": f"SKU {sku} not found!"}), 404)
        product['cache'] = 'miss'
        if redis_client:
            redis_client.hmset(product['sku'], product)
    else:
        pass
        product['cache'] = 'hit'

    return jsonify(product)


@app.route('/product', methods=['GET', 'POST'])
def list_all_products():
	'''Operar con los componentes COperar con los componentes CRUD'''
	print("Hola mundo")
	if request.method == 'GET':
		response = get_products()
		return jsonify(response)

	if request.method == 'POST':
		data = request.get_json()
		new_sku = create_product(
			None,
			data['title'],
			data['long_description'],
			data['price_euro'])
		return jsonify({"status": "ok", "sku": new_sku})


@app.route('/hello')
def hello_world():
	message = "Hola Mundo, soy Pyton! Ahora con CloudBuild y hablando JSON."
	response = {
			"messaje": message,
			"length": len(message)
	}
	return jsonify(response)


@app.route('/bye')
def bye_world():
    return ("Adios mundo cruel")

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
