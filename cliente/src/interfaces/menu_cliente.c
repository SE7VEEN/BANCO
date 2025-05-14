#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../include/cliente.h"

EstadoCliente menu_cliente(int socket)
{
    int opcion;
    char *respuesta;

    do
    {
        limpiar_pantalla();
        mostrar_encabezado("MENÚ PRINCIPAL - CLIENTE");

        printf("1. Operaciones de ventanilla\n");
        printf("2. Asistencia personalizada\n");
        printf("3. Consultar información de cuenta\n");
        printf("4. Cerrar sesión\n");
        printf("5. Salir\n");

        opcion = obtener_opcion_valida(1, 5);

        // switch (opcion)
        // {
        // case 1:
        //     return menu_operaciones(socket);
        // case 2:
        //     return menu_asistencia(socket);
        // case 3:
        //     return menu_consultas(socket);
        // case 4:
        //     enviar_comando(socket, "LOGOUT");
        //     respuesta = recibir_respuesta(socket);
        //     mostrar_mensaje(respuesta);
        //     pausa();
        //     return ESTADO_VISITANTE;
        // case 5:
        //     enviar_comando(socket, "EXIT");
        //     return ESTADO_SALIR;
        // }
    } while (opcion != 5);

    return ESTADO_CLIENTE;
}

// EstadoCliente menu_operaciones(int socket)
// {
//     // Implementación similar para operaciones bancarias
//     // ...
// }

// EstadoCliente menu_consultas(int socket)
// {
//     // Implementación para consultas
//     // ...
// }