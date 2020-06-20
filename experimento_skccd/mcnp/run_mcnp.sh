#! /bin/bash

INPUT=skccd

rm ${INPUT}.*
mcnp6 tasks 8 i=${INPUT} n=${INPUT}.

