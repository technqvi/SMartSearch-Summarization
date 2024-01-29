
# %%
def get_incident_content(incident_id,content_template,config):
    """
    Take incident id to get data from incident to create incident as content.
    Parameters:
    - incidetn_id (int):  id from app_incident table.
    - content_template (str):  path to template file to create desired summarization content.
    - config (int):  config values loaded from dotenv_values
    Returns:
    str: proper text to be fed to Generative AI to generate summarization.
    """
    # template='v1_incident_content.txt'

    import psycopg2
    import pandas as pd
    from datetime import datetime,timezone

    import os
    import sys 
    import re

    import pandas as pd
    import numpy as np
    from datetime import datetime 
    from google.cloud import bigquery
    from google.oauth2 import service_account

    from google.api_core import exceptions

    from dotenv import dotenv_values

# %%
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
    
    def list_data_pg(sql,params,connection):
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


    _ILLEGAL_CHARACTERS_RE = re.compile(r"[\000-\010]|[\013-\014]|[\016-\037]")
    def replace_ILLEGAL_CHARACTERS(text):
        text_fixed = _ILLEGAL_CHARACTERS_RE.sub("", text)
        return  text_fixed  
    def replace_NewLine_CHARACTERS(text):
        text_fixed= text.replace("\r\n", " ").replace("\r\n\r", " ")   
        return  text_fixed  
    # %%
    sql_incident=f" SELECT * FROM view_incident_summarization WHERE id = {incident_id} "
    dfIncident=list_data_pg(sql_incident,None,get_postgres_conn())
    if dfIncident.empty!=True:
        dfIncident['subject']=dfIncident['subject'].apply(replace_ILLEGAL_CHARACTERS)
        dfIncident['description']=dfIncident['description'].apply(replace_ILLEGAL_CHARACTERS)
        sr=dfIncident.iloc[0,:]
        
    else:
        raise Exception(f"Not found incident id {incident_id}")

    print(sr)


    # %%
    sql_detail=f" SELECT * FROM view_incident_detail_summarization WHERE incident_id = {incident_id} "
    df=list_data_pg(sql_detail,None,get_postgres_conn())
    if dfIncident.empty == False:
        df['running_number'] = list(range(1, len(df) + 1))
        df['solution']=df['solution'].apply(replace_ILLEGAL_CHARACTERS)
        print(df)
    else:
        raise Exception(f"Not found detail of incident id {incident_id}")


    # %%
    # https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/prompts/examples/text_summarization.ipynb
    # https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/getting-started/intro_gemini_pro_python.ipynb
    #-------------------------------------------------------------------------------------------------------
    # https://cloud.google.com/vertex-ai/docs/generative-ai/text/text-prompts#summarization_prompts
    # https://medium.com/@roybanerjee.supriyo/text-summarization-with-generative-models-on-vertex-ai-f035668b9594
    # https://cloud.google.com/vertex-ai/docs/samples/aiplatform-sdk-summarization#aiplatform_sdk_summarization-python

    # create template on text file as below.
    
    from jinja2 import Template
    try:
        # Read your Jinja template file
        with open(content_template, 'r') as file:
            template_text = file.read()
        # Create a Jinja template object
        template = Template(template_text)
        # Render the template with Pandas variables
        content_text = template.render( sr=sr,df=df )
    except Exception as e:
        raise e

    

    # # # # Print the rendered text
    # print(content_text)


    # %%
    return content_text








