
def import_incident_json_to_search_datestore(list_json:list[str],config,import_mode="INCREMENTAL")  :
    # """
    # Import json data to Vertex AI Search DataStore.
    # Args:
    #     list_json (list[str]): List json files.
    #     config : .env Config file
    #     import_mode : import_mode=FULL for 1st time, and import_mode=INCREMENTAL
    # """


    # # Link reference 
    # * https://cloud.google.com/generative-ai-app-builder/docs/samples/genappbuilder-import-documents?hl=en
    # * https://cloud.google.com/generative-ai-app-builder/docs/samples/genappbuilder-list-documents?hl=en

    # # Step to import each file in GS to datastore increamentally
    # * To get datastore id and scheme definition generation , we need to create data store and import json file via Console 
    # * Purge data and re-import programatice with Full Mode
    # * This way, you get  get your custom id (incident id) from importing as document id 

    # In[3]:

    
    listNDJsonFiles=list_json



    # In[4]:


    from google.api_core.client_options import ClientOptions
    from google.cloud import discoveryengine
    import os
    from dotenv import dotenv_values


    # In[5]:

    # remove


    my_data_store_id = config['SEARCH_DATA_STORE']
    target_gs_bucket=config['TARGET_SEARCH_GS_PATH']


    my_project_id=config["PROJECT_ID"]
    my_location = config["LOCATION"] # Values: "global"

    #Options: 'FULL', 'INCREMENTAL'
    my_mode=import_mode
    # it is unlikely to import n item(1 files /1 incident)  from gs at once because we can not control limit of no.file in bucket (default :100 files)
    # if  my_mode=="FULL":  # The full mode 
    #     my_gcs=f"gs://{target_gs_bucket}/*.ndjson"
    # else:
    # import individual file over the list , it have to be incremantal
    # however, if you are attemping to insert data with Full , you will always get one file as last file imported 
    my_gcs=f"gs://{target_gs_bucket}/"  
    print(my_gcs)


    # In[6]:


    def import_documents_from_gs_to_datastore(
        import_mode:str, 
        project_id: str,
        location: str,
        data_store_id: str,
        gcs_uri: str
    ) -> str:
        #  For more information, refer to:
        # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
        client_options = (
            ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
            if location != "global"
            else None
        )
        if import_mode.upper()=='FULL':
            selective_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.FULL
        else:
            selective_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL

        # Create a client
        client = discoveryengine.DocumentServiceClient(client_options=client_options)

        # The full resource name of the search engine branch.
        # e.g. projects/{project}/locations/{location}/dataStores/{data_store_id}/branches/{branch}
        parent = client.branch_path(
            project=project_id,
            location=location,
            data_store=data_store_id,
            branch="default_branch",
        )


        request = discoveryengine.ImportDocumentsRequest(
            parent=parent,
            gcs_source=discoveryengine.GcsSource(input_uris=[gcs_uri], data_schema='custom'),
            reconciliation_mode=selective_mode
        )

        # Make the request
        operation = client.import_documents(request=request)

        print(f"Waiting for operation to complete: {operation.operation.name}")
        response = operation.result()

        # Once the operation is complete,
        # get information from operation metadata
        metadata = discoveryengine.ImportDocumentsMetadata(operation.metadata)

        # Handle the response
        print(response)
        print(metadata)

        return operation.operation.name



    # In[7]:


    # Incremetal mode because of 100 files limitation issue
    listNDJsonPath=[  os.path.join(my_gcs,file_name) for file_name in listNDJsonFiles   ]
    print(f"{listNDJsonPath}")
    for json_file in listNDJsonPath:
     print(json_file)   
     opt_name=import_documents_from_gs_to_datastore(import_mode=my_mode, project_id=my_project_id,location=my_location
                                     ,data_store_id=my_data_store_id,gcs_uri= json_file)


    # In[ ]:





    # In[ ]:


    return True

