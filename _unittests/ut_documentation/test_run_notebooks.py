# -*- coding: utf-8 -*-
"""
@brief      test log(time=33s)
"""

import sys
import os
import unittest
import shutil
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder
from pyquickhelper.ipythonhelper import execute_notebook_list, execute_notebook_list_finalize_ut


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

import src.lecture_citation


class TestRunNotebooksPython(unittest.TestCase):

    def test_run_notebook_python(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        temp = get_temp_folder(__file__, "temp_run_notebooks")
        logs = os.path.join(temp, "logs")
        os.mkdir(logs)

        # selection of notebooks
        fnb = os.path.normpath(os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", "..", "_doc", "notebooks"))
        keepnote = []
        for f in os.listdir(fnb):
            if os.path.splitext(f)[-1] == ".ipynb" and "_long" not in f:
                keepnote.append(os.path.join(fnb, f))

        shutil.copy(os.path.join(fnb, "logs", "QCMApp.log"), logs)

        # run the notebooks
        res = execute_notebook_list(temp, keepnote, fLOG=fLOG,
                                    additional_path=[os.path.dirname(src.__file__)])
        execute_notebook_list_finalize_ut(res, fLOG=fLOG, dump=src.lecture_citation)


if __name__ == "__main__":
    unittest.main()
