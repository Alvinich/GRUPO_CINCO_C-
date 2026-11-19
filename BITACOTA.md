## 1. Objetivo de la actividad

Diseñar la base de datos de un sistema de captación de fondos y gestión de donantes para Aldeas Infantiles SOS, siguiendo estas etapas: análisis de diseño, diagrama entidad-relación, implementación en SQL, normalización e integridad de datos.

## 2. Actividades realizadas

| N.° | Actividad | Descripción | Resultado |
|---|---|---|---|
| 1 | Análisis de diseño | Se identificaron los problemas del caso (abandono de padrinos, errores de conciliación, falta de pago con QR y billetera móvil, falta de transparencia para padrinos internacionales). Se definieron actores, módulos y reglas de negocio. | Lista de requerimientos del sistema |
| 2 | Diagrama E-R | Se identificaron las entidades principales (donante, compromiso, programa, pago, método de pago, reporte) y sus relaciones 1:N. Después se hicieron una versión simple y una ampliada a 10 entidades (aldea, niño, pasarela y conciliación). | Diagramas en formato SVG |
| 3 | Implementación | Se escribió el script SQL con `CREATE TABLE`, claves primarias y foráneas. Se crearon 2 consultas: pagos pendientes de conciliar y padrinos en riesgo de abandono. | Script SQL de 6 tablas |
| 4 | Normalización | Se partió de una tabla sin normalizar y se aplicó 1FN, 2FN y 3FN, separando donante, programa, método de pago, compromiso y pago. | Modelo en 3FN |
| 5 | Integridad de datos | Se definieron integridad de entidad, referencial, de dominio, reglas de negocio y transaccional (ACID), con `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `CHECK` y transacciones. | Reglas de integridad aplicadas al script |

## 3. Herramientas utilizadas

- Lenguaje SQL (MySQL) para la creación de tablas y consultas.
- Diagramas entidad-relación elaborados en formato SVG.
- Asistente de inteligencia artificial como apoyo para estructurar el diseño, que fue revisado y comprendido por el estudiante.

## 4. Conceptos aplicados de programación y bases de datos

- **Clave primaria (PK):** identifica de forma única cada registro.
- **Clave foránea (FK):** relaciona tablas y evita registros huérfanos.
- **Tipos de dato y restricciones:** `INT`, `VARCHAR`, `DECIMAL`, `ENUM`, `NOT NULL`, `UNIQUE`, `CHECK`.
- **Consultas con `JOIN`, `GROUP BY` y `HAVING`:** para unir tablas y filtrar resultados.
- **Transacciones (`START TRANSACTION`, `COMMIT`, `ROLLBACK`):** para que una operación se complete entera o no se haga.

## 5. Dificultades encontradas

- Decidir qué entidades incluir para que el diagrama fuera completo pero fácil de entender.
- Distinguir las dependencias parciales y transitivas al normalizar.
- Elegir qué reglas de negocio podían resolverse con restricciones de la base de datos y cuáles necesitaban lógica adicional.

## 6. Soluciones aplicadas

- Se empezó con 6 entidades y luego se amplió a 10 para tener una versión simple y una completa.
- Se aplicó la normalización paso a paso, preguntando en cada forma normal qué dato depende de qué clave.
- Se usaron `CHECK` y `UNIQUE` para las reglas más importantes, como montos positivos y referencias de pago no repetidas.

## 7. Aprendizajes

- Un buen diseño de base de datos evita duplicados y errores desde el inicio.
- La normalización y las restricciones de integridad protegen datos sensibles como pagos y datos de donantes.
- Un diagrama claro facilita la comunicación entre el equipo antes de programar.
- Las herramientas de IA ayudan a avanzar, pero hay que entender y verificar lo que producen.

## 8. Conclusiones

El diseño propuesto cubre los problemas detectados en el caso: el control de pagos y su conciliación, el seguimiento de los padrinos y la base para un portal de transparencia. El modelo queda en tercera forma normal y con reglas de integridad que mantienen los datos confiables.