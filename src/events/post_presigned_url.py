import json
from src.utils.s3_client import get_s3_client


def handle_post_presigned_url(event):
    bucket_name = event.get("bucket_name")
    object_key = event.get("object_key")
    expiration = event.get("expiration", 60)
    #  xlsx contentype
    content_type = event.get(
        "content_type",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    if not bucket_name or not object_key:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Se requieren 'bucket_name' y 'object_key'"}),
        }

    s3_client = get_s3_client()
    url = s3_client.generate_presigned_post(
        bucket_name,
        object_key,
        ExpiresIn=expiration,
    )

    return {"statusCode": 200, "body": json.dumps({"url": url})}
