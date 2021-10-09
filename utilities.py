import os
import re

import boto3
from werkzeug.utils import secure_filename
from config.config import AWS_BUCKET_NAME, AWS_URL_EXPIRE_SECONDS, AWS_UPLOAD_FOLDER, AWS_ACCESS_KEY_ID, \
    AWS_SECRET_ACCESS_KEY, AWS_REGION

STUDENT_ACCOUNT = '1'
CLIENT_ACCOUNT = '2'
SUPERUSER_ACCOUNT = '3'

account_type = {
    'student': '1',
    'client': '2',
    'superuser': '3',
}

STATUS_CODE = {
    'ok': 200,
    'created': 201,
    'bad_request': 400,
    'unauthorized': 401,
    'not_found': 404,
}


def validate_email(email):
    return re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$', email)


def concat_list_to_string(list):
    return ', '.join(list)


def validate_user_info(data):
    expected_params = ['first_name', 'last_name', 'email', 'password', 'type', 'q_type1', 'q_type2', 'ans1', 'ans2']
    if data is None:
        return 'The following parameters are required: ' + concat_list_to_string(expected_params)

    for param in expected_params:
        if param not in data:
            return 'The following parameters are required: ' + concat_list_to_string(expected_params)

    if data['type'] == account_type['student'] and re.match(r'^.+@upr\.edu$', data['email']) is None:
        return 'A upr email is needed to register as student'

    if validate_email(data['email']) is None:
        return 'Email provided is not valid'

    return None


def validate_login_data(data):
    expected_params = ['email', 'password']
    if data is None:
        return 'The following parameters are required: ' + concat_list_to_string(expected_params)

    for param in expected_params:
        if param not in data:
            return 'The following parameters are required: ' + concat_list_to_string(expected_params)

    if validate_email(data['email']) is None:
        return 'Email provided is not valid'

    return None


def validate_profile_data(data):
    expected_params = ['first_name', 'last_name', 'user_id', 'password', 'image', 'about', 'street', 'city', 'zipcode']

    if data.__len__() == 0:
        return "The following parameters are required: {expected}.".format(
            expected=', '.join(expected_params),
        )

    for param in expected_params:
        if param not in data:
            return "The following parameters are required: {expected}.".format(
                expected=', '.join(expected_params)
            )

    return None


def generate_profile_pic_url(image_path):
    try:
        s3_client = boto3.client('s3',
                                 aws_access_key_id=AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                 region_name=AWS_REGION,
                                 )
        key = os.path.join(AWS_UPLOAD_FOLDER, image_path)
        presigned_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': AWS_BUCKET_NAME, 'Key': key},
                                                         ExpiresIn=AWS_URL_EXPIRE_SECONDS)
        return presigned_url
    except Exception as e:
        return None


def upload_image_aws(user_id, image_file):
    try:
        file_name = 'profile_pic_{user_id}.{type}'.format(user_id=user_id, type=image_file.content_type.split('/')[-1])
        image_file.save(os.path.join(AWS_UPLOAD_FOLDER, secure_filename(file_name)))
        s3_client = boto3.client('s3',
                                 aws_access_key_id=AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                 region_name=AWS_REGION,
                                 )
        bucket_file_name = f"{AWS_UPLOAD_FOLDER}/{file_name}"
        s3_client.upload_file(bucket_file_name, AWS_BUCKET_NAME, bucket_file_name)
        return file_name
    except Exception as e:
        return None
