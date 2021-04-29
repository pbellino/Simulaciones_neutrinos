#!/usr/bin/env python3

"""
Script para leer los resultados de cada corrida de PHITS
TODO
"""

import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
sys.path.append('/home/pablo/CinePy/')
from modules.simulacion_modules import lee_espectro_phits_eng
sns.set()


if __name__ == '__main__':

    archivos = [
                'cross_reg_1col.out',
                'cross_reg_2col.out',
                ]
    labels = [
              'After 1 el. collisin',
              'After 2 el. collisions',
              ]

    zona = '2 - 3'

    fig, ax = plt.subplots(1, 1)

    for archivo, label in zip(archivos, labels):
        data = lee_espectro_phits_eng(archivo, zona)
        # Puntos centrados en el bin
        eng = (data['e-lower'] + data['e-upper']) / 2.
        val = data['neutron'][:, 0]
        std_val = val * data['neutron'][:, 1]
        (_, caps, _) = ax.errorbar(eng, val, yerr=std_val, fmt='.-',
                                   label=label,
                                   capsize=3, drawstyle='steps-mid',
                                   )

        for cap in caps:
            cap.set_markeredgewidth(1)
        #ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Energy [MeV]')
        ax.set_ylabel('Probability per neutron source')
        ax.legend()
        fig.gca().set_title('Neutrons leaving detector')

    fig.savefig('espectro_neutrones.png')
    plt.show()
