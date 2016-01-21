import boto3
import os

def s3_download(boto3_client, boto3_resource, s3_prefix, local_root='/tmp', bucket_name='your_bucket', trim_path=True):
    """
    Stolen from http://stackoverflow.com/questions/31918960/boto3-to-download-all-files-from-a-s3-bucket
    :param boto3_client: The object returned by boto3.client('s3')
    :param s3_resource: The object returned by boto3.resource('s3')
    :param s3_prefix: The s3 prefix (key, i.e., s3 url without bucket name) you want to download
    :param local_root: The loocal destination for the downloaded files
    :param bucket_name: The name of the path where the key resides
    :param trim_path: Indicates whether or not to store downloaded files at their absolute s3 path or
    relative to s3_prefix
    :return:
    """
    paginator = boto3_client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket_name, Delimiter='/', Prefix=s3_prefix):
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                s3_download(boto3_client, boto3_resource, subdir.get('Prefix'), local_root)
        if result.get('Contents') is not None:
            for file in result.get('Contents'):
                if trim_path is True:
                    local_path = os.path.join(local_root,
                        file.get('Key').replace(os.path.dirname(s3_prefix)+"/", ""))
                else:
                    local_path = os.path.join(local_root, file.get('Key'))
                if not os.path.exists(os.path.dirname(local_path)):
                     os.makedirs(os.path.dirname(local_path))
                boto3_resource.meta.client.download_file(bucket_name, file.get('Key'), local_path)

