# Proyecto: TallerPracticoII
# Programa para gestionar citas del consultorio odontológico del Dr.Nowzaradan

import re
from datetime import datetime

# Definición de constantes (tabla de criterios)
# Precios base por tipo de atención
PRECIOS_BASE = {
    "Limpieza": 30,
    "Calzas": 80,
    "Extracción": 100,
    "Diagnóstico": 50
}

# Multiplicador según tipo de cliente
MULTIPLICADOR_CLIENTE = {
    "Particular": 1.0,
    "EPS": 0.8,
    "Prepagada": 1.2
}

# Recargo por prioridad
RECARGO_PRIORIDAD = {
    "Normal": 0,
    "Urgente": 20
}

# Valor fijo de la cita (consulta)
VALOR_CITA_FIJO = 10

# Lista para almacenar todos los clientes
clientes = []


# Función para mostrar menú y validar opción numérica
def menu_con_opciones(titulo, opciones):
    """
    Muestra un menú con opciones numeradas y retorna la opción seleccionada.
    opciones: lista de strings con las opciones a mostrar
    """
    print(f"\n--- {titulo} ---")
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}. {opcion}")

    while True:
        try:
            seleccion = int(input("Seleccione una opción (número): "))
            if 1 <= seleccion <= len(opciones):
                return opciones[seleccion - 1]
            else:
                print(f"Opción inválida. Seleccione un número entre 1 y {len(opciones)}.")
        except ValueError:
            print("Debe ingresar un número válido.")


# Función para validar cédula (solo números, mínimo 5 dígitos)
def validar_cedula(mensaje):
    while True:
        cedula = input(mensaje).strip()
        if cedula.isdigit() and len(cedula) >= 5:
            return cedula
        print("Cédula inválida. Debe contener solo números y al menos 5 dígitos.")


# Función para validar nombre (solo letras y espacios, mínimo 2 caracteres)
def validar_nombre(mensaje):
    while True:
        nombre = input(mensaje).strip()
        if nombre and all(c.isalpha() or c.isspace() for c in nombre) and len(nombre) >= 2:
            return nombre.title()
        print("Nombre inválido. Debe contener solo letras y al menos 2 caracteres.")


# Función para validar teléfono (números, opcionalmente con guiones o espacios)
def validar_telefono(mensaje):
    while True:
        telefono = input(mensaje).strip()
        # Eliminar guiones y espacios para validar
        telefono_limpio = re.sub(r'[\s\-]', '', telefono)
        if telefono_limpio.isdigit() and len(telefono_limpio) >= 7:
            return telefono
        print("Teléfono inválido. Debe contener al menos 7 dígitos.")


# Función para validar fecha (DD/MM/AAAA y que sea una fecha real)
def validar_fecha(mensaje):
    while True:
        fecha = input(mensaje).strip()
        try:
            # Intentar parsear la fecha
            fecha_obj = datetime.strptime(fecha, "%d/%m/%Y")
            # Validar que no sea una fecha pasada
            if fecha_obj.date() >= datetime.now().date():
                return fecha
            else:
                print("La fecha no puede ser anterior al día de hoy.")
        except ValueError:
            print("Fecha inválida. Use el formato DD/MM/AAAA (ejemplo: 25/12/2024)")


# Función para validar continuar (solo s o n)
def validar_continuar(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ['s', 'n']:
            return respuesta
        print("Opción inválida. Responda 's' para sí o 'n' para no.")


# Captura de datos
print("=== REGISTRO DE CITAS ODONTOLÓGICAS ===")

while True:
    print("\n--- Nuevo cliente ---")

    cedula = validar_cedula("Cédula: ")
    nombre = validar_nombre("Nombre: ")
    telefono = validar_telefono("Teléfono: ")

    # Menú para tipo de cliente
    tipo_cliente = menu_con_opciones("TIPO DE CLIENTE", [
        "Particular",
        "EPS",
        "Prepagada"
    ])

    # Menú para tipo de atención
    tipo_atencion = menu_con_opciones("TIPO DE ATENCIÓN", [
        "Limpieza",
        "Calzas",
        "Extracción",
        "Diagnóstico"
    ])

    # Cantidad según tipo de atención con límites máximos
    if tipo_atencion == "Limpieza":
        cantidad = 1
        print("Cantidad fijada en 1 para limpieza.")
    elif tipo_atencion == "Diagnóstico":
        cantidad = 1
        print("Cantidad fijada en 1 para diagnóstico.")
    elif tipo_atencion == "Calzas":
        while True:
            try:
                print("\n--- CALZAS ---")
                print("Máximo 3 caries por cita")
                cantidad = int(input("Cantidad de caries a tratar: "))
                if 1 <= cantidad <= 3:
                    break
                elif cantidad <= 0:
                    print("La cantidad debe ser mayor que cero.")
                else:
                    print(f"La cantidad máxima para calzas es 3 por cita. Ingresó: {cantidad}")
            except ValueError:
                print("Debe ingresar un número entero.")
    elif tipo_atencion == "Extracción":
        while True:
            try:
                print("\n--- EXTRACCIÓN ---")
                print("Máximo 4 piezas por cita")
                cantidad = int(input("Cantidad de piezas a extraer: "))
                if 1 <= cantidad <= 4:
                    break
                elif cantidad <= 0:
                    print("La cantidad debe ser mayor que cero.")
                else:
                    print(f"La cantidad máxima para extracción es 4 por cita. Ingresó: {cantidad}")
            except ValueError:
                print("Debe ingresar un número entero.")

    # Menú para prioridad
    prioridad = menu_con_opciones("PRIORIDAD", [
        "Normal",
        "Urgente"
    ])

    fecha = validar_fecha("Fecha de la cita (DD/MM/AAAA): ")

    # Cálculos
    precio_unitario = PRECIOS_BASE[tipo_atencion]
    multiplicador = MULTIPLICADOR_CLIENTE[tipo_cliente]
    recargo = RECARGO_PRIORIDAD[prioridad]

    valor_atencion = precio_unitario * cantidad * multiplicador
    total_pagar = VALOR_CITA_FIJO + valor_atencion + recargo

    # Guardar datos en un diccionario
    cliente = {
        "cedula": cedula,
        "nombre": nombre,
        "telefono": telefono,
        "tipo_cliente": tipo_cliente,
        "tipo_atencion": tipo_atencion,
        "cantidad": cantidad,
        "prioridad": prioridad,
        "fecha": fecha,
        "valor_atencion": valor_atencion,
        "total": total_pagar
    }
    clientes.append(cliente)

    # Mostrar resumen del registro
    print(f"\n=== CLIENTE REGISTRADO ===")
    print(f"Nombre: {nombre}")
    print(f"Tipo de atención: {tipo_atencion}")
    print(f"Cantidad: {cantidad}")
    print(f"Total a pagar: ${total_pagar:.2f}")

    continuar = validar_continuar("\n¿Desea registrar otro cliente? (s/n): ")
    if continuar == 'n':
        break

# Verificar si hay clientes registrados
if not clientes:
    print("\nNo se registró ningún cliente. Programa finalizado.")
else:
    # Cálculos estadísticos
    total_clientes = len(clientes)
    ingresos_totales = sum(c["total"] for c in clientes)
    clientes_extraccion = sum(1 for c in clientes if c["tipo_atencion"] == "Extracción")

    print("\n=== RESULTADOS ESTADÍSTICOS ===")
    print(f"Total de clientes: {total_clientes}")
    print(f"Ingresos totales recibidos: ${ingresos_totales:.2f}")
    print(f"Número de clientes para extracción: {clientes_extraccion}")

    # Ordenar clientes por valor de la atención (de mayor a menor)
    clientes_ordenados = sorted(clientes, key=lambda c: c["valor_atencion"], reverse=True)

    print("\n=== LISTA ORDENADA POR VALOR DE ATENCIÓN (MAYOR A MENOR) ===")
    for i, c in enumerate(clientes_ordenados, 1):
        print(f"{i}. {c['nombre']} (Cédula: {c['cedula']}) - Valor atención: ${c['valor_atencion']:.2f} - Total: ${c['total']:.2f}")

    # Búsqueda de cliente por cédula en la lista ordenada
    print("\n=== BÚSQUEDA DE CLIENTE ===")
    buscar_cedula = input("Ingrese la cédula del cliente a buscar: ")
    encontrado = None
    for cliente in clientes_ordenados:
        if cliente["cedula"] == buscar_cedula:
            encontrado = cliente
            break

    if encontrado:
        print("\n=== DATOS DEL CLIENTE ===")
        print(f"Cédula: {encontrado['cedula']}")
        print(f"Nombre: {encontrado['nombre']}")
        print(f"Teléfono: {encontrado['telefono']}")
        print(f"Tipo de cliente: {encontrado['tipo_cliente']}")
        print(f"Tipo de atención: {encontrado['tipo_atencion']}")
        print(f"Cantidad: {encontrado['cantidad']}")
        print(f"Prioridad: {encontrado['prioridad']}")
        print(f"Fecha: {encontrado['fecha']}")
        print(f"Valor atención: ${encontrado['valor_atencion']:.2f}")
        print(f"Total a pagar: ${encontrado['total']:.2f}")
    else:
        print("No se encontró ningún cliente con esa cédula.")

print("\n=== FIN DEL PROGRAMA ===")