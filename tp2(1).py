import json
import csv

def nombre_compuesto(dic):
    """Recibe un diccionario y devuelve el nombre del compuesto"""
    nombre_compuesto=dic["compound"][0]["names"][0]["name"].upper()
    return nombre_compuesto

def calcular_spectrum(spec):
    """Recibe un diccionario y devuelve los datos de espectro como diccionario con clave y valor de punto flotante"""
    lista = spec.split()
    diccionario_spectrum={}
    for medicion in lista:
        clave=float(medicion.split(":")[0])
        valor=float(medicion.split(":")[1])
        diccionario_spectrum[clave]=valor
    return diccionario_spectrum

def combinar_diccionarios(lista_diccionarios):
    """Recibe una lista de diccionarios y devuelve un diccionario con cada clave y el total de valores asignados a esa clave como su valor."""
    diccionario_final={}
    for diccionario in lista_diccionarios:
        for key in diccionario:
            if key not in diccionario_final:
                diccionario_final[key] = diccionario[key]
            else:
                diccionario_final[key] += diccionario[key]
    return diccionario_final

def db_load():
    '''Abre el archivo json y lo carga los datos a un diccionario.'''
    with open('MoNA-export-GC-MS_Spectra.json','r', encoding = 'UTF-8') as archivo_json:
        linea = archivo_json.readline()
        dic = {}
        for linea in archivo_json:
            if not linea.startswith(']'):
                dic_json = json.loads(linea.rstrip('\n,'))
                value = calcular_spectrum(dic_json['spectrum'])
                key = nombre_compuesto(dic_json)
                if key not in dic:
                    dic[key] = [value]
                else:
                    dic[key].append(value)
            continue
        for nombre in dic:
            dic[nombre] = combinar_diccionarios(dic[nombre])
        return dic

def calcular_distancia(dic_final,dic_inicial,intensidad=2):
    """Recibe 2 diccionarios y calcula la suma de las diferencias entre claves iguales
    elevadas a la intensidad (por defecto 2 para que toda diferencia tenga peso por mas que se compense"""
    diferencia=0
    for key in dic_final:
        diferencia+=(dic_final[key]-dic_inicial.get(key,0))**intensidad
    for key in dic_inicial:
        if not key in dic_final:
            diferencia+=(dic_inicial[key])**intensidad
    return diferencia

def mediciones_csv():
    '''Abre el archivo csv lo lee y devuelve un diccionario con los datos del csv'''
    dic_mediciones = {}
    with open('muestra_grupo_13.csv','r') as archivo_csv:
        for linea in archivo_csv:
            linea = linea.split(',')
            dic_mediciones[float(linea[0])] = float(linea[1].rstrip('\n'))
    return dic_mediciones

def compuestos_similares():
    """Compara las mediciones del csv con cada compuesto y devuelve los 5 compuestos más similares a la muestra"""
    dic=db_load()
    lista_diferencias=[]
    for key in dic:
        distancia=float(calcular_distancia(mediciones_csv(),dic[key]))
        compuesto=key
        lista_diferencias.append((distancia,compuesto))
    lista_5_similares=sorted(lista_diferencias)[0:5]
    print("Los 5 compuestos mas similares a la muestra (en cuanto a los cuadrados de las diferencias entre medidas) son:\n")
    for i in range(5):
        print(str(i+1)+")",str(lista_5_similares[i][1])+", con",lista_5_similares[i][0],"de dif.\n")
    print("\n")
    return lista_5_similares,lista_diferencias

def compuestos_diferentes():
    """Devuelve los 5 compuestos más diferentes a la muestra"""
    _,lista_diferencias=compuestos_similares()
    lista_5_diferentes=sorted(lista_diferencias)[-1:-6:-1]
    #return lista_5_diferentes
    print("Los 5 compuestos mas diferentes a la muestra son:\n")
    for i in range(5):
        print(str(i+1)+")",str(lista_5_diferentes[i][1])+", con",lista_5_diferentes[i][0],"de dif.\n")
    print("\n")

#def main():
 #   """a"""
  #  opcion = int(input('opcion: \n>>'))
   # if opcion == 1:
    #    db_load()
    #elif opcion ==2:
     #   calcular_distancia(dic_mediciones,dic)
#main()
compuestos_diferentes()
