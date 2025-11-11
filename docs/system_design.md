# System Design

## Diagrama
```mermaid
graph LR
A[Logs raw] --> B[Parser]
B --> C[Features]
C --> D[Modelos no supervisados]
C --> E[Reglas (weak labels)]
D --> F[Ranking]
E --> G[Evaluación proxy]
F --> G
```

## Decisiones
- Validación temporal para evitar leakage.
- Pipelines sklearn para reproducibilidad.
- Configuración YAML para portabilidad.
