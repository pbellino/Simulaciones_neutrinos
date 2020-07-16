#! /bin/bash

INPUT=skccd_depo

rm ${INPUT}.*
mcnp6 tasks 8 i=${INPUT} n=${INPUT}.

