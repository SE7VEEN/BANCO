# Compilación del Proyecto

## Agregar nuevos archivos

Cuando agreguen otro archivo, deben incluir lo siguiente en el `Makefile`:

```makefile
$(SRC_DIR)/$(CARPETA)/archivo.c \

#Para compilar solo deben ir ya sea a la carpeta del servidor o cliente desde la terminal y ejecutar el siguiente comando:

-make

#Si quieren limpiar usen:

-make clean

#El ejecutable es el de la respectiva carpeta bin

```
## Agregar carpetas

```makefile

#Solo deben agregar actualizar el subdirectorio y agregar lo siguiente en la parte de flags 
-I$(INC_DIR)/$(CARPETA)

```