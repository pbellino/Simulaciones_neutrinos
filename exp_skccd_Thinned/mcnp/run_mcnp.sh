#! /bin/bash

INPUT=skccd_thinned

rm ${INPUT}.*
mcnp6 tasks 8 i=${INPUT} n=${INPUT}.

