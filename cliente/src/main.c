#include <stdio.h>
#include <stdlib.h>

#include "../include/conexion/socket_cliente.h"
#include "../include/interfaces/interfaz.h"
#include "../../mensajes.h"
#include "../../config.h"

// #include "../include/interfaces/menu_principal.h"

int main()
{
    printf("%s=== BANCO DIGITAL (v%s) ===%s\n",
           COLOR_PRIMARIO, VERSION_CLIENTE, COLOR_RESET);

    int socket_cliente = conectar_servidor();
    if (socket_cliente == -1)
    {
        printf("%sNo se pudo conectar al servidor%s\n", COLOR_ERROR, COLOR_RESET);
        return EXIT_FAILURE;
    }

    mostrar_bienvenida();

    cerrar_conexion(socket_cliente);
    printf("%sSesión finalizada correctamente%s\n", COLOR_EXITO, COLOR_RESET);

    return EXIT_SUCCESS;
}