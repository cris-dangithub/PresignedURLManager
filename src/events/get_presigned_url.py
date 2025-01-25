import json
from src.utils.s3_client import get_s3_client


def handle_get_presigned_url(event):
    bucket_name = event.get("bucket_name")
    object_key = event.get("object_key")
    expiration = event.get("expiration", 3600)

    if not bucket_name or not object_key:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Se requieren 'bucket_name' y 'object_key'"}),
        }

    s3_client = get_s3_client()
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=expiration,
    )

    return {"statusCode": 200, "body": json.dumps({"url": url})}
