# 🦷 TallerPracticoII: Gestión de Citas Odontológicas
### Consultorio Dr. Nowzaradan

Este proyecto es una aplicación de consola desarrollada en **PythonPython 3.13.3** diseñada para automatizar la gestión de pacientes y la facturación de servicios odontológicos. El sistema integra validaciones avanzadas de datos y lógica de negocio basada en diferentes tipos de afiliación (EPS, Prepagada, Particular).

---

## 🚀 Características Principales

* **Validación Rigurosa de Entradas:** Implementación de lógica personalizada para:
    * **Nombres Reales:** Detección de entradas inválidas mediante análisis de proporción de vocales y repetición de caracteres.
    * **Fechas Inteligentes:** Restricción de citas pasadas o con más de un año de antelación.
    * **Formatos Estrictos:** Validación de cédulas y números telefónicos.
* **Motor de Facturación Dinámico:** Cálculo automático de costos según el procedimiento y el convenio del paciente.
* **Control de Procedimientos:** Límites lógicos por sesión (ej. máximo 3 calzas o 4 extracciones).
* **Módulo Estadístico:** Generación de reportes de ingresos totales y conteo de servicios al finalizar el día.
* **Gestión de Datos:** Ordenamiento de registros por valor de atención y búsqueda indexada por cédula.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.13.3
* **Módulos Estándar:** * `datetime` (Manejo de tiempos y plazos).
    * `re` (Expresiones regulares para limpieza de datos).
    * `collections.Counter` (Análisis de calidad de strings).

---

## 📊 Estructura de Costos

| Tipo de Cliente | Valor Base Cita | Limpieza | Calzas (u) | Extracción (u) | Diagnóstico |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Particular** | $80,000 | $60,000 | $80,000 | $100,000 | $50,000 |
| **EPS** | $5,000 | $0 | $40,000 | $40,000 | $0 |
| **Prepagada** | $30,000 | $0 | $10,000 | $10,000 | $0 |

---

## 💻 Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/jupis2015/TallerPracticoII.git](https://github.com/jupis2015/TallerPracticoII.git)
    ```
2.  **Ejecutar la aplicación:**
    ```bash
    python gestion_odontologica.py
    ```

---

## 🧠 Lógica de Validación (Ingeniería de Sistemas)

Para asegurar la integridad de la base de datos, el sistema no solo verifica tipos de datos, sino también la **verosimilitud** del nombre ingresado:
1.  Calcula que al menos el **20%** de los caracteres sean vocales.
2.  Valida que ninguna letra represente más del **60%** del total del nombre.
3.  Esto previene ingresos accidentales como `"asdfghjkl"` o `"aaaaaaa"`.

---

**Autor:** Henry Franco Velez  
**Facultad:** Ingeniería de Sistemas  
**Asignatura:** Programación de Sistemas / Taller Práctico II