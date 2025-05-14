#include <stdio.h>
#include <stdlib.h>

#include "../include/ui_helpers.h"

void limpiar_pantalla()
{
    system("clear || cls");
}

void mostrar_encabezado(const char *titulo)
{
    printf("\n\033[1;34m=== %s ===\033[0m\n\n", titulo);
}

void mostrar_mensaje(const char *mensaje)
{
    if (mensaje == NULL)
        return;

    if (strstr(mensaje, "ERROR") != NULL)
    {
        printf("\n\033[1;31m%s\033[0m\n", mensaje);
    }
    else if (strstr(mensaje, "éxito") != NULL || strstr(mensaje, "correctamente") != NULL)
    {
        printf("\n\033[1;32m%s\033[0m\n", mensaje);
    }
    else
    {
        printf("\n\033[1;36m%s\033[0m\n", mensaje);
    }
}

void pausa()
{
    printf("\nPresione Enter para continuar...");
    while (getchar() != '\n')
        ;      // Limpiar buffer
    getchar(); // Esperar Enter
}

char obtener_opcion_sn()
{
    char opcion;
    char input[10];

    while (1)
    {
        fgets(input, sizeof(input), stdin);
        opcion = tolower(input[0]);

        if (opcion == 's' || opcion == 'n')
        {
            return opcion;
        }

        printf("Opción inválida. Ingrese 's' o 'n': ");
    }
}