# 💾 UASDdb_aspx2json

**UASDdb_aspx2json** is a python script that allows you to get data from the UASD ASPX server (Semester Schedule Server) and translate it into JSON. This allows the developer to manage raw data from the server.

## Requirements

![Python](https://img.shields.io/pypi/pyversions/pandas?style=for-the-badge&logo=python&logoColor=white)

*Requiered* packages:

* Requests
* Json
* Pandas
* OS

In order to use the script, you should query the server with two arguments: **Location of the subjects [Campus]** and **Subjects Code [Key]**


>     UASD_db_query(args)
>
>     Args:
>       campus (str): location of the subject (ex. 'SED':Sede Central (Santo Domingo))
>       key (str): subject code or subject key (ex. IEM347)
>       
>       
>      ⚠️ If you have more than 1 key, you shoud loop the keys storaged in a list

<h5>Example</h5>

```python
  
from UASDdb_aspx2json import *
  
campus = 'SED' #campus name
keys = ['list', 'of', 'subjects', 'code', 'ex. IEM'] #IEM means, every subject of electromechanical engineering
  
for key in keys:
  request = UASD_db_query(campus, key) #request the data
  data_translator = FormatASPX(request.get_responce()).tojson() #translate the data into json
  Save(data).to_json() #save the data in json format
  
#if you want to save the json data into an excel spreadsheet do this
Save(data).to_excel()

```

