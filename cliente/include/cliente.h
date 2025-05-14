/*----ESTRUCTURAS Y FUNCIONES----*/

#ifndef CLIENTE_H
#define CLIENTE_H

/**
 * Estados posibles del cliente en la aplicación.
 * Determina qué menú mostrar y permisos.
 */
typedef enum
{
    ESTADO_VISITANTE,         // Usuario no autenticado
    ESTADO_VISITANTE_EN_COLA, // Visitante esperando asistencia
    ESTADO_CLIENTE,           // Cliente autenticado
    ESTADO_SALIR              // Para salir
} EstadoCliente;

// Funciones de menú
EstadoCliente menu_visitante(int socket);
EstadoCliente menu_cliente(int socket);
EstadoCliente autenticar_usuario(int socket);

#endif