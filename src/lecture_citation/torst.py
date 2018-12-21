# -*- coding: utf-8 -*-
"""
@file
@brief Converts quotes into :epkg:`rst`.
"""
import textwrap


def to_rst(quote):
    """
    Converts a quote defined as a dictionary
    into :epkg:`rst`.

    @param      quote           dictionary
    @return                     text file
    """
    rows = [".. quote::"]
    for k, v in quote.items():
        if k != 'content':
            rows.append("    :{0}: {1}".format(k, v))
    if 'content' not in quote:
        raise KeyError("Unable to kind key 'content'.")

    content = quote['content'].replace("\n\n", '#LINE#').replace('\n', ' ')
    content = content.replace('\r', '').replace('\t', ' ')
    content = ' '.join(content.split()).strip()
    text = "\n".join(textwrap.wrap(content, 60))
    text = text.replace("`", "").replace("\\textit", "")
    text = text.replace('{', '*').replace('}', '*')
    text = text.replace('#LINE#', '\n\n').strip("\n")
    text = textwrap.indent(text, '    ')
    text = text.replace("    - ", "    — ")
    rows.append('')
    rows.append(text)
    rows.append('')
    return "\n".join(rows)
