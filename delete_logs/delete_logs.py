import boto3
import argparse

def get_all_regions():
    """Retrieve all AWS regions."""
    ec2 = boto3.client('ec2')
    response = ec2.describe_regions(AllRegions=False)
    regions = [region['RegionName'] for region in response['Regions']]
    return regions

def delete_log_groups(region, prefixes):
    """Delete log groups in a region matching any prefix."""
    logs_client = boto3.client('logs', region_name=region)
    paginator = logs_client.get_paginator('describe_log_groups')
    print(f"\n🌍 Region: {region}")

    for prefix in prefixes:
        print(f"🔍 Looking for log groups starting with: {prefix}")

        for page in paginator.paginate():
            log_groups = page.get('logGroups', [])

            matching_groups = [lg['logGroupName'] for lg in log_groups if lg['logGroupName'].startswith(prefix)]

            if not matching_groups:
                print(f"    ⚠️ No log groups matched in {region} with prefix '{prefix}'")
            else:
                for log_group_name in matching_groups:
                    print(f"    ❌ Deleting log group: {log_group_name}")
                    try:
                        logs_client.delete_log_group(logGroupName=log_group_name)
                    except Exception as e:
                        print(f"    ❌ Error deleting {log_group_name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Delete CloudWatch log groups by prefix across all regions.")
    parser.add_argument(
        '--prefix',
        required=True,
        help='Comma-separated list of prefixes to match log groups'
    )
    args = parser.parse_args()

    prefixes = [p.strip() for p in args.prefix.split(',') if p.strip()]

    print("Patterns to match:")
    for pattern in prefixes:
        print(f"  - {pattern}")

    regions = get_all_regions()

    for region in regions:
        delete_log_groups(region, prefixes)

    print("\n✅ Script finished.")

if __name__ == "__main__":
    main()
