#include <stdio.h>

#include "../../config.h"
#include "../../include/cliente.h"
#include "../../include/interfaces/interfaz.h"

void mostrar_bienvenida()
{
    // limpiar_pantalla();
    printf("\033[1;34m");
    printf("========================================\n");
    printf("      BIENVENIDO AL BANCO DIGITAL\n");
    printf("========================================\n");
    printf("\033[0m\n");

    printf("Sistema cliente versión: %s\n", VERSION_CLIENTE);
    printf("Conectando al servidor: %s:%d\n\n", IP_SERVIDOR, PUERTO_SERVIDOR);

    // pausa();
}

EstadoCliente menu_principal(int socket)
{
    int opcion;

    do
    {
        limpiar_pantalla();
        mostrar_encabezado("MENÚ PRINCIPAL");

        printf("1. Acceder como cliente\n");
        printf("2. Entrar como visitante\n");
        printf("3. Configuración\n");
        printf("4. Salir\n");

        opcion = obtener_opcion_valida(1, 4);

        // switch (opcion)
        // {
        // case 1:
        //     return autenticar_usuario(socket); // maneja el login, enviamos el parametro socket para permitir la comunicacion con el servidor
        // case 2:
        //     return ESTADO_VISITANTE;
        // case 3:
        //     return ESTADO_SALIR;
        // }
    } while (opcion != 3);

    return ESTADO_SALIR;
}
