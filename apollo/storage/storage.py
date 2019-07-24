from googleapiclient.errors import HttpError
import json
import io
from pprint import pprint as p

from google.cloud._helpers import _to_bytes
from io import BytesIO

from apiclient import http

from google.cloud import storage

from google.cloud.storage import Blob


_MEME_TYPES = {
        'txt': 'text/plain',                
        'csv': 'text/csv',
        'json': 'application/json',            
        'png': 'image/png',
        'jpg': 'image/jpeg',                    
    }

class CloudStorageClient:
    def __init__(self,
                credentials,
                project_id,
                bucket=None,
                num_retries=10,
                content_type='json'):
        self._credentials = credentials
        self._project_id = project_id
        self._bucket = bucket
        self._content_type = content_type
        self._num_retries = num_retries
    
    @property
    def credentials(self,):
        try:
            return self._credentials._get_credentials()
        except Exception as e:
            # print(e)
            return self._credentials            

    @property
    def content_type(self,):
        return self._content_type

    @property
    def num_retries(self,):
        return self._num_retries

    @property
    def client(self,):
        try:
            return storage.Client(
                        credentials=self.credentials,
                        project=self.project_id
            )
        except:
            return storage.Client(
                        project=self.project_id
            ).from_service_account_json(self.credentials)

    @property
    def bucket(self,):
        return self._bucket

    @property
    def project_id(self,):
        return self._project_id

    def read(self,
            file_path,
            bucket=None):
            
        bucket = self.client.get_bucket(self.bucket or bucket)
        blob = bucket.get_blob(file_path)
        return blob.download_as_string()        

    def list_blobs(self,
                   prefix,
                   bucket=None):
        
        bucket = self.client.bucket(self.bucket or bucket)
        return bucket.list_blobs(
            prefix=prefix
        )

    def write(self,
               file_path,               
               data,
               num_retries=10,
               content_type=None,               
               bucket=None):

        bucket = self.client.get_bucket(self.bucket or bucket)

        try:
            blob = Blob(file_path, bucket)
        except:
            blob = bucket.get_blob(file_path)

        try:
            data = json.loads(data)
        except:
            pass

        if isinstance(data,(dict,list)):
            data = json.dumps(data)
        else:
            data =  data

        data = _to_bytes(data, encoding="utf-8")
        string_buffer = BytesIO(data)    

        blob.upload_from_file(
            file_obj = string_buffer,
            size = len(data),
            client = self.client,
            num_retries = num_retries or self.num_retries,
            content_type = _MEME_TYPES[self.content_type or content_type]
        )
        return 

