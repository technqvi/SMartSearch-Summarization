# import requests
#http://127.0.0.1:5000/get_incident_summarization_by_id/1
# incident_id = 4431  #4300  # Replace with the desired incident ID
# response = requests.get(f'http://127.0.0.1:5000/get_incident_summarization_by_id/{incident_id}')
# if response.status_code == 200:
#     data=response.json()
#     if data['success'] == True:
#         incident_summarization=data['incident_summarization']
#         print(f"=======================Incident Summarization # {incident_id}=======================")
#         print(incident_summarization)
#     else:
#         print(f"Error: {data['error']}")
# else:
#     print(f"Error: {response.status_code}")

# write code python read line to get input console



def get_incident_summarization_by_id(incident_id,model_id):
    import incident_content_creator as cc
    import text_bison as bison
    import text_gemini as gemini
    from dotenv import dotenv_values
    import os
    
    inout_path="test-input-output"
    config = dotenv_values('.env')
    content_template="v2_incident_template.txt"
    content_text=cc.get_incident_content(incident_id=incident_id,content_template=content_template,config=config)
    print(content_text)
    print("find length of content_text variable")
    n_str=len(content_text)
    print(f"=============Total length of content_text {n_str}====================")
    print(n_str)

    if model_id==1: 
        incident_summarization=bison.summarize_incident(content_text,config)
        
    else:    
        incident_summarization=""
        responses=gemini.summarize_incident(content_text,config)
        for response in responses:
            # incident_summarization=incident_summarization+response       
            print(response.text, end="")

    print(f"=============Total length of summary_text {len(incident_summarization)}====================")

    file_path = f"{incident_id}-conent_model{model_id}.txt"
    with open(os.path.join(inout_path,file_path), 'w') as file:
        file.write(content_text)
    output_file_path = f"{incident_id}-_summary_model{model_id}.txt"
    with open(os.path.join(inout_path,output_file_path), 'w') as file:
        # Write the content to the file
        file.write(incident_summarization)

if __name__ == "__main__":
    incident_id= 4300 #4431  #4300  #4438 # 3743 long sample AIS
    model_id = 1

    print("Enter the following incident id: ")
    id = input("Incident ID : ")

    # print("1=bison and 2=gemini ")
    # model_id = input("Model ID : ")

    get_incident_summarization_by_id(int(id),int(model_id))


