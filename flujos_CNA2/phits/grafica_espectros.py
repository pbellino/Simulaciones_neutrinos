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

    archivo = 'cross_reg_unit2.out'
    zonas = [
             '51 - 1',
             '1 - 51',
             '20 - 31',
            ]

    fig, ax = plt.subplots(1, 1)

    for zona in zonas:
        data = lee_espectro_phits_eng(archivo, zona)
        # Puntos centrados en el bin
        eng = (data['e-lower'] + data['e-upper']) / 2.
        deng = data['e-upper'] - data['e-lower']
        val = data['neutron'][:, 0] * deng
        print(val)
        print(val.sum())
        std_val = val * data['neutron'][:, 1]
        (_, caps, _) = ax.errorbar(eng, val, yerr=std_val, fmt='.-',
                                   label=zona, capsize=3,
                                   drawstyle='steps-mid',
                                   )
        for cap in caps:
            cap.set_markeredgewidth(1)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Energy [MeV]')
        ax.set_ylabel('Current [1/cm2/MeV/source]')
        ax.legend()
        fig.gca().set_title('Neutrons')

    fig.savefig('espectro_corriente.png')
    plt.show()
