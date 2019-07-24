
from multiprocessing.pool import ThreadPool

import itertools

from time import sleep

import requests

from pprint import pprint as p

from apollo.utils import FilePath
from apollo import APIRequest

from apollo.auth.auth import _ENDPOINTS

class ClientBuilder:
    """Wrapper for making rate-limited API requests

    Args:
        api (str): 
            name of API, e.g. 'Harvest,' 'BambooHR,' 'Pipedrive'

        folders (list): 
            nested list of folders that'll generate the API url path,
            e.g. [1,[2,3]] >> ['1/2', '1/3']

        params (dict): 
            nested list of parameters that'll generate the API url,
            e.g. {1:[2,3]} >> [{1:2}, {1:3}]

        headers (dict): 
            headers to be added to each API request, in addition to any
            headers from Auth

        mod_response (func): 
            can intercept a requests.Request object from an APIRequest to alter before
            storage. Must return a requests.Request object

        storage_criteria (func): 
            can intercept an APIRequest to modify before storage. 
            Must return a APIRequest
        
        data (dict):
            Data to be passed into the requests.Request method.
        
        method (str):
            requests.Request HTTP method. Options are 'GET' 'PUT'
            'DELETE' 'POST'. Visit requests.Request for more docs.
    
        storage (StorageClient):
            Class that must inherit from StorageClient with read() and
            write() methods.
        
        file_pattern (FilePath):
            Accesses APIRequest instance to create a file pattern
        
        threads (int):
            Number of concurrent requests
        
        sleep_interval (int):
            Pauses (in seconds) between thread executions
        
        stop_criteria (func):



    """

    def __init__(
        self,
        api,
        auth=None, 
        folders=[],
        params={}, 
        headers={},
        zip_folder_params=None,
        zip_folder_data=None,
        mod_response=lambda x: x,
        storage_criteria=lambda x: x,
        data=None, 
        method='GET',
        storage=None,
        file_pattern=FilePath(),
        threads=10, 
        sleep_interval=10,
        save=True,
        stop_criteria=lambda x: x
    ):

        self.auth = auth
        self.api = api
        self.base_url = _ENDPOINTS.get(api,'')
        self.folders = folders
        self.method = method
        self.mod_response = mod_response
        self.params = params
        self.headers = headers
        self.data = data
        self.threads = threads
        self.storage = storage
        self.file_pattern = file_pattern
        self.sleep_interval = sleep_interval
        self.storage_criteria = storage_criteria
        self.stop_criteria = stop_criteria
        self.zip_folder_params = zip_folder_params
        self.zip_folder_data = zip_folder_data
        self.save = save

    @staticmethod
    def create_params(**params):
        """
        params = {
        'p1': 'a',
        ('p2','p3'): zip([[1,2,3],[4,5,6]]),
        }
        >>> {'p2': 1, 'p1': 'a'}
            {'p2': 2, 'p1': 'a'}
            {'p2': 3, 'p1': 'a'}
            {'p3': 4, 'p1': 'a'}
            {'p3': 5, 'p1': 'a'}
            {'p3': 6, 'p1': 'a'}
        """

        cnt = 0

        for k,v in params.items():
            
            if isinstance(v,zip) and isinstance(k,tuple):            
                z = list(zip(k,v))
                
                for m in z:
                    w,v = m
                    v,*_ = v
                    
                    for f in v:
                        param = {}
                        p = params.copy()
                        del p[k]
                        param.update({w:f}) 
                        param.update(p)
                        cnt += 1
                        yield param

            elif isinstance(v,list):
                for f in v:
                    param = {}
                    p = params.copy()
                    del p[k]
                    param.update({k:f}) 
                    param.update(p)
                    cnt += 1
                    yield param
        if cnt == 0:
            yield params
    
    @staticmethod
    def create_urls(*folders):
        cnt = 0
        to_str = lambda x: [str(i) for i in x]
        for n,val in enumerate(folders):
            if isinstance(val,(list,range)):
                for f in val:
                    row = []
                    row.extend(folders[:n])
                    row.extend([f])
                    row.extend(folders[n+1:])
                    cnt += 1
                    yield '/'.join(to_str(row))
        if cnt == 0:
            yield '/'.join(to_str(folders)) 

    @staticmethod
    def _build_request(base_url,method='GET',
            folders=[],params={},
            zip_folder_params=None,
            zip_folder_data=None,
            headers={},auth=(),
            mod_response=lambda x: x,
            data=None,storage=None,
            file_pattern=FilePath()):
        """
        Accepts a list of dicts or a dict with lists
        """    
        if zip_folder_data:
            for url, data in zip_folder_data:
                yield APIRequest(
                        method=method,
                        url=f'{base_url}/{url}',
                        params=params,
                        headers=headers,
                        auth=auth,
                        data=data,
                        storage=storage,
                        file_pattern=file_pattern,
                        mod_response=mod_response
                )

        elif zip_folder_params:
            for url, param in zip_folder_params:
                yield APIRequest(
                        method=method,
                        url=f'{base_url}/{url}',
                        params=param,
                        headers=headers,
                        auth=auth,
                        data=data,
                        storage=storage,
                        file_pattern=file_pattern,
                        mod_response=mod_response
                )

        else:
            for url in ClientBuilder.create_urls(*folders):
                if isinstance(params,dict):            
                    for param in ClientBuilder.create_params(**params):
                        yield APIRequest(
                                method=method,
                                url=f'{base_url}/{url}',
                                params=param,
                                headers=headers,
                                auth=auth,
                                data=data,
                                storage=storage,
                                file_pattern=file_pattern,
                                mod_response=mod_response
                        )
                elif isinstance(params,list):
                    for param in params:
                        yield APIRequest(
                                method=method,
                                url=f'{base_url}/{url}',
                                params=param,
                                headers=headers,
                                auth=auth,
                                data=data,
                                storage=storage,
                                file_pattern=file_pattern,
                                mod_response=mod_response
                        )
                else:
                    raise "Params must be a list or dict"


    @staticmethod
    def _make_requests(api_requests,threads,sleep_interval,storage,storage_criteria,stop_criteria):

        p = ThreadPool(threads)
        pool_output = p.map(lambda x: x.request(),api_requests)

        pool_output = stop_criteria(pool_output)

        if not pool_output:                

            return

        if storage:
            clean_pool = storage_criteria(pool_output)
            if clean_pool:
                pool_output = p.map(lambda x: x.save(),clean_pool)

        sleep(sleep_interval)
        
        yield pool_output

    def execute(self):
        '''

        '''
        
        self.headers.update(self.auth.headers)
        self.params.update(self.auth.params)

        api_requests = ClientBuilder._build_request(
                base_url=self.base_url,
                folders=self.folders,
                method=self.method,
                data=self.data,
                params=self.params,
                headers=self.headers,
                auth=self.auth.auth,
                storage=self.storage,
                file_pattern=self.file_pattern,
                mod_response=self.mod_response,
                zip_folder_params=self.zip_folder_params,
                zip_folder_data = self.zip_folder_data
            )

        def chunks(iterable, size=2):
            iterator = iter(iterable)
            for first in iterator:
                yield itertools.chain([first], itertools.islice(iterator, size - 1))

        chunked_requests = chunks(api_requests)

        save = []

        for api_request_chunk in chunked_requests:
            r = ClientBuilder._make_requests(
                api_requests=list(api_request_chunk),
                threads=self.threads,
                sleep_interval=self.sleep_interval,
                storage=self.storage,
                storage_criteria= self.storage_criteria,
                stop_criteria = self.stop_criteria
            )
            vals = list(r)
            if self.save:
                save.extend(vals)
            if not vals:
                break

        return save
