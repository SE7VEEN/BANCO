#ifndef SERVIDOR_H
#define SERVIDOR_H

#include <stdbool.h>
#include <signal.h>

// Declaración extern de la variable global de control del servidor
extern volatile sig_atomic_t server_running;

// Prototipos de funciones de conexión
void *iniciar_servidor(void *arg);
void manejar_cliente(int client_socket);

// Prototipos de funciones de operaciones
void procesar_solicitud(const char *solicitud, char *respuesta);
void inicializar_cuentas();
void guardar_estado_cuentas();

// Prototipos de funciones de planificación
void inicializar_planificacion();
void agregar_cliente_cola(int socket, int tipo_cliente);

// Prototipos de funciones administrativas
void *iniciar_menu_administrativo(void *arg);

#endif // SERVIDOR_H