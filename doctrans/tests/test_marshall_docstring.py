"""
Tests for docstring parsing
"""

from ast import BinOp, Mult
from collections import OrderedDict
from copy import deepcopy
from unittest import TestCase

import doctrans.emit
import doctrans.emitter_utils
from doctrans import parse
from doctrans.ast_utils import set_value
from doctrans.docstring_parsers import _set_name_and_type, parse_docstring
from doctrans.emitter_utils import to_docstring
from doctrans.tests.mocks.docstrings import (
    docstring_extra_colons_str,
    docstring_google_pytorch_lbfgs_str,
    docstring_google_str,
    docstring_google_tf_adadelta_str,
    docstring_google_tf_adam_str,
    docstring_google_tf_lambda_callback_str,
    docstring_google_tf_squared_hinge_str,
    docstring_header_and_return_str,
    docstring_no_default_doc_str,
    docstring_numpydoc_only_doc_str,
    docstring_numpydoc_only_params_str,
    docstring_numpydoc_only_returns_str,
    docstring_numpydoc_str,
    docstring_only_return_type_str,
    docstring_str,
)
from doctrans.tests.mocks.ir import (
    docstring_google_pytorch_lbfgs_ir,
    docstring_google_tf_adadelta_ir,
    docstring_google_tf_adam_ir,
    docstring_google_tf_lambda_callback_ir,
    docstring_google_tf_squared_hinge_ir,
    intermediate_repr,
    intermediate_repr_extra_colons,
    intermediate_repr_no_default_doc,
    intermediate_repr_no_default_doc_or_prop,
    intermediate_repr_only_return_type,
)
from doctrans.tests.utils_for_tests import unittest_main


class TestMarshallDocstring(TestCase):
    """
    Tests whether docstrings are parsed out—and emitted—correctly
    """

    def test_ir_equality(self) -> None:
        """
        Tests whether `parse_docstring` produces `intermediate_repr`
              from `docstring_str`"""
        self.assertDictEqual(
            parse_docstring(docstring_str), intermediate_repr_no_default_doc
        )

    def test_intermediate_repr_no_default_doc_equality(self) -> None:
        """
        Tests whether `parse_docstring` produces `docstring_str_no_default_doc`
              from `docstring_str_no_default_doc`"""
        ir = parse_docstring(
            docstring_no_default_doc_str,
            emit_default_doc=False,
            emit_default_prop=False,
        )
        self.assertDictEqual(
            ir,
            intermediate_repr_no_default_doc_or_prop,
        )

    def test_intermediate_repr_extra_colons_equality(self) -> None:
        """
        Tests whether `parse_docstring` produces `docstring_str_no_default_doc`
              from `docstring_str_no_default_doc`"""

        self.assertDictEqual(
            parse_docstring(docstring_extra_colons_str, emit_default_doc=False),
            intermediate_repr_extra_colons,
        )

    def test_intermediate_repr_only_return_type_equality(self) -> None:
        """
        Tests whether `parse_docstring` produces `docstring_str_no_default_doc`
              from `docstring_str_no_default_doc`"""

        self.assertDictEqual(
            parse_docstring(docstring_only_return_type_str, emit_default_doc=False),
            intermediate_repr_only_return_type,
        )

    def test_ir2docstring(self) -> None:
        """ Tests whether `to_docstring` produces `docstring_str` from `intermediate_repr` """
        self.assertEqual(
            docstring_str.strip(),
            doctrans.emitter_utils.to_docstring(
                deepcopy(intermediate_repr),
                indent_level=0,
                emit_types=True,
                emit_default_doc=True,
                emit_separating_tab=False,
                word_wrap=False,
            ).strip(),
        )

    def test_from_docstring(self) -> None:
        """
        Tests whether `docstring` produces `intermediate_repr_no_default_doc`
              from `docstring_str`"""
        ir, returns = parse.docstring(
            docstring_str, return_tuple=True, emit_default_doc=False
        )
        self.assertTrue(returns)
        self.assertDictEqual(ir, intermediate_repr_no_default_doc)

    def test_from_docstring_numpydoc(self) -> None:
        """
        Tests whether `docstring` produces `intermediate_repr_no_default_doc`
              from `docstring_numpydoc_str`"""
        ir, returns = parse.docstring(
            docstring_numpydoc_str, return_tuple=True, emit_default_doc=False
        )
        self.assertTrue(returns)
        self.assertDictEqual(ir, intermediate_repr_no_default_doc)

    def test_from_docstring_numpydoc_only_params(self) -> None:
        """
        Tests whether `docstring` produces `intermediate_repr_no_default_doc`
              from `docstring_numpydoc_only_params_str`"""
        ir, returns = parse.docstring(
            docstring_numpydoc_only_params_str,
            return_tuple=True,
            emit_default_doc=False,
        )
        self.assertFalse(returns)
        gold = deepcopy(intermediate_repr_no_default_doc)
        del gold["returns"]
        gold.update({"doc": "", "returns": None})
        self.assertDictEqual(ir, gold)

    def test__set_name_and_type(self) -> None:
        """
        Tests that `_set_name_and_type` parsed AST code into a code str.
        Not working since I explicitly deleted the typ from ``` quoted defaults. Changed mock to match.
        """
        self.assertTupleEqual(
            _set_name_and_type(
                (
                    "adder",
                    {
                        "default": BinOp(
                            set_value(5),
                            Mult(),
                            set_value(5),
                        ),
                    },
                ),
                infer_type=True,
                word_wrap=True,
            ),
            ("adder", {"default": "```(5 * 5)```"}),
        )

        self.assertTupleEqual(
            _set_name_and_type(
                (
                    "adder",
                    {
                        "default": BinOp(
                            set_value(5),
                            Mult(),
                            set_value(5),
                        ),
                        "doc": ["5", "b"],
                    },
                ),
                infer_type=True,
                word_wrap=True,
            ),
            ("adder", {"default": "```(5 * 5)```", "doc": "5b"}),
        )

    def test_from_docstring_numpydoc_only_returns(self) -> None:
        """
        Tests whether `docstring` produces `intermediate_repr_no_default_doc`
              from `docstring_numpydoc_only_returns_str`"""
        ir, returns = parse.docstring(
            docstring_numpydoc_only_returns_str,
            return_tuple=True,
            emit_default_doc=False,
        )
        self.assertTrue(returns)
        self.assertDictEqual(
            ir,
            {
                "doc": "",
                "name": None,
                "params": OrderedDict(),
                "returns": intermediate_repr_no_default_doc["returns"],
                "type": "static",
            },
        )

    def test_from_docstring_numpydoc_only_doc_str(self) -> None:
        """
        Tests whether `docstring` produces `intermediate_repr_no_default_doc`
              from `docstring_numpydoc_only_doc_str`"""
        ir, returns = parse.docstring(
            docstring_numpydoc_only_doc_str, return_tuple=True
        )
        self.assertFalse(returns)
        self.assertDictEqual(
            ir,
            {
                "doc": intermediate_repr_no_default_doc["doc"],
                "name": None,
                "params": OrderedDict(),
                "returns": None,
                "type": "static",
            },
        )

    def test_from_docstring_google_str(self) -> None:
        """
        Tests whether `parse_docstring` produces `intermediate_repr_no_default_doc`
              from `docstring_google_str`
        """
        ir = parse_docstring(docstring_google_str)
        self.assertDictEqual(ir, intermediate_repr_no_default_doc)

    def test_from_docstring_google_tf_squared_hinge(self) -> None:
        """
        Tests whether `parse_docstring` produces the right IR
              from `docstring_google_tf_squared_hinge_str`
        """
        self.assertDictEqual(
            parse_docstring(
                docstring_google_tf_squared_hinge_str,
                emit_default_doc=True,
                infer_type=True,
                default_search_announce=("Default value is", "defaults to"),
            ),
            docstring_google_tf_squared_hinge_ir,
        )

    def test_from_docstring_google_tf_adam(self) -> None:
        """
        Tests whether `parse_docstring` produces the right IR
              from `docstring_google_tf_squared_hinge_str`
        """
        self.assertDictEqual(
            parse_docstring(
                docstring_google_tf_adam_str, emit_default_doc=True, infer_type=True
            ),
            docstring_google_tf_adam_ir,
        )

    def test_from_docstring_google_tf_adadelta_str(self) -> None:
        """
        Tests whether `parse_docstring` produces the right IR
              from `docstring_google_tf_adadelta_str`
        """
        self.assertDictEqual(
            parse_docstring(
                docstring_google_tf_adadelta_str, emit_default_doc=True, infer_type=True
            ),
            docstring_google_tf_adadelta_ir,
        )

    def test_from_docstring_google_tf_lambda_callback_str(self) -> None:
        """
        Tests whether `parse_docstring` produces the right IR
              from `docstring_google_tf_lambda_callback_str`
        """
        self.assertDictEqual(
            parse_docstring(
                docstring_google_tf_lambda_callback_str,
                emit_default_doc=True,
                infer_type=True,
            ),
            docstring_google_tf_lambda_callback_ir,
        )

    maxDiff = None

    def test_from_docstring_google_pytorch_lbfgs_str(self) -> None:
        """
        Tests whether `parse_docstring` produces the right IR
              from `docstring_google_pytorch_lbfgs_str`
        """
        self.assertDictEqual(
            parse_docstring(
                docstring_google_pytorch_lbfgs_str,
                emit_default_doc=False,
                infer_type=True,
            ),
            docstring_google_pytorch_lbfgs_ir,
        )

    def test_to_docstring_fails(self) -> None:
        """
        Tests docstring failure conditions
        """
        self.assertRaises(
            NotImplementedError,
            lambda: to_docstring(
                deepcopy(intermediate_repr_no_default_doc), docstring_format="numpydoc"
            ),
        )

    def test_docstring_header_and_return_str(self) -> None:
        """ Tests that `docstring_header_and_return_str` can produce IR """
        _intermediate_repr = deepcopy(intermediate_repr_no_default_doc)
        _intermediate_repr["params"] = OrderedDict()
        self.assertDictEqual(
            parse_docstring(docstring_header_and_return_str), _intermediate_repr
        )


unittest_main()
