#                ** Reporte de Métricas – Motor de Extracción G2 **

# 1 Resumen

Se realizaron tres pruebas progresivas de carga y estabilidad (20, 50 y 100 iteraciones) con variación de categorías y delays humanos controlados.

-> En todas las ejecuciones:

- No se detectaron bloqueos.
- No se registraron errores.
- La tasa de éxito fue del 100%.
- No hubo degradación progresiva de latencia.
- El dataset final fue consistente y sin duplicados.

# Resultados por Escenario

** Prueba 1 – 20 Iteraciones
=> Métrica	    => Resultado
Iteraciones	        20
Success Count	    20
Error Count	        0
Tasa de Éxito	    100%
Latencia Promedio	7.56s
Tiempo Total	    389.7s
Bloqueos Detectados	0

** Prueba 2 – 50 Iteraciones
=> Métrica	     => Resultado
Iteraciones	         50
Success Count	     50
Error Count	         0
Tasa de Éxito	     100%
Latencia Promedio	 9.74s
Tiempo Total	     1055.97s
Bloqueos Detectados	 0

** Prueba Final – 100 Iteraciones
Métrica	Resultado
Iteraciones	100
Success Count	100
Error Count	0
Tasa de Éxito	100%
Latencia Promedio	7.12s
Tiempo Total	2080.93s
Bloqueos Detectados	0
Dataset Final

-> Productos extraídos: 432

- Enlaces únicos: 432
- Categorías procesadas: 5
- Duplicados: 0
- Pérdida de datos por fallos dinámicos: 0

NOTA: Aqui se aumenta el range delay de (5.0s - 15.0s) a (6.0s - 18.0s), con motivo de validar si el estado de latencia baja y el score de deteccion de datadome y cloudflare disminuye al usar tiempos de carga y espera mas pausados.

# 3 Análisis de Estabilidad

- No se detectó degradación progresiva en latencia.
- No se registraron reintentos críticos.
- No hubo activación de mecanismos de challenge.
- El sistema mantuvo consistencia entre la iteración 1 y la 100.

# Manejo de Excepciones

-> El motor incorpora:

- Retry con backoff exponencial.
- Detector de bloqueos por HTML reducido.
- Validación mínima de productos extraídos.
- Registro estructurado de métricas.
- Control de latencia y pausas humanas variables.