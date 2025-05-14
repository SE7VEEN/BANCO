#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <pthread.h>

#include "../include/servidor.h"
#include "../../config.h"
#include "../../mensajes.h"

volatile sig_atomic_t server_running = 1;

void manejar_senal(int sig)
{
    printf("\n%sRecibida señal %d. Cerrando servidor...%s\n",
           COLOR_ERROR, sig, COLOR_RESET);
    server_running = 0;
}

int main()
{
    // Configurar manejadores de señal
    signal(SIGINT, manejar_senal);
    signal(SIGTERM, manejar_senal);
    signal(SIGCHLD, SIG_IGN); // Ignorar hijos terminados

    printf("%sIniciando servidor bancario v%s...%s\n",
           COLOR_PRIMARIO, VERSION_SERVIDOR, COLOR_RESET);

    // Inicializar subsistemas
    // inicializar_cuentas();
    // inicializar_planificacion();

    // Hilos principales
    pthread_t hilo_servidor, hilo_menu;

    if (pthread_create(&hilo_servidor, NULL, iniciar_servidor, NULL) != 0)
    {
        fprintf(stderr, "%sError al crear hilo del servidor%s\n", COLOR_ERROR, COLOR_RESET);
        return EXIT_FAILURE;
    }

    // if (pthread_create(&hilo_menu, NULL, iniciar_menu_administrativo, NULL) != 0) //
    // {
    //     fprintf(stderr, "%sError al crear hilo del menú%s\n", COLOR_ERROR, COLOR_RESET);
    //     return EXIT_FAILURE;
    // }

    // Esperar a que los hilos terminen
    pthread_join(hilo_servidor, NULL);
    pthread_join(hilo_menu, NULL);

    // Limpieza final
    // guardar_estado_cuentas();
    printf("%sServidor detenido correctamente.%s\n", COLOR_EXITO, COLOR_RESET);

    return EXIT_SUCCESS;
}