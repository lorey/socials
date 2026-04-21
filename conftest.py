"""Pytest configuration and fixtures."""

import types

import pytest_markdown_docs.plugin as pmd  # type: ignore[import-untyped]

# Fix for pytest-markdown-docs stdout capture bug.
# The plugin's runtest() incorrectly uses `capman.global_and_fixture_disabled()`
# which DISABLES capture instead of enabling it, causing print() output to leak.
# See: https://github.com/modal-labs/pytest-markdown-docs/blob/main/pytest_markdown_docs/plugin.py#L103-L106
# TODO: Remove this fix once upstream is patched.


def _patched_runtest(self):
    """Run markdown code fence test with proper stdout capture."""
    global_sets = self.parent.config.hook.pytest_markdown_docs_globals()
    mod = types.ModuleType("fence")
    all_globals = mod.__dict__
    for global_set in global_sets:
        all_globals.update(global_set)
    for fixture_name in self._fixtureinfo.names_closure:
        self.fixture_request.getfixturevalue(fixture_name)
    for argname, value in self.funcargs.items():
        all_globals[argname] = value
    self.runner.runtest(self.test_definition, all_globals)


pmd.MarkdownInlinePythonItem.runtest = _patched_runtest
