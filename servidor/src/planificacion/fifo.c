#include "include/planificacion.h"

void ordenarPorLlegada(Proceso procesos[], int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (procesos[j].tiempo_llegada > procesos[j + 1].tiempo_llegada)
            {
                Proceso temp = procesos[j];
                procesos[j] = procesos[j + 1];
                procesos[j + 1] = temp;
            }
        }
    }
}

void fifo(Proceso procesos[], int n)
{
    ordenarPorLlegada(procesos, n); // Ordenamos para que el primer proceso en llegar sea el primero en ejecutarse
    int tiempo_actual = 0;
    float total_espera = 0, total_retorno = 0; // Para saber el tiempo que un cliente espera en la cola y el tiempo que tarda en su operacion

    for (int i = 0; i < n; i++)
    {
        if (tiempo_actual < procesos[i].tiempo_llegada) // Esperamos si el proceso no ha llegado
        {

            int espera = procesos[i].tiempo_llegada - tiempo_actual;
            printf("Esperando %d unidades hasta que llegue el proceso %d...\n", espera, procesos[i].pid);
            sleep(espera);                              // Simulamos la espera
            tiempo_actual = procesos[i].tiempo_llegada; // Avanzamos el tiempo actual al momento en el que proceso llego
        }
        // Comenzamos con la ejecucion del proceso
        {
            int espera = procesos[i].tiempo_llegada - tiempo_actual;
            printf("Esperando %d unidades hasta que llegue el proceso %d...\n", espera, procesos[i].pid);
            sleep(espera);
            tiempo_actual = procesos[i].tiempo_llegada;
        }

        int tiempo_inicio = tiempo_actual;
        int tiempo_fin = tiempo_actual + procesos[i].tiempo_ejecucion;     // Tiempo que se termina de ejecutar
        int tiempo_espera = tiempo_actual - procesos[i].tiempo_llegada;    // Tiempo que espero para ser atentido
        int tiempo_retorno = tiempo_espera + procesos[i].tiempo_ejecucion; // Tiempo que permanecio en el sistema

        printf("Proceso %d: Ejecutado de %d a %d | Espera: %d | Retorno: %d\n",
               procesos[i].pid, tiempo_inicio, tiempo_fin, tiempo_espera, tiempo_retorno);

        sleep(procesos[i].tiempo_ejecucion); // Simulamos la ejecucion

        tiempo_actual = tiempo_fin; // Actualizamos el tiempo actual en el tiempo que termino el proceso
        total_espera += tiempo_espera;
        total_retorno += tiempo_retorno;
    }

    printf("\nTiempo promedio de espera: %.2f\n", total_espera / n);
    printf("Tiempo promedio de retorno: %.2f\n", total_retorno / n);
}