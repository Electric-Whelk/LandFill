import re

from simulation_objects.GameCards import Land, Spell


class InputParser:
    def __init__(self):
        self._categories = {}
        self._editions = {}
        self._input_format = None
        self._default = "DEFAULT"
        self._cardcats = {}
        self._has_cats = True
        self._landcat = None

    @property
    def landcat(self):
        return self._landcat
    @landcat.setter
    def landcat(self, value):
        self._landcat = value

    @property
    def has_cats(self):
        return self._has_cats
    @has_cats.setter
    def has_cats(self, has_cats):
        self._has_cats = has_cats

    @property
    def cardcats(self):
        return self._cardcats
    @cardcats.setter
    def cardcats(self, cardcats):
        self._cardcats = cardcats

    @property
    def default(self):
        return self._default

    @property
    def editions(self):
        return self._editions
    @editions.setter
    def editions(self, editions):
        self._editions = editions

    @property
    def input_format(self):
        return self._input_format
    @input_format.setter
    def input_format(self, value):
        self._input_format = value

    @property
    def categories(self):
        return self._categories
    @categories.setter
    def categories(self, categories):
        self._categories = categories

    def refresh_deck_submission(self):
        self._categories = {}
        self._editions = {}
        self._input_format = None
        self._default = "DEFAULT"
        self._cardcats = {}
        self._has_cats = True
        self._landcat = None


    def decklist_to_categories(self, decklist):
        self.landcat = self.determine_landcat(decklist)
        decklist = self.assign_attributes(decklist)
        tmpcats = self.copycat()

        for card in decklist:
            self.insert_gamecard_from_name(card, tmpcats)

        self.cardcats = tmpcats
        self.has_cats = not self.default in self.cardcats.keys()
        return tmpcats

    def insert_gamecard_from_name(self, card, tmpcats):
        #checks categories to see if a card with a given name is there
        #if it is, adds it to the equivalent location in tmpcat
        #if it isn't, adds it to tmpcat[landcat]
        location = self.card_in_categories(card)
        if location is None:
            self.handle_unknown_card(card, tmpcats)
            #tmpcats[self.landcat].append(card)
        else:
            tmpcats[location].append(card)

    def handle_unknown_card(self, card, tmpcats):
        edge_cases = {
            "Song of Eärendil":"Song of Earendil"
        }
        if card.name in edge_cases:
            location = self.name_in_categories(edge_cases[card.name])
        else:
            sides = card.name.split(" // ")
            location = self.name_in_categories(sides[0])
            if location is None and len(sides) > 1:
                location = self.name_in_categories(sides[1])
        if location is None:
            tmpcats[self.landcat].append(card)
        else:
            tmpcats[location].append(card)



    def copycat(self):
        output = {}
        for key in self.categories:
            output[key] = []

        outkeys = output.keys()
        if self.landcat not in outkeys:
            output[self.landcat] = []

        return output



    def assign_attributes(self, decklist):
        #assigns the count of each card (deleting multipled)
        #if the card is new, sets its "added" variable to true
        #gives the card an Edition
        #returns the decklist but with all duplicate cards removed

        as_dict = {}
        for card in decklist:
            if card.name not in as_dict.keys():
                as_dict[card.name] = card
                card.added = self.card_in_categories(card) is None
                try:
                    card.edition = self.editions[card.name]
                except KeyError:
                    pass
                card.count = 1
            else:
                as_dict[card.name].count += 1

        output = []
        for key in as_dict:
            output.append(as_dict[key])

        return output


    def card_in_categories(self, card):
        for key in self.categories:
            for name in self.categories[key]:
                if name == card.name:
                    return key
        return None

    def name_in_categories(self, input):
        for key in self.categories:
            if input in self.categories[key]:
                    return key
        return None




    def assign_categories_to_cards(self, decklist):
        landcat = self.determine_landcat(decklist)

        for card in decklist:
            for key in self.categories:
                if card.name in self.categories[key]:
                    card.category = key
                    break
            if card.name in self.editions.keys():
                card.edition = self.editions[card.name]
            if not card.mandatory:
                card.category = landcat

    def determine_landcat(self, decklist):
        if self.default in self.categories.keys():
            return self.default
        for card in decklist:
            if isinstance(card, Land) and card.mandatory:
                for key in self.categories:
                    if card.name in self.categories[key]:
                        return key
        if "Land" in self.categories.keys():
            return "Land"
        return "Lands"


    def format_moxbox_lands(self):
        tmp = []
        for card in self.cardcats[self.landcat]:
            tmp.append(self.format_moxbox_line(card))
        return self.add_newlines(tmp)

    def format_tappedout_lands(self):
        tmp = []
        for card in self.cardcats[self.landcat]:
            tmp.append(self.format_tappedout_line(card))
        return self.add_newlines(tmp)

    def format_archidekt_lands(self):
        tmp = []
        for card in self.cardcats[self.landcat]:
            tmp.append(f"{self.format_tappedout_line(card)} [{self.landcat}]")
        return self.add_newlines(tmp)





    def format_for_moxbox(self):
        tmp = []
        for key in self.cardcats:
            for card in self.cardcats[key]:
                tmp.append(self.format_moxbox_line(card))
        return self.add_newlines(tmp)

    def format_moxbox_line(self, card):
        return f"{card.count} {card.name}"

    def format_for_archidekt(self):
        if not self.has_cats:
            return self.add_newlines([self.format_archidekt_line(x) for x in self.cardcats[self.default]])
        tmp = []
        for key in self.cardcats:
            for card in self.cardcats[key]:
                tmp.append(f"{self.format_archidekt_line(card)} [{key}]")
        return self.add_newlines(tmp)


    def format_for_tappedout(self):
        if not self.has_cats:
            return self.add_newlines([self.format_tappedout_line(x) for x in self.cardcats[self.default]])

        tmp = []
        for key in self.cardcats:
            tmp.append(f"#{key}")
            for card in self.cardcats[key]:
                tmp.append(self.format_tappedout_line(card))
        return self.add_newlines(tmp)


    def add_newlines(self, lines):
        for i in range(len(lines) - 1):
            lines[i] = lines[i] + "\n"

        return "".join(lines)

    def format_tappedout_line(self, card):
        if isinstance(card, Spell) and card.commander:
            return f"{card.count}x {card.name} *CMDR*"
        return f"{card.count}x {card.name}"

    def format_archidekt_line(self, card):
        return f"{card.count}x {card.name}"



    def parse_decklist(self, input:str) -> str:
        lines = input.splitlines()
        input_format = self.determine_input_format(lines)
        self.input_format = input_format
        match input_format:
            case "TappedOutFront":
                self.parse_tappedout_front(lines)
            case "TappedOutBack":
                self.parse_tappedout_back(lines)
            case "MoxfieldFront":
                self.parse_moxfield_front(lines)
            case "MoxfieldBack":
                self.parse_moxfield_back(lines)
            case "ArchidektExport":
                self.parse_archidekt_export(lines)
            case "DeckboxExport":
                self.parse_deckbox_export(lines)
        return self.LandFill_input()

    def normalize_lines(self, lines):
        edge_cases = {
            "Song of Earendil": "Song of Eärendil"
        }
        output = []
        for line in lines:
            if line in edge_cases.keys():
                output.append(edge_cases[line])
            else:
                output.append(line)
        return output



    def LandFill_input(self):
        output = []
        for key in self.categories:
            for card in self.categories[key]:
                if len(card) != 0:
                    output.append(card)

            #output.extend(self.categories[key])
        return "\n".join(output)

    def parse_partner(self, input:str):
        if input == "":
            return None
        return input

    def determine_input_format(self, lines:list) -> str:
        for i in range(len(lines)):
            if lines[i] != "":
                break

        if self.is_archidekt_export(lines[i]):
            return "ArchidektExport"
        if self.is_tappedout_front_label(lines[i]) and lines[i+1] == "":
            return "TappedOutFront"
        if self.is_tappedout_back_label(lines[i]) or self.is_tappedout_card_line(lines[i]):
            return "TappedOutBack"
        if self.is_tappedout_front_label(lines[i]) and lines[i+1].isdigit:
            return "MoxfieldFront"
        if self.is_moxfield_back_label(lines[i]):
            return "MoxfieldBack"
        if self.is_deckbox_export_label(lines[i]):
            return "DeckboxExport"

        return "Failure"

    def parse_tappedout_front(self, lines:list) -> str:
        category = None
        for line in lines:
            if self.is_tappedout_front_label(line):
                category = re.sub(r" \([0-9]*\)", "", line)
                self.categories[category] = []
            elif self.is_tappedout_front_commander(line):
                self.categories[category].append(re.sub(r"^Commander: ", "", line))
            elif self.is_tappedout_card_line(line):
                self.categories[category].append(self.parse_tappedout_front_line(line))

    def parse_tappedout_back(self, lines):
        category = None
        for line in lines:
            if self.is_tappedout_back_label(line):
                category = re.sub(r"#", "", line)
                self.categories[category] = []
            elif self.is_tappedout_card_line(line):
                self.categories[category].append(self.parse_tappedout_front_line(line))

    def parse_moxfield_front(self, lines:list) -> str:
        category = None
        for line in lines:
            if self.is_tappedout_front_label(line):
                category = line
                self.categories[category] = []
            elif not line.isdigit():
                self.categories[category].append(line)

    def parse_deckbox_export(self, lines:list) -> str:
        self.categories[self.default] = []
        for line in lines:
            if line == "Sideboard:":
                pass
            else:
                line = line.strip()
                line = line.split(" // ")[0]
                tokenized = line.split(" ")
                title = tokenized[1:len(tokenized)]
                self.categories[self.default].append(" ".join(title))



    def parse_archidekt_export(self, lines:list) -> str:
        for line in lines:
            tokenized = line.split("[")
            category = tokenized[1].replace("]", "")
            tokenized = tokenized[0].split(" ")


            title = tokenized[1:-3]
            title = " ".join(title)
            title = title.split(" // ")[0]

            try:
                self.categories[category].append(title)
            except KeyError:
                self.categories[category] = [title]




    def parse_moxfield_back(self, lines:list) -> str:
        self.categories[self.default] = []
        for line in lines:
            tokenized = line.split(" ")
            title = tokenized[1:-3]
            title = " ".join(title)
            title = title.split(" // ")[0]
            self.editions[title] = tokenized[-2]
            self.categories[self.default].append(title)



    def parse_tappedout_front_line(self, line:str) -> str:
        badendings = [" *CMDR*", " Flip", "GC", "foil", "alteredfoil", " *fetch*", " *oversized*", " *f-etch*"]

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

    def is_tappedout_back_label(self, line:str) -> bool:
        return re.search(r"#.*", line)

    def is_moxfield_back_label(self, line:str) -> bool:
        return re.search(r"^[0-9]\s.*\s\([A-Z]*\)\s[0-9]*", line)

    def is_archidekt_export(self, line:str) -> bool:
        return re.search(r"^[0-9]x .* \(.*\) .* \[.*\]", line)

    def is_deckbox_export_label(self, line:str) -> bool:
        return re.search(r"^\s*[0-9] .*", line)


