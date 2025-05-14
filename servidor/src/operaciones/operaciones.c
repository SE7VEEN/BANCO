#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include "../../include/servidor.h"
#include "../../../config.h"
#include "../../../mensajes.h"

pthread_mutex_t mutex_cuentas = PTHREAD_MUTEX_INITIALIZER;

void procesar_solicitud(const char *solicitud, char *respuesta)
{
    char comando[20], cuenta1[20], cuenta2[20];
    double monto;

    if (sscanf(solicitud, "%19s %19s %lf", comando, cuenta1, &monto) >= 2)
    {
        pthread_mutex_lock(&mutex_cuentas);

        if (strcmp(comando, "CONSULTAR") == 0)
        {
            // consultar_saldo(cuenta1, respuesta);
        }
        else if (strcmp(comando, "DEPOSITAR") == 0)
        {
            // depositar(cuenta1, monto, respuesta);
        }
        else if (strcmp(comando, "RETIRAR") == 0)
        {
            // retirar(cuenta1, monto, respuesta);
        }
        else if (strcmp(comando, "TRANSFERIR") == 0 &&
                 sscanf(solicitud, "%*s %*s %19s %lf", cuenta2, &monto) >= 1)
        {
            // transferir(cuenta1, cuenta2, monto, respuesta);
        }
        else
        {
            snprintf(respuesta, BUFFER_SIZE, "%sERROR: Comando no reconocido%s", COLOR_ERROR, COLOR_RESET);
        }

        pthread_mutex_unlock(&mutex_cuentas);
    }
    else
    {
        snprintf(respuesta, BUFFER_SIZE, "%sERROR: Formato inválido%s", COLOR_ERROR, COLOR_RESET);
    }
}