#!/usr/bin/env python3 
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


    #archivo = 'cross_reg_10Pb05Cu05Si.out'
    archivo = 'cross_reg_4Pb05Cu05Si.out'

    zonas = [
             '10 - 11',
             '11 - 12',
             '12 - 98',
            ]

    fig, ax = plt.subplots(1, 1)
    particles = ['all']

    for zona in zonas:
        data = lee_espectro_phits_eng(archivo, zona)
        # Puntos centrados en el bin
        eng = (data['e-lower'] + data['e-upper']) / 2.
        for part in particles:
            val = data[part][:, 0]
            std_val = val * data[part][:, 1]
            (_, caps, _) = ax.errorbar(eng, val, yerr=std_val, fmt='.-',
                                       label=zona, capsize=3,
                                       drawstyle='steps-mid',
                                       )

            for cap in caps:
                cap.set_markeredgewidth(1)
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_xscale('log')
            ax.set_xlabel('Energy [MeV]')
            ax.set_ylabel('Number [1/source]')
            ax.legend(loc='upper left')
            # ax.set_xlim(0, 5e-1)
            # ax.set_ylim(1e-8, 2e-5)
        fig.gca().set_title('Particles entering the detector')

    fig.savefig('deposited_Si.png')
    plt.show()
