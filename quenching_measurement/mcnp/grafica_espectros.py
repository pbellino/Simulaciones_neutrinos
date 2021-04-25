#!/usr/bin/env python3

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

    #archivo = 'med_qf_poly.o'
    archivo = 'med_qf_vacio.o'
    labels = [
              'Particle current over surface',
              ]
    fig_n, ax_n = plt.subplots(1, 1, figsize=(8, 6))
    fig_p, ax_p = plt.subplots(1, 1, figsize=(8, 6))
    tals = {'neutrones': ['11', '21', '31', '41'],
            'fotones': ['501', '511', '521', '531']}
    axs = [ax_n, ax_p]
    datos, nombre, bins = lee_tally_E_card(archivo)
    for key, ax in zip(tals.keys(), axs):
        for talkey in tals[key]:
            # escribe_espectros(archivo, talkey, datos[talkey])
            eng = datos[talkey][:, 0]
            val = datos[talkey][:, 1]
            std_val = datos[talkey][:, 2] * val
            bin_limits = bins[talkey]
            # Calcula ancho del bin
            bin_width = np.diff(bin_limits, axis=1)[:, 0]
            # Normalizo con ancho del bin
            # val = val / bin_width
            # std_val = std_val / bin_width
            ax.errorbar(eng, val, yerr=std_val, label=talkey,
                        drawstyle='steps-mid')

    for ax in axs:
        ax.set_xlabel('Energy [MeV]')
        ax.set_ylabel('# particles [1/source]')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend(title='Tally')

    ax_n.set_title('Neutrons')
    ax_p.set_title('Photons')
    fig_n.savefig(archivo.rsplit('.')[0] + '_neutrons.png')
    fig_p.savefig(archivo.rsplit('.')[0] + '_photons.png')

    plt.show()
