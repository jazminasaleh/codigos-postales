import re
#Analizador lexico
class AnalizadorLexico:

    def __init__(self):
        self.letras = "^[a-zA-Z][^\\u00C0-\\u017F]*$"
        self.numeros = "^[0-9]+$"
        self.espacio = "^[ ]+$"
        self.guion = "^[\-]$"
        #falta el -
      
    def analizar(self, codigoPostal):
        er = r"^[a-zA-Z0-9-\s]+$"
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
            elif re.match(self.guion,i):
                tokens.append({f'{i}':'guion'})
            else:
                tokens.append({f'{i}':'invalido'})
        return tokens

