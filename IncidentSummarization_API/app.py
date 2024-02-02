# Guide line to create FLASK project ChatGPT :https://chat.openai.com/c/a0735846-ac4e-4cc3-bf01-0e16fba8897e
# Duet AI: Code Generation as below
"""
How to initialize project after installing FLASK for building Flask REST APIs project as The following requirement.
1. create app.py
2. create 1 function in file  app.py named get_incident_summarization_by_id as specified requirement.
   - GET Method function
   - Desing 1 parameter named incident_id as int64.
   - The return type is a string
3. The function name get_incident_summarization_by_id is  responsible for doing the following
   - call get_incident_content function in incident_content_creator(incident_content_creator.py) module to return to content_text  variable as string
   - call summarize_incident function in text_bison(text_bison.py) module  and resturn result to  incident_summarization 
5. Create a Python client file, that will Invoke get_incident_summarization_by_id in   through Rest-API by passing incident_id as an argument to the API.

"""
from flask import Flask, request, jsonify
from incident_content_creator import get_incident_content
from dotenv import dotenv_values
import text_bison as bison
import text_gemini as gemini

app = Flask(__name__)

@app.route('/get_incident_summarization_by_id/<int:incident_id>', methods=['GET'])
def get_incident_summarization_by_id(incident_id):
    try:
        config = dotenv_values('.env')
        # content_template="v1_incident_template.txt"
        incident_content=get_incident_content(incident_id=incident_id,config=config)
        model_id=config["GEN_AI_MODEL_ID"]
        if model_id==1:
            model='bison'
            incident_summarization=bison.summarize_incident(incident_content,config)
        else:
            incident_summarization=""
            model='gemini'
            responses=gemini.summarize_incident(incident_content,config)
            for response in responses:
                incident_summarization=incident_summarization+response.text 

        # return jsonify({'success': True, 
        #         'incident_summarization': incident_summarization
        #         })
        return jsonify({'success': True, 
                        'incident_content': incident_content,
                        'incident_summarization': incident_summarization,
                        'model':model,
                        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
        # raise Exception(str(e))

# cd IncidentSummarization and run this command  python app.py
if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=True)

# open cmd and do the following
#cd IncidentSummarization_API
#python app.py

