from common_helper_files import human_readable_file_size
from time import localtime, strftime, struct_time
from base64 import decodebytes

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

def nice_number_filter(i):
    if isinstance(i, int):
        return '{:,}'.format(i)
    elif isinstance(i, float):
        return '{:,.2f}'.format(i)
    elif i is None:
        return 'not available'
    else:
        return i

def filter_latex_special_chars(input):
    if "$" in input:
        input = input.replace("$", "\$")
    if "#" in input:
        input = input.replace("#", "\#")
    if "%" in input:
        input = input.replace("%", "\%")
    if "&" in input:
        input = input.replace("&", "\&")
    if "_" in input:
        input = input.replace("_", "\_")
    if "{" in input:
        input = input.replace("{", "\{")
    if "}" in input:
        input = input.replace("}", "\}")
    if "^" in input:
        input = input.replace("^", "\\textasciicircum{}")
    if "~" in input:
        input = input.replace("~", "\\textasciitilde{}")
    if ">" in input:
        input = input.replace(">", "\\textgreater{}")
    if "<" in input:
        input = input.replace("<", "\\textless{}")
    return input

def count_elements_in_list(list):
    return len(list)

def convert_base64_to_png_filter(s):
    base64_encoded = s.encode('utf-8')
    file_name = "entropy_analysis_graph.png"
    with open(file_name, "wb") as fh:
        fh.write(decodebytes(base64_encoded))

    return file_name

def check_if_list_empty(list):
    if list:
        return list
    else:
        empty_list = []
        empty_list.append('list is empty')
        return empty_list

'''
def filter(texfile):
    if "&" in texfile:
        texfile = texfile.replace("&", "\&")

    if "\r" in texfile:
        texfile = texfile.replace("\r", "\\\r")

    if "^" in texfile:
        texfile = texfile.replace("^", "\string^")

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
'''