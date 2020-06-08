"""
@file
@brief Extracts old quote from tex files.
"""
import re


class FormatException(Exception):
    """
    Raised when not able to interpret a line.
    """
    pass


def enumerate_quotes(filename, encoding="utf-8", empty_name="Inconnu"):
    """
    Enumerates quote from a filename or a stream

    @param      filename        filename or stream
    @param      encoding        applicable only if filename
    @param      empty_name      replces an empty author name
    @return                     enumerate on quote

    A quote is defined a dictionary.
    """
    if isinstance(filename, str):
        with open(filename, "r", encoding=encoding) as f:
            for q in enumerate_quotes(f):
                yield q
    else:
        re1 = re.compile("chapter[{]([0-9]+)[}]")
        re2 = re.compile(
            "[\\]begin[{]xcitt?[}][{](.*?)[}][{](.*?)[}][{](.*?)[}][{](.+?)[}]")
        re3 = re.compile(
            "[\\]begin[{]xcita[}][{](.*?)[}][{](.*?)[}][{](.+?)[}][{](.*?)[}][{](.*?)[}][{](.+?)[}]")
        re4 = re.compile(
            "[\\]begin[{]xcitenfant[}][{](.*?)[}][{](.*?)[}][{](.*?)[}][{](.+?)[}]")
        re5 = re.compile(
            "[\\]begin[{]xcitw[}][{](.*?)[}][{](.*?)[}][{](.*?)[}][{](.+?)[}][{](.+?)[}]")
        re6 = re.compile(
            "[\\]begin[{]xcita3[}][{](.*?)[}][{](.*?)[}][{](.+?)[}][{](.*?)[}][{](.+?)[}][{](.*?)[}][{](.*?)[}][{](.+?)[}]")

        def process_content(il, content):
            find = re2.search(content[0])
            if find:
                author, name, book, index = find.groups()
                obs = dict(author="{0} {1}".format(name, author),
                           book=book, index=index, year=year)
            else:
                find = re3.search(content[0])
                if find:
                    author1, name1, author2, name2, book, index = find.groups()
                    obs = dict(author="{0} {1}, {2} {3}".format(name1, author1, name2, author2),
                               book=book, index=index, year=year)
                else:
                    find = re4.search(content[0])
                    if find:
                        author, name, book, index = find.groups()
                        obs = dict(author="{0} {1}".format(name, author),
                                   book=book, index=index, year=year,
                                   tag="enfant")
                    else:
                        find = re5.search(content[0])
                        if find:
                            author, name, book, index, date = find.groups()
                            obs = dict(author="{0} {1}".format(name, author),
                                       book=book, index=index, year=year,
                                       date=date)
                        else:
                            find = re6.search(content[0])
                            if find:
                                author, name, a2, n2, a3, n3, book, index = find.groups()
                                obs = dict(author="{} {}, {} {}, {} {}".format(name, author, n2, a2, n3, a3),
                                           book=book, index=index, year=year)
                            else:
                                raise FormatException(  # pragma: no cover
                                    "Unable to interpret line {0}: '{1}'".format(il, content[0]))

            content = "\n".join(content[1:-1])
            content = content.replace("~", " ")
            content = content.replace("\\quad", "...")
            obs["content"] = content
            if not obs["author"]:
                obs["author"] = empty_name
            return obs

        year = None
        content = []
        for il, line in enumerate(filename):
            sline = line.strip()
            if sline.startswith("\\chapter{"):
                chap = re1.search(sline)
                if chap:
                    year = chap.groups()[0]
                else:
                    raise FormatException(  # pragma: no cover
                        "Unable to process line {0}: '{1}'".format(il, sline))
            else:
                if sline.startswith("\\begin{xcit"):
                    content.append(sline)
                elif sline.startswith("\\end{xcit"):
                    content.append(sline)
                    yield process_content(il, content)
                    content.clear()
                else:
                    if content:
                        content.append(sline)
                    else:
                        # between quotes
                        pass
