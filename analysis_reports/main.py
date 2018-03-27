import json
import requests
import jinja2
import os
from datetime import datetime
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
    maintexfile = template.render(meta_data = meta_data)
    #filehandler
    fh = open("main.tex", 'w')
    fh.write(maintexfile)
    fh.close
    pass

def erstelle_input_meta_tex():
    template = latex_jinja_env.get_template('templates/meta_data_template.tex')
    
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

def convert_date(datetime_var):
    converted_date = datetime.fromtimestamp(int(datetime_var)) #fromtimestamp(int(float(datetime_var)))

    return converted_date


def erstelle_analyse():

    for cursor_analysis in analysis:

        element = analysis[cursor_analysis]

        if cursor_analysis == "exploit_mitigations":

            analysis_date = convert_date(element['analysis_date'])
            plugin_version = element['plugin_version']
            summary = element['summary']

            template = latex_jinja_env.get_template('templates/exploit_mitigations_template.tex')

            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, summary = summary)

            fh = open("exploitmitigations.tex", 'w')
            fh.write(texfile)
            fh.close
            
            pass

        elif cursor_analysis == "crypto_material":

            analysis_date = convert_date(element['analysis_date'])
            plugin_version = element['plugin_version']
            summary = element['summary']

            template = latex_jinja_env.get_template('templates/crypto_material_template.tex')
            
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, summary = summary)

            fh = open("cryptomaterial.tex", 'w')
            fh.write(texfile)
            fh.close

            pass
        elif cursor_analysis == "cpu_architecture":

            analysis_date = convert_date(element['analysis_date'])
            plugin_version = element['plugin_version']
            summary = element['summary']

            template = latex_jinja_env.get_template('templates/cpu_architecture_template.tex')
            
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, summary = summary)

            fh = open("cpuarchitecture.tex", 'w')
            fh.write(texfile)
            fh.close

            pass 

        elif cursor_analysis == "base64_decoder":

            analysis_date = convert_date(element['analysis_date'])
            plugin_version = element['plugin_version']
            summary = element['summary']

            template = latex_jinja_env.get_template('templates/base64_decoder_template.tex')
            
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, summary  = summary)

            fh = open("base64decoder.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "file_hashes":

            analysis_date = convert_date(element['analysis_date'])
            plugin_version = element['plugin_version']

            del element['analysis_date']
            del element['plugin_version']

            template = latex_jinja_env.get_template('templates/file_hashes_template.tex')
                                    
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, element = element)

            fh = open("filehashes.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "file_type":

            analysis_date = convert_date(element['analysis_date'])
            plugin_version = element['plugin_version']
            summary = element['summary']

            del element['analysis_date']
            del element['plugin_version']
            del element['summary']
            
            template = latex_jinja_env.get_template('templates/file_type_template.tex')
            
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, summary = summary, element = element)

            fh = open("filetype.tex", 'w')
            fh.write(texfile)
            fh.close
            
            pass

        elif cursor_analysis == "init_systems":

            analysis_date = convert_date(element['analysis_date'])
            plugin_version = element['plugin_version']
            summary = element['summary']

            template = latex_jinja_env.get_template('templates/init_systems_template.tex')
            
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, summary = summary)

            fh = open("initsystems.tex", 'w')
            fh.write(texfile)
            fh.close
            
            pass

        elif cursor_analysis == "ip_and_uri_finder":

            template = latex_jinja_env.get_template('templates/ip_and_uri_finder_template.tex')

            analysis_date = convert_date(element['analysis_date'])
            plugin_version = element['plugin_version']
            ips_v4 = element['ips_v4']
            ips_v6 = element['ips_v6']
            uris = element['uris']
            summary = element['summary']

            if len(ips_v4) == 0:
                ips_v4.append('List is empty.')
            if len(ips_v6) == 0:
                ips_v6.append('The List is empty.')
            if len(uris) == 0:
                uris.append('The List is empty.')
            
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, ips_v4 =  ips_v4, ips_v6 = ips_v6, uris = uris, summary = summary)

            fh = open("ipandurifinder.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "software_components":

            analysis_date = convert_date(element['analysis_date'])
            plugin_version = element['plugin_version']
            summary = element['summary']
            
            template = latex_jinja_env.get_template('templates/software_components_template.tex')
            
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, summary = summary)

            #texfile = filter(texfile)

            fh = open("softwarecomponents.tex", 'w' )
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "printable_strings":

            analysis_date = convert_date(element['analysis_date'])
            plugin_version = element['plugin_version']
            strings = element['strings']

            template = latex_jinja_env.get_template('templates/printable_strings_template.tex')
            
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, strings = strings)

            fh = open("printablestrings.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "users_and_passwords":

            analysis_date = convert_date(element['analysis_date'])
            plugin_version = element['plugin_version']
            summary = element['summary']

            template = latex_jinja_env.get_template('templates/users_and_passwords_template.tex')
            
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, summary = summary)

            #texfile = filter(texfile)

            fh = open("usersandpasswords.tex", 'w')
            fh.write(texfile)
            fh.close

            pass
        
        elif cursor_analysis == "string_evaluator":

            analysis_date = convert_date(element['analysis_date'])
            plugin_version = element['plugin_version']
            strings = element['string_eval']

            template = latex_jinja_env.get_template('templates/string_evaluator_template.tex')
            
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, strings = strings)

            #texfile = filter(texfile)

            fh = open("stringevaluator.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "unpacker":

            analysis_date = convert_date(element['analysis_date'])
            plugin_version = element['plugin_version']
            entropy =  element['entropy']
            entropy = round(entropy, 2)
            summary = element['summary']

            del element['analysis_date']
            del element['plugin_version']
            del element['entropy']
            del element['summary']

            template = latex_jinja_env.get_template('templates/unpacker_template.tex')
            
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, entropy = entropy, element = element, summary = summary)

            fh = open("unpacker.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "malware_scanner":

            analysis_date = convert_date(element['analysis_date'])
            plugin_version = element['plugin_version']
            scanners = element['scanners']
            scans = element['scans']
            summary = element['summary']

            del element['analysis_date']
            del element['plugin_version']
            del element['scanners']
            del element['scans']
            del element['summary']

            template = latex_jinja_env.get_template('templates/malware_scanner_template.tex')


            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, scanners = scanners, scans = scans, summary = summary, element = element)

            #texfile = filter(texfile)

            fh = open("malwarescanner.tex", 'w')
            fh.write(texfile)
            fh.close

    pass

erstelle_haupttex()
erstelle_input_meta_tex()
erstelle_analyse()
print("done")
