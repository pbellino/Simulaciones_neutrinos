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

    archivos = [
                'Pb0.o',
                'Pb1.o',
                'Pb2.o',
               ]
    labels = [
              'Sin mesa óptica y sin blindaje',
              'Con mesa óptica y sin blindaje',
              'Con mesa óptica y con blindaje',
              ]
    fig_n, ax_n = plt.subplots(1, 1, figsize=(8, 6))
    fig_p, ax_p = plt.subplots(1, 1, figsize=(8, 6))
    tals = ['11', '51']
    axs = [ax_n, ax_p]
    for archivo, label in zip(archivos, labels):
        datos, nombre, bins = lee_tally_E_card(archivo)
        for tal, ax in zip(tals, axs):
            eng = datos[tal][:, 0]
            val = datos[tal][:, 1]
            std_val = datos[tal][:, 2] * val
            bin_limits = bins[tal]
            # Calcula ancho del bin
            bin_width = np.diff(bin_limits, axis=1)[:, 0]
            # Normalizo con ancho del bin
            val = val / bin_width
            std_val = std_val / bin_width
            ax.errorbar(eng, val, yerr=std_val, fmt='.-', label=label)

    for ax in axs:
        ax.set_xlabel('Energía [MeV]')
        ax.set_ylabel('# particulas 1/MeV/source')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend()
    ax_p.set_xlim(5e-4, 1e2)

    ax_n.set_title('Neutrones a 6" de la fuente')
    ax_p.set_title('Fotones a 6" de la fuente')
    fig_n.savefig('espectros_neutrones.png')
    fig_p.savefig('espectros_fotones.png')

    plt.show()
