import argparse


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()
    
    def top(self):
        if self.items == []:
            return None
        else:
            return self.items[-1]

    def is_empty(self):
        return (self.items == [])
    
    def has_more_than_one(self):
        return len(self.items)>1


class Transition:
    def __init__(self, state_from, transition_symbol, state_to):
        self.state_from = state_from
        self.transition_symbol = transition_symbol
        self.state_to = state_to
    
    def __str__(self):
        return str(self.state_from)+'--('+str(self.transition_symbol)+')-->'+str(self.state_to)


class DFA:
    def __init__(self, states, transitions , initial_state, final_states, alphabets):
        self.states = states
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
        self.alphabets = alphabets

    
    def __str__(self):
        trans = ''
        for t in self.transitions:
            trans+= str(t) +' '
        return str(self.states)+'\n'+str(self.alphabets)+'\n'+str(self.initial_state)+'\n'+str(self.final_states)+'\n'+trans


def main(input, dfa, labels, actions):
    pointer = -1
    action = '"DEFAULT"'
    current_state = dfa.initial_state

    res = ''
    while input!='':
        for idx, c in enumerate(input):
            for transition in dfa.transitions:
                if transition.state_from == current_state and transition.transition_symbol == c:
                    current_state = transition.state_to
                    if current_state in dfa.final_states:
                        pointer = idx
                        action = actions[labels[current_state]]
                    break
        if pointer==-1:
            res+=input+', '+actions[labels[current_state]]+'\n'
            return res
        else:
            res+=input[:pointer+1]+', '+action+'\n'
            input = input[pointer+1:]
            current_state = dfa.initial_state
            pointer = -1
            action = '"DEFAULT"'   
    return res


if __name__ == '__main__':

    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--dfa-file', action="store", help="path of file to take as input to construct DFA", nargs="?", metavar="dfa_file")
    parser.add_argument('--input-file', action="store", help="path of file to take as input to test strings in on DFA", nargs="?", metavar="input_file")
    
    args = parser.parse_args()

    print(args.dfa_file)
    print(args.input_file)

    # get the file object
    output_file = open("task_3_1_result.txt", "w+")


    with open(args.dfa_file, "r") as file:
        f = file.readlines()
        states = f[0].strip('\n').split(',')

        alphabets = f[1].strip('\n').split(',')
        alphabets = [a for a in alphabets if a != ' ']

        initial_state = f[2].strip('\n')
        final_states = f[3].strip('\n').replace(' ', '').split(',')

        tranistions_line = f[4].strip('\n')
        tranistions_line = tranistions_line.replace(' ', '')
        tranistions_line = tranistions_line.replace('(', '')
        transitions_temp =  tranistions_line.split('),')

        transitions = []
        for transition in transitions_temp:
            transition = transition.replace(')', '')
            t = transition.split(',')
            transitions.append(Transition(t[0], t[1], t[2]))
        
        labels_line = f[5].strip('\n')
        labels_line = labels_line.replace(' ', '')
        labels_line = labels_line.replace('(', '')
        labels_temp =  labels_line.split('),')
        labels = {}
        for label in labels_temp:
            label = label.replace(')', '')
            t = label.split(',')
            labels[t[0]] = t[1]


        actions_line = f[6].strip().strip('\n')
        actions_line = actions_line.replace('(', '')
        actions_temp =  actions_line.split('),')
        actions = {}
        for action in actions_temp:
            action = action.strip().replace(')', '')
            t = action.strip().split(',')
            actions[t[0]] = t[1].strip()

        # print(states)
        # print(alphabets)
        # print(initial_state)
        # print(final_states)
        # print([str(t) for t in transitions])
        # print(labels)
        # print(actions)

        dfa = DFA(states, transitions, initial_state, final_states, alphabets)

        with open(args.input_file, "r") as file:
            for line in file.readlines():
                line = line.strip().strip('\n')
                output_file.write(main(line, dfa, labels, actions))

        output_file.close()