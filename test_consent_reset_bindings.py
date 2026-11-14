"""Guard the exact desktop consent reset bindings against accidental regression.

Static source contract only: does not replace interactive Windows Tk testing.
"""
import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent

class ConsentResetBindingTests(unittest.TestCase):
    def test_single_and_batch_destination_variables_reset_consent(self):
        tree = ast.parse((ROOT / "data2web_desktop.py").read_text(encoding="utf-8"))
        bindings = {}
        for node in ast.walk(tree):
            if not isinstance(node, ast.For) or not isinstance(node.iter, (ast.Tuple, ast.List)):
                continue
            names = [x.id for x in node.iter.elts if isinstance(x, ast.Name)]
            for child in node.body:
                if not isinstance(child, ast.Expr) or not isinstance(child.value, ast.Call):
                    continue
                call = child.value
                if not isinstance(call.func, ast.Attribute) or call.func.attr != "trace_add":
                    continue
                if len(call.args) != 2 or not isinstance(call.args[1], ast.Name):
                    continue
                bindings[call.args[1].id] = set(names)
        self.assertGreaterEqual(
            bindings.get("reset_consent", set()),
            {"id_key", "title_key", "category_key", "parent", "folder"},
        )
        self.assertGreaterEqual(
            bindings.get("clear_batch_consent", set()),
            {"batch_id", "batch_title", "batch_category", "batch_parent", "batch_leaf"},
        )

    def test_desktop_module_parses(self):
        ast.parse((ROOT / "data2web_desktop.py").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
