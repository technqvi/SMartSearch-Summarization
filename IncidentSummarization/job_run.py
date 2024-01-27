import requests

#================================================================
# local
# get_incident_summarization_by_id  
incident_id = 4438  #4300  # Replace with the desired incident ID

#http://127.0.0.1:5000/get_incident_summarization_by_id/1
response = requests.get(f'http://127.0.0.1:5000/get_incident_summarization_by_id/{incident_id}')
if response.status_code == 200:
    data=response.json()
    if data['success'] == True:
        incident_summarization=data['incident_summarization']
        print(f"=======================Incident Summarization # {incident_id}=======================")
        print(incident_summarization)
    else:
        print(f"Error: {data['error']}")
else:
    print(f"Error: {response.status_code}")



# def get_incident_summarization_by_id():
#     import incident_content_creator as cc
#     import text_bison as bison
#     from dotenv import dotenv_values
#     import os
#     incident_id=4300  #4438 # 3743 long sample AIS
#     config = dotenv_values('.env')
#     content_text=cc.get_incident_content(incident_id=incident_id,config=config)
#     print(content_text)
#     print("find length of content_text variable")
#     n_str=len(content_text)
#     print(f"=============Total length of content_text {n_str}====================")
#     print(n_str)

 
#     file_path = "incident_conent.txt"
#     with open(file_path, 'w') as file:
#         file.write(content_text)

#     incident_summarization=bison.summarize_incident(content_text,config)
#     print(incident_summarization)


#     output_file_path = "incident_summary.txt"
#     with open(output_file_path, 'w') as file:
#         # Write the content to the file
#         file.write(incident_summarization)

# if __name__ == "__main__":
#     get_incident_summarization_by_id()


