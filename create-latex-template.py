from string import Template
def ask_for(param: str, type_of_param: type):
    if type_of_param == str:
        return input("Key in '%s': " % (param))
    elif type_of_param == bool:
        input_string = input("'%s'? (y,n): " % (param)).strip()
        return input_string.strip() in ('y', 'Y', 'yes', 'Yes', 'YES')
    else:
        raise Exception("'%s' is not supported as a type parameter" % (str(type_of_param)))


title = ask_for("title", str)
author = ask_for("author", str)
include_pl_lang_support = ask_for("include_pl_lang_support", bool)
include_amsmath = ask_for("include_amsmath", bool)
include_inkscape = ask_for("include https://github.com/gillescastel/inkscape-figures support", bool)
include_title_page = ask_for("include_title_page", bool)
include_toc = ask_for("include_toc", bool)

substitution_map = {}

# title and author
substitution_map["title"] = title
substitution_map["author"] = author

# polish language support
pl = r"""\usepackage[polish]{babel}
\usepackage{polski} """
substitution_map["pl"] = pl if include_pl_lang_support else ""

# amsmath
amsmath = r"\usepackage{amsmath}"
substitution_map["amsmath"] = amsmath if include_amsmath else ""

# inkscape
inkscape = r"""\usepackage{import}
% Don't forget to run 'inkscape_figures watch' in cli in the same directory where your *.latex file resides
\usepackage{pdfpages}
\usepackage{transparent}
\usepackage{xcolor}

\newcommand{\incfig}[2][1]{%
    \def\svgwidth{#1\columnwidth}
    \import{./figures/}{#2.pdf_tex}
}

\pdfsuppresswarningpagegroup=1""" if include_inkscape else ""
substitution_map["inkscape"] = inkscape

# title page
title_page = r"""\begin{titlepage}
    \maketitle
\end{titlepage}""" if include_title_page else ""
substitution_map["title_page"] = title_page

# table of contents
toc = "\\tableofcontents\n\\newpage" if include_toc else ""
substitution_map["toc"] = toc

template = Template(r"""\documentclass{article}
\usepackage[utf8]{inputenc}
$pl
$amsmath
$inkscape

\title{$title}
\author{$author}

\begin{document}
$title_page
$toc



\end{document}
""").substitute(substitution_map)

print("\n\nBe aware that this will overwrite the file")
print("If you want to exit click CTRL+C")
file_name = ask_for("file_name", str)
with open(file_name, "w") as file:
    file.write(template)
