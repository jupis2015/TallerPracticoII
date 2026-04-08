# Proyecto: TallerPracticoII
# Programa para gestionar citas del consultorio odontológico del Dr.Nowzaradan

import re
from datetime import datetime, timedelta

# Valores de cita por tipo de cliente
VALOR_CITA = {
    "Particular": 80000,
    "EPS": 5000,
    "Prepagada": 30000
}

# Valores de atención por tipo de cliente y tipo de atención
VALORES_ATENCION = {
    "Particular": {
        "Limpieza": 60000,
        "Calzas": 80000,
        "Extracción": 100000,
        "Diagnóstico": 50000
    },
    "EPS": {
        "Limpieza": 0,
        "Calzas": 40000,
        "Extracción": 40000,
        "Diagnóstico": 0
    },
    "Prepagada": {
        "Limpieza": 0,
        "Calzas": 10000,
        "Extracción": 10000,
        "Diagnóstico": 0
    }
}

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


def validar_nombre(mensaje):
    while True:
        nombre = input(mensaje).strip()
        
        # Validaciones básicas
        if not nombre or len(nombre) < 2:
            print("❌ Nombre inválido. Debe tener al menos 2 caracteres.")
            continue
            
        # Validar que solo contenga letras, espacios, y algunos acentos comunes
        if not all(c.isalpha() or c.isspace() or c in "áéíóúñÁÉÍÓÚÑ" for c in nombre):
            print("❌ Nombre inválido. Use solo letras y espacios.")
            continue
        
        # Validar que no tenga más de 2 espacios seguidos
        if "  " in nombre:
            print("❌ Nombre inválido. No use espacios dobles.")
            continue
        
        # Validar proporción de vocales (los nombres reales tienen vocales)
        letras = [c for c in nombre if c.isalpha()]
        if len(letras) < 2:
            print("❌ Nombre inválido. Demasiado corto.")
            continue
            
        vocales = sum(1 for c in letras if c.lower() in "aeiouáéíóú")
        consonantes = len(letras) - vocales
        
        # Un nombre real debe tener al menos 20% de vocales
        if vocales == 0 or (vocales / len(letras)) < 0.2:
            print("❌ Nombre inválido. Parece no ser un nombre real (sin vocales suficientes).")
            continue
        
        # Validar que no tenga repeticiones excesivas de la misma letra
        from collections import Counter
        conteo = Counter(c.lower() for c in letras)
        max_repeticion = max(conteo.values())
        if max_repeticion > len(letras) * 0.6:  # Una letra no puede ser más del 60%
            print("❌ Nombre inválido. Demasiadas letras repetidas.")
            continue
        
        return nombre.title()


# Función para validar teléfono (solo números, sin caracteres especiales)
def validar_telefono(mensaje):
    while True:
        telefono = input(mensaje).strip()
        
        # Validar que solo contenga números
        if not telefono.isdigit():
            print("❌ Teléfono inválido. Use solo números, sin espacios, guiones ni otros caracteres.")
            print("   Ejemplo: 3012762712")
            continue
        
        # Validar longitud (mínimo 7 dígitos, máximo 15)
        if len(telefono) < 7:
            print(f"❌ Teléfono inválido. Debe tener al menos 7 dígitos. Ingresó {len(telefono)} dígito(s).")
            continue
        
        if len(telefono) > 15:
            print(f"❌ Teléfono inválido. Máximo 15 dígitos. Ingresó {len(telefono)} dígito(s).")
            continue
        
        # Validación extra: evitar números sospechosos (todos iguales)
        if len(set(telefono)) == 1:
            print("❌ Teléfono inválido. Número no válido (todos los dígitos iguales).")
            continue
        
        print(f"✅ Teléfono válido: {telefono}")
        return telefono


# Función para validar fecha (DD/MM/AAAA y que sea una fecha real)
def validar_fecha(mensaje, max_dias=365):
    while True:
        fecha = input(mensaje).strip()
        try:
            # Intentar parsear la fecha
            fecha_obj = datetime.strptime(fecha, "%d/%m/%Y")
            fecha_actual = datetime.now().date()
            fecha_ingresada = fecha_obj.date()
            
            # Calcular diferencia en días
            diferencia_dias = (fecha_ingresada - fecha_actual).days
            
            # Validaciones
            if fecha_ingresada < fecha_actual:
                print("❌ La fecha no puede ser anterior al día de hoy.")
            elif diferencia_dias > max_dias:
                fecha_limite = fecha_actual + timedelta(days=max_dias)
                print(f"❌ La fecha no puede superar {max_dias} días a partir de hoy.")
                print(f"📅 Fecha límite permitida: {fecha_limite.strftime('%d/%m/%Y')}")
            else:
                print(f"✅ Fecha válida: {fecha}")
                return fecha
        except ValueError:
            print("❌ Fecha inválida. Use el formato DD/MM/AAAA (ejemplo: 25/12/2024)")


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

    # Menú para prioridad (se mantiene pero sin efecto en el precio)
    prioridad = menu_con_opciones("PRIORIDAD", [
        "Normal",
        "Urgente"
    ])

    fecha = validar_fecha("Fecha de la cita (DD/MM/AAAA): ")

    # Cálculo: Valor a pagar = valor de la cita + (valor de atención × cantidad)
    valor_cita = VALOR_CITA[tipo_cliente]
    valor_atencion_unitario = VALORES_ATENCION[tipo_cliente][tipo_atencion]
    valor_atencion_total = valor_atencion_unitario * cantidad
    
    total_pagar = valor_cita + valor_atencion_total

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
        "valor_cita": valor_cita,
        "valor_atencion": valor_atencion_total,
        "total": total_pagar
    }
    clientes.append(cliente)

    # Mostrar resumen del registro
    print(f"\n=== CLIENTE REGISTRADO ===")
    print(f"Nombre: {nombre}")
    print(f"Tipo de cliente: {tipo_cliente}")
    print(f"Tipo de atención: {tipo_atencion}")
    print(f"Cantidad: {cantidad}")
    print(f"Valor cita: ${valor_cita:,.0f}")
    print(f"Valor atención: ${valor_atencion_total:,.0f}")
    print(f"Total a pagar: ${total_pagar:,.0f}")

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
    print(f"Ingresos totales recibidos: ${ingresos_totales:,.0f}")
    print(f"Número de clientes para extracción: {clientes_extraccion}")

    # Ordenar clientes por valor de la atención (de mayor a menor)
    clientes_ordenados = sorted(clientes, key=lambda c: c["valor_atencion"], reverse=True)

    print("\n=== LISTA ORDENADA POR VALOR DE ATENCIÓN (MAYOR A MENOR) ===")
    for i, c in enumerate(clientes_ordenados, 1):
        print(f"{i}. {c['nombre']} (Cédula: {c['cedula']}) - Valor atención: ${c['valor_atencion']:,.0f} - Total: ${c['total']:,.0f}")

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
        print(f"Valor cita: ${encontrado['valor_cita']:,.0f}")
        print(f"Valor atención: ${encontrado['valor_atencion']:,.0f}")
        print(f"Total a pagar: ${encontrado['total']:,.0f}")
    else:
        print("No se encontró ningún cliente con esa cédula.")

print("\n=== FIN DEL PROGRAMA ===")