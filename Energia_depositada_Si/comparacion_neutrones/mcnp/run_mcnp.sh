#! /bin/bash

INPUT=esfera

rm ${INPUT}.*
mcnp6 tasks 8 i=${INPUT} n=${INPUT}.

