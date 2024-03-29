from modules.lexical_aux import build_my_tree, build_ouput_file, dfa_mine, eval_tree, get_current_directory, get_start_accept, get_table_dict, get_tokens_sole, list_to_str, print_dfa_trans, reverse_dict, write_file
from modules.Lexical import Lexical
from modules.color_print import print_blue, print_yellow
import sys

def get_arg(param_index, default=None):
    """
        Gets a command line argument by index (note: index starts from 1)
        If the argument is not supplies, it tries to use a default value.

        If a default value isn't supplied, an error message is printed
        and terminates the program.
    """
    try:
        return sys.argv[param_index]
    except IndexError as e:
        if default:
            return default
        else:
            print(e)
            print(
                f"[FATAL] The comand-line argument #[{param_index}] is missing")
            exit(-1)    # Program execution failed.




def main():

    ## set default file for args
    lexical_file = get_arg(1, "/inputs/lexical.txt")
    program_file = get_arg(2, "/inputs/program.txt")

    ## get directory for lexical and program
    cd = get_current_directory()
    lex_file = lexical_file
    lex_path = cd + '/' +  lex_file
    program_path = cd + '/' + program_file

    ## build full dfa
    lx = Lexical()
    lx.lex_path = lex_path
    lx.program_path = program_path
    lx.run_scan()
    
    
    ac_tok = lx.dfa_stuff()

    for j in ac_tok:
        print(''.join(j),end='\t')

    dfa_tab = lx.machine.dfa_table

    print(len(dfa_tab))
    print("*"*20)
    
    ######################
    ## build symbol table
    ######################

    operators={'(', ')', 'STAR', 'OR', 'PLUS','CONCAT'}

     
    exp_rd_rev = reverse_dict(lx.lex_scan.expanded_rd)
    exp_rd_rev = lx.lex_scan.expanded_rd
    accepted_tokens = ac_tok.copy()

    visited_tokens = set()
    detection_table = {}

  
    #print_blue(lx.lex_scan.keywords)
    for k in accepted_tokens:
        k_str = ''.join(k)
        if k_str in lx.lex_scan.keywords:
            visited_tokens.add(tuple(k))
            detection_table[k_str] = k_str

    for k in accepted_tokens:
        k_str = ''.join(k)
        if k_str in lx.lex_scan.punctuations:
            visited_tokens.add(tuple(k))
            detection_table[k_str] = k_str

    for key, val in exp_rd_rev.items():

        tree1 = build_my_tree(val,operators.copy())
        tree1.assign_id()
        eval_tree(tree1)
        m = dfa_mine(tree1)
        # tree1.print_tree()

       
        acc_tokens = []
        for j in accepted_tokens:
           if tuple(j) not in visited_tokens:
               c =  get_tokens_sole(m, j.copy())
               if c:
                   visited_tokens.add(tuple(j))
                   detection_table[''.join(j)] = key
    
    
    symbol_table = build_ouput_file(accepted_tokens, detection_table)
    print("")
    
    print_blue(list_to_str(accepted_tokens))
    lexeme_path = cd + '/' + 'outputs'+ '/' + 'lexemes.txt'
    write_file(lexeme_path, list_to_str(accepted_tokens))



    #print(len(dfa_tab))
    print("*"*20)

    print("*.*. Stream of Tokens .*.*")
    print_yellow(symbol_table)
    output_path = cd + '/' + 'outputs' + '/' + 'tokens.txt'
    quote_tokens = []

    for i in symbol_table:
        quote_tokens.append("'" + str(i) + "'")


    write_file(output_path, quote_tokens)

    
    table_dict = get_table_dict(frozenset(dfa_tab))
    #print_dark_cyan(table_dict)

    print("\n*.*. Transition Table .*.*")
    print_dfa_trans(dfa_tab, table_dict)
    start, accept = get_start_accept(frozenset(lx.start_state), lx.accept_states, table_dict)
    print_yellow(f"Start State: {start}")
    print_yellow(f"Accept States: {accept}\n")
    
    







if __name__ == "__main__":
    main()