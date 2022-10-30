"""Parser for the Sinope Language."""
import typing

import pyparsing as ppp


# Unused Characters: § & | \ ` ~ ' @
#


ParamT = typing.ParamSpec("ParamT")


def with_ws(
    func: typing.Callable[ParamT, ppp.ParserElement]
) -> typing.Callable[ParamT, ppp.ParserElement]:
    """
    Set white space and comment.

    Parameters
    ----------
    func: typing.Callable[ParamT,  ppp.ParserElement]
        the function to be wrapped

    Returns
    -------
    typing.Callable[ParamT,  ppp.ParserElement]
        the wrapped function

    """
    comment = ppp.Regex(r";.*").set_name("comment")
    white_space = " \t"

    def wrapper(*args: ParamT.args, **kwargs: ParamT.kwargs) -> ppp.ParserElement:
        inner = func(*args, **kwargs)
        return inner.ignore(comment).set_whitespace_chars(white_space)

    return wrapper


@with_ws
def identifier() -> ppp.ParserElement:
    """
    Build the parser element for an identifier.

    Returns
    -------
    ppp.ParserElement
        the parser element for an identifier

    """
    id_start: str = ppp.alphas + "_?!"
    id_follow: str = id_start + ppp.nums
    return ppp.Word(id_start, id_follow).set_name("identifier")


@with_ws
def integer_literal() -> ppp.ParserElement:
    """
    Build the parser element for an integer literal.

    Returns
    -------
    ppp.ParserElement
        the parser element for an integer literal

    """
    return ppp.Word(ppp.nums, ppp.nums + "_").set_name("integer-literal")


@with_ws
def symbol_literal() -> ppp.ParserElement:
    """
    Build the parser element for a symbol literal.

    Returns
    -------
    ppp.ParserElement
        the parser element for an symbol literal

    """
    symbol_chars = ppp.alphanums + "!?_+-*/%.:<>=()[]"
    content = ppp.Word(symbol_chars).set_name("symbol-literal")
    return ppp.Suppress("#") + content


@with_ws
def string_literal(exp: ppp.ParserElement) -> ppp.ParserElement:
    """
    Build the parser element for a string literal.

    Parameters
    ----------
    exp: ppp.ParserElement
        the parser element of an expression, required for string interpolation

    Returns
    -------
    ppp.ParserElement
        the parser element for an string literal

    """
    string_lit_simple = ppp.QuotedString(quote_char='"', end_quote_char='"')
    string_lit_head = ppp.QuotedString(quote_char='"', end_quote_char="$")
    string_lit_mid = ppp.QuotedString(quote_char="$", end_quote_char="$")
    string_lit_end = ppp.QuotedString(quote_char="$", end_quote_char='"')

    mid_group = exp[0, 1] + string_lit_mid
    end_group = exp[0, 1] + string_lit_end
    string_interp = string_lit_head + mid_group[0, ...] + end_group
    return string_lit_simple | string_interp


@with_ws
def argument_message(arg_element: ppp.ParserElement) -> ppp.ParserElement:
    """
    Build the parser element for an argument message.

    Parameters
    ----------
    arg_element: ppp.ParserElement
        the element for the arguments of the argument message

    Returns
    -------
    ppp.ParserElement
        a parser element for an argument message

    """
    arg = ppp.Dict(
        identifier().copy().set_name("argument-label")
        + ppp.Suppress(":")
        + arg_element.copy().set_name("argument-value")
    )
    return ppp.Group(arg[1, ...]).set_name("argument-message")


@with_ws
def expression() -> ppp.ParserElement:
    """
    Build the parser element for an expression.

    Returns
    -------
    ppp.ParserElement
        the parser element for an expression

    """
    # Operators
    add_operator = ppp.one_of(["+", "-", "(+)", "(-)", "[+]", "[-]"])
    mul_operator = ppp.one_of(
        [
            "*",
            "**",
            "/",
            "%",
            "(.)",
            "(*)",
            "(**)",
            "(/)",
            "(%)",
            "[.]",
            "[*]",
            "[**]",
            "[/]",
            "[%]",
        ]
    )
    pow_operator = ppp.one_of(["^", "(^)", "[^]"])
    rel_operator = ppp.one_of(
        [
            "<",
            ">",
            "<=",
            ">=",
            "<>",
            "==",
            "(<)",
            "(>)",
            "(<=)",
            "(>=)",
            "(<>)",
            "(==)",
            "(=)",
            "[<]",
            "[>]",
            "[<=]",
            "[>=]",
            "[<>]",
            "[==]",
            "[=]",
        ]
    )
    # Assignments
    assign = ppp.one_of(["=", "+=", "-=", "*=", "/=", "%="])

    sinope_terminator = ppp.Literal(".") | ppp.Word("\r\n").set_name("line terminator")
    sinope_comment = ppp.Regex(r";.*").set_name("comment")
    sinope_exp = (
        ppp.Forward()
        .ignore(sinope_comment)
        .set_whitespace_chars(" \t")
        .set_name("expression")
    )

    message = ppp.Or(
        [identifier(), integer_literal(), string_literal(sinope_exp), symbol_literal()]
    )
    message_chain = message[1, ...]
    op_expression = ppp.infix_notation(
        message_chain,
        [
            (
                add_operator | mul_operator | pow_operator | rel_operator,
                1,
                ppp.OpAssoc.RIGHT,
            ),
            (pow_operator, 2, ppp.OpAssoc.LEFT),
            (mul_operator, 2, ppp.OpAssoc.LEFT),
            (add_operator, 2, ppp.OpAssoc.LEFT),
            (rel_operator, 2, ppp.OpAssoc.LEFT),
        ],
    )
    subexp = ppp.delimited_list(
        op_expression + argument_message(op_expression)[0, 1],
        delim=assign,
        combine=True,
    ).set_name("sub-expression")
    sinope_exp <<= ppp.delimited_list(
        subexp, delim=sinope_terminator, allow_trailing_delim=True
    )
    return sinope_exp
