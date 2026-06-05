def execute_expression(expr):
    text = str(expr)
    stripped = text.strip()
    result = eval(stripped)
    return result


def demo_safe_math():
    expr = "2 + 2 * 5"
    result = eval(expr)
    return result
