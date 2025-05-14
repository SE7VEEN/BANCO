#include "../../include/interfaces/interfaz.h"
#include "../../include/cliente.h"
#include "../../mensajes.h"
#include "../../config.h"
#include "../../util/include/ui_helpers.h"

#include <stdio.h>

void mostrar_bienvenida()
{
    limpiar_pantalla();

    printf("%s", COLOR_PRIMARIO);
    printf("========================================\n");
    printf("      BIENVENIDO AL BANCO DIGITAL\n");
    printf("========================================\n");
    printf("%s\n", COLOR_RESET);

    printf("%sSistema cliente versión: %s%s\n", COLOR_SECUNDARIO, VERSION_CLIENTE, COLOR_RESET);
    printf("%sConectando al servidor: %s:%d%s\n\n", COLOR_SECUNDARIO, IP_SERVIDOR, PUERTO_SERVIDOR, COLOR_RESET);

    pausa();
}