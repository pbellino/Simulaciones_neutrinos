#! /bin/bash

INPUT=skccd

rm ${INPUT}.*
mcnp6  i=${INPUT} n=${INPUT}.

