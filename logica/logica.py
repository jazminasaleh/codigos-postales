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


def checkCondition(code: Expresion_Data, data, codigo):
    coincidences = 0
    for i in code.caracteres:
        if i == len(codigo):
            coincidences += 1
            
    if coincidences == 0:
        return False
    
    for i in data:
        if i == "numero":
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


def checkItemInList(item: Code, list):
    if len(list) == 0: 
        return False
    for i in list:
        if item.place_name == i.place_name and item.country_code == i.country_code:
            return True
    return False

#depenidndo del codigo se dirge a X pantalla
def getCodes(codigo):
    
    #Codigo sin carcateres
    print('___codigo sin carcteres epseciales___\n')
    resultado = objeto.codigoSinCarcateres(codigo)
    codigo = resultado
    
    
    
     #analizador lexico
    print('Analizador lexico\n')
    analisisLexico = objeto.analisisLexico(codigo)
    print(analisisLexico)
    
    formatos_validos = validateExpresion(analisisLexico, codigo)
   
    
     #consumo de la api
    print('___CONSUMO API___\n')
    print(infoapi(resultado))
    
        
    
    
    result = infoapi(resultado)
    
    table_list = []
    
    for i in result:
        if codigo != i.get("postalCode"):
            continue
        
        if not checkItemInList(Code(i.get("placeName"), i.get("adminCode1"), i.get("adminCode2"), i.get("adminName1"), i.get("adminName2"), i.get("ISO3166-2"), i.get("countryCode")), table_list):
            table_list.append(Code(i.get("placeName"), i.get("adminCode1"), i.get("adminCode2"), i.get("adminName1"), i.get("adminName2"), i.get("ISO3166-2"), i.get("countryCode")))

    #Dirigir a X pagina segun el codigo postal, si este es valido o no
    print(len(table_list))
    
    if result != '' and len(table_list) != 0: 
        return render_template("result.html", codigos=formatos_validos, resultado = table_list, code = codigo)
    else:
        return render_template('error.html', codigo = codigo)

def get_data_json(country):
    for i in postalCodes:
        if i.code == country:
            return i

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
    dataa = data["postalCodes"]
    if(len(dataa) >= 1):
        return dataa
    return ''


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
