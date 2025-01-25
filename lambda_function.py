import json
import logging
from src.events.get_presigned_url import handle_get_presigned_url
from src.events.post_presigned_url import handle_post_presigned_url

# Configuración de logs
logging.basicConfig(level=logging.INFO)


def lambda_handler(event, context):
    print("Evento recibido: ", event)
    logging.info(f"Evento recibido: {event}")

    event_type = event.get("type")
    if not event_type:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Falta el campo 'type' en el evento"}),
        }

    try:
        if event_type == "get-presigned-url":
            logging.info("Ejecutando operación: Get Presigned URL")
            return handle_get_presigned_url(event)
        elif event_type == "post-presigned-url":
            logging.info("Ejecutando operación: Post Presigned URL")
            return handle_post_presigned_url(event)
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Tipo de evento no soportado"}),
            }
    except Exception as e:
        logging.error(f"Error procesando el evento: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Error interno del servidor"}),
        }
