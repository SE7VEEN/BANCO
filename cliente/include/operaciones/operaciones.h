#ifndef OPERACIONES
#define OPERACIONES

bool depositar(int socket, const char *cuenta, double monto);
bool retirar(int socket, const char *cuenta, double monto);
double consultar_saldo(int socket, const char *cuenta);
void consultar_movimientos(int socket);
void consultar_prestamos(int socket);
void consultar_tarjetas(int socket);

#endif