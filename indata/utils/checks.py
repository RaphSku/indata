"""Functions specialised on checking specific conditions"""

def isNumeric(x: str) -> bool:
    """Checks whether a string is numeric

    Parameters
    ----------
    x : str
        Input string which should be checked

    Returns
    -------
    bool
        Evaluates to `True` if x is numeric and `False` if not

    Raises
    ------
    TypeError
        Is raised when the input `x` is not a string
    """
    if not isinstance(x, str):
        raise TypeError("The input {x} is not a string!")

    if x.isdigit() or (x.replace('.', '', 1).isdigit() and x.count('.') < 2):
        return True
    return False