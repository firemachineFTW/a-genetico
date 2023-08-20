from flask import Flask, render_template, request, jsonify

import math
import random

app = Flask(__name__)

def poblacion_inicial(max_poblacion, num_vars):
    poblacion = []
    for i in range(max_poblacion):
        gen = []
        for j in range(num_vars):
            if random.random() > 0.5:
                gen.append(1)
            else:
                gen.append(0)
        poblacion.append(gen[:])
    return poblacion

def adaptacion_3sat(gen, solucion):
    n = 3
    cont = 0
    clausula_ok = True
    for i in range(len(gen)):
        n = n - 1
        if gen[i] != solucion[i]:
            clausula_ok = False
            if n == 0:
                if clausula_ok:
                    cont = cont + 1
                n = 3
                clausula_ok = True
        if n == 0:
            if clausula_ok:
                cont = cont + 1
            n = 3
            clausula_ok = True
    return cont

def evalua_poblacion(poblacion, solucion):
    adaptacion = []
    for i in range(len(poblacion)):
        adaptacion.append(adaptacion_3sat(poblacion[i], solucion))
    return adaptacion

def seleccion(poblacion, solucion):
    adaptacion = evalua_poblacion(poblacion, solucion)
    total = sum(adaptacion)
    val1 = random.randint(0, total)
    val2 = random.randint(0, total)
    sum_sel = 0
    gen1 = []
    gen2 = []
    for i in range(len(adaptacion)):
        sum_sel = sum_sel + adaptacion[i]
        if sum_sel >= val1 and not gen1:
            gen1 = poblacion[i]
        if sum_sel >= val2 and not gen2:
            gen2 = poblacion[i]
        if gen1 and gen2:
            break
    return gen1, gen2

def cruce(gen1, gen2):
    corte = random.randint(1, len(gen1) - 1)
    nuevo_gen1 = gen1[:corte] + gen2[corte:]
    nuevo_gen2 = gen2[:corte] + gen1[corte:]
    return nuevo_gen1, nuevo_gen2

def mutacion(prob, gen):
    if random.random() < prob:
        cromosoma = random.randint(0, len(gen) - 1)
        gen[cromosoma] = 1 - gen[cromosoma]
    return gen

def elimina_peores_genes(poblacion, solucion):
    adaptacion = evalua_poblacion(poblacion, solucion)
    for _ in range(2):
        i = adaptacion.index(min(adaptacion))
        del poblacion[i]
        del adaptacion[i]

def mejor_gen(poblacion, solucion):
    adaptacion = evalua_poblacion(poblacion, solucion)
    return poblacion[adaptacion.index(max(adaptacion))]

def algoritmo_genetico():
    max_iter = 10
    max_poblacion = 50
    num_vars = 20
    fin = False
    solucion = poblacion_inicial(1, num_vars)[0]
    poblacion = poblacion_inicial(max_poblacion, num_vars)
    
    iteraciones = 0
    while not fin:
        iteraciones = iteraciones + 1
        for i in range(len(poblacion) // 2):
            gen1, gen2 = seleccion(poblacion, solucion)
            nuevo_gen1, nuevo_gen2 = cruce(gen1, gen2)
            nuevo_gen1 = mutacion(0.1, nuevo_gen1)
            nuevo_gen2 = mutacion(0.1, nuevo_gen2)
            poblacion.append(nuevo_gen1)
            poblacion.append(nuevo_gen2)
            elimina_peores_genes(poblacion, solucion)
        if max_iter <= iteraciones:
            fin = True
    print("Solucion: " + str(solucion))
    mejor = mejor_gen(poblacion, solucion)
    return mejor, adaptacion_3sat(mejor, solucion)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/algoritmo_genetico', methods= ['GET', 'POST'])
def a_genetico():
    random.seed()
    mejor_gen = algoritmo_genetico()
    return jsonify({
        'mejor_gen': mejor_gen[0],
        'funcion_adaptacion': mejor_gen[1]
    })
    
if __name__ == "__main__":
    app.run(debug = False, host = '0.0.0.0')