# As I understand it, freemarker parsing is only needed to support update_groups
import ast
import re

def get_decimal_or_variable_value(token, variables):
    if (token.isdecimal()):
        return int(token)
    assert(token in variables)
    return variables[token]


def parse_freemarker_assign_expr(full_expr, variables):
    full_expr = full_expr.decode("ascii")
    pos_eq = full_expr.find("=")
    assert(pos_eq != -1)
    var = full_expr[: pos_eq].strip()
    assert(re.search(r"^\w+$", var))

    expr = full_expr[pos_eq + 1:].strip()
    pos = 0

    # TODO: Replace my parser by parser from ast

    ops = [
            {
                "+": lambda x, y: x + y,
                "-": lambda x, y: x - y
            },
            {
                "*": lambda x, y: x * y,
                "/": lambda x, y: x // y
            }
        ]

    def skip_spaces():
        nonlocal pos
        while pos < len(expr) and expr[pos].isspace():
            pos += 1

    def parse_binary(lvl):
        nonlocal pos
        if lvl == 2:
            return parse_unary()

        ret = parse_binary(lvl + 1)
        while True:
            if pos == len(expr) or not expr[pos] in ops[lvl]:
                skip_spaces()
                return ret

            f = ops[lvl][expr[pos]]
            pos += 1
            skip_spaces()

            tmp = parse_binary(lvl + 1)

            ret = f(ret, tmp)

    def parse_unary():
        nonlocal pos
        assert(pos < len(expr))
        if expr[pos] == "(":
            pos += 1
            skip_spaces()
            ret = parse_binary(0)
            assert(expr[pos] == ")")
            pos += 1
            skip_spaces()
            return ret

        if expr[pos] == "-":
            pos += 1
            skip_spaces()
            return -parse_unary()

        token = ""
        while pos < len(expr) and not expr[pos].isspace():
            token += expr[pos]
            pos += 1

        skip_spaces()
        return get_decimal_or_variable_value(token, variables)

    val = parse_binary(0)
    
    assert(pos == len(expr))

    return [var, val]


def parse_freemarker_list_as(s, variables):
    s = s.decode("ascii").strip()
    match = re.search(r"(.*)\bas\b(.*)", s)
    assert(match)
    arr, var = map(lambda x: x.strip(), match.groups())
    assert(re.search(r"^\w+$", var))
    if ".." in arr:
        assert(arr.count("..") == 1)
        left_part, right_part = map(lambda x: x.strip(), arr.split(".."))
        from_value = get_decimal_or_variable_value(left_part, variables)
        to_value = get_decimal_or_variable_value(right_part, variables)
        assert(from_value <= to_value)
        return [var, range(from_value, to_value + 1)]

    assert(arr[0] == "[" and arr[-1] == "]")
    ret = ast.literal_eval(arr)
    return [var, ret]

# Only used in problem.update_groups
def parse_script_groups(content, hand_tests):
    groups = {"0": []}
    scores = {"0": None}
    cur_group = "0"
    test_id = 0
    any = False
    script = []
    for i in filter(lambda x: x.strip(), content.splitlines()):
        match = re.search(rb"<#-- *group *([-0-9]*) *(score *(\d*))? *(depends *(([-0-9]* +)*))? *-->", i)
        if not match:
            match_freemarker_single_tag = re.search(rb"<#(\w*)(.*)/>", i)
            if match_freemarker_single_tag:
                script.append(["single_tag", match_freemarker_single_tag.groups()])
                continue

            match_freemarker_opening_tag = re.search(rb"<#(\w*)(.*)>", i)
            if match_freemarker_opening_tag:
                script.append(["opening_tag", match_freemarker_opening_tag.groups()])
                continue

            match_freemarker_closing_tag = re.search(rb"</#(\w*)(.*)>", i)
            if match_freemarker_closing_tag:
                tmp = match_freemarker_closing_tag.groups()
                assert tmp[1].decode("ascii").strip() == "", "strange closing tag \"" + i + "\""
                script.append(["closing_tag", tmp[0]])
                continue

            t = i.split(b'>')[-1].strip()
            script.append(["test", t])
        else:
            script.append(["group", match.group(1).decode("ascii"), match.group(3), match.group(5)])
            any = True
        
    if not any:
        return None

    pos = 0
    stack_cycles = []
    variables = dict()
    while pos < len(script):
        if script[pos][0] == "test":
            t = script[pos][1]
            if t == b'$':
                test_id += 1
                while test_id in hand_tests:
                    test_id += 1
            else:
                test_id = int(t)
                assert test_id not in hand_tests
            groups[cur_group].append(test_id)
        elif script[pos][0] == "group":
            cur_group = script[pos][1]
            groups[cur_group] = []
            if script[pos][2] is None:
                scores[cur_group] = None
            else:
                scores[cur_group] = {}
                scores[cur_group]["score"] = int(script[pos][2].decode("ascii"))
                if script[pos][3] is None:
                    scores[cur_group]["depends"] = None
                else:
                    scores[cur_group]["depends"] = list(map(lambda a: a.decode("ascii"), filter(None, script[pos][3].split())))
        elif script[pos][0] == "single_tag":
            if script[pos][1][0] == rb"assign":
                name, val = freemarker_parsers.parse_freemarker_assign_expr(script[pos][1][1], variables)
                variables[name] = val
        elif script[pos][0] == "opening_tag":
            if script[pos][1][0] == rb"list":
                name, values = freemarker_parsers.parse_freemarker_list_as(script[pos][1][1], variables)
                variables[name] = values[0]
                stack_cycles.append([name, values[1:], pos])
            elif script[pos][1][0] == rb"assign":
                name, val = freemarker_parsers.parse_freemarker_assign_expr(script[pos][1][1], variables)
                variables[name] = val
        elif script[pos][0] == "closing_tag":
            if script[pos][1] == rb"list":
                if len(stack_cycles[-1][1]):
                    variables[stack_cycles[-1][0]] = stack_cycles[-1][1][0]
                    stack_cycles[-1][1] = stack_cycles[-1][1][1:]
                    pos = stack_cycles[-1][2]
                else:
                    stack_cycles.pop()

        pos += 1

    return groups, scores
