# Simulación experimento Skipper CCD con PHITS

**No se simulan los fotones de la fuente de Cf252**

## Contenido:

* `experimeto_phits` : input con la geometría para phits

* `skccd_phits.inp` : input con los parámetros de la simulación y las tallies (llama al archivo `experimento_phits`

* `run_phits.sh` : script auxiliar para correr el input y transfromar imágenes


## Geometría simulada

![Esquema 3D del experimento](3dshow.png)

![Esquema xy del experimento](track_xy_geom.png)

![Esquema xz del experimento](track_xz_geom.png)


## Resultados de prueba

![Esquema xy del experimento](track_xy.png)

![Esquema xz del experimento](track_xz.png)




## Notas

- Cuando se piden tallies por regiones, se debe poner el volúmen a mano. Existe la forma de que lo calcule, pero al tener geometrías de tamaños muy distintos (el Si sobre todo) es bastante ineficiente. Puse los valores calculados a mano (que son exactamente los que calcula MCNP).
