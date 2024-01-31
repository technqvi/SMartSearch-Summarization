# SMart-Search-Summarization
Build Enterprise Search using [Vertex AI Search](https://cloud.google.com/vertex-ai-search-and-conversation?hl=en) and Text Summarization using  [Google Generative-AI Model](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/introduction-prompt-design) for IT Incident of [SMartApp](https://github.com/technqvi/SMartApp). The figure and description below how it works. 
<img width="998" alt="overview" src="https://github.com/technqvi/SMartSearch-Summarization/assets/38780060/b028d869-b75e-473c-9c38-8dd7cec69347">


### Incident Search (Vertex AI Search) 
* Retrive incident and detail data from database to create ndjson file.
* Ingest recently created json file to Google Cloud Storage.
* Import json file from Google Cloud Storage to Search DataStore.
### Incident Summarization (Vertex AI Gen-AI)
* Try seach somthing on Search page and click to view search results detail.
* Click Summarization on Search page 
* Grab entire incidence detail to create incident content template to let Gen-AI create incident summary.

## Program Structure
* [RunImportData.py](https://github.com/technqvi/SMartSearch-Summarization/blob/main/RunImportData.py) : main scrip to run  [IncidentSearch_DataProcessing](https://github.com/technqvi/SMartSearch-Summarization/tree/main/IncidentSearch_DataProcessing)
* [IncidentSearch_DataProcessing](https://github.com/technqvi/SMartSearch-Summarization/tree/main/IncidentSearch_DataProcessing)  : 3 Core module files to ingest json data from database to cloud starage and  data store in Searh App accordingly. 
* [IncidentSummarization_API](https://github.com/technqvi/SMartSearch-Summarization/tree/main/IncidentSummarization_API) : Modul files and template file to perform incident summarization, it can be used as FLASK API. 

## References Service and Solution
* [Google Cloud Storage](https://cloud.google.com/storage/docs/creating-buckets)
* [Introduction to Vertex AI Search](https://cloud.google.com/generative-ai-app-builder/docs/enterprise-search-introduction?hl=en)
* [Gen-TI Vetex AI](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/overview)
* [Prompt-Design](https://cloud.google.com/vertex-ai/docs/generative-ai/text/text-prompts#summarization_prompts)
* [Google-Generative-aI](https://github.com/GoogleCloudPlatform/generative-ai/tree/main)
* [Text Summarization](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/prompts/examples/text_summarization.ipynb)