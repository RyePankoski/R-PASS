import secrets
import math
import sys
import os


def calculate_entropy(password, is_passphrase=False, num_words=None, wordlist_size=7776):
    if is_passphrase and num_words:
        return num_words * math.log2(wordlist_size)

    # Random character password entropy
    charset_size = 0

    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(not c.isalnum() for c in password):
        charset_size += 32

    if charset_size == 0:
        return 0

    entropy = len(password) * math.log2(charset_size)
    return entropy


class Password:
    def __init__(self):
        self.no_of_tokens = 12
        self.ascii_range_begin = 33
        self.ascii_range_end = 126

        self.spaces = False
        self.hyphens = True
        self.mixed = False

        if getattr(sys, 'frozen', False):
            # Running as exe
            base_path = sys._MEIPASS
        else:
            # Running as script
            base_path = os.path.dirname(__file__)

        with open(os.path.join(base_path, 'eff_list'), 'r') as f:
            lines = f.readlines()
            self.words = [line.split()[1] for line in lines]

    def generate_random_password(self):
        password = ''
        index = 0

        while index < self.no_of_tokens:
            password += (
                chr(secrets.randbelow(self.ascii_range_end - self.ascii_range_begin + 1) + self.ascii_range_begin))
            index += 1

        return password

    def generate_passphrase(self):
        password = ''
        index = 0

        choices = [" ", "-"]

        while index < self.no_of_tokens:
            password += secrets.choice(self.words)
            if index != self.no_of_tokens - 1:
                if self.hyphens:
                    password += "-"
                elif self.spaces:
                    password += " "
                elif self.mixed:
                    password += secrets.choice(choices)

            index += 1

        return password