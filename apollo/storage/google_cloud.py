#standard
import json
import io
from pprint import pprint as p
from io import BytesIO

#third party
import attr
from attr.validators import instance_of
from attr.validators import in_

from google.cloud import storage
from google.cloud.storage import Blob
from google.cloud._helpers import _to_bytes

from googleapiclient.errors import HttpError

from apiclient import http


#local
from apollo.storage.base import StorageBase

_MEME_TYPES = {
    "txt": "text/plain",
    "csv": "text/csv",
    "json": "application/json",
    "png": "image/png",
    "jpg": "image/jpeg",
}

@attr.s
class CloudStorageClient(StorageBase):
    """A wrapper around Google's `Cloud Storage Client <https://googleapis.github.io/google-cloud-python/latest/storage/index.html>`_

    :type credentials: oauth2client.client.OAuth2Credentials or str
    :param credentials: Authentication from Google Cloud or path to services account

    :type project_id: str
    :param project_id: The name of the Google Cloud project

    :type bucket: str
    :param bucket: The name of the Google Cloud Storage bucket

    :type num_retries: int
    :param num_retries: (Optional) The number of attempts to save to Cloud Storage

    :type content_type: str
    :param content_type: The type of content being uploaded. Default is 'json'. Options are txt, csv, json, png, jpg
    """

    project_id = attr.ib(validator = instance_of(str))
    credentials = attr.ib()
    bucket = attr.ib(default = None, validator = instance_of(str))
    content_type = attr.ib(default = 'json', validator = in_(_MEME_TYPES))
    num_retries = attr.ib(default = 10, validator = instance_of(str))

    @credentials.default
    def _(self,):
        """Google Cloud Credentials

        :returns: oauth2client.client.OAuth2Credentials or str
        """
        try:
            return self.credentials._get_credentials()
        except Exception:
            return self.credentials

    @property
    def client(self,):
        """Google Storage Client used to make API calls

        :returns: `google.cloud.storage.client.Client <https://googleapis.github.io/google-cloud-python/latest/storage/client.html>`_
        """
        try:
            return storage.Client(
                credentials=self.credentials, 
                project=self.project_id
            )
        except:
            return storage.Client(project=self.project_id).from_service_account_json(
                self.credentials
            )


    def read(self, file_path, bucket=None):
        """Reads a file from Google Cloud Storage

        :type file_path: str
        :param file_path: The path to the file where the data will be written.

        :type bucket: str or None
        :param bucket: The name of the bucket. (Optional) if given in class instantiation.

        :returns: the downloaded string
        """

        bucket = self.client.get_bucket(self.bucket or bucket)
        blob = bucket.get_blob(file_path)
        return blob.download_as_string()

    def list_blobs(self, prefix="/", bucket=None):
        """List `Google Cloud Storage Blobs <https://googleapis.github.io/google-cloud-python/latest/storage/blobs.html>`_


        :type prefix: str
        :param prefix: (Optional) prefix used to filter blobs. Default is '/'.

        :type bucket: str or None
        :param bucket: The name of the bucket. (Optional) if given in class instantiation.

        :returns: Iterator of all Blob in this bucket matching the arguments.

        """

        bucket = self.client.bucket(self.bucket or bucket)
        return bucket.list_blobs(prefix=prefix)

    def write(self, file_path, data, num_retries=10, content_type=None, bucket=None):

        """Writes data to Google Cloud Storage

        :type data: bytes
        :param data: The data that will be written to Google Cloud Storage

        :type file_path: str
        :param file_path: The path to the file where the data will be written

        :type num_retries: int
        :param num_retries: (Optional) The number of attempts to save to Cloud Storage

        :type content_type: str
        :param content_type: The type of content being uploaded. Default is 'json'. Options are txt, csv, json, png, jpg

        :type bucket: str
        :param bucket: The name of the bucket. (Optional) if given in class instantiation.

        :returns: None
        """

        bucket = self.client.get_bucket(self.bucket or bucket)

        try:
            blob = Blob(file_path, bucket)
        except:
            blob = bucket.get_blob(file_path)

        try:
            data = json.loads(data)
        except:
            pass

        if isinstance(data, (dict, list)):
            data = json.dumps(data)
        else:
            data = data

        data = _to_bytes(data, encoding="utf-8")
        string_buffer = BytesIO(data)

        blob.upload_from_file(
            file_obj=string_buffer,
            size=len(data),
            client=self.client,
            num_retries=num_retries or self.num_retries,
            content_type=_MEME_TYPES[self.content_type or content_type],
        )
        return
