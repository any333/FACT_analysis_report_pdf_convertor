import json
import requests
import jinja2
import os
import sys
from filter import byte_number_filter, nice_unix_time, nice_number_filter, filter_latex_special_chars, count_elements_in_list, convert_base64_to_png_filter, check_if_list_empty

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
latex_jinja_env.filters['base64_to_png'] = convert_base64_to_png_filter
latex_jinja_env.filters['check_list'] = check_if_list_empty

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

    for processed_analysis in analysis:

        selected_analysis = analysis[processed_analysis]

        if processed_analysis == "base64_decoder":

            template = latex_jinja_env.get_template('templates/base64_decoder_template.tex')

            texfile = template.render(selected_analysis=selected_analysis)

            fh = open("base64decoder.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif processed_analysis == "binwalk":

            template = latex_jinja_env.get_template('templates/binwalk_template.tex')

            texfile = template.render(selected_analysis = selected_analysis)

            fh = open("binwalk.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif processed_analysis == "cpu_architecture":

            template = latex_jinja_env.get_template('templates/cpu_architecture_template.tex')

            texfile = template.render(selected_analysis=selected_analysis)

            fh = open("cpuarchitecture.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif processed_analysis == "crypto_material":

            template = latex_jinja_env.get_template('templates/crypto_material_template.tex')

            texfile = template.render(selected_analysis=selected_analysis)

            fh = open("crypto_material.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif processed_analysis == "exploit_mitigations":

            template = latex_jinja_env.get_template('templates/exploit_mitigations_template.tex')

            texfile = template.render(selected_analysis = selected_analysis)

            fh = open("exploitmitigations.tex", 'w')
            fh.write(texfile)
            fh.close
            
            pass

        elif processed_analysis == "file_hashes":

            template = latex_jinja_env.get_template('templates/file_hashes_template.tex')
                                    
            texfile = template.render(selected_analysis = selected_analysis)

            fh = open("filehashes.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif processed_analysis == "file_type":
            
            template = latex_jinja_env.get_template('templates/file_type_template.tex')
            
            texfile = template.render(selected_analysis = selected_analysis)

            fh = open("filetype.tex", 'w')
            fh.write(texfile)
            fh.close
            
            pass

        elif processed_analysis == "init_systems":

            template = latex_jinja_env.get_template('templates/init_systems_template.tex')
            
            texfile = template.render(selected_analysis = selected_analysis)

            fh = open("initsystems.tex", 'w')
            fh.write(texfile)
            fh.close
            
            pass

        elif processed_analysis == "ip_and_uri_finder":

            template = latex_jinja_env.get_template('templates/ip_and_uri_finder_template.tex')

            texfile = template.render(selected_analysis = selected_analysis)

            fh = open("ipandurifinder.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif processed_analysis == "malware_scanner":

            template = latex_jinja_env.get_template('templates/malware_scanner_template.tex')

            texfile = template.render(selected_analysis=selected_analysis)

            fh = open("malwarescanner.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif processed_analysis == "printable_strings":
            '''
            strings = element['strings']
            filtered_strings = []
            for string in strings:
                new_string = filter(string)
                filtered_strings.append(new_string)
            '''

            template = latex_jinja_env.get_template('templates/printable_strings_template.tex')

            texfile = template.render(selected_analysis=selected_analysis)

            fh = open("printablestrings.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif processed_analysis == "software_components":
            
            template = latex_jinja_env.get_template('templates/software_components_template.tex')
            
            texfile = template.render(selected_analysis = selected_analysis)

            fh = open("softwarecomponents.tex", 'w' )
            fh.write(texfile)
            fh.close

            pass

        elif processed_analysis == "string_evaluator":

            template = latex_jinja_env.get_template('templates/string_evaluator_template.tex')

            texfile = template.render(selected_analysis=selected_analysis)

            fh = open("stringevaluator.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif processed_analysis == "unpacker":

            template = latex_jinja_env.get_template('templates/unpacker_template.tex')

            texfile = template.render(selected_analysis=selected_analysis)

            fh = open("unpacker.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif processed_analysis == "users_and_passwords":

            template = latex_jinja_env.get_template('templates/users_and_passwords_template.tex')
            
            texfile = template.render(selected_analysis = selected_analysis)

            fh = open("usersandpasswords.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

    pass

create_main_tex()
create_meta_tex()
create_analysis_texs()
print("all .tex files successfully created")