import json
import requests
import jinja2
import os
from jinja2 import Template
latex_jinja_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('.'))
    #filters['escape_tex'] = escape_tex
)
'''
LATEX_SUBS = (
    (re.compile(r'\\'), r'\\textbackslash'),
    (re.compile(r'([{}_#%&$])'), r'\\\1'),
    (re.compile(r'~'), r'\~{}'),
    (re.compile(r'\^'), r'\^{}'),
    (re.compile(r'"'), r"''"),
    (re.compile(r'\.\.\.+'), r'\\ldots'),
)


def escape_tex(value):
    newval = value
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval
'''

QUERY=""
HOST = "http://localhost:5000"
PATH =  "/rest/firmware/"

#curl 'http://localhost:5000/rest/firmware/e692eca8505b0f4a3572d4d42940c6d5706b8aabec6ad1914bd4d733be9dfecf_25221120' -X GET

def _make_get_requests(url):
    response = requests.get(url)
    response_data=response.text
    response_dict=json.loads(response_data)
    return response_dict

firmware_data =_make_get_requests("http://localhost:5000/rest/firmware/b7c55a6de9fd1b85ec07f661b4d21638021999e2b1e754de1922f3b01f2cedb8_3378139")
meta_data = firmware_data['firmware']['meta_data']
analysis = firmware_data['firmware']['analysis']


def erstelle_haupttex():
    
    template = latex_jinja_env.get_template('templates/main_template.tex')
    #print(template.render(analysis=analysis))
    maintexfile = template.render(analysis=analysis)
    #filehandler
    fh = open("new_main.tex", 'w')
    fh.write(maintexfile)
    fh.close
    pass

def erstelle_input_meta_tex():
    template = latex_jinja_env.get_template('templates/meta_template.tex')
    
    '''
    meta_copy = {}

    for i in meta_data:
        copy = i
        if "_" in i:
            i = i.replace("_", "\_")
            meta_copy[i] = meta_data[copy]
        else:
            meta_copy[copy] = meta_data[copy]
       '''     
    
    #print(template.render(meta_copy = meta_copy))
    maintexfile = template.render(meta_data = meta_data)
    
    fh = open("meta.tex", 'w')
    fh.write(maintexfile)
    fh.close

    pass


def filter(texfile):
    if "&" in texfile:
        texfile = texfile.replace("&", "\&")

    if "\r" in texfile:
        texfile = texfile.replace("\r", "\\\r")

    if "^" in texfile:
        texfile = texfile.replace("^", "\string^")

    if "_" in texfile:
        texfile = texfile.replace("_", "\_")

    if "\n\'" in texfile:
        texfile = texfile.replace("\n\'", "")

    if "#" in texfile:
        texfile = texfile.replace("#", "\\#")

    if "\\nchar" in texfile:
        texfile = texfile.replace("\\nchar", "\\\\nchar")

    if "\\nLSS" in texfile:
        texfile = texfile.replace("\\nLSS", "\\\\nLSS")

    if "\\@" in texfile:
        texfile = texfile.replace("\\@", "\\\\@")

    return texfile


def erstelle_analyse():

    for cursor_analysis in analysis:

        element = analysis[cursor_analysis]

        if cursor_analysis == "exploit_mitigations":
            
            template = latex_jinja_env.get_template('templates/exploit_mitigations_template.tex')
            
            summary = element['summary']
            
            texfile = template.render(exploit = element, summary = summary)            

            #texfile = filter(texfile)
            

            fh = open("exploitmitigations.tex", 'w')
            fh.write(texfile)
            fh.close
            
            pass

        elif cursor_analysis == "crypto_material":

            template = latex_jinja_env.get_template('templates/crypto_material_template.tex')
            
            summary = element['summary']
            
            texfile = template.render(element = element, summary = summary)            

            #texfile = filter(texfile)

            fh = open("cryptomaterial.tex", 'w')
            fh.write(texfile)
            fh.close

            pass
        elif cursor_analysis == "cpu_architecture":

            template = latex_jinja_env.get_template('templates/cpu_architecture_template.tex')
            
            summary = element['summary']
            
            texfile = template.render(element = element, summary = summary)            

           # texfile = filter(texfile)

            fh = open("cpuarchitecture.tex", 'w')
            fh.write(texfile)
            fh.close

            pass 

        elif cursor_analysis == "base64_decoder":

            template = latex_jinja_env.get_template('templates/analysis_template.tex')
            
            summary = element['summary']
            
            texfile = template.render(element = element)            

            #texfile = filter(texfile)

            fh = open("base64decoder.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "file_hashes":

            template = latex_jinja_env.get_template('templates/analysis_template.tex')
                                    
            texfile = template.render(element = element)            

            #texfile = filter(texfile)

            fh = open("filehashes.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "file_type":
            
            template = latex_jinja_env.get_template('templates/file_type_template.tex')
            
            summary = element['summary']
            
            texfile = template.render(file = element)            

            #texfile = filter(texfile)

            fh = open("filetype.tex", 'w')
            fh.write(texfile)
            fh.close
            
            pass

        elif cursor_analysis == "init_systems":

            template = latex_jinja_env.get_template('templates/analysis_template.tex')
            
            summary = element['summary']
            
            texfile = template.render(element = element)            

            #texfile = filter(texfile)

            fh = open("initsystems.tex", 'w')
            fh.write(texfile)
            fh.close
            
            pass

        elif cursor_analysis == "ip_and_uri_finder":

            template = latex_jinja_env.get_template('templates/analysis_template.tex')
            
            summary = element['summary']
            
            texfile = template.render(element = element)            

            #texfile = filter(texfile)

            fh = open("ipandurifinder.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "software_components":
            
            template = latex_jinja_env.get_template('templates/analysis_template.tex')
            
            summary = element['summary']
            
            texfile = template.render(element = element)            

            #texfile = filter(texfile)

            fh = open("softwarecomponents.tex", 'w' )
            fh.write(texfile)
            fh.close

            pass
        
        elif cursor_analysis == "printable_strings":

            template = latex_jinja_env.get_template('templates/analysis_template.tex')
            
            texfile = template.render(element = element)            

            #texfile = filter(texfile)

            fh = open("printablestrings.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "users_and_passwords":

            template = latex_jinja_env.get_template('templates/analysis_template.tex')
            
            summary = element['summary']
            
            texfile = template.render(element = element)            

            #texfile = filter(texfile)

            fh = open("usersandpasswords.tex", 'w')
            fh.write(texfile)
            fh.close

            pass
        
        elif cursor_analysis == "string_evaluator":

            template = latex_jinja_env.get_template('templates/analysis_template.tex')
            
            texfile = template.render(element = element)            

            #texfile = filter(texfile)

            fh = open("stringevaluator.tex", 'w')
            fh.write(texfile)
            fh.close

            pass
        
        elif cursor_analysis == "unpacker":

            template = latex_jinja_env.get_template('templates/analysis_template.tex')
            
            summary = element['summary']
            
            texfile = template.render(element = element)            

            #texfile = filter(texfile)

            fh = open("unpacker.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "malware_scanner":

            template = latex_jinja_env.get_template('templates/analysis_template.tex')
            
            summary = element['summary']
            
            texfile = template.render(element = element)            
            
            #texfile = filter(texfile)
            
            fh = open("malwarescanner.tex", 'w')
            fh.write(texfile)
            fh.close

    pass

#erstelle_haupttex()
erstelle_input_meta_tex()
erstelle_analyse()
print("done")
