#! /bin/bash

INPUT=med_qf
#OUTPUT=med_qf_vacio.
#OUTPUT=med_qf_poly.
OUTPUT=med_qf_vacio_sin_fotones_de_fuente.

rm ${OUTPUT}.*
mcnp6 tasks 8 i=${INPUT} n=${OUTPUT}

