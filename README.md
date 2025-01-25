
# AWS Lambda: Presigned URL Manager

Esta Lambda genera URLs prefirmadas de S3 para descargar o subir archivos, según el evento recibido.

## Estructura del Proyecto

```plaintext
.
├── .github
│   └── workflows
│       ├── deploy_lambda.yaml          # Para desplegar la Lambda
│       └── update_layer.yaml           # Para actualizar la Layer si cambia requirements.txt
├── src
│   ├── events
│   │   ├── get_presigned_url.py        # Manejador del evento 'get-presigned-url'
│   │   └── post_presigned_url.py       # Manejador del evento 'post-presigned-url'
│   └── utils
│       └── s3_client.py                # Cliente de S3 reutilizable
├── lambda_function.py                  # Punto de entrada de la Lambda
├── requirements.txt                    # Lista de dependencias
├── README.md                           # Documentación del proyecto

```

- **lambda_function.py**: Entrada principal de la Lambda, gestiona los eventos.
- **src/events**: Contiene la lógica específica para cada tipo de evento.
- **src/utils**: Funciones comunes y utilidades, como el cliente S3.

## Input y Output

### Entrada
El evento debe incluir:

```json
{
  "type": "get-presigned-url", // O "post-presigned-url"
  "bucket_name": "nombre-del-bucket",
  "object_key": "nombre-del-archivo",
  "expiration": 3600 // (opcional) Tiempo en segundos
}
```

### Salida

**Éxito:**
```json
{
  "url": "https://bucket.s3.amazonaws.com/object?..."
}
```

**Error:**
```json
{
  "error": "Mensaje de error"
}
```

## Uso desde JavaScript

### Llamada a la Lambda

```javascript
const fetch = require('node-fetch');

async function callLambda(type, bucketName, objectKey) {
    const response = await fetch('https://tu-lambda-url.amazonaws.com/default/PresignedURLManager', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            type,
            bucket_name: bucketName,
            object_key: objectKey,
            expiration: 3600
        })
    });

    const data = await response.json();
    if (response.ok) {
        console.log('Presigned URL:', data.url);
    } else {
        console.error('Error:', data.error);
    }
}
```

### Ejemplo

```javascript
// Obtener URL para descargar
callLambda('get-presigned-url', 'mi-bucket', 'mi-archivo.txt');

// Obtener URL para subir
callLambda('post-presigned-url', 'mi-bucket', 'mi-archivo.txt');
```

## Despliegue

1. Sube el código a AWS Lambda y asegúrate de que tenga permisos para acceder a S3.
2. Configura el rol de IAM con permisos:
   - `s3:GetObject`
   - `s3:PutObject`
3. Configura el entorno de ejecución con Python 3.x.
4. Asegúrate de incluir las dependencias necesarias (si las hay).

## Notas

- **Seguridad**: Limita los permisos del bucket a usuarios o roles específicos según sea necesario.
- **Logs**: Los eventos y errores se registran en CloudWatch para facilitar la depuración.

## Autor

Este proyecto fue generado para gestionar presigned URLs de manera eficiente en AWS.

