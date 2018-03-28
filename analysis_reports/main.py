import json
import requests
import jinja2
import os
import sys
from jinja2 import Template
from common_helper_files import human_readable_file_size
from time import localtime, strftime, struct_time

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

def byte_number_filter(i, verbose=True):
    if isinstance(i, int) or isinstance(i, float):
        if verbose:
            return '{} ({})'.format(human_readable_file_size(i), format(i, ',d') + ' bytes')
        else:
            return human_readable_file_size(i)
    else:
        return 'not available'

def nice_unix_time(unix_time_stamp):
    '''
    input unix_time_stamp
    output string 'YYYY-MM-DD HH:MM:SS'
    '''
    if isinstance(unix_time_stamp, float) or isinstance(unix_time_stamp, int):
        tmp = localtime(unix_time_stamp)
        return strftime('%Y-%m-%d %H:%M:%S', tmp)
    else:
        return unix_time_stamp

def comment_out_regex_meta_chars(input_data):
    '''
    comments out chars used by regular expressions in the input string
    '''
    meta_chars = ['^', '$', '.', '[', ']',
                  '|', '(', ')', '?', '*', '+', '{', '}']
    for c in meta_chars:
        if c in input_data:
            input_data = input_data.replace(c, '\\{}'.format(c))
    return input_data


def create_main_tex():
    
    template = latex_jinja_env.get_template('templates/main_template.tex')
    #print(template.render(analysis=analysis))
    maintexfile = template.render(meta_data = meta_data)
    #filehandler
    fh = open("main.tex", 'w')
    fh.write(maintexfile)
    fh.close
    pass

def create_meta_tex():

    size = byte_number_filter(meta_data['size'])

    template = latex_jinja_env.get_template('templates/meta_data_template.tex')
    
    #print(template.render(meta_copy = meta_copy))
    maintexfile = template.render(meta_data = meta_data, size = size)
    
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


def create_analysis_texs():

    for cursor_analysis in analysis:

        element = analysis[cursor_analysis]

        if cursor_analysis == "exploit_mitigations":

            analysis_date = nice_unix_time(element['analysis_date'])
            plugin_version = element['plugin_version']
            summary = element['summary']

            template = latex_jinja_env.get_template('templates/exploit_mitigations_template.tex')

            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, summary = summary)

            fh = open("exploitmitigations.tex", 'w')
            fh.write(texfile)
            fh.close
            
            pass

        elif cursor_analysis == "crypto_material":

            analysis_date = nice_unix_time(element['analysis_date'])
            plugin_version = element['plugin_version']
            summary = element['summary']

            template = latex_jinja_env.get_template('templates/crypto_material_template.tex')
            
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, summary = summary)

            fh = open("cryptomaterial.tex", 'w')
            fh.write(texfile)
            fh.close

            pass
        elif cursor_analysis == "cpu_architecture":

            analysis_date = nice_unix_time(element['analysis_date'])
            plugin_version = element['plugin_version']
            summary = element['summary']

            template = latex_jinja_env.get_template('templates/cpu_architecture_template.tex')
            
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, summary = summary)

            fh = open("cpuarchitecture.tex", 'w')
            fh.write(texfile)
            fh.close

            pass 

        elif cursor_analysis == "base64_decoder":

            analysis_date = nice_unix_time(element['analysis_date'])
            plugin_version = element['plugin_version']
            summary = element['summary']

            template = latex_jinja_env.get_template('templates/base64_decoder_template.tex')
            
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, summary  = summary)

            fh = open("base64decoder.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "file_hashes":

            analysis_date = nice_unix_time(element['analysis_date'])
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

            analysis_date = nice_unix_time(element['analysis_date'])
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

            analysis_date = nice_unix_time(element['analysis_date'])
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

            analysis_date = nice_unix_time(element['analysis_date'])
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

            analysis_date = nice_unix_time(element['analysis_date'])
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

            analysis_date = nice_unix_time(element['analysis_date'])
            plugin_version = element['plugin_version']
            strings = element['strings']
            filtered_strings = []
            for string in strings:
                new_string = comment_out_regex_meta_chars(string)
                filtered_strings.append(new_string)


            template = latex_jinja_env.get_template('templates/printable_strings_template.tex')
            
            texfile = template.render(analysis_date = analysis_date, plugin_version = plugin_version, strings = filtered_strings)

            fh = open("printablestrings.tex", 'w')
            fh.write(texfile)
            fh.close

            pass

        elif cursor_analysis == "users_and_passwords":

            analysis_date = nice_unix_time(element['analysis_date'])
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

            analysis_date = nice_unix_time(element['analysis_date'])
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

            analysis_date = nice_unix_time(element['analysis_date'])
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

            analysis_date = nice_unix_time(element['analysis_date'])
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

create_main_tex()
create_meta_tex()
create_analysis_texs()
print("All .tex Files successfully created.")
