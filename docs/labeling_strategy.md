# Estrategia de Weak Labels

Reglas heurísticas configurables:
- >= N fallos en ventana T por IP/usuario.
- Usuarios privilegiados/administrativos.
- Horarios inusuales.

Se combinan en una etiqueta binaria `weak_label` para evaluación proxy y re-ranking.
