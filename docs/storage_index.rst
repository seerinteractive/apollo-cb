.. _storage_usage:

Storage
=======

Users can use ``apollo.storage.basse.StorageBase`` to create
custom storage classes. Any custom storage class
must inherit from the base and implement the write
method. 

Example:

.. code-block:: python

    from apollo.storage.base import StorageBase

    class MyStorage(StorageBase):
        
        def write(self, file_path, data):
            #save data somewhere
            pass

    storage = MyStorage()

Google Cloud Storage is provided. 

.. toctree::
  :maxdepth: 1

  Google Cloud <storage/google_cloud>
  StorageBase <storage/base>
  
Indices and tables

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`