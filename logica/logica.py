from flask import redirect, render_template
from urllib.request import urlopen
from urllib.parse import quote  
import json, re
from logica.analizador_lexico import AnalizadorLexico
from model.code import Code
from model.expresionData import Expresion_Data

f = open("./static/data/datos.json", mode="r", encoding="utf-8")
jsonData = json.load(f)

postalCodes = []

objeto = AnalizadorLexico();
for i in jsonData["data"]:
    postalCodes.append(Expresion_Data(i["abreviatura"],i["pais"],i["expresionRegular"],i["numeros"], i["letras"], i["guiones"], i["espacios"], i["numeroCaracteres"], i["analisisSemantico"], i["usar"]))
  
# Closing file
f.close()

#Poder ver si el codigo postal tiene numeros, letras, guiones o espacios
def checkCondition(code: Expresion_Data, data, codigo):
    coincidences = 0
    for i in code.caracteres:
        if i == len(codigo):
            coincidences += 1
            
    if coincidences == 0:
        return False
    
    for i in data:
        if i == "número":
            if code.numeros:
                return True
        if i == "letra":
            if code.letras:
                return True
        if i == "guion":
            if code.guiones:
                return True
        if i == "espacio":
            if code.espacios:
                return True
    return False

#Ya teniendo el token, ahora se valida la expresion regular y los resultados se guardan en una lista    
def validateExpresion(analisisLexico, codigo):
    temp_caracteres = []
    
    for i in analisisLexico:
        temp_caracteres.append(list(i)[0])

    data = list(set(temp_caracteres))
    
    codigos_postales = filter(lambda code: checkCondition(code, data, codigo), postalCodes)
    
    formatos_validos = []
    
    for i in codigos_postales:
        regex = r""+i.expression
        match = re.match(regex, codigo)
        
        if match:
            formatos_validos.append(i)
    
    return formatos_validos

#Se mira si en la lista ya se encuentra ese codigo almacenado
def checkItemInList(item: Code, list):
    if len(list) == 0: 
        return False
    for i in list:
        if item.country_code == i.country_code and item.place_name == i.place_name:
            return True
    return False

#depenidndo del codigo se dirge a X pantalla
#Si el coidgo es igual se almacena en una lista, de lo contrario en otra lista.
def getCodes(codigo):
    
    #Codigo sin carcateres
    resultado = objeto.codigoSinCarcateres(codigo)
    codigo = resultado
    
    #analizador lexico
    analisisLexico = objeto.analisisLexico(codigo)
    
    formatos_validos = validateExpresion(analisisLexico, codigo)
    
    result = infoapi(resultado)
    
    table_list = []
    table_listD = []
    
    for i in result:
        if codigo != i.get("postalCode"):
            table_listD.append(Code(i.get("placeName"), i.get("adminCode1"), i.get("adminCode2"), i.get("adminName1"), i.get("adminName2"), i.get("ISO3166-2"), i.get("countryCode"), i.get("postalCode")))
        else: 
            table_list.append(Code(i.get("placeName"), i.get("adminCode1"), i.get("adminCode2"), i.get("adminName1"), i.get("adminName2"), i.get("ISO3166-2"), i.get("countryCode"), i.get("postalCode")))
           

    #Dirigir a X pagina segun el codigo postal, si este es valido o no   
    if result != '' and (len(table_list) != 0 or len(table_listD) != 0): 
        return render_template("result.html", codigos=formatos_validos, resultado = table_list,  resultados = table_listD, code = codigo)
    else:
        return render_template('error.html', codigo = codigo)

def get_data_json(country):
    for i in postalCodes:
        if i.code == country:
            return i

#analisis estructural
def getDescription(codigo, place, country):
    data = infoapiExtraParameters(codigo, place, country)
    
    analisisLexico = objeto.analizar(codigo)
    
    estructura = ''
    contador = 0
    contLetras =0
    contNumeros = 0
    contEspacios = 0
    contGuiones = 0
    for i in analisisLexico:
        if(list(i.values()) == ['número']):
            if(contador == 0):
                estructura += 'El primer dígito es un número,'
            else:
                contNumeros +=  1
                if(contLetras != 0):
                    estructura += ' seguido de '+ str(contLetras) +' letras,'
                    contLetras = 0
                    if(contador == len(analisisLexico)-1):
                        estructura += ' terminado en ' + str(contNumeros) +' números.'
                elif(contador == len(analisisLexico)-1):
                    estructura += ' terminado en ' + str(contNumeros) +' números.'
                elif(contEspacios !=0):
                    estructura += ' seguido de '+ str(contEspacios) +' espacio,'
                    contEspacios = 0
                elif(contGuiones !=0):
                    estructura += ' seguido de '+ str(contGuiones) +' guion,'
                    contGuiones = 0
        elif(list(i.values()) == ['letra']):
            if(contador == 0):
                estructura += 'El primer dígito es una letra,'
            else:
                contLetras += 1
                if(contNumeros != 0):     
                    estructura += ' seguido de '+ str(contNumeros) +' números,'
                    contNumeros = 0
                    if(contador == len(analisisLexico)-1):
                         estructura += ' terminado en '+ str(contLetras) +' letras.'
                elif(contador == len(analisisLexico)-1):
                    estructura += ' terminado en '+ str(contLetras) +' letras.'
                elif(contEspacios !=0):
                    estructura += ' seguido de '+ str(contEspacios) +' espacio,'
                    contEspacios = 0
                elif(contGuiones !=0):
                    estructura += ' seguido de '+ str(contGuiones) +' guion,'
                    contGuiones = 0
        elif(list(i.values()) == ['guion']):
            if(contador == 0):
                estructura += 'El primer dígito es un guion,'
            else:
                contGuiones += 1
                if(contLetras != 0):
                    estructura += ' seguido de '+ str(contLetras) +' letras,'
                    contLetras = 0
                elif(contador == len(analisisLexico)-1):
                    estructura += ' terminado en '+ str(contGuiones) +' guion'
                elif(contEspacios !=0):
                    estructura += ' seguido de '+ str(contEspacios) +' espacio,'
                    contEspacios = 0
                elif(contNumeros !=0):
                    estructura += ' seguido de '+ str(contNumeros) +' números,'
                    contNumeros = 0
               
        elif(list(i.values()) == ['espacio']):
            if(contador == 0):
                estructura += 'El primer dígito es un espacio,'
            else:
                contEspacios += 1
                if(contLetras != 0):
                    estructura += ' seguido de '+ str(contLetras) +' letras,'
                    contLetras = 0
                elif(contador == len(analisisLexico)-1):
                    estructura += ' terminado en '+ str(contEspacios) +' espacio'
                elif(contGuiones !=0):
                    estructura += ' seguido de '+ str(contGuiones) +' guion,'
                    contGuiones = 0
                elif(contNumeros !=0):
                    estructura += ' seguido de '+ str(contNumeros) +' números,'
                    contNumeros = 0
        contador += 1
    
    json_data = get_data_json(country)
    
    
    for i in json_data.usar:
        json_data.semantico = json_data.semantico.replace("{"+i+"}", data[i])
    
    datosLexico = []
    contador2 = 1
    
    for i in analisisLexico:
        datosLexico.append("Posición "+ str(contador2) +": Digito " + list(i.keys())[0] + ", Tipo " + list(i.values())[0])
        contador2 += 1
    
    
    return render_template("description.html", lexico = datosLexico, estructura = estructura, semantico = json_data.semantico, code = codigo, pais = json_data.pais)
    
    
#consumir la api de los coidgos postales a nivel mundial
def infoapi(codigo):
    codigo = codigo.strip().replace(" ", "%20")
    url = f'http://api.geonames.org/postalCodeSearchJSON?postalcode={codigo}&username=sebastiancorrea13'
    respuesta = urlopen(url)
    data = json.loads(respuesta.read())
    print(data)
    dataa = data["postalCodes"]
    if(len(dataa) >= 1):
        return dataa
    return ''

#consumir la api, pero teniendo en cuenta parametros como el codigo, pais y abreviatrura
def infoapiExtraParameters(codigo, place, country):
    codigo = codigo.strip().replace(" ", "%20")
    place = place.strip().replace(" ", "%20")
    country = country.strip().replace(" ", "%20")
    url = f'http://api.geonames.org/postalCodeSearchJSON?postalcode={codigo}&countrycode={country}&placename={place}&username=sebastiancorrea13'
    
    print(url)
    respuesta = urlopen(url)
    data = json.loads(respuesta.read())
    dataa = data["postalCodes"]
    if(len(dataa) >= 1):
        return dataa[0]
    return ''
