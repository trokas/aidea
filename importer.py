import json
import os

def import_from_nb(prefix: str, name: str):
    """Looks for last occurance of function or class (based on the name case)
    and returns it."""
    is_function = name == name.lower()
    query = f'def {name}' if is_function else f'class {name}'
    files = os.listdir()
    try:
        match = next(f for f in files if f[:len(prefix)] == prefix)
    except:
        raise FileNotFoundError(prefix, files)
    cells = json.load(open(match, 'r'))['cells']
    for c in cells:
        if c['cell_type'] == 'code':
            # Run all lines that contain imports
            [exec(line, globals()) for line in c['source']
             if line[:7] == 'import ' or line[:5] == 'from ' or '= import_from_nb' in line]
            # Exec cell that contains function or class definition
            if len([line for line in c['source'] if line[:len(query)] == query]):
                exec(''.join(c['source']), globals())
    if name in globals():
        return globals()[name]
    else:
        raise Exception(f'{name} is missing from {match}')
