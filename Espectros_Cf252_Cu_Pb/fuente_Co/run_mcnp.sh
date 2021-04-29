#! /bin/bash

INPUT=co60_src

rm ${INPUT}.*
mcnp6 tasks 8 i=${INPUT} n=${INPUT}.

