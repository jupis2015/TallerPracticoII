# Taller Práctico II - Consultorio Odontológico

## 📋 Descripción

Sistema de gestión de citas para el consultorio odontológico del Dr.Nowzaradan . El programa permite registrar pacientes, calcular costos de atención según el tipo de servicio, tipo de cliente y prioridad, generar estadísticas y buscar clientes por cédula.

## 🚀 Funcionalidades

### Registro de clientes
- Validación de cédula (solo números, mínimo 5 dígitos)
- Validación de nombre (solo letras, mínimo 2 caracteres)
- Validación de teléfono (mínimo 7 dígitos)
- Menús numéricos para selección de opciones:
  - **Tipo de cliente**: Particular, EPS, Prepagada
  - **Tipo de atención**: Limpieza, Calzas, Extracción, Diagnóstico
  - **Prioridad**: Normal, Urgente
- Validación de cantidad según tipo de atención:
  - **Limpieza**: 1 (fijo)
  - **Diagnóstico**: 1 (fijo)
  - **Calzas**: 1 a 3 caries
  - **Extracción**: 1 a 4 piezas
- Validación de fecha (formato DD/MM/AAAA, no puede ser anterior al día actual)

### Cálculo de costos
El valor total a pagar se calcula con la siguiente fórmula:
Total = VALOR_CITA_FIJO + (PRECIO_BASE × CANTIDAD × MULTIPLICADOR) + RECARGO


| Concepto | Valor |
|----------|-------|
| Valor cita fijo | $10 |
| Limpieza | $30 |
| Calzas | $80 |
| Extracción | $100 |
| Diagnóstico | $50 |

| Tipo de cliente | Multiplicador |
|-----------------|---------------|
| Particular | 1.0 |
| EPS | 0.8 |
| Prepagada | 1.2 |

| Prioridad | Recargo |
|-----------|---------|
| Normal | $0 |
| Urgente | $20 |

### Estadísticas
- Total de clientes registrados
- Ingresos totales recibidos
- Número de clientes para extracción

### Listado ordenado
- Muestra todos los clientes ordenados por valor de atención (de mayor a menor)

### Búsqueda de cliente
- Permite buscar un cliente por su número de cédula y mostrar todos sus datos

## 📁 Estructura del código
taller_practico_ii.py
├── Constantes (PRECIOS_BASE, MULTIPLICADOR_CLIENTE, RECARGO_PRIORIDAD, VALOR_CITA_FIJO)
├── Funciones de validación
│ ├── menu_con_opciones() # Menús numéricos
│ ├── validar_cedula() # Validación de cédula
│ ├── validar_nombre() # Validación de nombre
│ ├── validar_telefono() # Validación de teléfono
│ ├── validar_fecha() # Validación de fecha
│ └── validar_continuar() # Validación de continuar
├── Bucle principal de registro
├── Cálculos estadísticos
├── Listado ordenado
└── Búsqueda de cliente


## ▶️ Ejecución

### Requisitos
- Python 3.6 o superior

### Ejecutar el programa
```bash
python taller_practico_ii.py