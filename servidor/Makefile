# Makefile para el cliente

# Compilador
CC = gcc

# Carpetas
SRC_DIR = src
INC_DIR = include
BIN_DIR = bin

# Subdirectorios
PLANIFICACION = planificacion
SINCRONIZACION = sincronizacion
CONEXION = conexion
OPERACIONES = operaciones

# Flags
CFLAGS = -Wall -I$(INC_DIR) -I$(INC_DIR)/$(CONEXION) -I$(INC_DIR)/$(PLANIFICACION) -I$(INC_DIR)/$(SINCRONIZACION) -I$(INC_DIR)/$(OPERACIONES)

# Archivos fuente
SRCS = \
	$(SRC_DIR)/main.c \
	$(SRC_DIR)/$(CONEXION)/socket_servidor.c \
	$(SRC_DIR)/$(CONEXION)/manejarClientes.c \
	$(SRC_DIR)/$(OPERACIONES)/operaciones.c \
	
	
	



# Objetos
OBJS = $(SRCS:.c=.o)

# Ejecutable
TARGET = $(BIN_DIR)/servidor

# Regla por defecto
all: $(TARGET)

# Compilación
$(TARGET): $(OBJS)
	@mkdir -p $(BIN_DIR)
	$(CC) $(OBJS) -o $@

# Regla para objetos
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Limpiar
clean:
	rm -rf $(SRC_DIR)/**/*.o $(TARGET)

# Limpiar todo
mrproper: clean
	rm -rf $(BIN_DIR)
