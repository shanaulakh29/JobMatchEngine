# import boto3
# from botocore.exceptions import ClientError
# import logging
# import os
# from dotenv import load_dotenv
# from fastapi import UploadFile
# from io import BytesIO

# load_dotenv()

# BUCKET_NAME=os.environ["AWS_BUCKET_NAME"]


# async def upload_s3(file: UploadFile, file_name: str)->bool:
#     """Upload a file to the S3 bucket
    
#         :param file: File to upload
#         :param filename: The name of the file
#     """
#     contents = await file.read()
#     file_obj = BytesIO(contents)
#     s3_client = boto3.client('s3', region_name='ap-south-1')
#     try:
#         # upload the file 
#         s3_client.upload_fileobj(file_obj, BUCKET_NAME, f"resumes/{file_name}")
#         logging.info("Uploaded to S3")
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True


# async def create_presigned_url(file_name: str, expiration=86400):
#     """Generates a presigned URL to share an S3 Object

#     :param file_name: string
#     :param expiration: Time in seconds for the presigned URL to remain valid
#     :return: Presigned URL as a string. If error, returns None
    
#     """
#     key = f"resumes/{file_name}"
#     # Generate the URL
#     s3_client = boto3.client('s3', region_name='ap-south-1')
#     try:
#         response = s3_client.generate_presigned_url(
#             'get_object',
#             Params={'Bucket': BUCKET_NAME, 'Key': key},
#             ExpiresIn=expiration,
                  
#         )
    
#     except ClientError as e:
#         logging.error(e)
#         return None 
#     # response contains presigned URL as a string
#     return response