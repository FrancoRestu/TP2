import json
import csv

def db_load():
    with open('MoNA-export-GC-MS_Spectra.json','r', encoding='utf-8') as archivo_json:
        lineas = archivo_json.readlines()
        del lineas[0]
        del lineas[-1]
        dic_json = json.loads(lineas.rstrip('\n,'))
    return dic_json

def mediciones_csv():
    dic_mediciones = {}
    with open('muestra_grupo_13.csv','r') as archivo_csv:
        for linea in archivo_csv:
            linea = linea.split(',')
            dic_mediciones[linea[0]] = [linea[1].rstrip('\n')]
    print(dic_mediciones)
    return dic_mediciones
def main():
    opcion = int(input('opcion: '))
    if opcion == 1:
        db_load()
    elif opcion ==2:
        mediciones_csv()
main()