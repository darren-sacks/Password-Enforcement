# Define classes to be used for password tests
from re import match, search

class PasswordTest:
    def __init__(self, test_name):
        self.name = test_name
    def __str__(self):
        return self.name
    def test_outcome(self, password_str):
        pass

class PasswordTest_Regex(PasswordTest):
    def __init__(self, test_name, regex_method, regex_string):
        super().__init__(test_name)
        self.regex_method = regex_method
        self.regex_string = regex_string
    def test_outcome(self, password_str):
        """
        Return the test outcome based on REGEX pattern for password input
        """
        if (self.regex_method == "match"):
            return bool(match(self.regex_string, password_str))
        else:
            return bool(search(self.regex_string, password_str))

class PasswordTest_Dictionary(PasswordTest):
    def __init__(self, test_name, hitlist_file="rockyou.txt", useTransformations=False):
        super().__init__(test_name)
        self.hitlist_file = hitlist_file
        self.useTransformations = useTransformations
    def test_outcome(self, password_str):
        """
        Return the test outcome based on hitlist file
        """
        with open(self.hitlist_file, 'r', errors='ignore') as default_pw_hitlist:
            for line_index, line in enumerate(default_pw_hitlist, 1):
                        #print(password_str, line)
                        line = line[:-1] # Remove newlines always placed at end of

                        # Directed to apply transformations, useful for small number of custom keywords
                        if self.useTransformations:
                            # Create dictionary to map common LEET mappings as character sets for regex
                            leetmap_common = {"a": "[a4@]", "e": "[e3]", "o": "[o0]", "i": "[i1!]", "l": "[l1!]",
                                              "s": "[s$5]"}

                            current_word_leet_regex_pattern = ''.join(leetmap_common.get(char, char) for char in line.lower())

                            # print(current_word_leet_regex_pattern, password_str)

                            if bool(search(current_word_leet_regex_pattern, password_str.lower())):
                                print("Password looks similar to obvious keyword:", line, " used in hitlist:", self.hitlist_file)
                                return False
                        else:

                            if (password_str == line):
                                print("Password matches weak password:", line, " used in hitlist:", self.hitlist_file)
                                return False



        return True

class PasswordTest_KeyboardWalkHorizontal(PasswordTest):
    def __init__(self, test_name, consec_chars_allowed=5):
        super().__init__(test_name)
        self.consec_chars_allowed = consec_chars_allowed
    def test_outcome(self, password_str):
        """
        Return the test outcome based on HORIZONTAL keyboard walk threshold
        """
        # True => Compliant, doesn't keyboard walk
        # False => Non-compliant, keyboard walk detected

        password_input = password_str.lower() # Capitalized letters don't affect if keyboard walking or not
        adjacent_tracker = 0
        current_char_i = 0

        keyboard_horizontal_layout = {
        "!": ["@"], "@": ["!", "#"], "#": ["@", "$"], "$": ["#", "%"], "%": ["$", "^"], "^": ["%", "&"], "&": ["^", "*"], "*": ["&", "("], "(": ["*", ")"], ")": ["(", "_"], "_": [")", "+"], "+": ["_"],
        "1": ["2"], "2": ["1", "3"], "3": ["2", "4"], "4": ["3", "5"], "5": ["4", "6"], "6": ["5", "7"], "7": ["6", "8"], "8": ["7", "9"], "9": ["8", "0"], "0": ["9", "-"], "-": ["0", "="], "=": ["-"],
        "q": ["w"], "w": ["q", "e"], "e": ["w", "r"], "r": ["e", "t"], "t": ["r", "y"], "y": ["t", "u"], "u": ["y", "i"], "i": ["u", "o"], "o": ["i", "p"], "p": ["o", "["], "["
        : ["p", "]"], "]": ["["],
        "a": ["s"],  "s": ["a", "d"], "d": ["s", "f"], "f": ["d", "g"], "g": ["f", "h"], "h": ["g", "j"], "j": ["h", "k"], "k": ["j", "l"], "l": ["k", ";"], ";": ["l", "'"], "'": [";", "\\"], "\\": ["'"],
        "z": ["x"], "x": ["z", "c"], "c": ["x", "v"], "v": ["c", "b"], "b": ["v", "n"], "n": ["b", "m"], "m": ["n", ","], ",": ["m", "."], ".": [",", "/"], "/": ["."]
        }

        while current_char_i < (len(password_input) - 1):
            current_char = password_input[current_char_i]
            next_char = password_input[current_char_i + 1]

            #print("current_char_i", current_char_i, "current_char", password_input[current_char_i], "next_char", next_char, "password_input", password_input)

            # Test for horizontal keyboard adjacency
            if current_char in keyboard_horizontal_layout: # Only perform check if character is known

                if next_char in keyboard_horizontal_layout[current_char]:
                  adjacent_tracker = adjacent_tracker + 1
                else:
                    adjacent_tracker = 0

            if adjacent_tracker > self.consec_chars_allowed:
              return False

            current_char_i = current_char_i+1

        return True


password_tests = [
    PasswordTest_Regex("hasValidChars", "match", r"^[a-zA-Z0-9!@#$%^&*()_+-=]*$"),
    PasswordTest_Regex("isValidLength", "match", r"^.{8,20}$"),
    PasswordTest_Regex("hasUppercase", "search", r"[A-Z]+"),
    PasswordTest_Regex("hasLowercase", "search", r"[a-z]+"),
    PasswordTest_Regex("hasNumber", "search", "\d+"),
    PasswordTest_Regex("hasSpecialSymbol", "search", r"[!@#$%^&*()]+"),
    PasswordTest_Dictionary("notInThreatActorDicts"),
    PasswordTest_Dictionary("noObviousKeywords", "custom_hitlist.txt", True),
    PasswordTest_KeyboardWalkHorizontal("noHorizontalKeyboardWalk")
]
for password_test in password_tests:
    print(password_test, "=>", password_test.test_outcome("^&*()(+jeffrey"))