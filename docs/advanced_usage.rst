.. _advanced_usage:

Advanced Usage
==============

Let's build on the :ref:`basic_auth`, :ref:`basic_rate_limiting` 
and :ref:`basic_attributes` values from :ref:`basic_usage`.

* :ref:`advanced_storage`
* :ref:`advanced_mod_resp`
* :ref:`advanced_stop_criteria`
* :ref:`advanced_file_path`


.. _advanced_storage:

Storage
~~~~~~~

While :ref:`Google Cloud Storage <storage_usage>` is supported, you can create your custom
storage connector by inheriting from :class:`~apollo.storage.base.StorageBase`. Note you must have a write 
method that accepts a file_path and data. The ApolloCB implements the
write method::

    from apollo.storage.base import StorageBase
    from apollo.utils import RateLimit

    class MyStorage(StorageBase):
        """My custom storage"""    
        def write(self, file_path, data):
            #save data somewhere
            pass

    storage = MyStorage()

    storage_rate_limit = RateLimit(
        rate = 1, 
        limit = 1
    )

.. _advanced_mod_resp:

Modify Response
~~~~~~~~~~~~~~~

There are instances where you might need to provide meta data on an API request
before the request is stored. :class:`~apollo.ApolloCB` injects a function that can modify the 
:class:`~apollo.request.Response` object. Here is an example of deleting the API key 
(created from the :ref:`AuthBase example <basic_auth>`  from :ref:`basic_usage`)
from the httpbin json body representation::

    def mod_response(response):
        """remove the api key from the json response"""
        del resp.json['args']['my_api_key']
        return resp

.. _advanced_stop_criteria:

Stop Criteria
~~~~~~~~~~~~~

Some APIs do not provide an end to pagination -- forcing the user to continually
crawl pages until a given response, then stop. The ``stop_criteria`` argument enables users
to raise an internal error within :class:`~apollo.ApolloCB` to stop it from crawling. 
Users can manipulate the :class:`~apollo.request.Response` object to determine 
a stopping point. Asycnio will stop at the first exception::

    
    def stop_criteria(response):
        """Stop crawling after 10 responses"""
        if int(response.json['args']['b']) >= 10:
            return True

.. _advanced_file_path:

File Path
~~~~~~~~~
:class:`~apollo.utils.FilePattern` enables users to use the :func:`apollo.request.APIRequest.response` 
(instance of :class:`~apollo.request.Response`)
object and custom parameters to create
a file path::
    
    from apollo.utils import FilePattern

    def file_func(self, custom_param):
        """Uses the request method and value of the 'b' parameter to 
        contruct a file path."""
    
        json = self.response.json
        
        request_method = json['method']
        b_param = json['args']['b']

        return f"{request_method}/{b_param}/{custom_param}"

    file_pattern = FilePattern(
        file_func = file_func,
        custom_param = 'there'
    )        

*yields*::

    Filepath GET/0/there was saved
    Filepath GET/1/there was saved
    ...
    
Notice the parameter ``custom_param`` 'there' is a ``kwarg`` in ``file_func`` and referenced
as a ``kwarg`` as ``custom_param`` in ``FilePattern``. You can use any name instead of ``file_func``
and any ``kwarg``, not just ``custom_param``.


Executing Requests
~~~~~~~~~~~~~~~~~~

Once the above are complete, it's time
to make the request using :class:`~apollo.ApolloCB`.

ApolloCB uses the above values to make requests::

    from apollo import ApolloCB

    rf = ApolloCB(
        method = "GET", 
        url = url,
        param = param,
        api_auth = api_auth,        
        verbose = True,
        save = True,
        file_pattern = file_pattern,
        api_rate_limit = api_rate_limit,   
        stop_criteria = stop_criteria,
        storage = storage,
        mod_response = mod_response,
        storage_rate_limit = storage_rate_limit,
    )

    a = rf.execute()

*yields*::

    [08:23:10] Url http://httpbin.org/anything/folder0/subfolder0?b=0&param_a=a&my_api_key=123, Status 200
    [08:23:10] Url http://httpbin.org/anything/folder3/subfolder3?b=3&param_a=a&my_api_key=123, Status 200
    [08:23:10] Url http://httpbin.org/anything/folder2/subfolder2?b=2&param_a=a&my_api_key=123, Status 200
    [08:23:10] Url http://httpbin.org/anything/folder1/subfolder1?b=1&param_a=a&my_api_key=123, Status 200
    [08:23:10] Url http://httpbin.org/anything/folder4/subfolder4?b=4&param_a=a&my_api_key=123, Status 200
    [08:23:10] Filepath GET/0/there was saved
    [08:23:11] Filepath GET/3/there was saved
    [08:23:12] Filepath GET/2/there was saved
    [08:23:13] Filepath GET/1/there was saved
    [08:23:14] Filepath GET/4/there was saved
    [08:23:15] Filepath GET/9/there was saved
    [08:23:15] Url http://httpbin.org/anything/folder9/subfolder9?b=9&param_a=a&my_api_key=123, Status 200
    [08:23:15] Url http://httpbin.org/anything/folder5/subfolder5?b=5&param_a=a&my_api_key=123, Status 200
    [08:23:15] Url http://httpbin.org/anything/folder6/subfolder6?b=6&param_a=a&my_api_key=123, Status 200
    [08:23:15] Url http://httpbin.org/anything/folder8/subfolder8?b=8&param_a=a&my_api_key=123, Status 200
    [08:23:15] Url http://httpbin.org/anything/folder7/subfolder7?b=7&param_a=a&my_api_key=123, Status 200
    [08:23:16] Filepath GET/5/there was saved
    [08:23:17] Filepath GET/6/there was saved
    [08:23:18] Filepath GET/8/there was saved
    [08:23:19] Filepath GET/7/there was saved

Notice a few things about this response:

* **Rate limit**: There are five seconds between http requests and one second between storage executions. The API and storage rate limits are operating at different times.
* **URL structure**: The folder and subfolders are enumerated based on ``range(20)``.
* **Parameters**: ``static={'param_a': 'a'}`` appears as ``a`` in ``param_a`` in *all* urls while ``dynamic = {'b': [n for n in range(URL_LIMIT)]}`` is enumerated as ``b={n}``.
* **Storage**: The file path follows the pattern [METHOD]/[B PARAM VALUE]/[CUSTOM PARAM].
* **Stop Criteria**: While we provided 20 requests in ``URL_LIMIT``, the ``stop_criteria`` stopped future requests after it met a specified criteria.
* **Asynchronous**: The enumerated values are not in order.

Two parameters not covered above, but important:

* **verbose**: Writes the response to the terminal.
* **save**: Keeps the responses in memory for later use.

Further Reading 
~~~~~~~~~~~~~~~

.. toctree::
  :maxdepth: 2
  
  Authentication <auth_index>
  Storage <storage_index>
  Request <request_index>
  Utils <utils/helpers>
  
Indices and tables

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`