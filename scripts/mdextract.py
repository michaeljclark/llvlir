#!/usr/bin/env python3
#
# mdextract.py
#
# derived from extracttoc.py which is released under the MIT License
#
# Copyright (c) 2021 Cribber
# Copyright (c) 2022 Michael Clark
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import regex as re
import argparse
from os.path import exists
from typing import List, Tuple

def extract_table(lines: List[str], heading: str) -> List[str]:
    """
    Filters a list of lines to the header lines.
    Identifies headers of the 'leading-hashtag' type as well as
    headers of the 'subsequent-line' type by using regex.

    :param lines: List of header and text lines.
    :returns: List of header lines.
    """

    headers = []
    re_hashtag_headers = r"^#+\ .*$"
    re_alternative_header_lvl1 = r"^=+ *$"
    re_alternative_header_lvl2 = r"^-+ *$"

    current = '#xx'
    heading = '#%s' % heading

    for i, line in enumerate(lines):
        h = None

        # identify headers by leading hashtags
        if re.search(re_hashtag_headers, line):
            h = format_header(line)

        # identify alternative headers
        elif re.search(re_alternative_header_lvl1, line):
            h = format_header(lines[i - 1])
        elif re.search(re_alternative_header_lvl2, line):
            h = format_header(lines[i - 1])

        if h:
            current = h[2]

        if current == heading:
            print(line)

    return headers


def identify_headers(lines: List[str]) -> List[str]:
    """
    Filters a list of lines to the header lines.
    Identifies headers of the 'leading-hashtag' type as well as
    headers of the 'subsequent-line' type by using regex.

    :param lines: List of header and text lines.
    :returns: List of header lines.
    """

    headers = []
    re_hashtag_headers = r"^#+\ .*$"
    re_alternative_header_lvl1 = r"^=+ *$"
    re_alternative_header_lvl2 = r"^-+ *$"

    for i, line in enumerate(lines):
        # identify headers by leading hashtags
        if re.search(re_hashtag_headers, line):
            headers.append(line)

        # identify alternative headers
        elif re.search(re_alternative_header_lvl1, line):
            headers.append("# " + lines[i - 1])  # unified h1 format
        elif re.search(re_alternative_header_lvl2, line):
            headers.append("## " + lines[i - 1])  # unified h2 format

    return headers


def format_header(header: str) -> Tuple[str, int, str]:
    """Calculates the level of the header, removes leading and trailing whitespaces and creates the markdown-link.

    :param header: header line from the markdown file
    :return: a tuple consisting of the cleaned header, the header level and the formatted markdown link.
    """

    # determine the level of the header
    level = 0
    while header[0] == "#":
        level += 1
        header = header[1:]

    # create clickable link by allowing only certain characters,
    # by replacing whitespaces with hyphens and by removing colons
    headerlink = "#" + re.sub(r"[^a-zA-Z0-9 -]", "", header).lower().strip().replace(
        " ", "-"
    ).replace("--", "-")
    return (header.strip(), level, headerlink)


def remove_code_blocks(content: List[str]) -> List[str]:
    """Removes lines starting with "```" (=code blocks) from the markdown file.

    Since code blocks can contain lines with leading hashtags
    (e.g. comments in python) they need to be removed before looking for headers.

    :param content: file contents as a list of strings
    :return: Cleaned file contents as a list of strings
    """
    content_cleaned = []
    code_block = False

    for x in content:
        if x[:3] == "```":
            code_block = not code_block
        elif not code_block:
            content_cleaned.append(x)

    return content_cleaned


def create_toc(toc_levels: List[Tuple[str, int, str]], level_limit: int) -> List[str]:
    """Creates a list of strings representing the items in the table of content.

    :param toc_levels:  A list of Tuples consisting of the header,
                                        the level of the header and a formatted markdown-link to the header.
                        Example for toc_levels:

                                [
                                        ('First Header', 1, '#First-Header')
                                        ('Second level', 2, '#Second-level')
                                        ('First level again', 1, '#First-level-again')
                                ]
    :param level_limit: Limit to the number of levels included in the TOC
    :return: Ordered line items of the table of contents.

    """

    toc = ["# Table of Contents"]
    # create a dict to store the header numbering for each level
    max_header_level = max([x[1] for x in toc_levels]) + 1
    headerlevels = dict.fromkeys(range(1, max_header_level), 1)
    previous_level = 1
    for i, (h, level, link) in enumerate(toc_levels):

        # reset lower header-levels if current header level is higher than prev
        if previous_level > level:
            for x in range(level + 1, previous_level + 1):
                headerlevels[x] = 1

        # construct TOC element
        if level <= level_limit:
            toc.append(
                "\t" * (level - 1) + f"{headerlevels[level]}. [" + h + f"]({link})"
            )

        # increment matching header level
        headerlevels[level] = headerlevels[level] + 1
        previous_level = level
    return toc


def main():

    parser = argparse.ArgumentParser(
        prog="extracttoc",
        description="Extracts the table of contents from a markdown file.",
    )

    # an argument that results in a list of strings with one element ('file')
    parser.add_argument(
        "file",
        nargs=1,
        help="Provide a markdown file from which to extract the toc.",
        type=str,
    )

    # an argument whose passed value is stored in an integer variable ('limit')
    parser.add_argument(
        "-l",
        "--levels",
        dest="limit",
        default=3,
        type=int,
        help="Set the number of levels which will be included in the TOC.",
    )

    # an argument that results in a string variable ('extract_table')
    parser.add_argument(
        "-t",
        "--table",
        action="store",
        dest="table",
        help="Extract table",
    )

    args = parser.parse_args()

    # read file
    file_name = args.file[0]

    if not exists(file_name):
        raise ValueError(f"File {file_name} could not be found.")

    with open(file_name, "r", encoding="utf-8") as f:
        content = f.read().split("\n")

    content_cleaned = remove_code_blocks(content)

    headers = identify_headers(content_cleaned)

    toc_levels = [format_header(h) for h in headers]

    toc = create_toc(toc_levels, args.limit)

    if args.table:
        table = extract_table(content_cleaned, args.table)
        for i in table:
            print(i)
    else:
        # Output options
        for line in toc:
            print(line)

main()
