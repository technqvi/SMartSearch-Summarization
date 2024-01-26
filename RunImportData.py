#!/usr/bin/env python
# coding: utf-8

# In[3]:


from dotenv import dotenv_values
from configupdater import ConfigUpdater
from datetime import datetime,timezone
from  IncidentSearch_DataProcessing import CreateIncidentJsonForSearch,IngestIncidentDataToGSC,ImportIncidentDataToSearchApp


# # Name
# #### App Name : incident-search-app
# #### DataStore Name :  incident-search-ds
# #### GS: incident-search-essm-yip

# # Init

# In[4]:


#mode="FULL"  # For The first load to create search app and datastore for getting datasource id and data schema generation.
mode="INCREMENTAL"  # For periodict job

dt_imported=datetime.now()
dt_imported=datetime.strptime(dt_imported.strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
print(f"Import At : {dt_imported}")

# For manual load start and end+1 day '2023-11-22' - '2023-11-23'  
start_date_query=None
end_date_query=None  


# In[5]:


#env_path='../.env' # production
env_path='.env'  # dev
config = dotenv_values(dotenv_path=env_path)

updater = ConfigUpdater()
updater.read(".cfg")



last_imported=datetime.strptime(updater["metadata"]["last_import"].value,"%Y-%m-%d %H:%M:%S")

if start_date_query is None:
 start_date_query=last_imported


print(f"We are about to import incident from { start_date_query} to  {end_date_query}")

#Options: 'FULL', 'INCREMENTAL'

directory_path = config['INPUT_SEARCH_DATA_PATH']
gsc_path=['TARGET_SEARCH_GS_PATH']


# # Step#1 Create Incident Json Files

# In[6]:


print(f"Step#1 Create Incident Json on {start_date_query} to {end_date_query}")


# In[7]:


listNewlyCratedFiles=CreateIncidentJsonForSearch.create_incident_json_data(start_date_query,end_date_query,config)


# # Step#2 Ingest data to Google Storage

# In[8]:


# ! gsutil -m rm gs://incident-smart-search-yip/**
# listNewlyCratedFiles=['22112023_2-daily_incident.ndjson']


# In[9]:


print("Step#2 Ingest data to Google Storage")


# In[10]:


if len(listNewlyCratedFiles)>0:
   gs_ok= IngestIncidentDataToGSC.ingest_incident_json_to_gs(listNewlyCratedFiles,config)
   print(gs_ok)
else:
    print("No data to search.")
    exit()


# # Step#3 Import data from GS to DataStore

# ## Follow these steps for the first 
# ### upload doc muanually
# * if there is no search app and data store ,please create both
# * import data with file to dsatastore as full load at first with small file to generate schema (JSONL for structured data (Preview)
# * https://cloud.google.com/generative-ai-app-builder/docs/create-data-store-es
# * purge data in order to reload with _id(incident id in SMartApp) 
# * delete file on GS
# ### import jsonfile programmatically with "Full load mode"
# * repeat step#1 to full load
# * edit schema as necessary
# * Incrematal load 

# In[11]:


import_ok=ImportIncidentDataToSearchApp.import_incident_json_to_search_datestore(list_json=listNewlyCratedFiles
                                                                                 ,config=config
                                                                                 ,import_mode=mode)


# # Step#4 Delelte Json Files

# In[12]:


import os

def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
     print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")

# Usage


delete_files_in_directory(directory_path)


# In[13]:


updater["metadata"]["last_import"].value=dt_imported.strftime("%Y-%m-%d %H:%M:%S")
updater.update_file() 


# In[ ]:




