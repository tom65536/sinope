"""Test cases for the parser."""

from sinope.sinope_parser import expression


def test_good():
    """Check expressions that should compile."""
    exp = expression()
    exp.run_tests(
        """\
        x y z

        (1 to: 10) do: f
        """
    )
