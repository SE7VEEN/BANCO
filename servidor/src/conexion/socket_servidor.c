#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/select.h>
#include <errno.h>
#include <stdlib.h>

#include "../../include/servidor.h"
#include "../../config.h"
#include "../../mensajes.h"

void *iniciar_servidor(void *arg)
{
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0)
    {
        perror("socket failed");
        return NULL;
    }

    struct sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PUERTO_SERVIDOR);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
    {
        perror("bind failed");
        close(server_fd);
        return NULL;
    }

    if (listen(server_fd, MAX_CLIENTES_EN_COLA) < 0)
    {
        perror("listen failed");
        close(server_fd);
        return NULL;
    }

    printf("%sServidor escuchando en puerto %d%s\n",
           COLOR_EXITO, PUERTO_SERVIDOR, COLOR_RESET);

    while (server_running)
    {
        fd_set readfds;
        FD_ZERO(&readfds);
        FD_SET(server_fd, &readfds);

        struct timeval timeout = {.tv_sec = 1, .tv_usec = 0};

        int activity = select(server_fd + 1, &readfds, NULL, NULL, &timeout);

        if (activity < 0 && errno != EINTR)
        {
            perror("select error");
            continue;
        }

        if (activity > 0 && FD_ISSET(server_fd, &readfds))
        {
            struct sockaddr_in client_addr;
            socklen_t client_len = sizeof(client_addr);

            int client_socket = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
            if (client_socket < 0)
            {
                perror("accept failed");
                continue;
            }

            printf("%sNueva conexión de %s:%d%s\n",
                   COLOR_SECUNDARIO,
                   inet_ntoa(client_addr.sin_addr),
                   ntohs(client_addr.sin_port),
                   COLOR_RESET);

            // Crear proceso para manejar cliente
            pid_t pid = fork();
            if (pid == 0)
            { // Proceso hijo
                close(server_fd);
                // manejar_cliente(client_socket);
                exit(EXIT_SUCCESS);
            }
            else if (pid > 0)
            { // Proceso padre
                close(client_socket);
            }
            else
            {
                perror("fork failed");
            }
        }
    }

    close(server_fd);
    return NULL;
}