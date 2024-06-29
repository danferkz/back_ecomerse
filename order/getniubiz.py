import requests
from django.conf import settings

def get_niubiz_token():
    url = settings.NIUBIZ_SECURITY_URL
    auth = (settings.NIUBIZ_USERNAME, settings.NIUBIZ_PASSWORD)
    response = requests.get(url, auth=auth)
    response_data = response.json()
    if response.status_code == 200:
        return response_data.get('accessToken')
    else:
        raise Exception(f"Error obtaining token: {response_data}")
