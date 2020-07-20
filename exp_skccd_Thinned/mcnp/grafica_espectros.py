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


def escribe_espectros(archivo, tal, datos):
    nombre_out = 'espectro_' + archivo.split('.')[0] + '_' + tal + '.dat'
    np.savetxt(nombre_out, datos, fmt=['%1.4e', '%1.5e', '%1.4e'])
    return None


if __name__ == '__main__':

    archivos = [
                'skccd_thinned.o',
               ]
    labels = [
              'Flujo de partículas',
              ]
    fig_n, ax_n = plt.subplots(1, 1, figsize=(8, 6))
    fig_p, ax_p = plt.subplots(1, 1, figsize=(8, 6))
    tals = {'neutrones': '14', 'fotones': '514'}
    axs = [ax_n, ax_p]
    for archivo, label in zip(archivos, labels):
        datos, nombre, bins = lee_tally_E_card(archivo)
        for key, ax in zip(tals.keys(), axs):
            escribe_espectros(archivo, key, datos[tals[key]])
            eng = datos[tals[key]][:, 0]
            val = datos[tals[key]][:, 1]
            std_val = datos[tals[key]][:, 2] * val
            bin_limits = bins[tals[key]]
            # Calcula ancho del bin
            bin_width = np.diff(bin_limits, axis=1)[:, 0]
            # Normalizo con ancho del bin
            val = val / bin_width
            std_val = std_val / bin_width
            ax.errorbar(eng, val, yerr=std_val, label=label,
                        drawstyle='steps-mid')

    for ax in axs:
        ax.set_xlabel('Energía [MeV]')
        ax.set_ylabel('# particulas 1/MeV/source')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend()
    ax_p.set_xlim(5e-4, 15)
    ax_n.set_xlim(5e-4, 25)

    ax_n.set_title('Neutrones a 6" de la fuente')
    ax_p.set_title('Fotones a 6" de la fuente')
    fig_n.savefig('espectros_neutrones.png')
    fig_p.savefig('espectros_fotones.png')

    plt.show()
