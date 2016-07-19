import re


def add_all_occurrences(string, pattern, params_set):
    for match in reversed(list(pattern.finditer(string))):
        params_set.add(match.group(1))


def variables_set(argv, environment, output_type, output_parameters):
    pattern = re.compile(r'\$\{(.*)\}')
    params_set = set()

    for i in range(len(argv)):
        add_all_occurrences(argv[i], pattern, params_set)

    for env in environment:
        add_all_occurrences(environment[env], pattern, params_set)

    if output_type == u'file':
        if u'file_path' in output_parameters:
            add_all_occurrences(
                output_parameters[u'file_path'],
                pattern,
                params_set
            )

    return params_set


def files_set(argv, environment):
    pattern = re.compile(r'@\{(.*)\}')
    params_set = set()

    for i in range(len(argv)):
        add_all_occurrences(argv[i], pattern, params_set)

    for env in environment:
        add_all_occurrences(environment[env], pattern, params_set)

    return params_set
