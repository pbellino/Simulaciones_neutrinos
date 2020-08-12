#! /bin/bash

INPUT=fuente

rm ${INPUT}.*
mcnp6 tasks 8 i=${INPUT} n=${INPUT}.

