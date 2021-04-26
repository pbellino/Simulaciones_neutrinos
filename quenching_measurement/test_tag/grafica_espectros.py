#!/usr/bin/env python3

"""
Script para leer y graficar espectros de corriente sobre superficies
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append('/home/pablo/CinePy/')
from modules.io_modules import lee_tally_E_card, lee_tally_E_card_tagged
sns.set()


def escribe_espectros(archivo, tal, datos):
    nombre_out = 'espectro_' + archivo.split('.')[0] + '_' + tal + '.dat'
    np.savetxt(nombre_out, datos, fmt=['%1.4e', '%1.5e', '%1.4e'])
    return None


if __name__ == '__main__':

    # archivo = 'med_plomo.o'
    # archivo = 'med_poly.o'
    archivo = 'med_acero.o'
    labels = [
              'Particle current over surface',
              ]
    fig_n, ax_n = plt.subplots(1, 1, figsize=(8, 6))
    fig_p, ax_p = plt.subplots(1, 1, figsize=(8, 6))
    tals = {
            'neutrones': ['11', '21'],
            'fotones': ['501', '511']}
    datos, nombre, bins = lee_tally_E_card_tagged(archivo)
    tag_codes = {
                 '0.00000': "Scattered",
                 '82208.00000': '208Pb all',
                 '82000.00003': 'Fluorescence from Pb',
                 '82000.00005': 'Compton from Pb',
                 '0.00001': 'Bremsstrahlung e',
                 '10000000000.00000': 'Everything else',
                 'total': 'total',
                 '1001.00000': '1H all',
                 '1000.00005': 'Compton from H',
                 '6000.00005': 'Compton from C',
                 '6000.00000': 'nat C all nuc?',
                 '24000.00000': 'Cr all nuc',
                 '26000.00000': 'Fe all nuc',
                 '28000.00000': 'Ni all nuc',
                 '14000.00000': 'Si all nuc',
                 '25000.00000': 'Mn all nuc',
                 }
    axs = [ax_n, ax_p]
    for key, ax in zip(tals.keys(), axs):
        for talkey in tals[key]:
            for tag in datos[talkey].keys():
                # escribe_espectros(archivo, talkey, datos[talkey])
                eng = datos[talkey][tag][:, 0]
                val = datos[talkey][tag][:, 1]
                std_val = datos[talkey][tag][:, 2] * val
                bin_limits = bins[talkey]
                # Calcula ancho del bin
                bin_width = np.diff(bin_limits, axis=1)[:, 0]
                # Normalizo con ancho del bin
                # val = val / bin_width
                # std_val = std_val / bin_width
                ax.errorbar(eng, val, yerr=std_val,
                            label=talkey + '(' + tag_codes.get(tag, ' ') + ')',
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
