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

    # Flujos de los neutrones iniciales [n/cm2/s]
    flujos_iniciales = [
                        1.456e8, # térmico
                        1.099e9, # epitérmico
                        5.690e8, # 1 rápido
                        2.330e7, # 2 rápido
                        ]
    # Energías de los neutrones iniciales [MeV]
    grupos_ini = [
                   1e-12,
                   0.4e-6,
                   0.1,
                   1.0,
                  ]
    grupos_fin = [ 0.4e-6,
                   0.1,
                   1.0,
                   10.0,
                ]

    fig, ax = plt.subplots(1, 1)
    ax.plot(grupos_fin, flujos_iniciales, drawstyle='steps-mid',
            label='Initial neutron flux')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Energy [MeV]')
    ax.set_ylabel(r'Neutron flux [1/cm$^2$/s]')
    ax.legend()

    fig.savefig('initial_neutron_fluxes.png')

    ##################################################################

    carpetas = [
                'epitermico/',
                '1rapido/',
                #'2rapido/5MeV/',
                '2rapido/10MeV/',
                ]
    labels = [
              'Epithermal',
              '1 Fast',
              #'2 Fast (5MeV cut)',
              '2 Fast (10MeV cut)',
              ]

    archivos = [carpeta + 'cross_reg.out' for carpeta in carpetas]
    zona = '20 - 31'

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
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Energy [MeV]')
        ax.set_ylabel('Probability per neutron source')
        ax.legend(title="Initial neutron energy")
        fig.gca().set_title('Neutrons after 300 cm of concrete')

    fig.savefig('espectro_probabilidades.png')

    ##################################################################### 
    
    # Gráfico de los flujos

    flujos_in = flujos_iniciales[1:] + [flujos_iniciales[-1]]

    fig, ax = plt.subplots(1, 1)
    total_flux = 0
    for archivo, flujo, label in zip(archivos, flujos_in, labels):
        data = lee_espectro_phits_eng(archivo, zona)
        # Puntos centrados en el bin
        eng = (data['e-lower'] + data['e-upper']) / 2.
        val = data['neutron'][:, 0] * flujo
        total_flux += val
        std_val = val * data['neutron'][:, 1]
        (_, caps, _) = ax.errorbar(eng, val, yerr=std_val, fmt='.-',
                                   label=label,
                                   capsize=3, drawstyle='steps-mid',
                                   )

        for cap in caps:
            cap.set_markeredgewidth(1)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Energy [MeV]')
        ax.set_ylabel('Neutron flux [1/cm$^2$/s]')
        ax.legend(title="Initial neutron energy")
        fig.gca().set_title('Neutrons after 300 cm of concrete')

    # No tiene sentido graficar el total hasta no decidir dónde realizar
    # el corte para el segundo grupo rápido
    #
    #ax.errorbar(eng, total_flux, fmt='.-', label='Total flux',
    #            capsize=3, drawstyle='steps-mid',
    #            )

    print("Flujos sumados por energía")
    print(total_flux.T)
    print(f"Flujo total: {sum(total_flux):.4e}")


    fig.savefig('espectro_flujos.png')
    plt.show()
