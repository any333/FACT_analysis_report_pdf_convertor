import json
import requests
import jinja2
import os
import sys
from filter import byte_number_filter, nice_unix_time, nice_number_filter, filter_latex_special_chars, \
    count_elements_in_list, convert_base64_to_png_filter, check_if_list_empty

HOST = "http://localhost:5000"
PATH = "/rest/firmware/"
FIRMWARE_UID = sys.argv[1]
GET_URL = HOST + PATH + FIRMWARE_UID

latex_jinja_env = jinja2.Environment(
    block_start_string='\BLOCK{',
    block_end_string='}',
    variable_start_string='\VAR{',
    variable_end_string='}',
    comment_start_string='\#{',
    comment_end_string='}',
    line_statement_prefix='%%',
    line_comment_prefix='%#',
    trim_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.abspath('.'))
)

def setup_jinja_filters():
    latex_jinja_env.filters['number_format'] = byte_number_filter
    latex_jinja_env.filters['nice_unix_time'] = nice_unix_time
    latex_jinja_env.filters['nice_number'] = nice_number_filter
    latex_jinja_env.filters['filter_chars'] = filter_latex_special_chars
    latex_jinja_env.filters['elements_count'] = count_elements_in_list
    latex_jinja_env.filters['base64_to_png'] = convert_base64_to_png_filter
    latex_jinja_env.filters['check_list'] = check_if_list_empty

def _make_get_requests(URL):
    response = requests.get(URL)
    response_data = response.text
    response_dict = json.loads(response_data)
    return response_dict

firmware_data =_make_get_requests(GET_URL)
meta_data = firmware_data['firmware']['meta_data']
analysis = firmware_data['firmware']['analysis']

def create_main_tex():
    template = latex_jinja_env.get_template('templates/main_template.tex')

    maintexfile = template.render(meta_data=meta_data)

    fh = open("firmware_analysis_report.tex", 'w')
    fh.write(maintexfile)
    fh.close

    pass

def create_meta_tex():
    template = latex_jinja_env.get_template('templates/meta_data_template.tex')

    maintexfile = template.render(meta_data=meta_data)

    fh = open("meta.tex", 'w')
    fh.write(maintexfile)
    fh.close

    pass

def create_analysis_texs():
    for processed_analysis in analysis:

        selected_analysis = analysis[processed_analysis]

        template = latex_jinja_env.get_template('templates/' + processed_analysis + '_template.tex')

        texfile = template.render(selected_analysis=selected_analysis)

        processed_texfile = processed_analysis + ".tex"
        fh = open(processed_texfile, 'w')
        fh.write(texfile)
        fh.close

        pass

setup_jinja_filters()
create_main_tex()
create_meta_tex()
create_analysis_texs()
print("all .tex files successfully created")