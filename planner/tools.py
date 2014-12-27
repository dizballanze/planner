import re

_measure_patterns = re.compile(r'^([0-9]+\.?[0-9]*)([a-zA-Z]*)$')


def parse_measure_units(values, default_unit="mm"):
    matches = _measure_patterns.match(values)
    if not matches:
        raise ValueError()
    groups = matches.groups()
    if '.' in groups[0]:
        value = float(groups[0])
    else:
        value = int(groups[0])
    return (value, groups[1] or default_unit)
