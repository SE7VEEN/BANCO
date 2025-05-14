/*=================== CONFIGURACIONES GLOBALES =====================*/

#ifndef CONFIG_H
#define CONFIG_H

/*==== CONFIGURACION DE LA APLICACION =====*/
#define VERSION_CLIENTE "1.0.0"
#define VERSION_SERVIDOR "1.0.0"

/*==== CONFIGURACION DE RED =====*/
#define IP_SERVIDOR "127.0.0.1"
#define PUERTO_SERVIDOR 8080
#define TIMEOUT_CONEXION 15 // Tiempo de espera para conexiones (segundos), para evitar bloqueos
#define TIMEOUT_RESPUESTA 15
#define TIEMPO_ESPERA 10 //
#define BUFFER_SIZE 1024 // Tamaño del buffer para recibir datos
#define MAX_CLIENTES_EN_COLA 10

/*==== CONFIGURACION DE SEGURIDAD =====*/
#define MAX_INTENTOS_LOGIN 3 // Intentos máximos de autenticación
#define LONGITUD_MAX_NIP 4

/*==== CONFIGURACION DE CUENTAS Y TARJETAS =====*/
#define TIPOS_TARJETA {"DEBITO", "CREDITO", "TEMPORAL", "VIRTUAL"}
#define TIPOS_CUENTA {"ESTANDAR", "PREFERENTE", "EMPRESARIAL", "JOVEN"}
#define SALDO_INICIAL_MINIMO 100.0 // Saldo mínimo para apertura de cuenta
#define COMISION_TRANSFERENCIA 5.0 // Comisión por transferencia interbancaria

// Tarjetas
#define LIMITE_TARJETA_DEBITO 50000.0
#define LIMITE_TARJETA_CREDITO_BASE 20000.0
#define PLAZO_TARJETA_TEMPORAL 30 // días

/*==== LIMITES DE OPERACIONES =====*/
// Límites diarios (podrían ser por tipo de cuenta)
#define LIMITE_DEPOSITO_DIARIO 100000.0
#define LIMITE_RETIRO_DIARIO 10000.0
#define LIMITE_TRANSFERENCIA_DIARIO 40000.0

// Límites por operación
#define DEPOSITO_MAXIMO 100000.0
#define DEPOSITO_MINIMO 50.0
#define RETIRO_MAXIMO 15000.0
#define RETIRO_MINIMO 100.0
#define TRANSFERENCIA_MAXIMA 50000.0
#define TRANSFERENCIA_MINIMA 20.0

// Intereses
#define TASA_PRESTAMO 0.12

// #define MAX_HILOS_SERVIDOR 10  // Máximo de hilos trabajadores
#endif