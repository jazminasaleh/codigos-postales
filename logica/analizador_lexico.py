import re
#Analizador lexico
class AnalizadorLexico:
    #Constructor
    def __init__(self):
        self.letras = "^[A-Z][^\\u00C0-\\u017F]*$"
        self.numeros = "^[0-9]+$"
        self.espacio = "^[ ]+$"
        self.guion = "^[\-]$"
    
    #coidgo sin carcateres invalidos
    def codigoSinCarcateres(self, codigoPostal):
        er = r"^[a-zA-Z0-9-\s]+$"
        cadena = ''
        for i in range(len(codigoPostal)):
            if re.findall(er, codigoPostal[i]):
                cadena += codigoPostal[i]
        return cadena
    
    #Tokenizacion, de acuerdo si es letra, numero espacio o guion
    def analizar(self, codigoPostal):
        er = r"(^[A-Z0-9-\s]+$)"
        filtrar = []
        for i in range(len(codigoPostal)):
            if re.findall(er, codigoPostal[i]):
                filtrar.append(codigoPostal[i])
            else:
                print("La entrada %s no es valida y será retirada" % codigoPostal[i])
        
        tokens =[]
        
        for i in filtrar:
            if re.match(self.letras,i):
                tokens.append({f'{i}':'letra'})
            elif re.match(self.numeros,i):
                tokens.append({f'{i}':'numero'})
            elif re.match(self.espacio,i):
                tokens.append({f'{i}':'espacio'})
            else:
                tokens.append({f'{i}':'invalido'})
        return tokens
    
    
    def analisisLexico(self, codigoPostal):
        er = r"(^[a-zA-Z0-9-\s]+$)"
        filtrar = []
        for i in range(len(codigoPostal)):
            if re.findall(er, codigoPostal[i]):
                filtrar.append(codigoPostal[i])
            else:
                print("La entrada %s no es valida y será retirada" % codigoPostal[i])
        
        tokens =[]
        for i in filtrar:
            if re.match(self.letras,i):
                tokens.append({"letra": True})
            elif re.match(self.numeros,i):
                tokens.append({"numero":True})
            elif re.match(self.guion,i):
                tokens.append({"guion":True})
            elif re.match(self.espacio,i):
                tokens.append({"espacio":True})
        return tokens
    
        