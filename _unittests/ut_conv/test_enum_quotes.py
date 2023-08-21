import os
import unittest
from lecture_citation.ext_test_case import ExtTestCase
from lecture_citation.fromtex import enumerate_quotes
from lecture_citation.torst import to_rst


class TestEnumerateQuotes(ExtTestCase):

    def test_enumerate_quotes_tiny(self):
        fold = os.path.abspath(os.path.dirname(__file__))
        files = [os.path.join(fold, "data", "cit.tex")]
        res = []
        for name in files:
            quotes = list(enumerate_quotes(name))
            self.assertEqual(len(quotes), 7)
            self.assertEqual(quotes[0]['author'], "Douglas Coupland")
            self.assertIn("- Mais les gros ont plus ", quotes[0]['content'])
            res.extend([to_rst(_) for _ in quotes])
        whole = "\n".join(res)
        self.assertIn(":book: The Importance of Being Earnest", whole)
        self.assertIn(":date: 1945/08/16", whole)
        self.assertIn(
            ":author: Camille Landais, Piketty Thomas, Saez Emmanuel", whole)
        self.assertIn("    — Et là réside", whole)

    def test_enumerate_quotes(self):
        fold = os.path.abspath(os.path.dirname(__file__))
        files = [os.path.join(fold, "..", "..", "citation.tex")]
        temp = get_temp_folder(__file__, "temp_quotes")
        current = {}
        for name in files:
            if not os.path.exists(name):
                continue
            quotes = list(enumerate_quotes(name, encoding="latin-1"))
            self.assertGreater(len(quotes), 3)
            for q in quotes:
                y = q['year']
                rst = to_rst(q)
                if y not in current:
                    current[y] = open(os.path.join(  # pylint: disable=R1732
                        temp, "{}.rst".format(y)), "w", encoding="utf-8")
                    current[y].write("====\n{}\n====\n\n".format(y))
                current[y].write(rst)
                current[y].write('\n')
        for v in current.values():
            v.close()


if __name__ == "__main__":
    unittest.main()
