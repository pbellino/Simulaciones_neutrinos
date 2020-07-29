#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para leer los resultados de cada corrida
TODO
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append('/home/pablo/CinePy/')
from modules.io_modules import lee_tally_E_card
sns.set()


if __name__ == '__main__':

    archivo = 'skccd.o'
    labels = [
              'In Pb',
              'In Cu (bottom)',
              'In Si',
              ]
    tallies = [
               '514',
               '524',
               '534',
              ]
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    for tal, label in zip(tallies, labels):
        datos, nombre, bins = lee_tally_E_card(archivo)
        eng = datos[tal][:, 0]
        val = datos[tal][:, 1]
        std_val = datos[tal][:, 2] * val
        bin_limits = bins[tal]
        # Calcula ancho del bin
        bin_width = np.diff(bin_limits, axis=1)[:, 0]
        # Normalizo con ancho del bin
        val = val / bin_width
        std_val = std_val / bin_width
        ax.errorbar(eng, val, yerr=std_val, fmt='.-', label=label,
                    drawstyle='steps-mid')
        ax.set_xlabel('Energy [MeV]')
        ax.set_ylabel('Flux [1 / cm$^2$ / MeV / SF]')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlim(8e-4, 2e1)
        ax.set_ylim(1e-8, 1e-2)

    ax.set_title('Photom spectrum (file ' + archivo + ')')
    ax.legend()
    nom_graf = 'espectros_fotones_'
    nom_graf += archivo.split('.')[0].split('_')[-1] + '.png'
    fig.savefig(nom_graf)
    plt.show()
