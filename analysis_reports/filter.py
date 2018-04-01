from common_helper_files import human_readable_file_size
from time import localtime, strftime
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


def filter_latex_special_chars(data):
    if "$" in data:
        data = data.replace("$", "\$")
    if "#" in data:
        data = data.replace("#", "\#")
    if "%" in data:
        data = data.replace("%", "\%")
    if "&" in data:
        data = data.replace("&", "\&")
    if "_" in data:
        data = data.replace("_", "\_")
    if "{" in data:
        data = data.replace("{", "\{")
    if "}" in data:
        data = data.replace("}", "\}")
    if "^" in data:
        data = data.replace("^", "\\textasciicircum{}")
    if "~" in data:
        data = data.replace("~", "\\textasciitilde{}")
    if ">" in data:
        data = data.replace(">", "\\textgreater{}")
    if "<" in data:
        data = data.replace("<", "\\textless{}")
    return data


def count_elements_in_list(ls):
    return len(ls)


def convert_base64_to_png_filter(s, filename):
    base64_encoded = s.encode('utf-8')
    png_filename = filename + ".png"
    with open(png_filename, "wb") as fh:
        fh.write(decodebytes(base64_encoded))

    return png_filename


def check_if_list_empty(ls):
    if ls:
        return ls
    else:
        empty_ls = ['list is empty']
        return empty_ls


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