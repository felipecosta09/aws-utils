
# aws-utils

A collection of handy Python scripts to simplify day-to-day AWS operations.

## Overview

This repository contains lightweight utilities for automating AWS maintenance tasks, especially useful for DevOps and Cloud Engineers.  
Currently, it includes scripts for:

- Deleting **CloudWatch Log Groups** by name list (Python)
- Emptying and deleting **S3 Buckets** by one or multiple prefixes (Python)

More utilities will be added over time to assist with AWS resource management.

---

## Structure

```bash
aws-utils/
├── delete_logs/
│   ├── delete_logs.py
│   └── requirements.txt
├── delete_buckets/
│   ├── delete_buckets.py
│   └── requirements.txt
```

- **delete_logs/**:  
  Python script to delete CloudWatch Log Groups provided in a comma-separated list.

- **delete_buckets/**:  
  Python script to empty and delete S3 buckets that start with one or more given prefixes.

Each folder includes a `requirements.txt` to manage dependencies.

---

## Prerequisites

- Python 3.x installed
- AWS credentials configured (via environment variables, AWS CLI, or IAM roles)
- Install Python dependencies:

```bash
# For deleting logs
cd delete_logs
pip install -r requirements.txt

# For deleting buckets
cd delete_buckets
pip install -r requirements.txt
```

---

## Usage

### Delete CloudWatch Log Groups

```bash
cd delete_logs
python delete_logs.py --logs "/aws/lambda/test,/aws/lambda/test2"
```

- **--logs**: (Required) Comma-separated list of full log group names you want to delete.

Example: Deletes `/aws/lambda/test` and `/aws/lambda/test2`.

---

### Empty and Delete S3 Buckets

```bash
cd delete_buckets
python delete_buckets.py --prefix "aws-,test-"
```

- **--prefix**: (Required) Comma-separated list of prefixes.  
- Buckets that **start with** any of the given prefixes will be emptied and deleted.

Examples:

- `python delete_buckets.py --prefix "aws-"` → Deletes all buckets starting with `aws-`
- `python delete_buckets.py --prefix "aws-,test-"` → Deletes all buckets starting with `aws-` **or** `test-`

---

## Example Quick Start

```bash
# Install requirements
cd delete_logs
pip install -r requirements.txt
python delete_logs.py --logs "/aws/lambda/myapp,/aws/lambda/oldapp"

cd delete_buckets
pip install -r requirements.txt
python delete_buckets.py --prefix "tmp-,backup-"
```

---

## Disclaimer

⚠️ **Important:**  
These scripts **permanently delete** AWS resources and their data.  
Please double-check your inputs and always test carefully in non-production environments first.

---

## Contributing

If you encounter a bug, think of a useful feature, or find something confusing in the docs, please [create a new issue](https://github.com/felipecosta09/aws-utils/issues/new)!

We ❤️ pull requests. If you'd like to fix a bug, contribute to a feature, or just correct a typo, please feel free to do so.

If you're thinking of adding a new feature, consider opening an issue first to discuss it to ensure it aligns with the direction of the project (and potentially save yourself some time!).
