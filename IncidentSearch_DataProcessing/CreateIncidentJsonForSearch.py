
def create_incident_json_data(start_date_query:str,end_date_query:str,config)-> list[str] :
    """
    Retrive incident data from Database to create json file and save them in local directory.
    Args:
        start_date_query (str): Start date to get data.
        end_date_query (str): End date to get data.
        config : .env Config file
    Returns:
        list[str]: list of newly created json files to be imported to google cloud storage.
    """


    # In[49]:


    import psycopg2
    import psycopg2.extras as extras
    import pandas as pd
    import json
    from datetime import datetime
    from google.cloud import bigquery
    from dotenv import dotenv_values
    import re

    from google.cloud.exceptions import NotFound
    from google.api_core.exceptions import BadRequest

    from dotenv import dotenv_values


    # In[50]:

    local_data_path=config['INPUT_SEARCH_DATA_PATH']
    url_search_detail=config['SEARCH_DETAIL_URL']
    customDocumentId=config['CUSTOM_DOCUMENT_ID']

    str_postfix="daily_incident"

    listNewlyCratedFiles=[]


    # In[51]:


    dt_imported=datetime.now()
    str_imported=dt_imported.strftime('%Y-%m-%d %H:%M:%S')
    str_date_imported=dt_imported.strftime('%d%m%Y_%H%M')
    print(f"Imported DateTime: {str_imported}" )
    print(f"Imported Date: {str_date_imported}" )


    # In[52]:


    def get_postgres_conn():
     try:
      conn = psycopg2.connect(
            database=config['DATABASES_NAME'], user=config['DATABASES_USER'],
          password=config['DATABASES_PASSWORD'], host=config['DATABASES_HOST']
         )
      return conn

     except Exception as error:
      print(error)      
      raise error
    def list_data(sql,params,connection):
     df=None   
     with connection.cursor() as cursor:

        if params is None:
           cursor.execute(sql)
        else:
           cursor.execute(sql,params)

        columns = [col[0] for col in cursor.description]
        dataList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        df = pd.DataFrame(data=dataList) 
     return df 


    # In[53]:


    if end_date_query  is None:
        date_filter=f"incident.updated_at>='{start_date_query}'"
    else:
        date_filter=f"incident.updated_at>='{start_date_query}' and incident.updated_at<'{end_date_query}'"

    # ,CONCAT(incident_no,' - Serial: ',serial_number,' - Model:',model.model_name,' - Brand:',brand_name) as title
    sql_incident=f"""

    select
    incident.id as _id ,incident.incident_no as incident_no,ac.company_name
    ,CONCAT('{url_search_detail}',incident.id,'/') as uri,

    incident.incident_subject as title, incident_description description

    ,xtype.incident_type_name as incident_type,severity.severity_name as  severity

    ,CONCAT(brand.brand_name,' - ',model.model_name,'- ',serial_number) as inventory_item
    ,brand.brand_name as brand,model.model_name as model,inventory.serial_number


    from app_incident as incident
    inner join app_incident_type as  xtype on incident.incident_type_id = xtype.id
    inner join  app_incident_severity as severity on  incident.incident_severity_id = severity.id
    inner join app_inventory as inventory on incident.inventory_id = inventory.id
    inner join app_brand as brand on inventory.brand_id = brand.id
    inner join app_model as model on inventory.model_id = model.id
    inner join app_project ap on inventory.project_id = ap.id
    inner join app_company ac on ap.company_id = ac.id

    where {date_filter}
    and inventory.is_dummy=False and incident.incident_status_id<>3

    order by incident.id 

    """

    print(sql_incident)


    # In[54]:


    sql_detail="""
    select  detail.id as detail_id, detail.incident_master_id as incident_id ,
    workaround_resolution as solution
    ,(select service_team_name from app_serviceteam as team where team.id= service_team_id ) as engineer_team
    from app_incident_detail detail
     where detail.incident_master_id =  %(incident_id_param)s 
     """
    print(sql_detail)


    # In[59]:


    _ILLEGAL_CHARACTERS_RE = re.compile(r"[\000-\010]|[\013-\014]|[\016-\037]")
    # \r\n\r  \r\n
    # https://www.geeksforgeeks.org/python-removing-newline-character-from-string/
    def replace_ILLEGAL_CHARACTERS(text):
       text_fixed = _ILLEGAL_CHARACTERS_RE.sub("", text)
       return  text_fixed  

    def replace_NewLine_CHARACTERS(text):
       text_fixed= text.replace("\r\n", " ").replace("\r\n\r", " ")   
       return  text_fixed  

    df_all=list_data(sql_incident,None,get_postgres_conn())
    print(f"List all issues dataframe : {len(df_all)}")
    if df_all.empty==True:
        print("No data to create Json files")
        return listNewlyCratedFiles



    # In[60]:


    df_all[customDocumentId]=df_all[customDocumentId].astype(str)


    df_all['description']=df_all['description'].apply(replace_ILLEGAL_CHARACTERS) 
    df_all['description']=df_all['description'].apply(replace_NewLine_CHARACTERS)

    print(df_all.info())
    df_all.tail()


    # In[61]:


    # write json file/dataframe
    file_name=f"{str_date_imported}-{str_postfix}.ndjson"
    with open(f'{local_data_path}\\{file_name}', 'w',encoding='utf8') as f:

        for index, srCaseItem in df_all.iterrows(): 
            id=int(srCaseItem[customDocumentId])
            srDict=srCaseItem.to_dict()

            print(f"============================{id}==============================")    
            #incident_update_at= incident['imported_at']
            df_detail = list_data(sql_detail,{"incident_id_param": id},get_postgres_conn())
            if df_detail.empty==False:

              df_detail=df_detail.drop(columns=['incident_id','detail_id'])  
              df_detail['solution']=df_detail['solution'].apply(replace_ILLEGAL_CHARACTERS)
              df_detail['solution']=df_detail['solution'].apply(replace_NewLine_CHARACTERS)  

              detailDict = df_detail.to_dict(orient = 'records')
              srDict['solution_list']=detailDict

            json_object = json.dumps(srDict,ensure_ascii=False)
            f.write(json_object + '\n')

    listNewlyCratedFiles.append(file_name) 


    # In[25]:


    return  listNewlyCratedFiles


    # In[ ]:




