from copy import deepcopy


#################################### Các hàm chính ####################################    
"""Đọc dữ liệu từ tệp đầu vào và chuyển đổi thành dạng CNF."""
def read_input_data(input_filename: str):
    alpha = []
    KB = []
    
    f = open(input_filename, 'r')
    alpha = [f.readline().strip()]
    KB = [f.readline()[:-1].split(' OR ') for _ in range(int(f.readline()))]
    alpha = standard_cnf_sentence(alpha)
    KB = standard_cnf_sentence(KB)
    f.close()

    return alpha, KB

"""Hàm sử dụng phương pháp resulusion"""
def pl_resolution(alpha, KB):
    new_clauses_list = []
    solution = False
    
    cnf_clause_list = deepcopy(KB)
    neg_alpha = standard_cnf_sentence(negation_of_cnf_sentence(alpha))
    for clause in neg_alpha:
        if clause not in cnf_clause_list:
            cnf_clause_list.append(clause)

    while True:
        new_clauses_list.append([])

        for i in range(len(cnf_clause_list)):
            for j in range(i + 1, len(cnf_clause_list)):
                resolvents = resolve(cnf_clause_list[i], cnf_clause_list[j])
                if [] in resolvents:
                    solution = True
                    new_clauses_list[-1].append([])
                    return new_clauses_list, solution

                for resolvent in resolvents:
                    if not is_valid_clause(resolvent):
                        if resolvent not in cnf_clause_list and resolvent not in new_clauses_list[-1]:
                            new_clauses_list[-1].append(resolvent)

        if len(new_clauses_list[-1]) == 0:
            solution = False
            return new_clauses_list, solution
        cnf_clause_list += new_clauses_list[-1]

"""Ghi dữ liệu"""
def write_output_data(output_filename: str, new_clauses_list, solution):
    f = open(output_filename, 'w')
    for new_clauses in new_clauses_list:
        f.write(str(len(new_clauses)) + '\n')
        for clause in new_clauses:
            f.write(formated_clause(clause) + '\n')
    f.write('YES\n') if solution else f.write('NO\n')
    f.close()
    
#################################### Các hàm phụ ####################################    
    
"""Chuyển đổi mệnh đề logic sang dạng chuẩn CNF."""
def standard_cnf_sentence(cnf_sentence: list):
    std_cnf_sentence = []
    for clause in cnf_sentence:
        std_clause = standard_clause(clause)
        if not is_valid_clause(std_clause) and std_clause not in std_cnf_sentence:
            std_cnf_sentence.append(std_clause)
    return std_cnf_sentence

"""Chuyển đổi một mệnh đề thành dạng chuẩn."""
def standard_clause(clause: list):
    return sorted(list(set(deepcopy(clause))), key=lambda x: x[-1])

"""Kiểm tra phủ định"""
def are_complementary_literals(literal_1: str, literal_2: str):
    return len(literal_1) != len(literal_2) and literal_1[-1] == literal_2[-1]

"""Tạo mệnh đề phủ định của một mệnh đề CNF."""
def negation_of_cnf_sentence(cnf_sentence: list):
    neg_sentence = [[negation_of_literal(literal) for literal in clause] for clause in cnf_sentence]
    neg_cnf_sentence = generate_combinations(neg_sentence)
    return neg_cnf_sentence

"""Chuyển literal về dạng phủ định"""
def negation_of_literal(literal: str):
    if literal[0] == '-':
        return literal[1]
    return '-' + literal

"""Sinh các tổ hợp"""
def generate_combinations(set_list: list):
    combination_list, combination, depth = [], [], 0
    generate_combinations_recursively(set_list, combination_list, combination, 0)
    return combination_list

"""Tạo ra tất cả các tổ hợp có thể từ một danh sách các tập hợp"""
def generate_combinations_recursively(set_list: list, combination_list: list, combination: list, depth: int):
    if depth == len(set_list):
        combination_list.append(deepcopy(combination))
        return

    for element in set_list[depth]:
        combination.append(deepcopy(element))
        generate_combinations_recursively(set_list, combination_list, combination, depth + 1)
        combination.pop()

"""Phân giải 2 mệnh đề"""
def resolve(clause_1: list, clause_2: list):
    resolvents = []
    for i in range(len(clause_1)):
        for j in range(len(clause_2)):
            if are_complementary_literals(clause_1[i], clause_2[j]):
                resolvent = clause_1[:i] + clause_1[i + 1:] + clause_2[:j] + clause_2[j + 1:]
                resolvents.append(standard_clause(resolvent))
    return resolvents

"""Định dạng mệnh đề"""
def formated_clause(clause):
    if is_empty_clause(clause):
        return '{}'

    formated_clause = ''
    for i in range(len(clause) - 1):
        formated_clause += str(clause[i]) + ' OR '
    formated_clause += str(clause[-1])

    return formated_clause

"""Kiểm tra mệnh đề rỗng"""
def is_empty_clause(clause: list):
    return len(clause) == 0

"""Kiểm tra mệnh đề hợp lệ"""
def is_valid_clause(clause):
    for i in range(len(clause) - 1):
        if are_complementary_literals(clause[i], clause[i + 1]):
            return True
    return False


"""Danh sách file input và output"""
INPUT_LIST = [r'INPUT/input_1.txt',r'INPUT/input_2.txt',r'INPUT/input_3.txt',r'INPUT/input_4.txt',r'INPUT/input_5.txt']
OUTPUT_LIST = [r'OUTPUT/output_1.txt',r'OUTPUT/output_2.txt',r'OUTPUT/output_3.txt',r'OUTPUT/output_4.txt',r'OUTPUT/output_5.txt']
TESTCASE_NUMBER = len(INPUT_LIST)

def main():
    for index in range(TESTCASE_NUMBER):
        alpha, KB = read_input_data(input_filename=INPUT_LIST[index])
        new_clauses_list, solution = pl_resolution(alpha, KB)
        write_output_data(output_filename=OUTPUT_LIST[index], new_clauses_list=new_clauses_list, solution=solution)


if __name__ == '__main__':
    main()
