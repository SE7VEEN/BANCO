#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "../../include/servidor.h"
#include "../../config.h"
#include "../../mensajes.h"

void manejar_cliente(int client_socket)
{
    char buffer[BUFFER_SIZE];
    char respuesta[BUFFER_SIZE];

    while (1)
    {
        memset(buffer, 0, BUFFER_SIZE);
        memset(respuesta, 0, BUFFER_SIZE);

        ssize_t bytes_read = read(client_socket, buffer, BUFFER_SIZE - 1);
        if (bytes_read <= 0)
        {
            printf("%sCliente desconectado%s\n", COLOR_ADVERTENCIA, COLOR_RESET);
            break;
        }

        // Procesar comando según el protocolo
        procesar_solicitud(buffer, respuesta);

        if (send(client_socket, respuesta, strlen(respuesta), 0) < 0)
        {
            perror("send failed");
            break;
        }
    }

    close(client_socket);
}