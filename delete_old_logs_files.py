import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    bucket_name = 'nitish-assignment2'  # Replace with your S3 bucket name
    retention_days = 90

    s3 = boto3.client('s3')

    # Calculate the date 90 days ago from now
    deletion_date = datetime.now() - timedelta(days=retention_days)

    # List objects in the bucket
    objects = s3.list_objects_v2(Bucket=bucket_name)

    # Delete objects older than 90 days
    if 'Contents' in objects:
        for obj in objects['Contents']:
            last_modified = obj['LastModified']
            if last_modified.replace(tzinfo=None) < deletion_date:
                s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                print(f'Deleted object: {obj["Key"]}')
    else:
        print('No objects found in the bucket.')

    return {
        'statusCode': 200,
        'body': 'Logs older than 90 days deleted successfully.'
    }
