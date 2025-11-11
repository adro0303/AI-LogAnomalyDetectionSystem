# Model Card — OpenSSH Anomaly Detector

## Resumen
Detector no supervisado para priorizar eventos anómalos en logs OpenSSH. Métrica principal: PR-AUC (proxy) sobre etiquetas débiles.

## Datos
- Fuente: Loghub / OpenSSH (datos reales de aplicaciones de servidor)
- Preprocesamiento: parsing syslog → features temporales/semánticas.

## Uso previsto
Soporte a analistas de seguridad para priorizar alertas (offline). No sustituye revisiones humanas.

## Riesgos
- Weak labels con ruido → riesgo de falsos positivos/negativos.
- Potencial exposición de IP/usuarios → anonimización en muestras públicas.

## Métricas
- PR-AUC (proxy), Recall@K, reducción de alertas vs. baseline.
