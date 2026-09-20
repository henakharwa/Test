"""
# Advanced Calculator
# Provides basic arithmetic operations and a simple expression evaluator.
# Author: Hena
"""

from typing import Dict, Callable

class Calculator:
    """A simple calculator that can perform basic arithmetic and evaluate expressions.

    The class supports addition, subtraction, multiplication, division, exponentiation,
    and a rudimentary expression parser that can handle parentheses and the four
    basic operators.  All operations operate on floats.
    """

    def __init__(self) -> None:
        # Map operator symbols to corresponding methods
        self.operations: Dict[str, Callable[[float, float], float]] = {
            "+": self.add,
            "-": self.sub,
            "*": self.mul,
            "/": self.truediv,
            "**": self.pow,
        }

    # Basic operations
    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def sub(a: float, b: float) -> float:
        return a - b

    @staticmethod
    def mul(a: float, b: float) -> float:
        return a * b

    @staticmethod
    def truediv(a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b

    @staticmethod
    def pow(a: float, b: float) -> float:
        return a ** b

    # Expression evaluator
    def evaluate(self, expression: str) -> float:
        """Evaluate a mathematical expression consisting of numbers and +,-,*,/,** operators.

        Supports parentheses.  Example: "(2+3)*4-5/2**1"
        """
        # Tokenize input
        tokens = self._tokenize(expression)
        # Convert to Reverse Polish Notation (Shunting Yard algorithm)
        rpn = self._to_rpn(tokens)
        # Evaluate RPN
        return self._eval_rpn(rpn)

    def _tokenize(self, expr: str) -> list:
        import re
        token_spec = [
            ("NUMBER",  r"\d+(?:\.\d*)?"),
            ("OP",       r"\*\*|[+\-*/]"),
            ("LPAREN",   r"\("),
            ("RPAREN",   r"\)"),
            ("SKIP",     r"\s+"),
        ]
        token_re = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec))
        tokens = []
        for mo in token_re.finditer(expr):
            kind = mo.lastgroup
            value = mo.group()
            if kind == "SKIP":
                continue
            tokens.append((kind, value))
        return tokens

    def _to_rpn(self, tokens: list) -> list:
        # Operator precedence
        prec = {"+": 1, "-": 1, "*": 2, "/": 2, "**": 3}
        output = []
        ops = []
        for kind, value in tokens:
            if kind == "NUMBER":
                output.append(float(value))
            elif kind == "OP":
                while ops and ops[-1] != "(" and prec[ops[-1]] >= prec[value]:
                    output.append(ops.pop())
                ops.append(value)
            elif kind == "LPAREN":
                ops.append("(")
            elif kind == "RPAREN":
                while ops and ops[-1] != "(":
                    output.append(ops.pop())
                ops.pop()  # pop the "("
        while ops:
            output.append(ops.pop())
        return output

    def _eval_rpn(self, rpn: list) -> float:
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            else:  # operator
                b = stack.pop()
                a = stack.pop()
                stack.append(self.operations[token](a, b))
        return stack[0]

# Example usage
if __name__ == "__main__":
    calc = Calculator()
    expr = "(2+3)*4-5/2**1"
    print(f"{expr} = {calc.evaluate(expr)}")
    # Basic ops
    print("3 + 5 =", calc.add(3, 5))
    print("10 / 2 =", calc.truediv(10, 2))
