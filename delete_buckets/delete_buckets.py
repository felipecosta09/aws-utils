import boto3
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Delete S3 buckets by prefix.")
parser.add_argument(
    '--prefix',
    required=True,
    help='Comma-separated list of prefixes for the buckets to delete'
)
args = parser.parse_args()

# Prepare prefixes list
prefixes = [p.strip() for p in args.prefix.split(',') if p.strip()]

# Initialize global S3 client
s3_global = boto3.client('s3')

def get_bucket_region(bucket_name):
    """Get the region of a bucket"""
    response = s3_global.get_bucket_location(Bucket=bucket_name)
    return response.get('LocationConstraint') or 'us-east-1'

def empty_bucket(bucket_name, region):
    """Empty all objects and versions in a bucket"""
    s3_resource = boto3.resource('s3', region_name=region)
    bucket = s3_resource.Bucket(bucket_name)

    try:
        # Delete object versions (if any)
        bucket.object_versions.delete()
        print(f"✔️ Deleted all versions in: {bucket_name}")
    except Exception as e:
        print(f"⚠️ Skipping version deletion for {bucket_name}: {e}")

    try:
        # Delete all regular objects
        bucket.objects.all().delete()
        print(f"✔️ Deleted all objects in: {bucket_name}")
    except Exception as e:
        print(f"❌ Error deleting objects from {bucket_name}: {e}")

def delete_bucket(bucket_name, region):
    """Delete an empty bucket"""
    s3_client = boto3.client('s3', region_name=region)
    try:
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"🗑️ Bucket deleted: {bucket_name}")
    except Exception as e:
        print(f"❌ Error deleting bucket {bucket_name}: {e}")

def main():
    buckets = s3_global.list_buckets().get('Buckets', [])

    for bucket in buckets:
        name = bucket['Name']
        if any(name.startswith(prefix) for prefix in prefixes):
            print(f"\n📦 Found bucket: {name}")
            try:
                region = get_bucket_region(name)
                print(f"🌍 Region: {region}")
                empty_bucket(name, region)
                delete_bucket(name, region)
            except Exception as e:
                print(f"❌ Failed processing {name}: {e}")

if __name__ == "__main__":
    main()
