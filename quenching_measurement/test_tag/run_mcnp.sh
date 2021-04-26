#! /bin/bash

INPUT=med_qf
OUTPUT=med_acero

rm ${OUTPUT}.*
#mcnp6 tasks 8 i=${INPUT} n=${INPUT}.
mcnp6 tasks 8 i=${INPUT} n=${OUTPUT}.

