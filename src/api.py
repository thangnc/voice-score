import json

import requests
from openai.error import AuthenticationError

domain = "http://localhost:5000"


def login(username: str, password: str):
    url = f"{domain}/api/v1/oauth/token"

    # Prepare the data to be sent
    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "client_id": "test_client_id",
        "client_secret": "test_client_secret"
    }

    # Send the POST request with form data
    response = requests.post(url, data=data)

    # Check the response status code and content
    if response.status_code == 200:
        return response.json()
    else:
        raise AuthenticationError(
            "Failed to login"
        )


def fetch_candidates(token: str):
    url = f"{domain}/api/v1/candidates"

    # Set the authorization token
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise AuthenticationError(
            "Token has expired"
        )
    else:
        raise ValueError(
            "Could not get data"
        )


def get_resume_detail(token: str, resume_id: int):
    url = f"{domain}/api/v1/resumes/{resume_id}"

    # Set the authorization token
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise AuthenticationError(
            "Token has expired"
        )
    else:
        raise ValueError(
            "Could not get data"
        )


def get_resume_detail_scores(token: str, resume_id: int):
    url = f"{domain}/api/v1/resumes/{resume_id}/scores"

    # Set the authorization token
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise AuthenticationError(
            "Token has expired"
        )
    else:
        raise ValueError(
            "Could not get data"
        )


def get_pre_signed_url(token: str):
    url = f"{domain}/api/v1/pre-signed/resumes"

    # Set the authorization token
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise AuthenticationError(
            "Token has expired"
        )
    else:
        raise ValueError(
            "Could not get data"
        )


def upload_to_s3(file, pre_signed_url: str):
    headers = {
        "Content-Type": "application/pdf"
    }

    response = requests.put(pre_signed_url, data=file, headers=headers)

    if response.status_code == 200:
        print("PDF upload successful!")
    else:
        print("PDF upload failed. Status code:", response.status_code)


def parse_resume(token: str, file_key: str):
    url = f"{domain}/api/v1/resumes"

    # Set the authorization token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Prepare the data to be sent
    data = {
        "file_key": file_key
    }

    # Convert the data to JSON
    json_data = json.dumps(data)

    # Send the POST request with JSON data
    response = requests.post(url, data=json_data, headers=headers)

    if response.status_code == 201:
        return response.json()
    elif response.status_code == 401:
        raise AuthenticationError(
            "Token has expired"
        )
    else:
        raise ValueError(
            "Could not get data"
        )


def score_resume(token: str, resume_id: int, score_type: str):
    url = f"{domain}/api/v1/scores"

    # Set the authorization token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Prepare the data to be sent
    data = {
        "resume_id": resume_id,
        "score_type": score_type
    }

    # Convert the data to JSON
    json_data = json.dumps(data)

    # Send the POST request with JSON data
    response = requests.post(url, data=json_data, headers=headers)

    if response.status_code == 201:
        return response.json()
    elif response.status_code == 401:
        raise AuthenticationError(
            "Token has expired"
        )
    else:
        raise ValueError(
            "Could not get data"
        )


def generate_questions(token: str, resume_id: int, score_type: str):
    url = f"{domain}/api/v1/interviews"

    # Set the authorization token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Prepare the data to be sent
    data = {
        "resume_id": resume_id,
        "score_type": score_type
    }

    # Convert the data to JSON
    json_data = json.dumps(data)

    # Send the POST request with JSON data
    response = requests.post(url, data=json_data, headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise AuthenticationError(
            "Token has expired"
        )
    else:
        raise ValueError(
            "Could not get data"
        )
