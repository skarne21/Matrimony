import boto3
import json
from PIL import Image
import io

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

PUBLIC_BUCKET = 'matrimony-public-profiles'
RAW_BUCKET = 'matrimony-raw-uploads'

TARGET_SIZE = (800, 800)


def lambda_handler(event, context):
    record = event['Records'][0]
    raw_bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    raw_obj = s3.get_object(Bucket=raw_bucket, Key=key)
    raw_bytes = raw_obj['Body'].read()

    # Moderation check
    rekognition_response = rekognition.detect_moderation_labels(
        Image={'Bytes': raw_bytes},
        MinConfidence=75,
    )
    labels = [label['Name'] for label in rekognition_response.get('ModerationLabels', [])]

    if labels:
        # Route to quarantine — do not publish
        print(f"QUARANTINE: {key} flagged for {labels}")
        s3.copy_object(
            Bucket=raw_bucket,
            CopySource={'Bucket': raw_bucket, 'Key': key},
            Key=f'quarantine/{key}',
        )
        return {'statusCode': 200, 'body': json.dumps({'status': 'quarantined', 'labels': labels})}

    # Compress and convert to WebP
    image = Image.open(io.BytesIO(raw_bytes)).convert('RGB')
    image.thumbnail(TARGET_SIZE, Image.LANCZOS)

    output = io.BytesIO()
    image.save(output, format='WEBP', quality=85)
    output.seek(0)

    webp_key = key.rsplit('.', 1)[0] + '.webp'
    s3.put_object(
        Bucket=PUBLIC_BUCKET,
        Key=webp_key,
        Body=output,
        ContentType='image/webp',
    )

    print(f"Published: {webp_key}")
    return {'statusCode': 200, 'body': json.dumps({'status': 'published', 'key': webp_key})}
