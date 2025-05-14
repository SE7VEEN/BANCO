#include "include/planificacion.h"

void roundRobin(Proceso procesos[], int n, int quantum)
{
    int tiempo_actual = 0;
    int procesos_restantes = n;

    printf("\nOrden de ejecución de procesos:\n");

    while (procesos_restantes > 0)
    {
        for (int i = 0; i < n; i++)
        {
            if (procesos[i].tiempo_restante > 0)
            {
                int tiempo_ejec = (procesos[i].tiempo_restante > quantum) ? quantum : procesos[i].tiempo_restante;

                printf("Proceso %d ejecutado de %d a %d\n", procesos[i].pid, tiempo_actual, tiempo_actual + tiempo_ejec);

                tiempo_actual += tiempo_ejec;
                procesos[i].tiempo_restante -= tiempo_ejec;

                if (procesos[i].tiempo_restante == 0)
                {
                    procesos_restantes--;
                }
            }
        }
    }
}
