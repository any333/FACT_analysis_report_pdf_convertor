import json
import requests
import jinja2
import os
import sys
import argparse
from filter import byte_number_filter, nice_unix_time, nice_number_filter, filter_latex_special_chars, \
    count_elements_in_list, convert_base64_to_png_filter, check_if_list_empty, split_hash


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
    latex_jinja_env.filters['split_hash'] = split_hash


def _make_get_requests(url):
    response = requests.get(url)
    response_data = response.text
    response_dict = json.loads(response_data)

    return response_dict


def create_main_tex(meta_data):
    template = latex_jinja_env.get_template('templates/main_template.tex')

    main_tex_file = template.render(meta_data=meta_data)
    main_tex_file_name = meta_data['device_name']+"_Analysis_Report.tex"
    main_tex_file_name = main_tex_file_name.replace(" ", "_")
    main_tex_file_name = main_tex_file_name.replace("/", "__")

    fh = open(main_tex_file_name, 'w')
    fh.write(main_tex_file)
    fh.close()

    pass


def create_meta_tex(meta_data):
    template = latex_jinja_env.get_template('templates/meta_data_template.tex')

    meta_tex_file = template.render(meta_data=meta_data)

    fh = open("meta.tex", 'w')
    fh.write(meta_tex_file)
    fh.close()

    pass


def create_analysis_texs(analysis):
    for processed_analysis in analysis:

        selected_analysis = analysis[processed_analysis]

        if os.path.isfile('templates/' + processed_analysis + '_template.tex'):
            del selected_analysis['summary']

            template = latex_jinja_env.get_template('templates/' + processed_analysis + '_template.tex')

            analysis_tex_file = template.render(selected_analysis=selected_analysis)

            processed_texfile = processed_analysis + ".tex"
            fh = open(processed_texfile, 'w')
            fh.write(analysis_tex_file)
            fh.close()

            pass


def create_analysis_texs_with_summary(analysis):
    for processed_analysis in analysis:

        selected_analysis = analysis[processed_analysis]

        if os.path.isfile('templates/' + processed_analysis + '_template.tex'):

            template = latex_jinja_env.get_template('templates/' + processed_analysis + '_template.tex')

            analysis_tex_file = template.render(selected_analysis=selected_analysis)

            processed_texfile = processed_analysis + ".tex"
            fh = open(processed_texfile, 'w')
            fh.write(analysis_tex_file)
            fh.close()

            pass


def delete_generated_files():
    dir = "./"
    dir_content = os.listdir(dir)

    for file in dir_content:
        if file.endswith(".tex"):
            os.remove(os.path.join(dir, file))
        elif file.endswith(".log"):
            os.remove(os.path.join(dir, file))
        elif file.endswith(".aux"):
            os.remove(os.path.join(dir, file))

    os.remove(os.path.join(dir, "entropy_analysis_graph.png"))


def create_pdf_report(meta_data):
    main_tex_file_name = meta_data['device_name'] + "_Analysis_Report.tex"
    main_tex_file_name = main_tex_file_name.replace(" ", "_")
    main_tex_file_name = main_tex_file_name.replace("/", "__")
    os.system("env buf_size=1000000 pdflatex " + main_tex_file_name)


def main():
    HOST = "http://localhost:5000"
    PATH = "/rest/firmware/"

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", dest="summary", action="store_false")
    parser.add_argument("-uid", dest="uid")

    args = parser.parse_args()

    if args.summary:

        FIRMWARE_UID = args.uid
        GET_URL = HOST + PATH + FIRMWARE_UID

        firmware_data = _make_get_requests(GET_URL)
        meta_data = firmware_data['firmware']['meta_data']
        analysis = firmware_data['firmware']['analysis']

        setup_jinja_filters()
        create_main_tex(meta_data)
        create_meta_tex(meta_data)
        create_analysis_texs(analysis)
        create_pdf_report(meta_data)
        delete_generated_files()
        print("Analysis report generated successfully.")
    else:

        FIRMWARE_UID = args.uid
        GET_URL = HOST + PATH + FIRMWARE_UID

        firmware_data = _make_get_requests(GET_URL)
        meta_data = firmware_data['firmware']['meta_data']
        analysis = firmware_data['firmware']['analysis']

        setup_jinja_filters()
        create_main_tex(meta_data)
        create_meta_tex(meta_data)
        create_analysis_texs_with_summary(analysis)
        create_pdf_report(meta_data)
        delete_generated_files()
        print("Analysis report generated successfully.")


if __name__ == "__main__":
    main()
