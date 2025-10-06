# Bot Bancario - Prueba Técnica

**Link:** [t.me/bancotec_bot](https://t.me/bancotec_bot)

---

### Comandos

- `/start` - Iniciar sesión (solicita PIN de usuario)
- `/logout` - Cerrar sesión y limpiar historial

### Operaciones Disponibles

**Gestión de Cuenta:**

- Consulta de saldo actual
- Visualización de últimos movimientos

**Préstamos:**

- Simulación de préstamos con cálculo de tasa de interés
- Verificación de historial crediticio (aplica penalización por mora)
- Consulta de préstamos pendientes
- Detalle de cuotas pendientes por préstamo

**Información Bancaria:**

- Consultas sobre tarjetas disponibles
- Información sobre plazos fijos
- Tasas de interés para préstamos personales

> **Nota:** Las tasas de interés están basadas en el estándar BROU sin retención.

---

## Usuarios de Prueba

**Juan Pérez López**  
PIN:`1234`
Dos préstamos pendientes (no puede solicitar más)

**María González Ruiz**
PIN:`5678`
Un préstamo pendiente con cuota vencida (penalización por mora)

**Carlos Ramírez Soto**  
PIN:`9012`
Sin préstamos pendientes

---

## Instalación y Configuración

### Requisitos Previos

- Docker

### Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto con la siguiente estructura:

```env
token=Token_Telegram
MISTRAL_API_KEY=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
```

> **Nota:** Los valores específicos para estas variables fueron enviados por correo electrónico.

### Ejecución

```bash
docker-compose up
```

El bot estará disponible inmediatamente después de que los contenedores inicien correctamente.

---

## Limitaciones Conocidas

**Error de Capacidad (HTTP 429):**

Si se interactúa muy rápidamente con el bot, puede aparecer el siguiente error:

```
API error occurred: Status 429
Service tier capacity exceeded for this model
```

**Causa:** El proyecto utiliza Mistral (LLM open source) en su versión gratuita, la cual tiene límites de capacidad.

**Solución:** Esperar unos segundos entre mensajes. Agradezco su paciencia durante la evaluación.

---

## Tecnologías utilizadas

- **Bot Framework:** Python Telegram Bot
- **LLM:** Mistral AI (versión gratuita)
- **Base de Datos:** PostgreSQL
- **Containerización:** Docker
- **Referencia de Datos:** BROU (Banco República Oriental del Uruguay)

---
