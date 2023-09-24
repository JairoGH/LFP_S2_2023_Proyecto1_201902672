import math
from Lexema import lexema
from Errores import errores

class analizador():

    ltoken = []
    lerrores = []
    lista_tokens = []
    no_linea = 1
    no_columna = 1

    def analizar_texto(self, texto):
        tk_lexema = ''
        indice = 0
        
        while texto:      
            caracter = texto[indice]
            indice += 1

            if caracter == "\"":
                tk_lexema, texto = self.armar_lexema(texto[indice:])
                if tk_lexema and texto:
                    self.no_columna += 1
                    lex = lexema(tk_lexema, self.no_linea, self.no_columna, 0, 0) 
                    self.ltoken.append(lex)
                    self.no_columna  += len(tk_lexema) + 1
                    indice = 0
                    
            elif caracter.isdigit():
                token, texto = self.armar_numero(texto)
                if token and texto:
                    self.no_columna += 1

                    n = lexema('', self.no_linea, self.no_columna, token, 0)
                    self.ltoken.append(n)
                    self.no_columna += len(str(token)) + 1
                    indice = 0 

            elif caracter == '[' or caracter == ']':
                car = lexema(caracter, self.no_linea, self.no_columna, 0, 0)
                self.ltoken.append(car)
                texto = texto[1:]
                indice = 0
                self.no_columna += 1

            elif caracter =="\t":
                self.no_columna += 4
                texto = texto[4:]
                indice = 0

            elif caracter == "\n":
                texto = texto[1:]
                indice = 0
                self.no_linea += 1
                self.no_columna = 1

            elif caracter == ' ' or caracter == '\r' or caracter == '{' or caracter == '}' or caracter == ',' or caracter == '.' or caracter == ':':
                self.no_columna += 1
                texto = texto[1:]
                indice = 0
            else:
                self.lerrores.append(errores(caracter, self.no_linea, self.no_columna))
                texto = texto[1:]
                indice = 0
                self.no_columna += 1

        print("Tokens:")
        for l in self.ltoken:
            print(f"lexema: {l.lexema}, numero: {str(l.numero)}, total: {str(l.total)}")
        print("Errores: ")
        for e in self.lerrores:
            print(f"Errores: {e.error}, No. Linea: {str(e.no_linea)}, No. Columna: {str(e.no_columna)}")

    def armar_lexema(self,texto):
        tk_lexema = ''
        indice = ''

        for caracter in texto:
            indice += caracter
            if caracter == '\"':
                return tk_lexema, texto[len(indice):]    #! si encuentra una  " termino de leer el token
            else:
                tk_lexema += caracter 
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

    def operar(self, operacion, valor1, valor2):
        if operacion == 'suma':
            return valor1 + valor2
        elif operacion == 'resta':
            return valor1 - valor2
        elif operacion == 'multiplicacion':
            return valor1 * valor2
        elif operacion == 'division':
            return valor1 / valor2
        elif operacion == 'potencia':
            return valor1 ** valor2
        elif operacion == 'raiz':
            return valor1 ** (1/valor2) 
        elif operacion == 'inverso':
            return 1 / valor1
        elif operacion == 'seno':
            return math.sin(valor1)
        elif operacion == 'coseno':
            return math.cos(valor1)
        elif operacion == 'tangente':
            return math.tan(valor1)
        else:
            return None
            
    def operacion(self):
        operaciones = ''
        n1= ''
        n2= ''
        Resultado = ''

        lista_tokens = self.ltoken.copy()   

        while lista_tokens:

            lexema = lista_tokens.pop(0)

            if lexema.lexema == 'operacion':
                operaciones = lista_tokens.pop(0)
                print(operaciones.lexema)
                
            elif lexema.lexema == 'valor1':
                n1 = lista_tokens.pop(0)
                if n1.lexema == '[':  
                    n1 = self.operar(operaciones.lexema, n1.numero, 1)
                    print(n1)   

            elif lexema.lexema == 'valor2':
                n2 = lista_tokens.pop(0)
                if(n2.lexema == '['):
                    n2 = self.operar(operaciones.lexema, 1, n2.numero)
                    print(n2)
                
                if operaciones and n1 and n2:
                    Resultado = self.operar(operaciones.lexema, n1.numero, n2.numero)
                    print(f"Resultado: {Resultado}")
                
        return None

    def reporte_errores(self):
    
        lista_error = self.lerrores.copy()
        cont = {
        'errores': []
    }

        contador = 1

        while lista_error:
            error1 = lista_error.pop(0)
            if error1 is not None:
                lexema_e = error1.error
                cont_error = {
                    'No.': contador,
                    'lexema': lexema_e,
                    'fila': error1.no_linea,
                    'columna': error1.no_columna
                }
                cont['errores'].append(cont_error)
                contador += 1
            else:
                print("No hay errores")


        cont_json = '{\n'
        cont_json += '  "errores": [\n'
        for cont_error in cont['errores']:
            cont_json += '    {\n'
            cont_json += f'      "No.": {cont_error["No."]},\n'
            cont_json += '      "descripcion": {\n'
            cont_json += f'        "lexema": "{cont_error["lexema"]}",\n'
            cont_json += f'        "tipo": "error lexico",\n'
            cont_json += f'        "columna": {cont_error["columna"]},\n'
            cont_json += f'        "fila": {cont_error["fila"]}\n'           
            cont_json += '    }\n'
            cont_json += '    },\n'
        cont_json = cont_json.rstrip(',\n') + '\n'
        cont_json += '  ]\n'
        cont_json += '}\n'      

        with open("REPORTE_201902672.json", "w") as archivo:
            archivo.write(cont_json)
        print("Reporte Generado Correctamente!")
    

