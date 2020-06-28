#! /bin/bash

# Input que voy a procesar
ARCHIVO=skccd_phits.inp

# Ejecuto PHITS
phits.sh ${ARCHIVO}

# Se fija la variable icntl del input
icntl=$(grep "icntl" ${ARCHIVO} | awk '{print $3}')

# Si corrió con geometría, renombro salidas
if [ "${icntl}" == "8" ]; then
    mv track_xy.eps track_xy_geom.eps
    mv track_xz.eps track_xz_geom.eps
fi

# Convierto y roto los .eps a .png
for i in *.eps
do
    convert "$i" -rotate 90 "${i%.*}.png"
done

