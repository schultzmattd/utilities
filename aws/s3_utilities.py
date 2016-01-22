import boto3
import os

def s3_download(boto3_client, boto3_resource, s3_prefix, local_destination='/tmp',
                bucket_name='your_bucket', trim_path=True, recursive = False):
    """
    Stolen from http://stackoverflow.com/questions/31918960/boto3-to-download-all-files-from-a-s3-bucket
    :param boto3_client: The object returned by boto3.client('s3')
    :param boto3_resource: The object returned by boto3.resource('s3')
    :param s3_prefix: The s3 prefix (key, i.e., s3 url without bucket name) you want to download
    :param local_destination: The local destination for the downloaded files. If recursive is set to True,
    local_destination is assumed to point at a directory. If recursive is set to Falase, local_destination
    is assumed to point to the path on the local machine where you want the file downloaded
    :param bucket_name: The name of the path where the s3 prefix resides
    :param trim_path: Indicates whether or not to store downloaded files at their absolute s3 path or
    relative to s3_prefix
    :return downloaded_files: list of paths to all downloaded files
    """
    downloaded_files = []
    if recursive is True:
        for key_name in s3_list(boto3_client, bucket_name, s3_prefix):
            if trim_path is True:
                local_path = os.path.join(local_destination,
                                          key_name.replace(os.path.dirname(s3_prefix)+"/", ""))
            else:
                local_path = os.path.join(local_destination, key_name)
            if not os.path.exists(os.path.dirname(local_path)):
                 os.makedirs(os.path.dirname(local_path))
            boto3_resource.meta.client.download_file(bucket_name, key_name, local_path)
            downloaded_files.append(os.path.abspath(local_path))
    else:
        if not os.path.exists(os.path.dirname(local_destination)):
             os.makedirs(os.path.dirname(local_destination))
        boto3_resource.meta.client.download_file(bucket_name, s3_prefix, local_destination)
        downloaded_files.append(os.path.abspath(local_destination))
    return downloaded_files

def s3_list(boto3_client, bucket_name, s3_prefix):
    """
    Adapted from http://stackoverflow.com/questions/31918960/boto3-to-download-all-files-from-a-s3-bucket
    :param boto3_client: The object returned by boto3.client('s3')
    :param bucket_name: The name of the path where the s3 prefix resides
    :param s3_prefix: The s3 prefix you'd like to list
    :return key_names: A list of key names from the s3 prefix
    """
    key_names = []
    paginator = boto3_client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket_name, Delimiter='/', Prefix=s3_prefix):
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                key_names.extend(s3_list(boto3_client,  bucket_name, subdir.get('Prefix')))
        if result.get('Contents') is not None:
            for key_object in result.get('Contents'):
                key_names.append(key_object.get('Key'))

    return key_names
