# -*- coding: utf-8 -*-
import sys
import os
import alabaster
from pyquickhelper.helpgen.default_conf import set_sphinx_variables
import lecture_citation

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))
local_template = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "phdoc_templates")

set_sphinx_variables(__file__, "lecture_citation", "Xavier Dupré", 2022,
                     "alabaster", alabaster.get_path(),
                     locals(), extlinks=dict(
                         issue=('https://github.com/sdpython/lecture_citation/issues/%s', 'issue')),
                     title="Souvenirs de lecture", book=True, nblayout='table')

blog_root = "http://www.xavierdupre.fr/app/lecture_citation/helpsphinx/"
html_search_language = "fr"
pygments_style = 'sphinx'
html_css_files = ['my-styles.css']
html_logo = "phdoc_static/project_ico.png"
language = "fr"
mathdef_link_only = True

epkg_dictionary.update({
    'ALENA': 'https://fr.wikipedia.org/wiki/Accord_de_libre-%C3%A9change_nord-am%C3%A9ricain',
    'wikipedia': 'https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal',
})
