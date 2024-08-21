# from abc import abstractmethod
# from re import match, search
#
# class PasswordTest:
#     def __init__(self, test_name):
#         self.test_name = test_name
#
#     # To implement on a per class basis
#     @abstractmethod
#     def password_test(self, password, *args):
#         pass
#
#
# class PasswordTest_Regex:
#     def __init__(self, test_name, test_regex, regex_match_method):
#         super().__init__("PasswordTest")
#         self.test_name = test_name
#         self.test_regex = test_regex
#         self.regex_match_method = regex_match_method
#
#     def test_outcome(self, password_input):
#         """
#         Return the test outcome based on REGEX pattern for password input
#         """
#         if (self.regex_match_method == "match"):
#             return bool(match(self.test_regex, password_input))
#         else:
#             return bool(search(self.test_regex, password_input))
#
# # VALID CHARACTERS CHECKER
# hasValidChars = PasswordTest_Regex("hasValidChars", r"^[a-zA-Z0-9!@#$%^&*()_+-=]*$", "match")
#
# # PASSWORD LENGTH CHECKER
# isCorrectLength = PasswordTest_Regex("isCorrectLength", r"^.{8,20}$", "match")
#
# # CONTAINS UPPERCASE, LOWERCASE, NUMBER AND SPECIAL SYMBOL
# hasUppercase = PasswordTest_Regex("hasUppercase", r"[A-Z]+", "search")
# hasLowercase = PasswordTest_Regex("hasLowercase", r"[a-z]+", "search")
# hasNumber = PasswordTest_Regex("hasNumber", "\d+", "search")
# hasSpecialSymbol = PasswordTest_Regex("hasSpecialSymbol", r"[!@#$%^&*()]+", "search")
#
# # DOESN'T FOLLOW WALKING PATTERNS
# keyboard_horizontal_layout = {
#     "!": ["@"], "@": ["!", "#"], "#": ["@", "$"], "$": ["#", "%"], "%": ["$", "^"], "^": ["%", "&"], "&": ["^", "*"], "*": ["&", "("], "(": ["*", ")"], ")": ["(", "_"], "_": [")", "+"], "+": ["_"],
#     "1": ["2"], "2": ["1", "3"], "3": ["2", "4"], "4": ["3", "5"], "5": ["4", "6"], "6": ["5", "7"], "7": ["6", "8"], "8": ["7", "9"], "9": ["8", "0"], "0": ["9", "-"], "-": ["0", "="], "=": ["-"],
#     "q": ["w"], "w": ["q", "e"], "e": ["w", "r"], "r": ["e", "t"], "t": ["r", "y"], "y": ["t", "u"], "u": ["y", "i"], "i": ["u", "o"], "o": ["i", "p"], "p": ["o", "["], "["
# : ["p", "]"], "]": ["["],
# "a": ["s"],  "s": ["a", "d"], "d": ["s", "f"], "f": ["d", "g"], "g": ["f", "h"], "h": ["g", "j"], "j": ["h", "k"], "k": ["j", "l"], "l": ["k", ";"], ";": ["l", "'"], "'": [";", "\\"], "\\": ["'"],
#     "z": ["x"], "x": ["z", "c"], "c": ["x", "v"], "v": ["c", "b"], "b": ["v", "n"], "n": ["b", "m"], "m": ["n", ","], ",": ["m", "."], ".": [",", "/"], "/": ["."]
# }
#
# def keyboard_walking_test(password_input):
#     # True => Compliant, doesn't keyboard walk
#     # False => Non-compliant, keyboard walk detected
#     password_input = password_input.lower() # Capitalized letters don't affect if keyboard walking or not
#     num_adjacent_required = 6 # Number of adjacent characters to be considered as keyboard walking (too low will cause FP)
#     adjacent_tracker = 0
#     current_char_i = 0
#     while current_char_i < (len(password_input) - 1):
#         current_char = password_input[current_char_i]
#         next_char = password_input[current_char_i + 1]
#
#         #print("current_char_i", current_char_i, "current_char", password_input[current_char_i], "next_char", next_char, "password_input", password_input)
#
#         # Test for horizontal keyboard adjacency
#         if current_char in keyboard_horizontal_layout: # Only perform check if character is known
#
#             if next_char in keyboard_horizontal_layout[current_char]:
#                 adjacent_tracker = adjacent_tracker + 1
#             else:
#                 adjacent_tracker = 0
#
#             if adjacent_tracker == num_adjacent_required:
#                 return False
#
#         current_char_i = current_char_i+1
#
#     return True
#
#
#
# # DOESN'T MATCH COMMON THREAT ACTOR DICTIONARY(S)
# def known_hitlist(password_input, hitlist_text_file):
#     with open(hitlist_text_file, 'r', errors='ignore') as default_pw_hitlist:
#         for line_index, line in enumerate(default_pw_hitlist, 1):
#             #print(password_input, line)
#             line = line[:-1] # Remove newlines always placed at end of
#
#             if (password_input == line):
#                 print("Password matches weak password:", line, " used in hitlist:", hitlist_text_file)
#                 return False
#     return True
#
#
# # NO OBVIOUS COMPANY KEYWORDS (PREVENT CUSTOM DICTIONARY ATTACK)
#
# # Place all of these tests into an array
# regex_pw_tests_array = [hasValidChars, isCorrectLength, hasUppercase, hasLowercase, hasNumber, hasSpecialSymbol]
#
# # Go through each PW test and return the result against a test password for regex
# test_pw_input = "rockyou"
# print("Regex Tests --")
# for regex_pw_test in regex_pw_tests_array:
#     print(f"{regex_pw_test.test_name} => {regex_pw_test.test_outcome(test_pw_input)}")
#
# # Keyboard walk test
# print("noHorizontalKeyWalks => ", keyboard_walking_test(test_pw_input))
#
# # Dictionary tests
# print("notInKnownHitlist => ", known_hitlist(test_pw_input, "rockyou.txt"))
#
# # No tests fail, password compliant
# # return True
#
# #isCompliantPassword()