#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para leer los resultados de cada corrida de PHITS
TODO
"""

import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append('/home/pablo/CinePy/')
from modules.simulacion_modules import lee_espectro_phits_eng
sns.set()


if __name__ == '__main__':

    archivo = 'track_eng.out'
    zonas = [
             '101',
             '102',
             '103',
            ]

    fig_n, ax_n = plt.subplots(1, 1)
    fig_p, ax_p = plt.subplots(1, 1)

    for zona in zonas:
        data = lee_espectro_phits_eng(archivo, zona)
        # Puntos centrados en el bin
        eng = (data['e-lower'] + data['e-upper']) / 2.
        ax = {'neutron': ax_n, 'photon': ax_p}
        for part in ['neutron', 'photon']:
            val = data[part][:, 0]
            std_val = val * data[part][:, 1]
            (_, caps, _) = ax[part].errorbar(eng, val, yerr=std_val, fmt='.-',
                                             label=zona, capsize=3,
                                             )
            for cap in caps:
                cap.set_markeredgewidth(1)
            ax[part].set_xscale('log')
            ax[part].set_yscale('log')
            ax[part].set_xlabel('Energy [MeV]')
            ax[part].set_ylabel('Flux [1/cm2/MeV]')
            ax[part].legend()
        fig_n.gca().set_title('Neutrons')
        fig_p.gca().set_title('Photons')

    fig_n.savefig('espectro_neutrones.png')
    fig_p.savefig('espectro_fotones.png')
    plt.show()
