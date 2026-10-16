import importlib.util
import io
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('logs',Path(__file__).parents[1]/'scripts/parse_logs.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class LogTests(unittest.TestCase):
    def test_quoted_commas_and_blank_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'sample.log';path.write_text('now,alex,"export, report"\n\n')
            output=io.StringIO();errors=io.StringIO()
            self.assertEqual(module.parse_log_file(path,output,errors),(1,0))
            self.assertIn('Action: export, report',output.getvalue())

    def test_bad_row_does_not_discard_later_valid_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'sample.log';path.write_text('missing,field\nnow,sam,login\n')
            output=io.StringIO();errors=io.StringIO()
            self.assertEqual(module.parse_log_file(path,output,errors),(1,1))
            self.assertIn('Line 1:',errors.getvalue());self.assertIn('User: sam',output.getvalue())

    def test_unreadable_input_returns_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(module.main([str(Path(directory)/'missing.log')]),1)

if __name__=='__main__':unittest.main()
