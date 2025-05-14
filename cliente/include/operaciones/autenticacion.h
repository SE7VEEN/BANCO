
#ifndef AUTENTICACION_H
#define AUTENTICACION_H

#include "../cliente.h"

#include <sys/socket.h>
#include <stddef.h>

EstadoCliente autenticar_usuario(int socket);

void obtener_password(char *buffer, size_t size);

#endif