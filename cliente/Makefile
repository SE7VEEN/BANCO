# Makefile para el cliente

# Compilador
CC = gcc

# Carpetas
SRC_DIR = src
INC_DIR = include
BIN_DIR = bin

# Subdirectorios
CONEXION = conexion
INTERFACES = interfaces
OPERACIONES = operaciones

# Directorios compartidos (globales)
UTIL_SRC = ../util/src

# Flags
CFLAGS = -Wall -I$(INC_DIR) -I$(INC_DIR)/$(CONEXION) -I$(INC_DIR)/$(INTERFACES) -I$(INC_DIR)/$(OPERACIONES) -I$(UTIL_SRC) 

# Archivos fuente
SRCS = \
	$(SRC_DIR)/main.c \
	$(SRC_DIR)/$(CONEXION)/socket_cliente.c \
	$(SRC_DIR)/$(INTERFACES)/bienvenida.c \
	$(UTIL_SRC)/ui_helpers.c \
	

# Objetos
OBJS = $(SRCS:.c=.o)

# Ejecutable
TARGET = $(BIN_DIR)/cliente

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
