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
from modules.simulacion_modules import lee_espectro_phits_eng
sns.set()


if __name__ == '__main__':

    archivo = 'mcnp/skccd_depo.o'
    labels = [
               'Total',
              ]
    labels = ['MCNP-' + s for s in labels]
    tallies = [
               '918',
              ]
    normaliza = True
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    start = 2
    for tal, label in zip(tallies, labels):
        datos, nombre, bins = lee_tally_E_card(archivo)
        eng = datos[tal][start:, 0]
        val = datos[tal][start:, 1]
        std_val = datos[tal][start:, 2] * val
        if normaliza:
            bin_limits = bins[tal]
            # Calcula ancho del bin
            bin_width = np.diff(bin_limits, axis=1)[start:, 0]
            # Normalizo con ancho del bin
            val = val / bin_width
            std_val = std_val / bin_width
        (_, caps, _) = ax.errorbar(eng, val, yerr=std_val, fmt='.-',
                                   label=label)
    for cap in caps:
        cap.set_markeredgewidth(1)


###################

    archivo = 'phits/deposit_Si.out'
    zona = '103'

    # particles = ['30Si', '31Si', 'positron', 'electron', 'all']
    particles = ['all']

    data = lee_espectro_phits_eng(archivo, zona)
    normaliza = True
    # Puntos centrados en el bin
    eng = (data['e-lower'] + data['e-upper']) / 2.
    for part in particles:
        val = data[part][:, 0]
        std_val = val * data[part][:, 1]
        if normaliza:
            bin_width = data['e-upper'] - data['e-lower']
            # Normalizo con ancho del bin
            val = val / bin_width
            std_val = std_val / bin_width

        (_, caps, _) = ax.errorbar(eng, val, yerr=std_val, fmt='.-',
                                   label='PHITS-'+part, capsize=3,
                                   )
        for cap in caps:
            cap.set_markeredgewidth(1)

    # ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Energy [MeV]')
    ax.set_ylabel('Number [1/MeV/source]')
    # ax.set_ylim(1e-7, 1e3)
    ax.legend()

    title_str = 'Deposited energy in $^{28}$Si by $^{252}$Cf'
    title_str += '\n (without photons from the source)'
    fig.gca().set_title(title_str)

    fig.savefig('deposited_Si_comp.png')
    plt.show()

