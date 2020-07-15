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
                'skccd_depo_pCf.o',
                'skccd_depo.o',
                ]
    labels = [
              'With photons from Cf',
              'Without photons from Cf',
              ]
    tally = '518'
    # tallies = [
    #            '18',
    #            '518',
    #            '918',
    #           ]
    fig, axs = plt.subplots(1, 2, figsize=(10, 6), sharey=True)
    start = 2  # Punto al parti del cual se grafica (para los bines negativos)
    normaliza = True  # Se divide por el bin de energía
    limits = [
               [0, 3e-2],
               [0, 1]
             ]
    for arch, label in zip(archivos, labels):
        datos, nombre, bins = lee_tally_E_card(arch)
        eng = datos[tally][start:, 0]
        val = datos[tally][start:, 1]
        std_val = datos[tally][start:, 2] * val
        if normaliza:
            bin_limits = bins[tally]
            # Calcula ancho del bin
            bin_width = np.diff(bin_limits, axis=1)[start:, 0]
            # Normalizo con ancho del bin
            val = val / bin_width
            std_val = std_val / bin_width
            ylabel = 'Events / MeV / SF'
        else:
            ylabel = 'Events / SF'
        for ax, lim in zip(axs, limits):
            ax.errorbar(eng, val, yerr=std_val, fmt='.-', label=label,
                        drawstyle='steps-mid')
            ax.set_xlabel('Energy [MeV]')
            # ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_xlim(lim)
            ax.set_ylim(1e-4, 1e-1)
            ax.legend()

    axs[0].set_ylabel(ylabel)
    fig.suptitle('DRAFT - Deposited energy by photons')
    nom_graf = 'espectros_photons_from_Cf.png'
    fig.tight_layout()
    fig.savefig(nom_graf)
    plt.show()
