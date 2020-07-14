#! /bin/bash

INPUT=test

rm ${INPUT}.*
mcnp6 tasks 8 i=${INPUT} n=${INPUT}.

