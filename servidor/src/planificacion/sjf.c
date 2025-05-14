#include "include/planificacion.h"

// Función para intercambiar dos procesos
void swap(Proceso *a, Proceso *b)
{
    Proceso temp = *a;
    *a = *b;
    *b = temp;
}
void ordenarPorEjecucion(Proceso procesos[], int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            if (procesos[i].tiempo_ejecucion > procesos[j].tiempo_ejecucion)
            {
                swap(&procesos[i], &procesos[j]);
            }
        }
    }
}

void sjf(Proceso procesos[], int n)
{
    ordenarPorEjecucion(procesos, n);

    int tiempo_actual = 0;
    printf("Orden de ejecución de procesos:\n");

    for (int i = 0; i < n; i++)
    {
        if (tiempo_actual < procesos[i].tiempo_llegada)
        {
            tiempo_actual = procesos[i].tiempo_llegada;
        }

        printf("Proceso %d: Ejecutado de %d a %d\n", procesos[i].pid, tiempo_actual, tiempo_actual + procesos[i].tiempo_ejecucion);
        tiempo_actual += procesos[i].tiempo_ejecucion;
    }
}
