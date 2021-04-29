#! /bin/bash

INPUT=med_qf

rm ${INPUT}.*
#mcnp6 tasks 8 i=${INPUT} n=${INPUT}.
#mcnp6 tasks 8 i=${INPUT} n=med_qf_poly.
mcnp6 tasks 8 i=${INPUT} n=med_qf_vacio.

