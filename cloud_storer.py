from google.cloud import storage


def upload_blob(bucket_name, source_file, destination_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_name)
    blob.upload_from_filename(source_file)
    print(f'file uploaded')
