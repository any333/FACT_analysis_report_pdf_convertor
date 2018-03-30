import json
import requests
import jinja2
import os
import sys
from filter import byte_number_filter, nice_unix_time, nice_number_filter, filter_latex_special_chars, count_elements_in_list

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
)

latex_jinja_env.filters['number_format'] = byte_number_filter
latex_jinja_env.filters['nice_unix_time'] = nice_unix_time
latex_jinja_env.filters['nice_number'] = nice_number_filter
latex_jinja_env.filters['filter_chars'] = filter_latex_special_chars
latex_jinja_env.filters['elements_count'] = count_elements_in_list

HOST = "http://localhost:5000"
PATH =  "/rest/firmware/"
FIRMWARE_UID = sys.argv[1]
GET_URL = HOST+PATH+FIRMWARE_UID
print(GET_URL)

#curl 'http://localhost:5000/rest/firmware/e692eca8505b0f4a3572d4d42940c6d5706b8aabec6ad1914bd4d733be9dfecf_25221120' -X GET

def _make_get_requests(url):
    response = requests.get(url)
    response_data=response.text
    response_dict=json.loads(response_data)
    return response_dict

firmware_data =_make_get_requests(GET_URL)
meta_data = firmware_data['firmware']['meta_data']
analysis = firmware_data['firmware']['analysis']


def create_main_tex():
    
    template = latex_jinja_env.get_template('templates/main_template.tex')

    maintexfile = template.render(meta_data = meta_data)
    #filehandler
    fh = open("main.tex", 'w')
    fh.write(maintexfile)
    fh.close

    pass

def create_meta_tex():

    template = latex_jinja_env.get_template('templates/meta_data_template.tex')

    maintexfile = template.render(meta_data = meta_data)
    
    fh = open("meta.tex", 'w')
    fh.write(maintexfile)
    fh.close

    pass

def create_analysis_texs():

    for cursor_analysis in analysis:

        element = analysis[cursor_analysis]

        if cursor_analysis == "exploit_mitigations":

            template = latex_jinja_env.get_template('templates/exploit_mitigations_template.tex')

            texfile = template.render(element = element)

            fh = open("exploitmitigations.tex", 'w')
            fh.write(texfile)
            fh.close
            
            pass

        elif cursor_analysis == "crypto_material":

            template = latex_jinja_env.get_template('templates/crypto_material_template.tex')
            
            texfile = template.render(element = element)

            fh = open("cryptomaterial.tex", 'w')
            fh.write(texfile)
            fh.close

            pass
        elif cursor_analysis == "cpu_architecture":

            template = latex_jinja_env.get_template('templates/cpu_architecture_template.tex')
            
            texfile = template.render(element = element)

            fh = open("cpuarchitecture.tex", 'w')
            fh.write(texfile)
            fh.close

            pass 

        elif cursor_analysis == "base64_decoder":

            template = latex_jinja_env.get_template('templates/base64_decoder_template.tex')
            
            texfile = template.render(element = element)

            fh = open("base64decoder.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "file_hashes":

            template = latex_jinja_env.get_template('templates/file_hashes_template.tex')
                                    
            texfile = template.render(element = element)

            fh = open("filehashes.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "file_type":
            
            template = latex_jinja_env.get_template('templates/file_type_template.tex')
            
            texfile = template.render(element = element)

            fh = open("filetype.tex", 'w')
            fh.write(texfile)
            fh.close
            
            pass

        elif cursor_analysis == "init_systems":

            template = latex_jinja_env.get_template('templates/init_systems_template.tex')
            
            texfile = template.render(element = element)

            fh = open("initsystems.tex", 'w')
            fh.write(texfile)
            fh.close
            
            pass

        elif cursor_analysis == "ip_and_uri_finder":

            ips_v4 = element['ips_v4']
            ips_v6 = element['ips_v6']
            uris = element['uris']

            if len(ips_v4) == 0:
                ips_v4.append('list is empty')
            if len(ips_v6) == 0:
                ips_v6.append('list is empty')
            if len(uris) == 0:
                uris.append('list is empty')

            template = latex_jinja_env.get_template('templates/ip_and_uri_finder_template.tex')

            texfile = template.render(element = element, ips_v4 =  ips_v4, ips_v6 = ips_v6, uris = uris)

            fh = open("ipandurifinder.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "software_components":
            
            template = latex_jinja_env.get_template('templates/software_components_template.tex')
            
            texfile = template.render(element = element)

            fh = open("softwarecomponents.tex", 'w' )
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "printable_strings":
            '''
            strings = element['strings']
            filtered_strings = []
            for string in strings:
                new_string = filter(string)
                filtered_strings.append(new_string)
            '''

            template = latex_jinja_env.get_template('templates/printable_strings_template.tex')
            
            texfile = template.render(element = element)

            fh = open("printablestrings.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "users_and_passwords":

            template = latex_jinja_env.get_template('templates/users_and_passwords_template.tex')
            
            texfile = template.render(element = element)

            fh = open("usersandpasswords.tex", 'w')
            fh.write(texfile)
            fh.close

            pass
        
        elif cursor_analysis == "string_evaluator":

            template = latex_jinja_env.get_template('templates/string_evaluator_template.tex')
            
            texfile = template.render(element = element)

            fh = open("stringevaluator.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "unpacker":

            template = latex_jinja_env.get_template('templates/unpacker_template.tex')
            
            texfile = template.render(element = element)

            fh = open("unpacker.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "malware_scanner":

            template = latex_jinja_env.get_template('templates/malware_scanner_template.tex')

            texfile = template.render(element = element)

            fh = open("malwarescanner.tex", 'w')
            fh.write(texfile)
            fh.close

    pass

create_main_tex()
create_meta_tex()
create_analysis_texs()
print("All .tex Files successfully created.")