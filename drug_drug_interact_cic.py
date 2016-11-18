
# coding: utf-8

# In[1]:

import os
import glob
from openpyxl import load_workbook
import re
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element, SubElement , Comment, tostring
import numpy as np
#para hacer calculos de fechas -6h +6h y +48h
from datetime import datetime, timedelta


# In[3]:

os.chdir('C:\Users\Diego Salazar\Google Drive\Project_CIC')


# In[3]:

wb = load_workbook('Med_vs_Tiempo.xlsx')
#wb = load_workbook('drug_interact_to_py.xlsx')
ws = wb['Med_vs_Tiempo (5)']


# In[4]:

#Aqui se crea el xml de paciente, fecha adm y medicamento de esa fecha.
drug = Element('drug')
drug.append(Comment('Relacion med_med por paciente por fecha'))
#for fila in xrange(1, 1000):
for fila in xrange(1, ws.get_highest_row()-1):
    nueva_fecha = str(datetime.strptime(str(ws.cell(row= fila, column= 0).value).replace(' 00:00:00', '') + " " + str(ws.cell(row= fila, column= 1).value).replace('1900-01-01 ', ' '), '%Y-%m-%d %H:%M:%S')).replace(' ', '-').replace(':', '-')
    fecha_nueva = str(datetime.strptime(str(ws.cell(row= fila, column= 0).value).replace(' 00:00:00', '') + " " + str(ws.cell(row= fila, column= 1).value).replace('1900-01-01 ', ' '), '%Y-%m-%d %H:%M:%S'))
    if drug.findall(str(ws.cell(row= fila, column= 2).value)) == []:
        #crea el subelement paciente
        pac = SubElement(drug, str(ws.cell(row= fila, column= 2).value), name= str(ws.cell(row= fila, column= 2).value))
        #crea la nueva fecha fecha celda a1 sin hora 00 y se le adjunta la hora de la celda b1
        nueva_fecha = str(datetime.strptime(str(ws.cell(row= fila, column= 0).value).replace(' 00:00:00', '') + " " + str(ws.cell(row= fila, column= 1).value).replace('1900-01-01 ', ' '), '%Y-%m-%d %H:%M:%S')).replace(' ', '-').replace(':', '-')
        fecha_nueva = str(datetime.strptime(str(ws.cell(row= fila, column= 0).value).replace(' 00:00:00', '') + " " + str(ws.cell(row= fila, column= 1).value).replace('1900-01-01 ', ' '), '%Y-%m-%d %H:%M:%S'))
        #crea el subelement fecha
        fecha = SubElement(pac, nueva_fecha, name= fecha_nueva)
        #se deben detectar combinaciones y separarlas por "_"
        if "_" in str(ws.cell(row= fila, column= 3).value):
            for subfarmaco in str(ws.cell(row= fila, column= 3).value).split("_"):
                submedicamento = SubElement(fecha, subfarmaco, name= subfarmaco)
        else:
            medicamento = SubElement(fecha, str(ws.cell(row= fila, column= 3).value), name= str(ws.cell(row= fila, column= 3).value))
    elif drug.findall('./' + str(ws.cell(row= fila, column= 2).value) + '/' + str(nueva_fecha)) == []:
        #detecta el paciente ya existente
        pac = drug.findall('./' + str(ws.cell(row= fila, column= 2).value))[0]
        #igual, crear nueva fecha
        nueva_fecha = str(datetime.strptime(str(ws.cell(row= fila, column= 0).value).replace(' 00:00:00', '') + " " + str(ws.cell(row= fila, column= 1).value).replace('1900-01-01 ', ' '), '%Y-%m-%d %H:%M:%S')).replace(' ', '-').replace(':', '-')
        fecha_nueva = str(datetime.strptime(str(ws.cell(row= fila, column= 0).value).replace(' 00:00:00', '') + " " + str(ws.cell(row= fila, column= 1).value).replace('1900-01-01 ', ' '), '%Y-%m-%d %H:%M:%S'))
        fecha = SubElement(pac, nueva_fecha, name= fecha_nueva)
        if "_" in str(ws.cell(row= fila, column= 3).value):
            for subfarmaco in str(ws.cell(row= fila, column= 3).value).split("_"):
                submedicamento = SubElement(fecha, subfarmaco, name= subfarmaco)
        else:
            medicamento = SubElement(fecha, str(ws.cell(row= fila, column= 3).value), name= str(ws.cell(row= fila, column= 3).value))
    else:
        if "_" in str(ws.cell(row= fila, column= 3).value):
            for subfarmaco in str(ws.cell(row= fila, column= 3).value).split("_"):
                submedicamento = SubElement(fecha, subfarmaco, name= subfarmaco)
        else:
            medicamento = SubElement(fecha, str(ws.cell(row= fila, column= 3).value), name= str(ws.cell(row= fila, column= 3).value))
    #print fila,


# In[15]:

tree = ET.ElementTree(drug)
tree.write("drug.xml")


# In[5]:

lista_24 = []
lista_48 = []
lista_6 = []
for elemento in xrange(1,len(drug.getchildren())):
#for elemento in xrange(1,20):
    for subelemento in drug.getchildren()[elemento]:
        for subelemento_2 in drug.getchildren()[elemento]:
            date_1 = datetime.date(datetime.strptime(subelemento.get('name'), '%Y-%m-%d %H:%M:%S'))
            date_2 = datetime.date(datetime.strptime(subelemento_2.get('name'), '%Y-%m-%d %H:%M:%S'))
            date_4 = datetime.strptime(subelemento_2.get('name'), '%Y-%m-%d %H:%M:%S')
            mas_seis = datetime.strptime(subelemento.get('name'), '%Y-%m-%d %H:%M:%S') + timedelta(hours=6)
            menos_seis = datetime.strptime(subelemento.get('name'), '%Y-%m-%d %H:%M:%S') - timedelta(hours=6)
            
            if date_1 == date_2:
                for medicamento in subelemento.getchildren():
                    for medicamento_2 in subelemento_2.getchildren():
                        if medicamento.get('name') == medicamento_2.get('name'):
                            pass
                        else:
                            med_lista_24 = medicamento.get('name') + "_" + medicamento_2.get('name')
                            med_lista_24 = sorted(med_lista_24.split('_'), key=str.lower)
                            med_lista_24 = '_'.join(med_lista_24)
                            lista_24.append(med_lista_24)
            elif date_1 + timedelta(days=2) == date_2:
                for medicamento in subelemento.getchildren():
                    for medicamento_2 in subelemento_2.getchildren():
                        if medicamento.get('name') == medicamento_2.get('name'):
                            pass
                        else:
                            med_lista_48 = medicamento.get('name') + "_" + medicamento_2.get('name')
                            med_lista_48 = sorted(med_lista_48.split('_'), key=str.lower)
                            med_lista_48 = '_'.join(med_lista_48)
                            lista_48.append(med_lista_48)
            elif menos_seis < date_4 and mas_seis > date_4:
                for medicamento in subelemento.getchildren():
                    for medicamento_2 in subelemento_2.getchildren():
                        if medicamento.get('name') == medicamento_2.get('name'):
                            pass
                        else:
                            med_lista_6 = medicamento.get('name') + "_" + medicamento_2.get('name')
                            med_lista_6 = sorted(med_lista_6.split('_'), key=str.lower)
                            med_lista_6 = '_'.join(med_lista_6)
                            lista_6.append(med_lista_6)

#lista_24 = list(set(lista_24))
#lista_48.extend(lista_24)
#lista_48 = list(set(lista_48))
#lista_6 = list(set(lista_6))
#print len(lista_24), lista_24
#print len(lista_48), lista_48
#print len(lista_6), lista_6


# In[6]:

with open("combinaciones_24h_noSorted.txt", "w") as f:
    for x in lista_24:
        f.write(x+"\n")
    f.close()
with open("combinaciones_48_noSorted.txt", "w") as f:
    for x in lista_48:
        f.write(x+"\n")
    f.close()
with open("combinaciones_6_noSorted.txt", "w") as f:
    for x in lista_6:
        f.write(x+"\n")
    f.close()


# In[85]:

lista_med_med = []
import re
regex = re.compile("[a-z]")
regex_2 = re.compile('[0-9]')
for index in xrange(1, 5241):
#for index in range(1, ws.get_highest_row()-1):
    if len(drug.getchildren()[index].getchildren()[0].getchildren()) >= 2:
        for medicamento in drug.getchildren()[index].getchildren()[0].getchildren():
            for medicamento_2 in drug.getchildren()[index].getchildren()[0].getchildren():
                if medicamento == medicamento_2:
                    continue
                else:
                    a = regex.sub(r'', str(medicamento).replace('<Element ', '').replace('\'', '').replace(' at ','').replace('>', ''))
                    a = regex_2.sub(r'', a)
                    b = regex.sub(r'', str(medicamento_2).replace('<Element ', '').replace('\'', '').replace(' at ','').replace('>', ''))
                    b = regex_2.sub(r'', b)
                    lista_med_med.append(a + "_" + b)
#lista_med_med = list(set(lista_med_med))


# In[86]:

with open("intreacciones_cic_no_depurado.txt", "w") as f:
    for x in lista_med_med:
        f.write(x+"\n")
    f.close()


# In[4]:

#Creacion de lista de interacciones obtenidas de drugbank_2, 
#perfil corresponde a los medicamentos de la cic, 
#se realiza lectura del .xml de drugbank y se detectan todas la posibles interacciones, buscando el nombre de un medicamento
#dentro de la base de datos, si no lo encuentra dentro del nombre del medicamento, lo busca en los nombres sinoni

perfil = np.loadtxt("lista_med_cic.txt", delimiter="\t", dtype="string", unpack=True)
perfil = list(perfil)


# In[5]:

drugbank = ET.ElementTree(file='drugbank_2.xml')


# In[5]:

root = ET.parse('drugbank_2.xml').getroot()


# In[6]:

lista_interact = []
lista_no_encontrados = []
for farmaco in perfil:
    for i in xrange(0, len(root),1):
        #Busca en el nombre
        try:
            drug_name = root.getchildren()[i].findall('{http://www.drugbank.ca}name')
            if farmaco.lower() in drug_name[0].text.lower():
                #print drug_name[0].text
                try:
                    interaccion = root.getchildren()[i].findall('{http://www.drugbank.ca}drug-interactions')
                    for j in xrange(0,len(interaccion[0])):
                        interaccion_1 = interaccion[0].getchildren()[j].getchildren()[1].text.lower() + "_" + drug_name[0].text.lower()
                        interaccion_1 = sorted(interaccion_1.split('_'), key=str.lower)
                        interaccion_1 = '_'.join(interaccion_1)
                        lista_interact.append(interaccion_1 + '\t' + interaccion[0].getchildren()[j].getchildren()[2].text.lower())
                except:
                    #Busca en sinonimos
                    try: 
                        for sinonimo in root.getchildren()[i].find('{http://www.drugbank.ca}synonyms').getchildren():
                            if farmaco.lower() in sinonimo.text.lower():
                                try:
                                    interaccion = root.getchildren()[i].findall('{http://www.drugbank.ca}drug-interactions')
                                    for j in xrange(0,len(interaccion[0])):
                                        interaccion_1 = interaccion[0].getchildren()[j].getchildren()[1].text.lower() + "_" + drug_name[0].text.lower()
                                        interaccion_1 = sorted(interaccion_1.split('_'), key=str.lower)
                                        interaccion_1 = '_'.join(interaccion_1)
                                        lista_interact.append(interaccion_1 + '\t' + interaccion[0].getchildren()[j].getchildren()[2].text.lower())
                                except:
                                    pass
                    except:
                        pass
            else:
                lista_no_encontrados.append(farmaco.lower())
        except:
            pass

