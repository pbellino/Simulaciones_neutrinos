#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para leer los resultados de cada corrida de PHITS
TODO
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append('/home/pablo/CinePy/')
from modules.simulacion_modules import lee_espectro_phits_eng
from modules.io_modules import lee_tally_E_card
sns.set()


if __name__ == '__main__':

    archivos = [
#                'phits/track_eng_emode0_negs1.out',
                'phits/track_eng_emode2_negs1.out',
#                'phits/track_eng_emode2_negs-1.out',
                ]
    labels = [
#              'e-mode=0  negs=1  ',
              'e-mode=2  negs=1  ',
#              'e-mode=2  negs=-1  ',
              ]
    labels = ['PHITS - ' + s for s in labels]
    zona = '101'

    fig_n, ax_n = plt.subplots(1, 1)
    fig_p, ax_p = plt.subplots(1, 1)

    for archivo, label in zip(archivos, labels):
        data = lee_espectro_phits_eng(archivo, zona)
        # Puntos centrados en el bin
        eng = (data['e-lower'] + data['e-upper']) / 2.
        ax = {'neutron': ax_n, 'photon': ax_p}
        for part in ['neutron', 'photon']:
            val = data[part][:, 0]
            std_val = val * data[part][:, 1]
            (_, caps, _) = ax[part].errorbar(eng, val, yerr=std_val, fmt='.-',
                                             label=label, capsize=3,
                                             )
            for cap in caps:
                cap.set_markeredgewidth(1)

            ax[part].set_title(part + ' in cell ' + zona)
# ---------------------------------------------------
    archivo = 'mcnp/skccd.o'
    tallies = [
               '14',
               '514',
              ]
    for tal, ax in zip(tallies, [ax_n, ax_p]):
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
        (_, caps, _) = ax.errorbar(eng, val, yerr=std_val, fmt='.-',
                                   label='MCNP', capsize=3,
                                   )
        for cap in caps:
            cap.set_markeredgewidth(1)

    for ax in [ax_n, ax_p]:
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Energy [MeV]')
        ax.set_ylabel('Flux [1/cm$^2$/MeV/SF]')
        ax.set_xlim(4e-4, 1e2)
        ax.set_ylim(1e-8, 1e-2)
        ax.legend()

    fig_n.savefig('espectro_neutrones_fin.png')
    fig_p.savefig('espectro_fotones_fin.png')
    plt.show()
