.. apollo-cb documentation master file, created by
   sphinx-quickstart on Wed Sep  4 10:51:23 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ApolloCB Library for Python
===========================

.. toctree::
    :maxdepth: 3
    :hidden:

    ApolloCB <builder/client>
    Basic Usage <basic_usage>
    Advanced Usage <advanced_usage>
    
    
Getting Started
---------------

:class:`~apollo.ApolloCB` takes a set of inputs, including (but not limited to), API authentication, 
rate limiting and storage to make API requests asynchronously and store results.

Mac/Linux
~~~~~~~~~

.. code-block:: 

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install apollo-cb

Windows
~~~~~~~

.. code-block:: 

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install apollo-cb

Usage
-----

* :ref:`basic_usage` - This section will cover making the minimum requests with :ref:`basic_attributes`, :ref:`basic_rate_limiting` and :ref:`auth_usage` using :class:`~apollo.ApolloCB`.
* :ref:`advanced_usage` - This section builds on :ref:`basic_usage`, to include the :ref:`advanced_storage`, :ref:`advanced_mod_resp`, :ref:`advanced_stop_criteria` and :ref:`advanced_file_path`.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`