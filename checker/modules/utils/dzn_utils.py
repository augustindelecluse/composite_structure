import re


def read_dzn_array(dzn_array: str, parse_fun: callable, element_regex: str) -> list:
    """

    :param dzn_array:
    :param parse_fun:
    :param element_regex:
    :return:
    """
    string_elements = re.findall(element_regex, dzn_array)
    return [parse_fun(element) for element in string_elements]


def read_dzn(path) -> dict:
    """

    :param path:
    :return:
    """
    dzn_string = ""
    with open(path, "r") as file:
        for line in file:
            if not line.startswith("%"):
                dzn_string += line.strip()

    dzn_string = dzn_string.replace(" ", "")
    dzn_elements = dzn_string.split(";")

    dzn_dict = {}
    for element in dzn_elements:
        if element:
            key, value = element.split("=", 1)
            dzn_dict[key.strip()] = value.strip()

    return dzn_dict


def dzn_idx(idx):
    return idx + 1 if idx is not None else None
