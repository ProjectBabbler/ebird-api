import json


def save(fp, values, indent):
    """Save the JSON data to a file or stdout.

    :param fp: the writer.
    :param values: the python data to be saved.
    :param indent: the level of indentation when prettyprinting the output.

    """
    fp.write(json.dumps(values, indent=indent).encode('utf-8'))
    if fp.name == '<stdout>':
        fp.write(b'\n')
