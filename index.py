#va a iniciar el proyectp
from flask import Flask, render_template, request
from logica.logica import getDescription, getCodes

#Unir la parte de la interfaz con la logica
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/codigopostal', methods=["POST"])
def codigopostal():
    codigo = request.form['codigo']
    #REVISAR
    return getCodes(codigo)

@app.route('/descripcion', methods=["GET"])
def descripcion():
    codigo = request.args.get('code')
    place = request.args.get('placeName')
    country = request.args.get('countryCode')
    return getDescription(codigo, place, country)

if __name__ == '__main__':
    app.run(debug=True)