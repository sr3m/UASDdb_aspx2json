
import requests
import json
import pandas as pd
import os

#Developed by Willmers Hernández
#Used query and sort data for the reaserch titled: "Propuesta de mejora del desempeño energético enfocada en la implementación
# de un sistema de generación fotovoltaico. Caso de estudio: Laboratorio de Alta Tecnología UASD"

class UASD_db_query:
    """uasd_db_aspx2json is a translator that make a request to UASD database servers and get an utf-8 encoded 
    .aspx response. The function decoded utf-8 and translate the response from aspx to json.

    Args:
        campus (str): location of the subject ('SED':Sede Central (Santo Domingo))
        clave (str): subject code or subject key (IEM347)
    """
    def __init__(self,location,code):
        self.location = location
        self.code = code
        self.data_list = []
        
    def get_response(self):
        """This function makes a request to UASD database in order to
        get back the semester schedule filtered by location and subject code.

        Args:
            location (str): location of the subject ('SED':Sede Central (Santo Domingo))
            code (str): subject code or subject key (IEM347)

        Returns:
            .aspx str: returns and .aspx string from an ASP.NET server
        """
        s = requests.Session()
        payload_form = {
            'campus': self.location,
            'clave': self.code
        }
        request = s.post('https://soft.uasd.edu.do/ProgramacionPorAsignatura/Default.aspx/ObtenerData', json=payload_form)
        
        return request.content.decode('utf-8')

class FormatASPX:
    
    def __init__(self, uforDB):
        self.uforDB = uforDB
    
    def tojson(self):
        p_data = self.uforDB.replace("\\", "").split("],[")
        index = p_data[0].index("[")
        p_data[0] = p_data[0][int(index)+2:len(p_data[0])+1]
        cleaned_data = list()

        for _ in p_data:
            for char in [r"]","}","\"","\'"]:
                _ = _.replace(char,"")
            cleaned_data.append(_)

        for i,data in enumerate(cleaned_data):
            data = data.split(",")
            cleaned_data[i] = data

        list_headers = ['PERIODO','NRC','CLAVE','ASIGNATURA','SEC','TIPO',
                        'CAMPUS','HORARIO','DIAS','EDIFICIO','AULAS','CUPOS',
                        'INSCRITOS','DISPONIBLES','CODIGO','PROFESOR']

        data_list = list()

        for row in cleaned_data:
            json_structure = dict()
            for header,data in zip(list_headers,row):
                json_structure[header] = data
            data_list.append(json_structure)
                
        return data_list

class Save:
    def __init__(self, data_list):
        self.data_list = data_list
        
    def to_json(self):
        """Registra un log por día de todas las database_file realizadas en un archivo .txt, la función no
        sobreescribe el archivo, solo adjunta data en el archivo creado o lo crea si no existe"""

        log_foldername = "database_log"
        
        #1ero Verifica si existe la carpeta data_log, si no existe, la crea
        os.makedirs(log_foldername,exist_ok=True)
        
        #2do Verifica si existe un archivo json realizado en el día DD-MM-YYYY
        if os.path.isfile(f"{log_foldername}\\database_file.json") == False:
            
        #3ro Si no existe el archivo, lo crea y escribe    
            with open(f"{log_foldername}\\database_file.json",'w',encoding='utf-8') as f:
                f.write(json.dumps(self.data_list,ensure_ascii=False))    
            
        else:
        #4to Si existe el archivo, lo lee
            with open(f"{log_foldername}\\database_file.json",'r',encoding='utf-8') as f:
                json_data = json.loads(f.read())
        #5to Agrega las nuevas database_file
            for objects in self.data_list:
                json_data.append(objects)
        #6to Sobreescribe el archivo actualizado
            with open(f"{log_foldername}\\database_file.json",'w',encoding='utf-8') as f:
                f.write(json.dumps(json_data,ensure_ascii=False))
            
        
    def to_excel(self):
        
        log_foldername = "database_log"
        excel_file_dir = "excel_tables"
        
        os.makedirs(excel_file_dir,exist_ok=True)
        
        path = f"{log_foldername}\\database_file.json"
        
        with open(path) as js:
            db = json.loads(js.read())
            df = pd.json_normalize(db)
            df.to_excel(f"{excel_file_dir}\\database_file.xlsx")
        
        print(f"\nSe ha guardado la iteración correctamente con el nombre database_file_{len(self.data_list)}.xlsx\nEn la ruta: {os.getcwd()}\\{excel_file_dir}\\database_file.xlsx\n")

if __name__ == "__main__":

    keys = "IEM203	IEM206	IEM367	IEM335	IEM336	IEM343	IEM368	IEM433	IEM369	IEM425	IEM436	IEM417	IEM563	IEM204	IEM306	IEM357	IEM305	IEM339	IEM459	IEM407	IEM450	IEM516	IEM518	IEM612	IEM204	IEM306	IEM305	IEM309	IEM339	IEM359	IEM317	IEM407	IEM419	IEM504	IEM319	IEM502	IEM509	IEM203	IND334	IEM206	CIV219	CIV361	CIV442	CIV366	CIV444	INQ344	INQ346	INQ553".split("\t")

    for key in keys:
        db = UASD_db_query("SED",key)
        data = FormatASPX(db.get_response()).tojson()
        Save(data).to_json()
    
    Save(data).to_excel()
