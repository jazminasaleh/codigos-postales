from flask import redirect, render_template
from urllib.request import urlopen
import json, re
from logica.analizador_lexico import AnalizadorLexico
from model.expresionData import Expresion_Data

f = open("./static/data/datos.json")
jsonData = json.load(f)

postalCodes = []

objeto = AnalizadorLexico();
for i in jsonData["data"]:
    postalCodes.append(Expresion_Data(i["pais"],i["expresionRegular"],i["numeros"], i["letras"], i["guiones"], i["espacios"]))
  
# Closing file
f.close()

def validateExpresion(analisisLexico):
    print(analisisLexico)
    

#depenidndo del codigo se dirge a X pantalla
def prueba(codigo):
    
    #Codigo sin carcateres
    print('___codigo sin carcteres epseciales___\n')
    resultado = objeto.codigoSinCarcateres(codigo)
    print(resultado)
    
    
    
     #analizador lexico
    print('Analizador lexico\n')
    analisisLexico = objeto.analisisLexico(codigo)
    print(analisisLexico)
    
    validateExpresion(analisisLexico)
   
    
     #consumo de la api
    print('___CONSUMO API___\n')
    print(infoapi(resultado))
    
    #tokenizacion
    print('___RESULTADO___\n')
   
    
    #cadena con tokens
    for i in analisisLexico:
        print(i)
        
    #valores
    print('\n___KEYS___\n')
    for i in analisisLexico:
        print(list(i.keys()))
   
    #Analisis estructural
    print('\n___ANALISI ESTRUCTURAL___\n')
    estructura = ''
    contador = 0
    contLetras =0
    contNumeros = 0
    contEspacios = 0
    contGuiones = 0
    for i in analisisLexico:
        if(list(i.values()) == ['numero']):
            if(contador == 0):
                estructura += 'El primer digito es un número,'
            else:
                contNumeros +=  1
                if(contLetras != 0):
                    estructura += ' seguido de '+ str(contLetras) +' letras,'
                    contLetras = 0
                elif(contador == len(analisisLexico)-1):
                    estructura += ' terminado en ' + str(contNumeros) +' números.'
                elif(contEspacios !=0):
                    estructura += ' seguido de '+ str(contEspacios) +' espacios,'
                    contEspacios = 0
                elif(contGuiones !=0):
                    estructura += ' seguido de '+ str(contGuiones) +' guiones,'
                    contGuiones = 0
        elif(list(i.values()) == ['letra']):
            if(contador == 0):
                estructura += 'El primer digito es una letra,'
            else:
                contLetras += 1
                if(contNumeros != 0):     
                    estructura += ' seguido de '+ str(contNumeros) +' números,'
                    contNumeros = 0
                elif(contador == len(analisisLexico)-1):
                    estructura += ' terminado en '+ str(contLetras) +' letras.'
                elif(contEspacios !=0):
                    estructura += ' seguido de '+ str(contEspacios) +' espacios,'
                    contEspacios = 0
                elif(contGuiones !=0):
                    estructura += ' seguido de '+ str(contGuiones) +' guiones,'
                    contGuiones = 0
        elif(list(i.values()) == ['guion']):
            if(contador == 0):
                estructura += 'El primer digito es un guion,'
            else:
                contGuiones += 1
                if(contLetras != 0):
                    estructura += ' seguido de '+ str(contLetras) +' letras,'
                    contLetras = 0
                elif(contador == len(analisisLexico)-1):
                    estructura += ' terminado en '+ str(contGuiones) +' guion'
                elif(contEspacios !=0):
                    estructura += ' seguido de '+ str(contEspacios) +' espacios,'
                    contEspacios = 0
                elif(contNumeros !=0):
                    estructura += ' seguido de '+ str(contNumeros) +' números,'
                    contNumeros = 0
               
        elif(list(i.values()) == ['espacio']):
            if(contador == 0):
                estructura += 'El primer digito es un espacio,'
            else:
                contEspacios += 1
                if(contLetras != 0):
                    estructura += ' seguido de '+ str(contLetras) +' letras,'
                    contLetras = 0
                elif(contador == len(analisisLexico)-1):
                    estructura += ' terminado en '+ str(contEspacios) +' espacio'
                elif(contGuiones !=0):
                    estructura += ' seguido de '+ str(contGuiones) +' guiones,'
                    contGuiones = 0
                elif(contNumeros !=0):
                    estructura += ' seguido de '+ str(contNumeros) +' números,'
                    contNumeros = 0
        contador += 1
    print(estructura)
    
    #Dirigir a X pagina segun el codigo postal, si este es valido o no
    if infoapi(resultado) != '': 
        return redirect(f"https://www.google.com/maps/place/{resultado}/")
    else:
        return render_template('error.html')
    
    
    
#consumir la api de los coidgos postales a nivel mundial
def infoapi(codigo):
    codigo = codigo.strip().replace(" ", "%20")
    url = f'http://api.geonames.org/postalCodeSearchJSON?postalcode={codigo}&username=sebastiancorrea13'
    respuesta = urlopen(url)
    data = json.loads(respuesta.read())
    dataa = data["postalCodes"]
    if(len(dataa) >= 1):
        return dataa[0]['placeName'] 
    return ''
