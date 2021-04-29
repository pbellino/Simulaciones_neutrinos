#!/usr/bin/env python3

import numpy as np
import os
import subprocess

def corre_phits_single(X):
    """
    Function to run a single configuration of the shield

    TODO
    """
    # Diccionario con codificación para materiales
    # keys are the variables used by pymoo, and values are:
    # ('material number at input file', 'density of mat', 'id of material')
    mat_dict = {
                1: ('1', '-15.6', "208Pb"),
                2: ('2', '-8.96', "63Cu"),
                3: ('3', '-7.87', "56Fe"),
                4: ('4', '-2.33', "28Si"),
                5: ('5', '-2.70', "27Al"),
               }

    # Variables del problema
    # Ancho de cada material
    d1, d2, d3 = X[0:3]
    d_detector = 2
    # Típo de material (ver mat_dict)
    n1, n2, n3 = X[3:6]
    # Posiciones relativas de los materiales
    x = np.cumsum([d1, d2, d3, d_detector])

    # Directorio desde donde se corre
    parent = os.getcwd()
    # Carpeta donde se guardarán las corridas
    if not os.path.exists("runs"):
        os.mkdir("runs")
    # Nombre de la carpeta para cada corrida
    i = np.random.randint(10000)
    i_str = str(i).zfill(5)
    run_folder = os.path.join(parent, "runs", i_str)

    # Renombra si la carpeta ya existe que ya existe
    while os.path.exists(run_folder):
        i += 1
        i_str = str(i).zfill(4)
        run_folder = os.path.join(parent, "runs", i_str)

    # Leo archivo master
    with open("input_master", 'r') as f:
        master = f.readlines()
    # Se genera input para las variables
    os.mkdir(run_folder)
    os.chdir(run_folder)
    with open(i_str, 'w') as f:
        for line in master:
            # Escribe materiales
            if line.startswith("@@@MAT1"):
                f.write("  10 " + ' '.join(mat_dict[n1][0:2]) + " 2 -3 -999\n")
            elif line.startswith("@@@MAT2"):
                f.write("  11 " + ' '.join(mat_dict[n2][0:2]) + " 3 -4 -999\n")
            elif line.startswith("@@@MAT3"):
                f.write("  12 " + ' '.join(mat_dict[n3][0:2]) + " 4 -5 -999\n")
            # Escribe superficies
            elif line.startswith("@@@SUP1"):
                f.write("   3  pz  " + str(x[0]) + '\n')
            elif line.startswith("@@@SUP2"):
                f.write("   4  pz  " + str(x[1]) + '\n')
            elif line.startswith("@@@SUP3"):
                f.write("   5  pz  " + str(x[2]) + '\n')
            # Escribe detector
            elif line.startswith("@@@DET"):
                f.write("   998  pz " + str(x[-1]) + '\n')
            else:
                f.write(line)

    # Se corre el programa
    command = "phits.sh " + i_str
    p1 = subprocess.Popen(command.split(), stdout=subprocess.DEVNULL)
    p1.wait()

    # Se lee la salida
    with open("deposit.out", 'r') as f:
        for line in f:
            if line.startswith("#  num"):
                out = f.readline().split()[-2:]

    # Se vuelve a directorio principal
    os.chdir(parent)
    return out[0]

if __name__ == "__main__":

    out = corre_phits_single([10.0, 10.0, 10.0, 1, 1, 1])
    print(out)
