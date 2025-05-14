#include "../../include/conexion/socket_cliente.h"

#include "../../../config.h"
#include "../../../mensajes.h"

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>

int conectar_servidor()
{
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0)
    {
        fprintf(stderr, "%sError al crear socket: %s%s\n",
                COLOR_ERROR, strerror(errno), COLOR_RESET);
        return -1;
    }

    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PUERTO_SERVIDOR);

    if (inet_pton(AF_INET, IP_SERVIDOR, &serv_addr.sin_addr) <= 0)
    {
        fprintf(stderr, "%sDirección inválida o no soportada: %s%s\n",
                COLOR_ERROR, strerror(errno), COLOR_RESET);
        close(sock);
        return -1;
    }

    printf("%sConectando al servidor %s:%d...%s\n",
           COLOR_SECUNDARIO, IP_SERVIDOR, PUERTO_SERVIDOR, COLOR_RESET);

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        fprintf(stderr, "%sConexión fallida: %s%s\n",
                COLOR_ERROR, strerror(errno), COLOR_RESET);
        close(sock);
        return -1;
    }

    printf("%sConexión establecida correctamente con el servidor%s\n",
           COLOR_EXITO, COLOR_RESET);
    return sock;
}

void cerrar_conexion(int socket)
{
    if (socket >= 0)
    {
        // Enviar mensaje de desconexión ordenada si es posible
        const char *msg = "CLOSE_CONNECTION";
        send(socket, msg, strlen(msg), 0);

        // Cierre seguro del socket
        shutdown(socket, SHUT_RDWR);
        close(socket);

        printf("%sConexión cerrada correctamente%s\n",
               COLOR_SECUNDARIO, COLOR_RESET);
    }
}