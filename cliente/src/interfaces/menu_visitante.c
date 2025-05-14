#include <stdio.h>
#include "../include/cliente.h"
#include "../util/input_validation.c"

EstadoCliente menu_visitante(int socket)
{
    int opcion;

    do
    {
        limpiar_pantalla();
        mostrar_encabezado("MENÚ VISITANTE");

        printf("1. Consulta rápida\n");
        printf("2. Asistencia personalizada\n");
        printf("3. Registrarse como cliente\n");
        printf("4. Volver a autenticación\n");
        printf("5. Salir\n");

        opcion = obtener_opcion_valida(1, 5);

        // switch (opcion)
        // {
        // case 1:
        //     enviar_comando(socket, "CONSULTA_RAPIDA");
        //     mostrar_mensaje(recibir_respuesta(socket));
        //     pausa();
        //     break;
        // case 2:
        //     enviar_comando(socket, "ASISTENCIA");
        //     mostrar_mensaje(recibir_respuesta(socket));
        //     pausa();
        //     return ESTADO_VISITANTE_EN_COLA;
        // case 3:
        //     return registrar_nuevo_cliente(socket);
        // case 4:
        //     return ESTADO_VISITANTE;
        // case 5:
        //     return ESTADO_SALIR;
        // }
    } while (opcion != 5);

    return ESTADO_VISITANTE;
}

// EstadoCliente registrar_nuevo_cliente(int socket)
// {
//     // Implementación de registro nuevo cliente
//     // ...
//     return ESTADO_VISITANTE;
// }