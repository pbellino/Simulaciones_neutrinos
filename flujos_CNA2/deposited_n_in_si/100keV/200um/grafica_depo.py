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

    archivos = [
                'deposit_Si_1col.out',
                'deposit_Si_2morecol.out',
               ]
    zona = '2'

    fig, axs = plt.subplots(2, 1, sharex=True)
    # particles = ['28Si', '25Mg', 'positron', 'electron', 'alpha', 'all']
    particles = ['28Si', 'all']

    for archivo, ax in zip(archivos, axs):
        data = lee_espectro_phits_eng(archivo, zona)
        # Puntos centrados en el bin
        eng = (data['e-lower'] + data['e-upper']) / 2.
        for part in particles:
            val = data[part][:, 0]
            std_val = val * data[part][:, 1]
            (_, caps, _) = ax.errorbar(eng, val, yerr=std_val, fmt='.-',
                                       label=part, capsize=3,
                                       drawstyle='steps-mid',
                                       )
            for cap in caps:
                cap.set_markeredgewidth(1)
            # ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_ylabel('Number [1/source]')
            ax.legend()
            ax.set_xlim(1e-8, 0.05)
#            ax.set_ylim(1e-8, 2e-4)
    axs[1].set_xlabel('Energy [MeV]')
    axs[0].set_title('Deposited energy after 1 elastic collision')
    axs[1].set_title('Total deposited energy')

    fig.savefig('deposited_Si.png')
    plt.show()
