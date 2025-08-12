import re

class InputParser:
    def __init__(self):
        self._categories = {}

    @property
    def categories(self):
        return self._categories
    @categories.setter
    def categories(self, categories):
        self._categories = categories

    def parse_decklist(self, input:str) -> str:
        lines = input.splitlines()
        input_format = self.determine_input_format(lines)
        match input_format:
            case "TappedOutFront":
                self.parse_tappedout_front(lines)
        return self.LandFill_input()

    def LandFill_input(self):
        output = []
        for key in self.categories:
            output.extend(self.categories[key])
        return "\n".join(output)

    def parse_partner(self, input:str):
        if input == "":
            return None
        return input

    def determine_input_format(self, lines:list) -> str:

        if self.is_tappedout_front_label(lines[0]) and lines[1] == "":
            return "TappedOutFront"

        return "Failure"

    def parse_tappedout_front(self, lines:list) -> str:
        category = None
        for line in lines:
            if self.is_tappedout_front_label(line):
                category = line
                self.categories[category] = []
            elif self.is_tappedout_front_commander(line):
                self.categories[category].append(re.sub(r"^Commander: ", "", line))
            elif self.is_tappedout_card_line(line):
                self.categories[category].append(self.parse_tappedout_front_line(line))

    def parse_tappedout_front_line(self, line:str) -> str:
        badendings = [" *CMDR*", " Flip", "GC"]

        # 1. Remove leading "numberx " (e.g., "3x " or "12x ")
        new_line = re.sub(r"^\s*[0-9]*x\s+", "", line)
        line = new_line


        # 2. Remove any bad endings if present
        for ending in badendings:
            if line.endswith(ending):
                line = line[: -len(ending)].rstrip()  # trim and remove trailing space
                break  # stop after first match

        return line

    def is_tappedout_front_label(self, line:str) -> bool:
        return re.search(r".* \([0-9]*\)", line)

    def is_tappedout_card_line(self, line:str) -> bool:
        return re.search(r"[0-9]*x .*", line)

    def is_tappedout_front_commander(self, line:str) -> bool:
        return re.search(r"^Commander: .*", line)

