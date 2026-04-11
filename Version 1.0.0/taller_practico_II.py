# Proyecto: TallerPracticoII
# Programa para gestionar citas del consultorio odontológico del Dr.Nowzaradan

import re
from datetime import datetime, timedelta

# Los precios de la cita según el tipo de cliente
VALOR_CITA = {
    "Particular": 80000,
    "EPS": 5000,
    "Prepagada": 30000
}

# Los precios de los tratamientos según el tipo de cliente
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

# Aquí guardamos todos los clientes
clientes = []


# Esta función muestra un menú y pide que escojas una opción
def menu_con_opciones(titulo, opciones):
    print(f"\n--- {titulo} ---")
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}. {opcion}")

    while True:
        try:
            seleccion = int(input("Escoja una opción (número): "))
            if 1 <= seleccion <= len(opciones):
                return opciones[seleccion - 1]
            else:
                print(f"Esa opción no sirve. Escoja entre 1 y {len(opciones)}.")
        except ValueError:
            print("Tiene que escribir un número.")


# Validar que la cédula tenga solo números
def validar_cedula(mensaje):
    while True:
        cedula = input(mensaje).strip()
        if cedula.isdigit() and len(cedula) >= 5:
            return cedula
        print("Cédula no válida. Solo números y mínimo 5 dígitos.")


# Validar que el nombre no tenga cosas raras
def validar_nombre(mensaje):
    while True:
        nombre = input(mensaje).strip()
        
        if not nombre or len(nombre) < 2:
            print("ERROR Nombre muy corto, mínimo 2 caracteres.")
            continue
            
        # Solo letras y espacios
        if not all(c.isalpha() or c.isspace() or c in "áéíóúñÁÉÍÓÚÑ" for c in nombre):
            print("ERROR Use solo letras y espacios, sin números ni símbolos.")
            continue
        
        # Nada de espacios dobles
        if "  " in nombre:
            print("ERROR Sin espacios dobles por favor.")
            continue
        
        # Que tenga vocales (porque los nombres de verdad tienen vocales)
        letras = [c for c in nombre if c.isalpha()]
        if len(letras) < 2:
            print("ERROR Demasiado corto.")
            continue
            
        vocales = sum(1 for c in letras if c.lower() in "aeiouáéíóú")
        consonantes = len(letras) - vocales
        
        if vocales == 0 or (vocales / len(letras)) < 0.2:
            print("ERROR Eso no parece un nombre real, ¿dónde están las vocales?")
            continue
        
        # Que no repita mucho la misma letra
        from collections import Counter
        conteo = Counter(c.lower() for c in letras)
        max_repeticion = max(conteo.values())
        if max_repeticion > len(letras) * 0.6:
            print("ERROR Demasiadas letras repetidas, eso es sospechoso.")
            continue
        
        return nombre.title()


# Validar teléfono (solo números y que tenga sentido)
def validar_telefono(mensaje):
    while True:
        telefono = input(mensaje).strip()
        
        if not telefono.isdigit():
            print("ERROR Solo números, sin guiones ni espacios. Ejemplo: 3012762712")
            continue
        
        if len(telefono) < 7:
            print(f"ERROR El teléfono es muy corto. Mínimo 7 dígitos (ingresó {len(telefono)})")
            continue
        
        if len(telefono) > 15:
            print(f"ERROR Demasiados números. Máximo 15 dígitos (ingresó {len(telefono)})")
            continue
        
        # Que no sea 1111111 o algo así
        if len(set(telefono)) == 1:
            print("ERROR Ese número no es válido (todos los dígitos iguales).")
            continue
        
        print(f"Teléfono guardado: {telefono}")
        return telefono


# Validar fecha (formato y que no sea muy lejos)
def validar_fecha(mensaje, max_dias=365):
    while True:
        fecha = input(mensaje).strip()
        try:
            fecha_obj = datetime.strptime(fecha, "%d/%m/%Y")
            fecha_actual = datetime.now().date()
            fecha_ingresada = fecha_obj.date()
            
            diferencia_dias = (fecha_ingresada - fecha_actual).days
            
            if fecha_ingresada < fecha_actual:
                print("ERROR No se pueden agendar citas en el pasado.")
            elif diferencia_dias > max_dias:
                fecha_limite = fecha_actual + timedelta(days=max_dias)
                print(f"ERROR Muy lejos, máximo {max_dias} días.")
                print(f"Fecha tope: {fecha_limite.strftime('%d/%m/%Y')}")
            else:
                print(f"Fecha agendada: {fecha}")
                return fecha
        except ValueError:
            print("ERROR Formato incorrecto. Use DD/MM/AAAA (ejemplo: 25/12/2024)")


# Preguntar si quiere seguir o no
def validar_continuar(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ['s', 'n']:
            return respuesta
        print("Escriba 's' para sí o 'n' para no.")


# Empieza el programa
print("=== REGISTRO DE CITAS ODONTOLÓGICAS ===")

while True:
    print("\n--- Nuevo cliente ---")

    cedula = validar_cedula("Cédula: ")
    nombre = validar_nombre("Nombre Completo: ")
    telefono = validar_telefono("Teléfono: ")

    # Qué tipo de cliente es
    tipo_cliente = menu_con_opciones("TIPO DE CLIENTE", [
        "Particular",
        "EPS",
        "Prepagada"
    ])

    # Qué se va a hacer
    tipo_atencion = menu_con_opciones("TIPO DE ATENCIÓN", [
        "Limpieza",
        "Calzas",
        "Extracción",
        "Diagnóstico"
    ])

    # Cuántas cosas según el tratamiento
    if tipo_atencion == "Limpieza":
        cantidad = 1
        print("La limpieza solo se puede agendar de a 1.")
    elif tipo_atencion == "Diagnóstico":
        cantidad = 1
        print("El diagnóstico solo se puede agendar de a 1.")
    elif tipo_atencion == "Calzas":
        while True:
            try:
                print("\n--- CALZAS ---")
                print("Máximo 3 caries por cita")
                cantidad = int(input("Cuántas caries va a tratar: "))
                if 1 <= cantidad <= 3:
                    break
                elif cantidad <= 0:
                    print("Tiene que ser más de cero.")
                else:
                    print(f"Se pueden hacer máximo 3 calzas, usted puso {cantidad}")
            except ValueError:
                print("Escriba un número entero.")
    elif tipo_atencion == "Extracción":
        while True:
            try:
                print("\n--- EXTRACCIÓN ---")
                print("Máximo 4 dientes por cita")
                cantidad = int(input("Cuántos dientes va a sacar: "))
                if 1 <= cantidad <= 4:
                    break
                elif cantidad <= 0:
                    print("Tiene que ser más de cero.")
                else:
                    print(f"Máximo 4 extracciones, usted puso {cantidad}")
            except ValueError:
                print("Escriba un número entero.")

    # Urgente o normal (aunque no cambia el precio)
    prioridad = menu_con_opciones("PRIORIDAD", [
        "Normal",
        "Urgente"
    ])

    fecha = validar_fecha("Fecha de la cita (DD/MM/AAAA): ")

    # Hacer las cuentas
    valor_cita = VALOR_CITA[tipo_cliente]
    valor_atencion_unitario = VALORES_ATENCION[tipo_cliente][tipo_atencion]
    valor_atencion_total = valor_atencion_unitario * cantidad
    
    total_pagar = valor_cita + valor_atencion_total

    # Guardar los datos del cliente
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

    # Mostrar resumen
    print(f"\n=== CLIENTE REGISTRADO ===")
    print(f"Nombre Completo: {nombre}")
    print(f"Tipo de cliente: {tipo_cliente}")
    print(f"Procedimiento: {tipo_atencion}")
    print(f"Cantidad: {cantidad}")
    print(f"Valor cita: ${valor_cita:,.0f}")
    print(f"Valor tratamiento: ${valor_atencion_total:,.0f}")
    print(f"Total a pagar: ${total_pagar:,.0f}")

    continuar = validar_continuar("\n¿Registrar otro cliente? (s/n): ")
    if continuar == 'n':
        break

# Si no hay nadie registrado
if not clientes:
    print("\nNo se registró nada. Programa terminado.")
else:
    # Sacar cuentas
    total_clientes = len(clientes)
    ingresos_totales = sum(c["total"] for c in clientes)
    clientes_extraccion = sum(1 for c in clientes if c["tipo_atencion"] == "Extracción")

    print("\n=== ESTADÍSTICAS RÁPIDAS ===")
    print(f"Total clientes atendidos: {total_clientes}")
    print(f"Plata recibida: ${ingresos_totales:,.0f}")
    print(f"Clientes que sacaron dientes: {clientes_extraccion}")

    # Ordenar de mayor a menor por lo que pagaron en tratamiento
    clientes_ordenados = sorted(clientes, key=lambda c: c["valor_atencion"], reverse=True)

    print("\n=== LISTA DE CLIENTES (el que más pagó en tratamiento primero) ===")
    for i, c in enumerate(clientes_ordenados, 1):
        print(f"{i}. {c['nombre']} (C.C. {c['cedula']}) - Pagó en tratamiento: ${c['valor_atencion']:,.0f} - Total: ${c['total']:,.0f}")

    # Buscar cliente por cédula
    print("\n=== BUSCAR CLIENTE ===")
    buscar_cedula = input("Escriba la cédula a buscar: ")
    encontrado = None
    for cliente in clientes_ordenados:
        if cliente["cedula"] == buscar_cedula:
            encontrado = cliente
            break

    if encontrado:
        print("\n=== ACÁ ESTÁ EL CLIENTE ===")
        print(f"Cédula: {encontrado['cedula']}")
        print(f"Nombre Completo: {encontrado['nombre']}")
        print(f"Teléfono: {encontrado['telefono']}")
        print(f"Tipo de cliente: {encontrado['tipo_cliente']}")
        print(f"Tratamiento: {encontrado['tipo_atencion']}")
        print(f"Cantidad: {encontrado['cantidad']}")
        print(f"Prioridad: {encontrado['prioridad']}")
        print(f"Fecha: {encontrado['fecha']}")
        print(f"Valor cita: ${encontrado['valor_cita']:,.0f}")
        print(f"Valor tratamiento: ${encontrado['valor_atencion']:,.0f}")
        print(f"Total a pagar: ${encontrado['total']:,.0f}")
    else:
        print("No encontré a nadie con esa cédula.")

print("\n=== QUE TENGAS UN BUEN DÍA ===")