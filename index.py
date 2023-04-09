#va a iniciar el proyectp
from flask import Flask, render_template, request
from logica.logica import prueba

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/codigopostal', methods=["POST"])
def codigopostal():
    codigo = request.form['codigo']
   
    #REVISAR
    return prueba(codigo)

if __name__ == '__main__':
    app.run(debug=True)