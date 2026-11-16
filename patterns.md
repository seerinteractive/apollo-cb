# apollo-cb reviewer patterns

Snapshot: `c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7`. [Repository](https://github.com/seerinteractive/apollo-cb).

These reviewer patterns apply to the pinned snapshot. Accepted items passed independent refutation and deterministic evidence checks at the pinned snapshot. Quotes verify source presence; they do not prove every interpretation or current production behavior.

Coverage: 2 extracted business rules; 0 accepted, 0 uncertain, 2 rejected, 0 pending audit. 4 extracted dependencies; 4 accepted, 0 uncertain, 0 rejected, 0 pending audit.

Scanned branch: `master`. GitHub default branch: `master`.

## Accepted business rules

No business rule has cleared the acceptance gates for this snapshot.

## Accepted dependencies

### BambooHR (external system)

apollo-cb's BambooHR adapter exposes https://api.bamboohr.com/api/gateway.php/{subdomain}/v1 and supplies HTTP Basic authentication with the API key as username and an empty password. Its Accept header requests application/json.

**Keep in sync:** The BambooHR adapter's tenant-specific v1 URL template, API-key Basic authentication with an empty password, and Accept: application/json header.

**Why reviewers need it:** Changes to shared authentication or request construction affect this integration; tests/auth/test_api.py constructs an /employees/directory request using the adapter.

**Evidence:**

- [apollo-cb/apollo/auth/apis/bamboohr.py:33](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/apis/bamboohr.py#L33)

  ```text
  return f'https://api.bamboohr.com/api/gateway.php/{self.subdomain}/v1'
  ```
- [apollo-cb/apollo/auth/apis/bamboohr.py:47](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/apis/bamboohr.py#L47)

  ```text
  """The ``api_key`` is the username and the password is blank.
  ```
- [apollo-cb/apollo/auth/apis/bamboohr.py:50](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/apis/bamboohr.py#L50)

  ```text
  return (self.api_key, "")
  ```
- [apollo-cb/apollo/auth/apis/bamboohr.py:41](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/apis/bamboohr.py#L41)

  ```text
  "Accept": "application/json",
  ```
- [apollo-cb/apollo/auth/base.py:39](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/base.py#L39)

  ```text
  val.header.update(self.header)
  ```
- [apollo-cb/apollo/auth/base.py:41](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/base.py#L41)

  ```text
  val.auth = self.auth
  ```
- [apollo-cb/apollo/builder/client.py:273](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/builder/client.py#L273)

  ```text
  auth_req = self.api_auth >> req
  ```
- [apollo-cb/apollo/request/api_request.py:193](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/request/api_request.py#L193)

  ```text
  request_args.update({"auth": BasicAuth(*self.auth)})
  ```
- [apollo-cb/tests/auth/test_api.py:34](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/tests/auth/test_api.py#L34)

  ```text
  path_format = f'{api_auth.base}/employees/directory'
  ```

### Harvest (external system)

apollo-cb's Harvest adapter exposes https://api.harvestapp.com/v2 and supplies Authorization: Bearer <access_token>, Harvest-Account-Id, and User-Agent request headers.

**Keep in sync:** The Harvest adapter's v2 endpoint and Authorization: Bearer, Harvest-Account-Id, and User-Agent header contract.

**Why reviewers need it:** Changes to shared header injection or the Harvest adapter affect authenticated requests; tests/auth/test_api.py constructs a /users request using it.

**Evidence:**

- [apollo-cb/apollo/auth/apis/harvest.py:36](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/apis/harvest.py#L36)

  ```text
  return "https://api.harvestapp.com/v2"
  ```
- [apollo-cb/apollo/auth/apis/harvest.py:44](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/apis/harvest.py#L44)

  ```text
  "Authorization": f"Bearer {self.access_token}",
  ```
- [apollo-cb/apollo/auth/apis/harvest.py:45](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/apis/harvest.py#L45)

  ```text
  "Harvest-Account-Id": self.account_id,
  ```
- [apollo-cb/apollo/auth/apis/harvest.py:46](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/apis/harvest.py#L46)

  ```text
  "User-Agent": self.user_agent,
  ```
- [apollo-cb/apollo/auth/base.py:39](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/base.py#L39)

  ```text
  val.header.update(self.header)
  ```
- [apollo-cb/apollo/builder/client.py:273](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/builder/client.py#L273)

  ```text
  auth_req = self.api_auth >> req
  ```
- [apollo-cb/apollo/request/api_request.py:189](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/request/api_request.py#L189)

  ```text
  "headers": self.header,
  ```
- [apollo-cb/tests/auth/test_api.py:91](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/tests/auth/test_api.py#L91)

  ```text
  path_format = f'{api_auth.base}/users'
  ```

### Pipedrive (external system)

apollo-cb's Pipedrive adapter exposes https://api.pipedrive.com/v1, supplies the API key as the api_token query parameter, and requests JSON responses with Accept: application/json, */*.

**Keep in sync:** The Pipedrive adapter's v1 endpoint, api_token query-parameter authentication, and Accept: application/json, */* response-selection header.

**Why reviewers need it:** Changes to parameter merging or the Pipedrive adapter affect authenticated requests; tests/auth/test_api.py constructs a /pipelines request using it.

**Evidence:**

- [apollo-cb/apollo/auth/apis/pipedrive.py:36](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/apis/pipedrive.py#L36)

  ```text
  return "https://api.pipedrive.com/v1"
  ```
- [apollo-cb/apollo/auth/apis/pipedrive.py:55](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/apis/pipedrive.py#L55)

  ```text
  "api_token": self.api_key
  ```
- [apollo-cb/apollo/auth/apis/pipedrive.py:40](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/apis/pipedrive.py#L40)

  ```text
  """The header tells Pipedrive to provide a JSON response.
  ```
- [apollo-cb/apollo/auth/apis/pipedrive.py:44](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/apis/pipedrive.py#L44)

  ```text
  "Accept": "application/json, */*",
  ```
- [apollo-cb/apollo/auth/base.py:38](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/auth/base.py#L38)

  ```text
  val.param.update(self.param)
  ```
- [apollo-cb/apollo/builder/client.py:273](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/builder/client.py#L273)

  ```text
  auth_req = self.api_auth >> req
  ```
- [apollo-cb/apollo/request/api_request.py:186](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/request/api_request.py#L186)

  ```text
  "params": self.param,
  ```
- [apollo-cb/tests/auth/test_api.py:61](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/tests/auth/test_api.py#L61)

  ```text
  path_format = f'{api_auth.base}/pipelines'
  ```

### Google Cloud Storage (external system)

apollo-cb's CloudStorageClient provides read, list, and upload methods for objects in a caller-configured Google Cloud Storage project and bucket. APIRequest.save supplies response.text and its generated file path to storage.write when storage criteria, storage, and file path permit saving.

**Keep in sync:** none, informational dependency

**Why reviewers need it:** Changes to response serialization, file-path generation, credentials, or bucket selection affect what this adapter writes to Google Cloud Storage.

**Evidence:**

- [apollo-cb/docs/storage_index.rst:25](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/docs/storage_index.rst#L25)

  ```text
  Google Cloud Storage is provided.
  ```
- [apollo-cb/apollo/storage/google_cloud.py:12](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/storage/google_cloud.py#L12)

  ```text
  from google.cloud import storage
  ```
- [apollo-cb/apollo/storage/google_cloud.py:77](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/storage/google_cloud.py#L77)

  ```text
  credentials=self.credentials,
  ```
- [apollo-cb/apollo/storage/google_cloud.py:78](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/storage/google_cloud.py#L78)

  ```text
  project=self.project_id
  ```
  The same fragment also occurs at [L81](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/storage/google_cloud.py#L81).
- [apollo-cb/apollo/storage/google_cloud.py:98](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/storage/google_cloud.py#L98)

  ```text
  bucket = self.client.get_bucket(self.bucket or bucket)
  ```
  The same fragment also occurs at [L141](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/storage/google_cloud.py#L141).
- [apollo-cb/apollo/storage/google_cloud.py:99](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/storage/google_cloud.py#L99)

  ```text
  blob = bucket.get_blob(file_path)
  ```
  The same fragment also occurs at [L146](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/storage/google_cloud.py#L146).
- [apollo-cb/apollo/storage/google_cloud.py:100](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/storage/google_cloud.py#L100)

  ```text
  return blob.download_as_string()
  ```
- [apollo-cb/apollo/storage/google_cloud.py:116](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/storage/google_cloud.py#L116)

  ```text
  bucket = self.client.bucket(self.bucket or bucket)
  ```
- [apollo-cb/apollo/storage/google_cloud.py:117](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/storage/google_cloud.py#L117)

  ```text
  return bucket.list_blobs(prefix=prefix)
  ```
- [apollo-cb/apollo/storage/google_cloud.py:144](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/storage/google_cloud.py#L144)

  ```text
  blob = Blob(file_path, bucket)
  ```
- [apollo-cb/apollo/storage/google_cloud.py:154](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/storage/google_cloud.py#L154)

  ```text
  data = json.dumps(data)
  ```
- [apollo-cb/apollo/storage/google_cloud.py:161](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/storage/google_cloud.py#L161)

  ```text
  blob.upload_from_file(
  ```
- [apollo-cb/apollo/request/api_request.py:151](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/request/api_request.py#L151)

  ```text
  return self.file_pattern.path
  ```
- [apollo-cb/apollo/request/api_request.py:258](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/request/api_request.py#L258)

  ```text
  if self.storage_criteria(self) and self.storage and self.file_path:
  ```
- [apollo-cb/apollo/request/api_request.py:259](https://github.com/seerinteractive/apollo-cb/blob/c78b2bb154a37a09d079dd8ecddd79d55dc7bdd7/apollo/request/api_request.py#L259)

  ```text
  self.storage.write(file_path=self.file_path, data=self.response.text)
  ```

## Provenance and limits

Raw extraction: `out/apollo-cb.json`. Independent audit: `audit/apollo-cb.json` in the knowledge report bundle. The original whitespace-normalized `.verified.json` files are not acceptance inputs. This report does not assert a complete semantic audit of every tracked file, deployment verification, or owner approval. Excluded candidate text and audit rationale are kept in the separate review report.
