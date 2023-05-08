import streamlit as st
import pandas as pd
import math as mt
import random as rd
import itertools as it
import altair as alt
import numpy as np

def calcular_bits(cantidad_puntos):
    n = 0
    while (mt.pow(2, n) <= cantidad_puntos):
        n = n+1 

    return n

def crear_individuos(poblacion):
    lista_individuos = []

    for indice in range(poblacion):
        solucion = 'i' + str(indice+1)    
        lista_individuos.append(solucion)

    return lista_individuos

def agregar_individuos(poblacion_muta, indice):
    lista_individuos = []
    for solucion in range(poblacion_muta):
        solucion = 'i' + str(indice)
        indice += 1
        lista_individuos.append(solucion)
    return lista_individuos

def crear_poblacion(poblacion, rango):
    lista_poblacion = []
    for solucion in range(poblacion):
        solucion = rd.randint(0, rango)
        lista_poblacion.append(solucion)
    return lista_poblacion

def decimal_a_binario(numero_decimal):
    numero_binario = 0
    multiplicador = 1

    while numero_decimal != 0:
        # se almacena el módulo en el orden correcto
        numero_binario = numero_binario + numero_decimal % 2 * multiplicador
        numero_decimal //= 2
        multiplicador *= 10

    return numero_binario

def obtener_binarios(lista_poblacion, cantidadBits):
    poblacion_binaria = []
    binario = ''
    for individuo in lista_poblacion:
        binario = str(decimal_a_binario(individuo))
        if len(binario) < cantidadBits:
          while len(binario) < cantidadBits:
            binario = '0' + binario 
        poblacion_binaria.append(binario)
    return poblacion_binaria

def binario_a_decimal(numero_binario):
	numero_decimal = 0 

	for posicion, digito_string in enumerate(numero_binario[::-1]):
		numero_decimal += int(digito_string) * 2 ** posicion

	return numero_decimal

def obtener_decimales(lista_binarios):
    lista_decimales = []
    decimal = 0
    for binario in lista_binarios:
        decimal = binario_a_decimal(binario)   
        lista_decimales.append(decimal)
    return lista_decimales 

def calcular_x(lista_poblacion, interval_a):
    lista_x = []
    for i in lista_poblacion:
        x = interval_a + (i * intervalo)
        lista_x.append(x)
    return lista_x


def calcular_funcion(lista_x, m):
    lista_funcion = []
    for x in lista_x:
        #y = (mt.cos(x*mt.pi)*mt.sin(x*mt.pi/2) + mt.log(x))
        y = mt.log(m + abs(x)) * mt.cos(x) * mt.sin(x/10)
        lista_funcion.append(y)
    return lista_funcion   

#Funciones ciclo
def seleccion(individuos):
    lista_seleccion = []

    tuplas = it.combinations(individuos, 2)


    for i in list(tuplas):
        lista_seleccion.append(i)

    return lista_seleccion

def crear_cruza(lista_seleccion, individuos, poblacion_binaria, cantidad_bits):
    random = 0
    mitad_bits = int(cantidad_bits/2)
    nueva_cadena = ''
    lista_cruza = []
    for x in lista_seleccion:
        random = rd.randint(0, 100)/100
        #st.write(x, random)
        if random <= probabilidadCruza:

            nueva_cadena = poblacion_binaria[individuos.index(x[0])][:mitad_bits] + poblacion_binaria[individuos.index(x[1])][mitad_bits:]
            lista_cruza.append(nueva_cadena)

    return lista_cruza

def crear_mutacion(lista_cruza, pmi, pmg):
    randomMuta = 0
    randomGen = 0
    nueva_cadena = ''
    indiceCadena = 0
    lista_mutacion = lista_cruza
    if len(lista_cruza) > 0:
        #ciclo para cada cadena binaria de la lista de los resultados de la cruza
        for cadena in lista_cruza:
            nueva_cadena = cadena
            randomMuta =  rd.randint(0,100)/100
            #st.write(cadena, randomMuta)
            if randomMuta <= pmi:
                #ciclo para cada digito de la cadena binaria
                for indiceBit in range(len(cadena)):
                    randomGen = rd.randint(0,100)/100
                    #st.write(cadena[indiceBit], randomGen)
                    if randomGen <= pmg:
                        if int(cadena[indiceBit]):
                            nueva_cadena = nueva_cadena[:indiceBit] + '0' + nueva_cadena[indiceBit+1:]
                        else:
                            nueva_cadena = nueva_cadena[:indiceBit] + '1' + nueva_cadena[indiceBit+1:]
                lista_mutacion[indiceCadena] = nueva_cadena
            indiceCadena += 1

    return lista_mutacion

def podar_limites(poblacion_x_muta, a, b):
    lista_poda_limites = []
    for indice in range(len(poblacion_x_muta)):
        if poblacion_x_muta[indice] < a or poblacion_x_muta[indice] > b:
            lista_poda_limites.append(indice)
    return lista_poda_limites

def podar_funcion(poblacion_funcion, lista_limites, poblacion_max):
    #llenar la lista de indices de 0 hasta n
    lista_indice = list(range(len(poblacion_funcion)))
    diccionario_indices = {}
    #poner los indices en el diccionario en orden de la poblacion
    for indice in range(len(poblacion_funcion)):
        diccionario_indices[lista_indice[indice]] = poblacion_funcion[indice]
    #Eliminar elementos que estan fuera de limites
    for elemento in lista_limites:
        diccionario_indices.pop(elemento)    
    #ordenar de forma decreciente el diccionario 
    sorted_dict = dict(sorted(diccionario_indices.items(), key=lambda item: item[1]))
    print("diccionario ordenado")
    print(sorted_dict)
    #quitar elementos del diccionario acorde al numero de poblacion maximca
    while(len(sorted_dict) > poblacion_max):
        sorted_dict.popitem()
    
    return sorted_dict

def podar_lista(lista, diccionario_poda):
    lista_poda = []
    for elemento in diccionario_poda:
        lista_poda.append(lista[elemento])
    return lista_poda

#Funciones interfaz
def crear_dataframe(individuos, poblacion_binaria, poblacion, poblacion_x, poblacion_funcion,):
    df_poblacion = pd.DataFrame(
        list( 
            zip (
                    individuos, poblacion_binaria, poblacion, poblacion_x, poblacion_funcion)
                ), 
                columns = ['individuo', 'cadena','valor', 'x', 'f(x)']
    )

    return df_poblacion

def crear_chart(df_poblacion):
    chartLine = alt.Chart(df_poblacion).mark_line().encode(
        x='x' , y='f(x)'
    ).interactive()
    chartCircle = alt.Chart(df_poblacion).mark_circle().encode(
        x='x', y='f(x)', color='individuo'
    )

    return (chartLine + chartCircle).interactive()

def get_chart_evolution(data):

    #Diccionario para seleccioinar un color especídfico
    color_dict = {'mejores': 'blue', 'peores': 'red', 'promedio': 'gray'}
    color_scale = alt.Scale(domain=list(color_dict.keys()), range=list(color_dict.values()))

    hover = alt.selection_single(
        fields=["generacion"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Evolucion de aptitud ")
        .mark_line()
        .encode(
            alt.X('generacion', axis=alt.Axis(tickMinStep=1)),
            alt.Y('aptitud'),
            #color="category",
            color=alt.Color('category:N', scale=color_scale),
        )
    )

    points = lines.transform_filter(hover).mark_circle(size=65)

    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="generacion",
            y="aptitud",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("generacion", title="Generacion"),
                alt.Tooltip("aptitud", title="Aptitud"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

#Variables
generacion = 0
#a = 10
#b = 20
intervalo = 1
m = 1
indice = 1

#cantidadBits = calcular_bits(cantidadPuntos)

listaEvolucion = []
listaGraficaGeneracion = []

st.title('Algoritmo genético')
st.header('Función:')
st.latex(
    r'''
        [ln(m + |x|)][cos(x)][sin(x/10)]
    '''
)

st.subheader('Ingrese los datos')
col1, col2 = st.columns([2,2])

col1.write('Datos población inicial')
interval_A = col1.number_input('Valor de A', step=1)
poblacionInical = col1.number_input('Población inicial', step=1)
poblacionMax = col1.number_input('Población máxima', step=1)
generaciones = col1.number_input('Generaciones', step=1)


col2.write('Datos cruza y mutación')
interval_B = col2.number_input('Valor de B', step=1)
probabilidadCruza = col2.number_input('Probabilidad de cruza')
probabilidadMutacion = col2.number_input('Probabilidad de mutación')
probabilidadGen = col2.number_input('Probabilidad de mutación de gen')
m = col1.number_input('Valor de m')

st.caption('Presione el botón para continuar')

#button 

if st.button('Botón'):

    rango = interval_B - interval_A
    cantidadPuntos = int((rango/intervalo) + 1)
    cantidadBits = calcular_bits(cantidadPuntos)

    st.write(f'Valor de a y b: [{interval_A} , {interval_B}]')
    st.write(f'Valor precisión: {intervalo}')
    st.write(f'rango: {rango}')
    st.write(f'cantidad de puntos: {cantidadPuntos}')
    st.write(f'cantidad de bits: {cantidadBits}')

    #Generación inicial

    individuos = crear_individuos(poblacionInical)
    poblacion = crear_poblacion(poblacionInical, rango)
    poblacionBinaria = obtener_binarios(poblacion, cantidadBits)
    poblacionX = calcular_x(poblacion, interval_A)
    poblacionFuncion = calcular_funcion(poblacionX, m)
    indice = int(individuos[-1][1:])+1 

    st.write('Generación incial')

    dfPoblacion = crear_dataframe(individuos, poblacionBinaria, poblacion, poblacionX, poblacionFuncion)
    dfPoblacion['generacion'] = generacion
    dfEvolucion = dfPoblacion 
    st.dataframe(dfPoblacion)
    st.altair_chart(crear_chart(dfPoblacion), use_container_width=True)

    diccionarioMejor = {
        'category' : 'mejores', 
        'generacion': generacion,
        'aptitud' : poblacionFuncion[-1],
        'x': poblacionX[-1]
    }
    diccionarioPromedio = {
        'category' : 'promedio', 
        'generacion': generacion,
        'aptitud' : np.mean(poblacionFuncion),
        'x': np.mean(poblacionX)
    }
    diccionarioPeor = {
        'category' : 'peores', 
        'generacion': generacion,
        'aptitud' : poblacionFuncion[0],
        'x': poblacionX[0]
    }

    listaEvolucion.append(diccionarioMejor) 
    listaEvolucion.append(diccionarioPromedio) 
    listaEvolucion.append(diccionarioPeor) 

    while generacion < generaciones:

        generacion += 1
        #Cruza
        listaSeleccion = seleccion(individuos)
        listaCruza = crear_cruza(listaSeleccion, individuos, poblacionBinaria, cantidadBits)

        #Mutación
        listaMutacion = crear_mutacion(listaCruza, probabilidadMutacion, probabilidadGen)
        poblacionMuta = obtener_decimales(listaMutacion)
        poblacionXMuta = calcular_x(poblacionMuta, interval_A)
        poblacionFuncionMuta = calcular_funcion(poblacionXMuta, m)
        individuosMuta = agregar_individuos(len(poblacionMuta), indice)
        indice = indice + len(individuosMuta)
        
        #Calcular aptitud
        individuos.extend(individuosMuta)
        poblacionBinaria.extend(listaMutacion)
        poblacion.extend(poblacionMuta)
        poblacionX.extend(poblacionXMuta)
        poblacionFuncion.extend(poblacionFuncionMuta)

        dfPoblacion = crear_dataframe(individuos, poblacionBinaria, poblacion, poblacionX, poblacionFuncion)
        dfPoblacion['generacion'] = generacion

        #poda
        listaLimites = podar_limites(poblacionX, interval_A, interval_B)
        if ((len(poblacion) > poblacionMax) or len(listaLimites) > 0):
            diccionario_poda = podar_funcion(poblacionFuncion, listaLimites, poblacionMax)
            individuos = podar_lista(individuos, diccionario_poda)
            poblacion = podar_lista(poblacion, diccionario_poda)
            poblacionBinaria = podar_lista(poblacionBinaria, diccionario_poda)
            poblacionX = podar_lista(poblacionX, diccionario_poda)
            poblacionFuncion = podar_lista(poblacionFuncion, diccionario_poda)

        dfPoblacion = crear_dataframe(individuos, poblacionBinaria, poblacion, poblacionX, poblacionFuncion)
        dfPoblacion['generacion'] = generacion
        dfEvolucion = pd.concat([dfEvolucion, dfPoblacion])
        listaGraficaGeneracion.append(dfPoblacion)

        st.write("Generacion: ", generacion)
        st.dataframe(dfPoblacion)
        st.altair_chart(crear_chart(dfPoblacion), use_container_width=True)

        diccionarioMejor = {
            'category' : 'mejores', 
            'generacion': generacion,
            'aptitud' : min(poblacionFuncion),
            'x': min(poblacionX)
        }
        diccionarioPromedio = {
            'category' : 'promedio', 
            'generacion': generacion,
            'aptitud' : np.mean(poblacionFuncion),
            'x': np.mean(poblacionX)
        }
        diccionarioPeor = {
            'category' : 'peores', 
            'generacion': generacion,
            'aptitud' : max(poblacionFuncion),
            'x': max(poblacionX)
        }
        listaEvolucion.append(diccionarioMejor) 
        listaEvolucion.append(diccionarioPromedio) 
        listaEvolucion.append(diccionarioPeor) 

    # st.write(listaEvolucion)
    dfEvolution = pd.DataFrame(listaEvolucion)

    chartEvolution = get_chart_evolution(dfEvolution)
    st.altair_chart((chartEvolution).interactive(), use_container_width=True)
################################
    sliderGeneracion = alt.binding_range(min=0, max=generaciones, step=1, name='generacion: ')
    selectorGeneracion = alt.selection_single(name="SelectorName", fields=['generacion'], bind=sliderGeneracion, init={'generacion': 0})
    
    chartSliderGeneracionPoint = alt.Chart(dfEvolucion).mark_point().encode(
        alt.X('x', axis=alt.Axis(tickMinStep=1), scale=alt.Scale(domain=[interval_A, interval_B])),
        y='f(x)',
        color='individuo'
    )
    
    chartSliderGeneracionLine = alt.Chart(dfEvolucion).mark_line().encode(
        alt.X('x', axis=alt.Axis(tickMinStep=1), scale=alt.Scale(domain=[interval_A, interval_B])),
        y='f(x)',
    )
    
    st.altair_chart((chartSliderGeneracionPoint + chartSliderGeneracionLine).add_selection(selectorGeneracion).transform_filter(selectorGeneracion).interactive(), use_container_width=True)

    
