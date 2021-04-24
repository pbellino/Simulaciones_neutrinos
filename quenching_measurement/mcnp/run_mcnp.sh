#! /bin/bash

INPUT=med_qf

rm ${INPUT}.*
mcnp6 tasks 8 i=${INPUT} n=${INPUT}.

