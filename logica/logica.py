from flask import redirect, render_template
from urllib.request import urlopen
import json, re

from logica.analizador_lexico import AnalizadorLexico
#depenidndo del codigo se dirge a X pantalla
def prueba(codigo):
   
    #consumo de la api
    print('___CONSUMO API___\n')
    print(infoapi(codigo))
    
    #analizador lexico
    print('Analizador lexico\n')
    objeto = AnalizadorLexico();
    resultado = objeto.analizar(codigo)
    
    #tokenizacion
    print('___RESULTADO___\n')
    print(resultado)
    
    #cadena con tokens
    for i in resultado:
        print(i)
        
    #valores
    print('\n___KEYS___\n')
    for i in resultado:
        print(list(i.keys()))
   
    #tokens
    print('\n___VALOR___\n')
    for i in resultado:
        print(list(i.values()))
    
    #Dirigir a X pagina segun el codigo postal, si este es valido o no
    if codigo != '000000': 
        return redirect(f"https://www.google.com/maps/place/{codigo}/")
    else:
        return render_template('error.html')
    
    
    
#consumir la api de los coidgos postales a nivel mundial
def infoapi(codigo):
    codigo = codigo.strip().replace(" ", "%20")
    url = f'http://api.geonames.org/postalCodeSearchJSON?postalcode={codigo}&username=sebastiancorrea13'
    respuesta = urlopen(url)
    data = json.loads(respuesta.read())
    return data
