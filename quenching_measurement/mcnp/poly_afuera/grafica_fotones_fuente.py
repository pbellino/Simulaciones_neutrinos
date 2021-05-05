#!/usr/bin/env python3

"""
Script para comparar flujo de partículas entre espectros con y sin fotones de
la fuente de Cf252
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
                'med_qf_vacio.o',
                'med_qf_vacio_sin_fotones_de_fuente.o',
                ]
    labels = [
              'With photons from Cf252',
              'Without photons from Cf252',
              ]
    tallies = ['14', '504']
    fig_n, ax_n = plt.subplots(1, 1, figsize=(8, 6))
    fig_p, ax_p = plt.subplots(1, 1, figsize=(8, 6))
    axs = [ax_n, ax_p]
    normaliza = False  # Se divide por el bin de energía
    for arch, label in zip(archivos, labels):
        datos, nombre, bins = lee_tally_E_card(arch)
        for ax, tally in zip(axs, tallies):
            eng = datos[tally][:, 0]
            val = datos[tally][:, 1]
            std_val = datos[tally][:, 2] * val
            if normaliza:
                bin_limits = bins[tally]
                # Calcula ancho del bin
                bin_width = np.diff(bin_limits, axis=1)[:, 0]
                # Normalizo con ancho del bin
                val = val / bin_width
                std_val = std_val / bin_width
                ylabel = 'Flux [1 / cm$^2$ / MeV / source]'
            else:
                ylabel = 'Flux [1/ cm$^2$ / source]'
            ax.errorbar(eng, val, yerr=std_val, fmt='.-', label=label,
                        drawstyle='steps-mid')

    titles = [
              'Neutron flux in detector',
              'Photon flux in detector',
             ]

    for ax, title in zip(axs, titles):
        ax.set_xlabel('Energy [MeV]')
        ax.set_ylabel(ylabel)
        ax.set_xscale('log')
        ax.set_yscale('log')
        # ax.set_xlim(lim)
        # ax.set_ylim(4e-6, 5e-4)
        ax.set_title(title)
        ax.legend()
    #fig.suptitle('DRAFT - Deposited energy by photons')
    fig_n.tight_layout()
    fig_p.tight_layout()
    fig_n.savefig('diff_flux_vac_wo_photons_neutrons.png')
    fig_p.savefig('diff_flux_vac_wo_photons_photons.png')
    plt.show()
