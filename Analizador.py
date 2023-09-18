
class analizador():

    ltoken = []
    lerrores = []

    def lectura_archivo(self, texto):
        print("Analizando...")
        print(texto)
        
    def analizar_texto(self, texto):
        lexema = ''
        indice = 0
        
        while texto:      
            caracter = texto[indice]
            indice += 1
            if caracter == "\"":
                lexema, texto = self.armar_lexema(texto[indice:])
                if lexema and texto:
                    self.ltoken.append(lexema)
                    indice = 0
            elif caracter.isdigit():
                token, texto = self.armar_numero(texto)
                if token and texto:
                    self.ltoken.append(token)
                    indice = 0 
            elif caracter == '[' or caracter == ']':
                self.ltoken.append(caracter)
                texto = texto[1:]
                indice = 0
            elif caracter =="\t":
                texto = texto[4:]
                indice = 0
            elif caracter == "\n":
                texto = texto[1:]
                indice = 0
            elif caracter == ' ' or caracter == '\r' or caracter == '{' or caracter == '}' or caracter == ',' or caracter == '.' or caracter == ':':
                texto = texto[1:]
                indice = 0
            else:
                self.lerrores.append(caracter)
                texto = texto[1:]
                indice = 0
        print("Tokens:")
        print(self.ltoken)
        print("Errores: ")
        print(self.lerrores)

    def armar_lexema(self,texto):
        lexema = ''
        indice = ''

        for caracter in texto:
            indice += caracter
            if caracter == '\"':
                return lexema, texto[len(indice):]    #! si encuentra una  " termino de leer el token
            else:
                lexema += caracter 
        return None, None

    def armar_numero(self, texto):
        numero = ''
        indice = ''
        is_decimal =  False
        for caracter in texto:
            indice += caracter
            if caracter == '.':
                is_decimal = True
            if caracter == '"' or caracter == ' ' or caracter == '\n' or caracter == '\t':
                if is_decimal:
                    return float(numero), texto[len(indice)-1:]
                else:
                    return int(numero), texto[len(indice)-1:]
            else:
                if caracter != ',': 
                    numero += caracter
        return None, None