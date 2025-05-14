/*==== CONFIGURACION GLOBAL DE MENSAJES =====*/

// Colores principales
#define COLOR_PRIMARIO "\033[1;34m"   // Azul claro brillante (títulos principales)
#define COLOR_SECUNDARIO "\033[1;36m" // Cian brillante (subtítulos, información destacada)

// Colores de estado
#define COLOR_EXITO "\033[1;32m"       // Verde brillante (operaciones exitosas)
#define COLOR_ERROR "\033[1;31m"       // Rojo brillante (mensajes de error)
#define COLOR_ADVERTENCIA "\033[1;33m" // Amarillo brillante (advertencias)

#define COLOR_RESET "\033[0m" // Restablecer color (para volver al color por defecto)

// Nota: Pueden hacer esto: printf("%s%sTexto resaltado%s\n", COLOR_BLANCO, FONDO_AZUL, COLOR_RESET);
//  Colores para texto
#define COLOR_NEGRO "\033[0;30m"
#define COLOR_ROJO "\033[0;31m"
#define COLOR_VERDE "\033[0;32m"
#define COLOR_AMARILLO "\033[0;33m"
#define COLOR_AZUL "\033[0;34m"
#define COLOR_MAGENTA "\033[0;35m"
#define COLOR_CIAN "\033[0;36m"
#define COLOR_BLANCO "\033[0;37m"

// Colores para fondo

#define FONDO_NEGRO "\033[40m"
#define FONDO_ROJO "\033[41m"
#define FONDO_VERDE "\033[42m"
#define FONDO_AMARILLO "\033[43m"
#define FONDO_AZUL "\033[44m"
#define FONDO_MAGENTA "\033[45m"
#define FONDO_CIAN "\033[46m"
#define FONDO_BLANCO "\033[47m"

// Estilos

#define ESTILO_NEGRITA "\033[1m"
#define ESTILO_SUBRAYADO "\033[4m"
#define ESTILO_INVERTIDO "\033[7m"
#define ESTILO_OCULTO "\033[8m"
