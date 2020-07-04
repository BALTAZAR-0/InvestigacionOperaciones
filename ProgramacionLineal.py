# -*- coding: utf-8 -*-

from sympy import solve, Poly, Eq, Function, exp, Lambda
from sympy import plot_implicit, cos, sin, symbols, Eq, And, Or,Point, Point2D
from operator import itemgetter, attrgetter, methodcaller
from plot_points import plot_point
from ConfigParser import ConfigParser

config = ConfigParser()
#config.read("arc_config.cfg")
#config.read("5x1plus7x2.conf")
config.read("primal1.conf")
#config.read("dual1.conf")
#config.read("primal2.conf")
#config.read("dual2.conf")
#config.read("x1plus2x2.conf")
#config.read("solucion_infactible.conf")


parametros_incompletos = False
listado_restricciones = []
listado_ecuaciones = []
listado_rectas = []


x, y = symbols('x y')

if config.has_section('Restricciones'):

    print 'Con las restricciones: '
    for restriccion in config.options('Restricciones'):
        str_restriccion = config.get("Restricciones",restriccion)
        print str_restriccion
        inecuacion = eval('Lambda((x, y), '+str_restriccion+')')
        listado_restricciones.append(inecuacion)
        listado_ecuaciones.append(eval('Lambda((x, y),' + str(inecuacion._args[1]._args[0]) + '-1*(' + str(inecuacion._args[1]._args[1]).replace(' ','') + '))'))


else:
    parametros_incompletos = True

str_objectivo = ''
if config.has_section('FuncionObjetivo'):
    str_objectivo = config.get("FuncionObjetivo",'Objetivo')
    print 'La ecuacion Objetivo: '+str_objectivo
else:
    parametros_incompletos = True

EsMaximizar = False

if config.has_section('TipoOptimizacion'):
    bool_Maximizar = config.getboolean("TipoOptimizacion",'Maximizar')
    bool_Minimizar = config.getboolean("TipoOptimizacion",'Minimizar')

    if (bool_Maximizar and bool_Minimizar)or ((not bool_Maximizar) and (not bool_Minimizar)):
        parametros_incompletos = True

    EsMaximizar = bool_Maximizar
else:
    parametros_incompletos = True


if parametros_incompletos:
    print 'Parametros incompletos'
    exit(1)



funcion_objetivo = eval('Lambda((x, y), '+str_objectivo+')')


listado_funciones = [listado_restricciones,listado_ecuaciones]
puntos_validos = []

distancia = 0
puntos_grafica = []

for ecuacion in listado_funciones[1]:
    for ecuacion2 in  listado_funciones[1]:
        if ecuacion != ecuacion2:
            solucion_ecuacion = solve([ecuacion(x,y),ecuacion2(x,y)],[x,y])
            if solucion_ecuacion != []:
                if (solucion_ecuacion[x],solucion_ecuacion[y]) not in puntos_grafica:
                   puntos_grafica.append((solucion_ecuacion[x],solucion_ecuacion[y]))

                validacion = True
                for restriccion in listado_funciones[0]:
                    validacion = validacion and restriccion(solucion_ecuacion[x],solucion_ecuacion[y]);

                if validacion:

                    if (solucion_ecuacion[x],solucion_ecuacion[y]) not in puntos_validos:
                        puntos_validos.append((solucion_ecuacion[x],solucion_ecuacion[y]))


puntos_graficar_x = []
puntos_graficar_y = []
puntos_graficar_x_y = []




puntos = sorted(puntos_validos, key=itemgetter(0,1))
puntos_z = []
Max = -1000000000
Min = 1000000000
#print Max, Min
punto_optimizacion = []
punto_2d = None
Max_p = None
Min_p = None

if puntos != []:
    for punto in puntos:
        puntos_graficar_x_y.append(Point2D(punto[0],punto[1]))
        puntos_z = float(funcion_objetivo(punto[0],punto[1])), (punto[0],punto[1])
        #print funcion_objetivo(punto[0],punto[1])

        if funcion_objetivo(punto[0],punto[1]) > Max:
            Max = funcion_objetivo(punto[0],punto[1])
            Max_p = Point2D(punto[0],punto[1])

        if funcion_objetivo(punto[0],punto[1]) < Min:
            Min = funcion_objetivo(punto[0],punto[1])
            Min_p = Point2D(punto[0],punto[1])

    if (EsMaximizar):
        texto = '\n\nSolucion Unica Factible\nEl maximo es %f, en el punto %s' % (Max, Max_p)
        punto_optimizacion.append(Max_p)
        punto_2d = Max_p

    else:
        texto = '\n\nSolucion Unica Factible\nEl minimo es %f, en el punto %s' % (Min, Min_p)
        punto_optimizacion.append(Min_p)
        punto_2d = Min_p


    x_plus_010 = punto[0]*1.10
    y_plus_010 = punto[1]*1.10

    x_min_010 = punto[0]*0.90
    y_min_010 = punto[1]*0.90

    x_valor = punto[0]
    y_valor = punto[1]

    validacion = True

    for restriccion in listado_funciones[0]:
        validacion = validacion and restriccion(x_valor, y_plus_010);

    if validacion:
        if EsMaximizar:
            if funcion_objetivo(x_valor, y_plus_010) >= Max:
                texto = 'Solucion Ilimitada'
        elif funcion_objetivo(x_valor, y_plus_010) <= Min:
                texto = 'Solucion Ilimitada'

    for restriccion in listado_funciones[0]:
        validacion = validacion and restriccion(x_valor, y_min_010);

    if validacion:
        if EsMaximizar:
            if funcion_objetivo(x_valor, y_min_010) >= Max:
                texto = 'Solucion Ilimitada'
        elif funcion_objetivo(x_valor, y_min_010) <= Min:
                texto = 'Solucion Ilimitada'

    for restriccion in listado_funciones[0]:
        validacion = validacion and restriccion(x_min_010, y_plus_010);

    if validacion:
        if EsMaximizar:
            if funcion_objetivo(x_min_010, y_plus_010) >= Max:
                texto = 'Solucion Ilimitada'
        elif funcion_objetivo(x_min_010, y_plus_010) <= Min:
                texto = 'Solucion Ilimitada'

    for restriccion in listado_funciones[0]:
        validacion = validacion and restriccion(x_min_010, y_min_010);

    if validacion:
        if EsMaximizar:
            if funcion_objetivo(x_min_010, y_min_010) >= Max:
                texto = 'Solucion Ilimitada'
        elif funcion_objetivo(x_min_010, y_min_010) <= Min:
                texto = 'Solucion Ilimitada'

    for restriccion in listado_funciones[0]:
        validacion = validacion and restriccion(x_min_010, y_valor);

    if validacion:
        if EsMaximizar:
            if funcion_objetivo(x_min_010, y_valor) >= Max:
                texto = 'Solucion Ilimitada'
        elif funcion_objetivo(x_min_010, y_valor) <= Min:
                texto = 'Solucion Ilimitada'

    for restriccion in listado_funciones[0]:
        validacion = validacion and restriccion(x_plus_010, y_plus_010);

    if validacion:
        if EsMaximizar:
            if funcion_objetivo(x_plus_010, y_plus_010) >= Max:
                texto = 'Solucion Ilimitada'
        elif funcion_objetivo(x_plus_010, y_plus_010) <= Min:
                texto = 'Solucion Ilimitada'

    for restriccion in listado_funciones[0]:
        validacion = validacion and restriccion(x_plus_010, y_min_010);

    if validacion:
        if EsMaximizar:
            if funcion_objetivo(x_plus_010, y_min_010) >= Max:
                texto = 'Solucion Ilimitada'
        elif funcion_objetivo(x_plus_010, y_min_010) <= Min:
                texto = 'Solucion Ilimitada'

    for restriccion in listado_funciones[0]:
        validacion = validacion and restriccion(x_plus_010, y_valor);

    if validacion:
        if EsMaximizar:
            if funcion_objetivo(x_plus_010, y_valor) >= Max:
                texto = 'Solucion Ilimitada'
        elif funcion_objetivo(x_plus_010, y_valor) <= Min:
                texto = 'Solucion Ilimitada'

else:
    texto = 'Solucion Infactible'





print texto

puntos = sorted(puntos_grafica, key=itemgetter(0))
x_min = puntos[0][0]*0.80

puntos = sorted(puntos_grafica, key=itemgetter(0), reverse=True)
x_max = puntos[0][0]*1.20


puntos = sorted(puntos_grafica, key=itemgetter(1))
y_min = puntos[0][1]*0.80

puntos = sorted(puntos_grafica, key=itemgetter(1), reverse=True)
y_max = puntos[0][1]*1.20

puntos_interseccion = []

for punto in puntos_grafica:
    puntos_interseccion.append(Point2D(punto[0],punto[1]))



anterior = None
anterior_ecuacion = None
inecuacion = None
ecuacion = None
grafica_texto = None


for restriccion in listado_funciones[0]:
    inecuacion = restriccion.args[1]
    #Conversion hacia ecuacion
    ecuacion = 'Eq(' + str(restriccion._args[1]._args[0]) + ',' + str(restriccion._args[1]._args[1]) + ')'
    if anterior == None:
        anterior = str(inecuacion)
        anterior_ecuacion = ecuacion
    else:
        anterior = 'And('+str(anterior)+','+str(inecuacion)+')'
        anterior_ecuacion = 'Or('+anterior_ecuacion+','+ecuacion+')'



lineas = "plot_implicit("+anterior_ecuacion+", (x, x_min, x_max), (y,y_min, y_max), show=False, line_color='black' )"
area = "plot_implicit("+anterior+", (x, x_min, x_max), (y,y_min, y_max), show=False, line_color='red' )"



grafica = eval(area)
limites = eval(lineas)
puntos_vertices = plot_point(puntos_graficar_x_y, (x, x_min, x_max), (y,y_min, y_max), show=False,  markedsize=10, tipomarca ='bo')
graf_puntos_interseccion =  plot_point(puntos_interseccion, (x, x_min, x_max), (y,y_min, y_max), show=False,  markedsize=10, tipomarca ='go')
graf_punto_optimizacion =  plot_point(punto_optimizacion, (x, x_min, x_max), (y,y_min, y_max), show=False,  markedsize=20, tipomarca ='yo')


grafica.extend(limites)
grafica.extend(graf_puntos_interseccion)
grafica.extend(puntos_vertices)
grafica.extend(graf_punto_optimizacion)
grafica.show()
