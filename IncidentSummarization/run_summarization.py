import incident_content_creator as cc
import text_bison as bison
from dotenv import dotenv_values

if __name__ == "__main__":
    incident_id=4300  #4438 # 3743 long sample AIS
    config = dotenv_values('.env')
    content_text=cc.get_incident_content(incident_id=incident_id,config=config)
    print(content_text)
    print("find length of content_text variable")
    n_str=len(content_text)
    print(f"=============Total length of content_text {n_str}====================")
    print(n_str)

    import os
    file_path = "incident_conent.txt"
    with open(file_path, 'w') as file:
        file.write(content_text)

    incident_summarization=bison.summarize_incident(content_text,config)
    print(incident_summarization)


    output_file_path = "incident_summary.txt"
    with open(output_file_path, 'w') as file:
        # Write the content to the file
        file.write(incident_summarization)    