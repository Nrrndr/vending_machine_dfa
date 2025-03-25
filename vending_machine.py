class DFA:
    def __init__(self, config_file):
        self.states = set()
        self.alphabet = []
        self.start_state = None
        self.accept_states = set()
        self.transitions = {}
        self.Return=[]
        self.load_config(config_file)
        self.current_state = self.start_state
        self.prices = set()
        self.path = []
        self.status="REJECTED"
        for s in self.alphabet:
            if (s.isalpha() and len(s)==1) or s.startswith("*"):
                self.prices.add(s)

        

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("States:"):
                    self.states = set(line.split(": ")[1].split(", "))
                elif line.startswith("Alphabet:"):
                    self.alphabet = line.split(": ")[1].split(", ")
                elif line.startswith("Start:"):
                    self.start_state = line.split(": ")[1]
                elif line.startswith("Accept:"):
                    self.accept_states = set(line.split(": ")[1].split(", "))
                elif line.startswith("Return:"):
                    self.Return = line.split(": ")[1].split(", ")
                elif line.startswith("Transitions:"):
                    continue
                elif line:
                    state_from, input_symbol, state_to = line.split()
                    if state_from not in self.transitions:
                        self.transitions[state_from] = {}
                    self.transitions[state_from][input_symbol] = state_to

    def reset(self):
        self.current_state = self.start_state
        self.path = [self.start_state]

    def process_input(self, input_symbol):
        if input_symbol in self.transitions.get(self.current_state, {}):
            self.current_state = self.transitions[self.current_state][input_symbol]
            self.path.append(self.current_state)
            return True
        else:
            self.path.append("Rejected")
            return False
    
    def get_path(self):
        return " → ".join(self.path)

    def get_available_drinks(self):
        available = [drink for drink in self.prices if drink in self.transitions.get(self.current_state, {})]
        return available

    def process_purchase(self, drink):
        if drink in self.prices and drink in self.transitions.get(self.current_state, {}):
            self.current_state = self.transitions[self.current_state][drink]
            self.path.append(self.current_state)
            return True
        else:
            return False
    
    def change(self,input_symbol):
        if input_symbol in self.Return:
            return True
        return False
    
    def auto_change(self):
        times="Kembalian:"
        while self.Return[0] in self.transitions.get(self.current_state, {}):
            self.current_state = self.transitions[self.current_state][self.Return[0]]
            self.path.append(self.current_state)
            if not self.current_state in self.accept_states:
                times+="1000,"
        if times.endswith(','):
            times = times[:-1]
        else :
            times+="0"
        if self.current_state in self.accept_states:
            self.path.append("Accepted")
            self.status="Accepted"
        return times

def vending_machine():
    dfa = DFA("config.txt")
    dfa.reset()
    print("Vending Machine DFA Simulator")
    while True:
        user_input = input(f"Masukkan uang atau beli minuman {dfa.alphabet}: ").strip()
        if user_input not in dfa.alphabet:
            print("Input tidak valid, coba lagi.")
            continue

        if dfa.change(user_input):
            kembalian=dfa.auto_change()
            print(f"Penukaran uang sudah dilakukan dengan Status: {dfa.status}")
            print(f"Lintasan DFA: {dfa.get_path()}")
            print(kembalian)
            break
        if user_input in dfa.prices:
            success = dfa.process_purchase(user_input)
            if success:
                kembalian=dfa.auto_change()
                print(f"Minuman {user_input} dapat dibeli. Status: {dfa.status}")
                print(f"Lintasan DFA: {dfa.get_path()}")
                print(kembalian)
                break

        if not dfa.process_input(user_input):
            print(f"Uang tidak cukup atau uang terlalu besar. Status: {dfa.status}")
            print(f"Lintasan DFA: {dfa.get_path()}")
            kembalian=dfa.auto_change()
            print(kembalian)
            break

        drinks = dfa.get_available_drinks()
        if drinks:
            print("ON: " + ", ".join([f"Minuman {d}" for d in drinks]))

if __name__ == "__main__":
    vending_machine()
