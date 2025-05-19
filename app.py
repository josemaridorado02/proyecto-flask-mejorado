import json
from flask import Flask, render_template, request, abort, redirect, url_for

app = Flask(__name__)

# Cargar los datos del archivo JSON con manejo de errores
try:
    with open('juegos.json', 'r', encoding='utf-8') as file:
        juegos = json.load(file)
except FileNotFoundError:
    print("Error: El archivo 'juegos.json' no se encuentra en el directorio.")
    juegos = []
except json.JSONDecodeError:
    print("Error: El archivo 'juegos.json' tiene un formato JSON inválido.")
    juegos = []
except Exception as e:
    print(f"Error inesperado al cargar 'juegos.json': {e}")
    juegos = []

# Obtener lista única de desarrolladoras
desarrolladoras = sorted(list(set(juego['desarrolladora'] for juego in juegos)))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/juegos', methods=['GET', 'POST'])
def buscar_juegos():
    termino = request.form.get('termino', '').strip().lower() if request.method == 'POST' else ''
    desarrolladora = request.form.get('desarrolladora', '') if request.method == 'POST' else ''
    
    juegos_filtrados = juegos
    if termino or desarrolladora:
        juegos_filtrados = [juego for juego in juegos if 
                          (not termino or juego['titulo'].lower().startswith(termino)) and
                          (not desarrolladora or juego['desarrolladora'] == desarrolladora)]
    
    return render_template('buscar_juegos.html', juegos=juegos_filtrados, termino=termino, desarrolladoras=desarrolladoras, desarrolladora_seleccionada=desarrolladora)

@app.route('/juego/<id>')
def detalle_juego(id):
    juego = next((j for j in juegos if j['_id'] == id), None)
    if juego is None:
        abort(404)
    return render_template('detalle_juego.html', juego=juego)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)