import os
import requests
import json
from enum import Enum
from django.conf import settings
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
CREDS_FILENAME = '/d2ga/d2ga-gcloud-creds.json'

def get_gcloud_creds():
    fullpath = os.getcwd() + CREDS_FILENAME
    if os.path.exists(fullpath):
        return service_account.Credentials.from_service_account_file(fullpath, scopes=SCOPES)
    else:
        raise Exception('No credentials json file!')


class Opendota(object):
    api_url = "https://api.opendota.com/api"

    class LOBBY_TYPE(Enum):
        ranked = 7

    def __init__(self):
        self.api_key = settings.OPENDOTA_API_KEY
        self._session = requests.Session()
    
    def get(self, *args, **kwargs):
        params = kwargs.get('params', None) or {}
        params['api_key'] = self.api_key
        query_url = self.api_url + kwargs['path']

        r = self._session.get(query_url, params=params)
        json_data = r.json()
        
        return json_data
    
    def get_player_matches(
            self, 
            player_id,
            lobby_type,
            limit=200
        ):
        path = f'/players/{player_id}/matches'

        params = {
            "limit": limit,
            "lobby_type": lobby_type.value
        }

        matches = self.get(path=path, params=params)

        return matches
    
    def get_match_details(
        self,
        match_id
    ):
        path = f'/matches/{match_id}'
        return self.get(path=path)