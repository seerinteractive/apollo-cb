from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

from collections import namedtuple

from google.cloud import bigquery

from pprint import pprint as p

class BigQueryClient:
    def __init__(self,
                credentials,                
                project_id):
        self._credentials = credentials
        self._project_id = project_id
    
    @property
    def credentials(self,):
        try:
            credentials = self._credentials._get_credentials()
        except Exception as e:
            print(e)
            credentials = self._credentials
        return credentials

    @property
    def service(self,):
        return build('bigquery', 'v2', credentials=self.credentials)
        # return bigquery.Client(credentials=self.credentials)

    @property
    def project_id(self,):

        return self._project_id

    def insert_all(self,
                   dataset_id,
                   table_id,
                   rows):

        body = {
            'rows': rows
            }

        service_exec = self.service.tabledata().insertAll(
            body=body,
            projectId=self.project_id,
            tableId=table_id,
            datasetId=dataset_id
        )
        return service_exec.execute()

    def copy_table(
                  self,
                  source_table,
                  write_disposition,
                  destination_table,
                  table_description,
                  dataset_description,
                  time_partitioning,
                  cluster_fields,
                  access,
                  recurse=0):
                  
        source_project_id,source_dataset_table = source_table.split(':')
        source_dataset_id,source_table_id = source_dataset_table.split('.')

        destination_project_id,destination_dataset_table = destination_table.split(':')
        destination_dataset_id,destination_table_id = destination_dataset_table.split('.')

        body = {
            'configuration': {
                'copy': {
                    'sourceTable': {
                        'projectId':source_project_id,
                        'datasetId':source_dataset_id,
                        'tableId':source_table_id,
                    },
                    'createDisposition': 'CREATE_IF_NEEDED',
                    "destinationTable": {
                        "projectId": destination_project_id,
                        "datasetId": destination_dataset_id,
                        "tableId": destination_table_id
                    },
                    'writeDisposition': write_disposition,
                },
            }
        }

        service_exec = self.service\
                    .jobs()\
                    .insert(
                        projectId=self.project_id, 
                        body=body,                        
                    )

        # self.create_table(
        #              dataset_id=destination_dataset_id,
        #              table_id=destination_table_id,
        #              project_id=destination_project_id,
        #              description=table_description,
        #              time_partition=time_partitioning,
        #              cluster_fields=cluster_fields
        #     ) 
        error_no_dataset = 'Not found: Dataset'
        status = service_exec.execute()['status']
        error_result = status.get('errorResult',{}).get('message','')

        if error_no_dataset in error_result and recurse < 3:   

            self.create_dataset(
                project_id=destination_project_id, 
                dataset_id=destination_dataset_id
            )       
            
            recurse =+ 1

            self.copy_table(
                  source_table=source_table,
                  write_disposition=write_disposition,
                  destination_table=destination_table,
                  table_description=table_description,
                  dataset_description=dataset_description,
                  time_partitioning=time_partitioning,
                  cluster_fields=cluster_fields,
                  access=access,
                  recurse=recurse)
            print(f'Dataset not created. Recursed: {recurse}')

        
        self.update_table(
            project_id = destination_project_id,
            dataset_id=destination_dataset_id,
            table_id=destination_table_id,
            description=table_description
        )

        self.update_dataset(
            project_id = destination_project_id,
            dataset_id=destination_dataset_id,
            description=dataset_description,
            access=access,
        )
        print(f'Updated dataset: {destination_table_id}')

        return
        

    def query_to_table(self,
             sql,
             destination_table,
             access=[], 
             write_disposition=None,
             table_description=None,
             dataset_description=None,
             clustering_fields=None,
             time_paritioning_field=None,
             recurse=0):
        '''
        recurse if is the dataset doesn't exist, it tries again
        '''

        body = {
            'configuration':{
                'query': {
                    'query': sql
                    }
            }
        }

        destination_project_id,dataset_table = destination_table.split(':')
        destination_dataset_id,destination_table_id = dataset_table.split('.')
        query_config = body['configuration']['query']
        query_config.update(
            {'destinationTable':{
                'projectId': destination_project_id,
                'datasetId': destination_dataset_id,
                'tableId': destination_table_id,
                }})
        query_config.update(
            {
                'writeDisposition': write_disposition or 'WRITE_APPEND'
            }
        )
        query_config.update(
            {
                'useLegacySql':'false'
            }
        )
        query_config.update(
            {
                "timePartitioning": {

                    'field':time_paritioning_field,
                    'type': 'DAY'
                }
                        
            }
        )

        query_config.update(
            {
                "clustering": {                
                    "fields": clustering_fields
                }
                        
            }
        )

        body['configuration']['query'].update(query_config)        

        service_exec = self.service\
                    .jobs()\
                    .insert(
                        projectId=self.project_id, 
                        body=body,                        
                    )


        error_no_dataset = 'Not found: Dataset'
        status = service_exec.execute()['status']
        error_result = status.get('errorResult',{}).get('message','')

        if error_no_dataset in error_result and recurse < 3:   

            self.create_dataset(
                project_id=destination_project_id, 
                dataset_id=destination_dataset_id
            )        
            
            recurse =+ 1

            self.query_to_table(                
                sql=sql,
                destination_table=destination_table,
                access=access, 
                write_disposition=write_disposition,
                table_description=table_description,
                dataset_description=dataset_description,
                clustering_fields=clustering_fields,
                time_paritioning_field=time_paritioning_field,
                recurse=recurse)
            print(f'Dataset not created. Recursed: {recurse}')

        
        self.update_table(
            project_id = destination_project_id,
            dataset_id=destination_dataset_id,
            table_id=destination_table_id,
            description=table_description
        )

        self.update_dataset(
            project_id = destination_project_id,
            dataset_id=destination_dataset_id,
            description=dataset_description,
            access=access,
        )
        print(f'Updated dataset: {destination_table_id}')

        return
        
    def update_dataset(self,                        
                       dataset_id,
                       project_id=None,
                       description=None,
                       access=[]):

        DEFAULT_ACCESS = [
            {
                "role": 'OWNER', #READER, WRITER, OWNER
                "specialGroup": 'projectOwners'    
            },
            {
                "role": 'WRITER', #READER, WRITER, OWNER
                "specialGroup": 'projectReaders'    
            },
            {
                "role": 'READER', #READER, WRITER, OWNER
                "specialGroup": 'projectWriters'    
            },
            ]
        
        access.append(DEFAULT_ACCESS)

        body = {
            'description':description,
            'access':access
        }

        service_exec = self.service.datasets().update(
                    body=body,
                    projectId=project_id or self.project_id,
                    datasetId=dataset_id,
                    )
        try:                
            service_exec.execute()
            return f'Succeeded in updating: {dataset_id}'
        except HttpError as e: 
            return f'Error in creating: {dataset_id}, {e}'          

    def create_dataset(self, dataset_id, project_id=None):
        body = {
            'datasetReference':{
                'datasetId':dataset_id,
                'projectId': project_id or self.project_id
                }
            }

        service_exec = self.service.datasets().insert(
                    body=body,
                    projectId=project_id or self.project_id
                    )
        try:                
            service_exec.execute()
            return f'succeeded in creating {dataset_id}'
        except HttpError as e: 
            return f'error: in creating {dataset_id}, {e}'  

    def update_table(self,
                     dataset_id,
                     table_id,
                     description=None,
                     project_id=None,
                     schema=None):

        body = {}

        if description:
             body.update({'description': description})
        if schema:
             body.update({'schema': schema})             

        service_exec = self.service.tables().update(
            projectId=project_id or self.project_id,
            datasetId=dataset_id,
            tableId=table_id,
            body=body
            )

        try:                
            service_exec.execute()
            return f'Succeeded in updating: {table_id}'
        except HttpError as e: 
            return f'Error updating: {table_id}, {e}'            

    def create_table(self,
                     dataset_id,
                     table_id,
                     project_id=None,
                     description=None,
                     table_schema=None,
                     time_partition=None,
                     cluster_fields=None):

        body = {
                "tableReference": {
                        "projectId": project_id or self.project_id,
                        "datasetId": dataset_id,
                        "tableId": table_id
                    },
                
               
            }

        print(f'from client: {cluster_fields}')

        if time_partition:
            body.update({"timePartitioning": time_partition})

        if cluster_fields:
            body.update({'clustering': {
                'fields':cluster_fields}
                })
        
        if table_schema:
            body.update(
                {'schema': {
                    "fields": table_schema
                    }
                })
        if description:
            body.update({'description': description})



        service_exec = self.service.tables().insert(
            body=body,
            projectId=project_id or self.project_id,
            datasetId=dataset_id,
            )

        try:                
            service_exec.execute()
            return f'Succeeded in creating: {table_id}'
        except HttpError as e: 
            return f'Error creating: {table_id}, {e}'            

    def query(self,
              sql                         
              ):
        
        service = bigquery.Client(credentials=self.credentials)
        query_job = service.query(sql)  # API request
        rows = query_job.result()  # Waits for query to finish
        
        return rows 
