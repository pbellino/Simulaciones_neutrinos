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
                        1.33211952e+05,
                        2.60102701e+05,
                        4.85627872e+03,
                        1.33434440e+02,
                        1.26943060e+01,
                        1.22008120e+00,
                        1.17094150e-01,
                        1.49131650e-02,
                        3.27225200e-03,
                        1.03291230e-03,
                       ]

    # Energías de los neutrones iniciales [MeV]
    grupos_ini = [
                  1.0000E-09,
                  1.0000E-08,
                  1.0000E-07,
                  1.0000E-06,
                  1.0000E-05,
                  1.0000E-04,
                  1.0000E-03,
                  1.0000E-02,
                  1.0000E-01,
                  1.0000E+00,
                 ]
    grupos_fin = [
                  1.0000E-08,
                  1.0000E-07,
                  1.0000E-06,
                  1.0000E-05,
                  1.0000E-04,
                  1.0000E-03,
                  1.0000E-02,
                  1.0000E-01,
                  1.0000E+00,
                  1.0000E+01,
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
                'poly5cm/',
                'poly10cm/',
                'poly15cm/',
                ]
    labels = [
              '5 cm',
              '10 cm',
              '15 cm',
              ]

    archivos = [carpeta + 'cross_reg.out' for carpeta in carpetas]
    zona = '102 - 103'

    # Gráfico de los flujos

    flujos_in = flujos_iniciales[1:] + [flujos_iniciales[-1]]

    fig, ax = plt.subplots(1, 1)
    total_flux = 0
    for archivo, flujo, label in zip(archivos, flujos_in, labels):
        # Leo el espectro inicial
        if label == '5 cm':
            data = lee_espectro_phits_eng(archivo, '101 - 102')
            eng = (data['e-lower'] + data['e-upper']) / 2.
            val = data['neutron'][:, 0]
            std_val = val * data['neutron'][:, 1]
            (_, caps, _) = ax.errorbar(eng, val, yerr=std_val, fmt='.-',
                                   label='Inciden flux',
                                   capsize=3, drawstyle='steps-mid',
                                   )

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
        ax.set_ylabel('Neutron flux [1/cm$^2$/s]')
        ax.legend()
        fig.gca().set_title('Neutron with polyethilene shield')

    fig.savefig('espectro_flujos.png')
    plt.show()
