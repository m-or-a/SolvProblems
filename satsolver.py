import copy

def read_dismac(file_name):

    cnf = {}
    j = 1
    with open(file_name) as f:
        for line in f:
            if line[0] == 'p':
                tmp = line.split()
                v = int(tmp[2])
                d = int(tmp[3])

            tmp_list = []
            if line[0] > '0' and line[0] <= '9' or line[0] == '-':
                tmp = line.split()
                for i in tmp:
                    if i == '0':
                        break
                    tmp_list.append(int(i))
                cnf[j] = tmp_list
                j += 1

    return v, d, cnf


def solved_d_add_step(solved_d, step):
    for i in solved_d:
        if not 'step' in solved_d[i]:
            solved_d[i]['step'] = step
    return solved_d

def bcp(cnf, literal, solved_d): 
    new_cnf = cnf.copy()
    for i in cnf:
        if literal in cnf[i]:
            solved_d[i] = {'d': new_cnf.pop(i)}
        elif -literal in cnf[i]:
            new_cnf[i].remove(-literal)
            if new_cnf[i] == []:
                return new_cnf, True, solved_d
    return new_cnf, False, solved_d

def min_c(cnf, v): 
    min_len = v + 1
    minc = list(cnf.keys())[0]
    for n, d in cnf.items():
        if len(d) < min_len:
            min_len = len(d)
            minc = n
    return minc

def decide(cnf, v, v_sat, step):
    
    if len(v_sat) == v:
        flag = False

    elif cnf == {} and len(v_sat) != v:
        tmp = [abs(x) for x in v_sat.keys()]
        
        for i in range(v):
            if i+1 not in tmp:
               v_sat[i+1] = [0, 0]
        flag = False

    else:
        flag = True

    if flag:
        minc = min_c(cnf, v)

        if len(cnf[minc]) != 1 or len(cnf[minc]) == 1 and step == 0: 
            step += 1 
        v_sat[cnf[minc][0]] = [step, minc]
    
    return v_sat, step, flag


def create_new_d(cnf, cd, x, gd):
    new_d = []
    new_d = cnf[gd].copy()
    for i in cnf[cd]:
        if i not in cnf[gd]:
            new_d.append(i)
    new_d.remove(x)
    new_d.remove(-x)
    return new_d

def return_step(new_d, v_sat, step):
    new_step = step
    for i in new_d:
        if i in v_sat and v_sat[i][0] < new_step:
            new_step = v_sat[i][0]
    return new_step
    
def analyze_conflict(cnf_origin, cnf, v_sat, step):

    if step == 1:
        return cnf_origin, -1
    for d in cnf:
        if cnf[d] == []:
            cd = d 
            break
    x = list(v_sat.keys())[-1] 
    tmp = len(cnf_origin) + 1
    cnf_origin[tmp] = create_new_d(cnf_origin, cd, x, v_sat[x][1]) 
    new_step = return_step(cnf_origin[tmp], v_sat, step) 
    return cnf_origin, new_step

def backtrack(bl, cnf, v_sat, solved_d): 
    x = list(solved_d.keys())
    for i in x: 
        if solved_d[i]['step'] > bl:
            cnf[i] = solved_d[i][0]
            solved_d.pop(i)
    x = list(v_sat.keys())
    for i in x:
        if v_sat[i][0] > bl:
            for k, n in cnf.items():
                if -i in n:
                    cnf[k].append(-i)
            v_sat.pop(i)
    return cnf, solved_d, v_sat
    
def cdcl(cnf, v):
    step = 0
    new_cnf = copy.deepcopy(cnf)

    v_sat = {}
    solved_d = {}
    while(True):
        v_sat, step, flag = decide(new_cnf, v, v_sat, step)
        if not flag:
            return 'sat', v_sat

        new_cnf, conflict, solved_d = bcp(new_cnf, list(v_sat.keys())[-1], solved_d)

        solved_d = solved_d_add_step(solved_d, step)
        if conflict:
            cnf, bactrack_level = analyze_conflict(cnf, new_cnf, v_sat, step)
            if bactrack_level < 0:
               return 'unsat', 0
            new_cnf, solved_d, v_sat = backtrack(bactrack_level, new_cnf, v_sat, solved_d)


file_name = input('file name: ')
v, d, cnf = read_dismac(file_name)
check = cdcl(cnf, v)
if check[0] == 'sat':
    print('sat', list(check[1].keys()))
else:
    print('unsat')