#!/usr/bin/env python3

"""
Script para leer y graficar salidas de MCNP guardadas en mctal

Se usa MCNPTools
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append('/home/pablo/CinePy/')
from modules.simulacion_modules import lee_tally_E_mcnptools
sns.set()


def escribe_espectros(archivo, tal, datos):
    nombre_out = 'espectro_' + archivo.split('.')[0] + '_' + str(tal) + '.dat'
    np.savetxt(nombre_out, datos, fmt=['%1.4e', '%1.5e', '%1.4e'])
    return None


if __name__ == '__main__':

    archivo = 'fuente.m'
    tallies = [
               11,
               81,
              ]
    labels = {11: 'Neutrones', 81: 'fotones'}
    fig_n, ax_n = plt.subplots(1, 1, figsize=(8, 6))
    fig_p, ax_p = plt.subplots(1, 1, figsize=(8, 6))
    axs = [ax_n, ax_p]
    for tally, ax in zip(tallies, axs):
        bins, val, err = lee_tally_E_mcnptools(archivo, tally)
        # escribe archivo de texto con espectros
        # escribe_espectros(archivo, tally, np.c_[bins, val, err])
        std_val = err * val
        # Calcula ancho del bin
        bin_width = np.diff(bins)
        # Centrado bin
        bin_cen = bins[:-1] + 0.5 * bin_width
        # Normalizo con ancho del bin y descarto primer dato
        val = val[1:] / bin_width
        std_val = std_val[1:] / bin_width
        ax.errorbar(bin_cen, val, yerr=std_val, label=labels[tally],
                    drawstyle='steps-mid')

    for ax in axs:
        ax.set_xlabel('Energía [MeV]')
        ax.set_ylabel('Particulas 1/MeV/source')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend()
    ax_p.set_xlim(5e-4, 15)
    ax_n.set_xlim(1e-6, 25)

    ax_n.set_title('Espectro de neutrones')
    ax_p.set_title('Espectro de fotones')
    fig_n.savefig('espectros_neutrones.png')
    fig_p.savefig('espectros_fotones.png')

    plt.show()
