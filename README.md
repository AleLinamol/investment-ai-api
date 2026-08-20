# Investment AI API

Backend educativo para una sociedad de bolsa ficticia. El proyecto busca practicar el diseño de una API financiera realista con Python, FastAPI, PostgreSQL, autenticación y una integración segura con modelos de lenguaje.

## Problema que resuelve

La API centralizará la información de clientes, cuentas de inversión, instrumentos financieros y operaciones de compra y venta. A partir de ese historial permitirá consultar posiciones y exposición de cartera.

En una etapa posterior incorporará un asistente de IA capaz de explicar información financiera en lenguaje natural. El modelo no accederá directamente a la base de datos, no decidirá permisos y no podrá ejecutar operaciones financieras.

Ejemplos de consultas futuras:

- ¿Cuánto invirtió este cliente durante agosto?
- ¿En qué instrumentos tiene mayor exposición?
- ¿Cuál es su posición actual?
- ¿Qué porcentaje de su cartera está invertido en acciones?

## Alcance inicial

El proyecto simula un sistema interno de inversiones; no se conecta a mercados reales ni administra dinero real.

Las entidades principales serán:

- **User:** identidad que inicia sesión y posee un rol.
- **Client:** persona o empresa propietaria de las inversiones.
- **Account:** cuenta de inversión perteneciente a un cliente.
- **Instrument:** activo financiero, como una acción, un bono o un ETF.
- **Transaction:** compra o venta de un instrumento realizada desde una cuenta.

## Reglas de negocio decididas

### Posiciones y ventas

- Las operaciones iniciales serán `BUY` y `SELL`.
- La posición de un instrumento se calculará como la suma de compras menos la suma de ventas.
- La primera versión no permitirá ventas en corto.
- Una operación `SELL` se rechazará si su cantidad supera la posición disponible del instrumento en la cuenta.
- Esta validación será responsabilidad del backend y no del cliente de la API.
- Ante una venta incompatible con la posición actual, la API responderá con `409 Conflict`.
- Las transacciones confirmadas no se editarán ni eliminarán directamente.
- Una corrección deberá conservar el movimiento original y registrar una reversión para mantener un historial auditable.

### Importes y precisión

- Las cantidades, precios e importes se representarán con `Decimal`, no con `float`.
- Los importes monetarios del alcance inicial se redondearán a dos decimales usando `ROUND_HALF_UP`.
- La previsualización admite hasta ocho decimales para cantidades y cuatro para precios unitarios.
- Estas reglas evitan errores de representación binaria y hacen explícita la política de redondeo.
- El importe bruto se calculará como `cantidad × precio unitario`.
- La primera versión no incluirá comisiones, impuestos ni derechos de mercado; se excluyen deliberadamente para mantener el foco educativo.

### Clientes y cuentas

- Un cliente podrá tener varias cuentas de inversión.
- Cada cuenta tendrá una única moneda.
- Esta relación permitirá representar, por ejemplo, una cuenta en pesos y otra en dólares para un mismo cliente.

## Seguridad de la IA

La integración futura seguirá estas reglas:

- Autorizar la solicitud antes de recuperar información financiera.
- Enviar al modelo solamente los datos necesarios.
- No permitir que el modelo decida permisos ni reglas de negocio.
- Validar las respuestas estructuradas antes de utilizarlas.
- No permitir que el modelo ejecute operaciones financieras.
- No exponer secretos ni datos sensibles en prompts o logs.

## Logging y manejo de errores

La aplicación tendrá logging interno centralizado para facilitar el diagnóstico de errores y la auditoría técnica.

- Se usarán niveles de log (`DEBUG`, `INFO`, `WARNING`, `ERROR` y `CRITICAL`) según la gravedad del evento.
- En producción se preferirán logs estructurados para facilitar búsquedas y alertas.
- Los errores inesperados incluirán contexto técnico y un identificador de correlación, pero la respuesta HTTP no expondrá detalles internos.
- No se registrarán contraseñas, tokens JWT, secretos, documentos completos, prompts con datos sensibles ni información financiera innecesaria.
- Los eventos relevantes podrán identificar recursos mediante IDs internos cuando sea necesario, respetando el principio de mínima exposición.
- La configuración concreta se incorporará junto con el manejo centralizado de errores, cuando exista un caso real que registrar.

## Estado actual

La Etapa 1 está en desarrollo en la rama `feature/setup-fastapi`.

Implementado:

- Entorno virtual de Python.
- Aplicación FastAPI mínima.
- Endpoint operativo `GET /health`.
- Contrato de respuesta de `/health` validado y documentado con Pydantic.
- Previsualización de transacciones con validación Pydantic y cálculo decimal del importe bruto.

## Estructura actual

```text
app/
├── main.py
├── routers/
│   ├── health.py
│   └── transactions.py
└── schemas/
    ├── health.py
    └── transaction.py
```

- `main.py` crea la aplicación e incorpora sus routers.
- `routers/` define las rutas HTTP y coordina cada solicitud.
- `schemas/` contiene los contratos de entrada y salida validados por Pydantic.

Se agregarán capas como `services` y `repositories` cuando exista lógica de negocio y persistencia que justifiquen esa separación.

El endpoint de salud comprueba que el servidor pudo cargar la aplicación y que esta puede responder solicitudes HTTP. No comprueba todavía la conexión con PostgreSQL ni servicios externos.

## Ejecución local

Con el entorno virtual activado, instalar las dependencias:

```powershell
python -m pip install -r requirements.txt
```

`requirements.txt` declara las dependencias directas y sus versiones para que otra persona pueda reproducir el entorno. `pip` instalará también las dependencias transitivas requeridas por FastAPI y Uvicorn.

Levantar el servidor de desarrollo:

```powershell
python -m uvicorn app.main:app --reload
```

La API queda disponible en:

- Salud: <http://127.0.0.1:8000/health>
- Documentación interactiva: <http://127.0.0.1:8000/docs>

`--reload` se usa solamente durante el desarrollo para reiniciar el servidor cuando cambia el código.

### Verificar el endpoint de salud

Con Uvicorn en ejecución, abrir <http://127.0.0.1:8000/health> en el navegador o consultarlo desde una segunda terminal de PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

La respuesta esperada es:

```json
{
  "status": "ok"
}
```

La terminal de Uvicorn debería registrar una solicitud exitosa similar a:

```text
GET /health HTTP/1.1 200 OK
```

`200 OK` indica que el servidor recibió la solicitud y la aplicación respondió correctamente. Este control solo verifica que FastAPI está disponible; no comprueba todavía PostgreSQL ni servicios externos.

### Explorar la documentación interactiva

Abrir <http://127.0.0.1:8000/docs>, seleccionar `GET /health`, presionar **Try it out** y luego **Execute**. FastAPI genera esta interfaz a partir de las rutas, tipos y modelos declarados en el código.

### Previsualizar una transacción

`POST /transactions/preview` valida los datos y calcula el importe bruto sin guardar ni ejecutar la operación.

Con Uvicorn en ejecución, probar desde PowerShell:

```powershell
$body = @{
    operation_type = "BUY"
    symbol = "aapl"
    quantity = "10"
    unit_price = "180.25"
    currency = "USD"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri http://127.0.0.1:8000/transactions/preview `
    -ContentType "application/json" `
    -Body $body
```

Respuesta esperada:

```json
{
  "operation_type": "BUY",
  "symbol": "AAPL",
  "quantity": "10",
  "unit_price": "180.25",
  "currency": "USD",
  "gross_amount": "1802.50"
}
```

Los valores decimales se envían como strings en JSON para conservar su precisión durante el intercambio entre sistemas.

### Detener el servidor

En la terminal donde se está ejecutando Uvicorn, presionar:

```text
Ctrl + C
```

## Flujo de trabajo con Git

La Etapa 1 se desarrolla en `feature/setup-fastapi`. Una rama puede contener varios commits pequeños y coherentes.

Revisar los cambios antes de crear un commit:

```powershell
git status
git diff
```

Guardar el bloque inicial de FastAPI:

```powershell
git add .
git commit -m "feat: add initial FastAPI endpoints"
```

Publicar la rama por primera vez:

```powershell
git push -u origin feature/setup-fastapi
```

La rama se integrará en `main` cuando toda la Etapa 1 esté terminada y revisada.

## Roadmap

1. Configuración inicial, FastAPI, Pydantic y primer endpoint.
2. PostgreSQL, SQLAlchemy, migraciones y CRUD.
3. Autenticación, JWT, roles y autorización.
4. Operaciones financieras, agregaciones y transacciones SQL.
5. Integración con un LLM y validación de respuestas.
6. RAG y mitigaciones para prompt injection y alucinaciones.
7. Tests y revisión técnica del proyecto.
