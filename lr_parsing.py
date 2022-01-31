import re

def size(rule):
    rule = re.sub(r'[a-z]+', 'i', rule)
    return len(re.sub(r'[^A-Za-z0-9]', '', rule))

def lr_parse(w, action, goto):
    w = re.sub(r'id', 'i', w)
    stack = ['0']
    idx_w = 0
    a = w[idx_w]
    while True:
        s = stack[-1]
        if action.get(s, {}).get(a, [None])[0] == 's':
            stack.append( action[s][a][1] )
            idx_w += 1
            a = w[idx_w]
        elif action.get(s, {}).get(a, [None])[0] == 'r':
            for i in range(size(rules[ action[s][a][1] ].split('->')[1].strip())):
                stack.pop()
            t = stack[-1]
            A = rules[ action[s][a][1] ].split('->')[0].strip()
            if t in goto and A in goto[t]:
                stack.append(goto[t][A])
            print( rules[ action[s][a][1] ] )
        elif action.get(s, {}).get(a, [None])[0] == 'acc':
            break
        else:
            raise Exception('Error-Recovery routine')


if __name__ == '__main__':
    rules = {
        '1': 'E -> E + T',
        '2': 'E -> T',
        '3': 'T -> T * F',
        '4': 'T -> F',
        '5': 'F -> (E)',
        '6': 'F -> id'
    }

    action = {
        '0': {
            'i': ('s', '5'),
            '(': ('s', '4'),
        },
        '1': {
            '+': ('s', '6'),
            '$': ['acc']
        },
        '2': {
            '+': ('r', '2'),
            '*': ('s', '7'),
            ')': ('r', '2'),
            '$': ('r', '2')
        },
        '3': {
            '+': ('r', '4'),
            '*' : ('r', '4'),
            ')' :('r', '4'),
            '$': ('r', '4')
        },
        '4': {
            'i': ('s', '5'),
            '(': ('s', '4')
        },
        '5': {
            '+': ('r', '6'),
            '*': ('r', '6'),
            ')': ('r', '6'),
            '$': ('r', '6')
        },
        '6': {
            'i': ('s', '5'),
            '(': ('s', '4')
        },
        '7': {
            'i': ('s', '5'),
            '(': ('s', '4')
        },
        '8': {
            '+': ('s', '6'),
            ')': ('s', '11')
        },
        '9': {
            '+': ('r', '1'),
            '*': ('s', '7'),
            ')': ('r', '1'),
            '$': ('r', '1')
        },
        '10': {
            '+': ('r', '3'),
            '*': ('r', '3'),
            ')': ('r', '3'),
            '$': ('r', '3')
        },
        '11': {
            '+': ('r', '5'),
            '*': ('r', '5'),
            ')': ('r', '5'),
            '$': ('r', '5')
        }
    }

    goto = {
        '0': {
            'E': '1',
            'T': '2',
            'F': '3'
        },
        '4':{
            'E': '8',
            'T': '2',
            'F': '3'
        },
        '6': {
            'T': '9',
            'F': '3'
        },
        '7': {
            'F': '10'
        }

    }

    lr_parse('id*id+id$', action, goto)
