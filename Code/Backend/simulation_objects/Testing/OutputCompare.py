with open('output_files/generated', 'r') as file:
    generated = [l.strip() for l in file.readlines()]

with open('output_files/handmade', 'r') as file:
    handmade = [l.strip() for l in file.readlines()]

in_both = []
in_generated = []
in_handmade = []

def add_if_not_there(item):
    if item not in in_both:
        in_both.append(item)

def highlight_list(inputlist, name):
    print(name)
    for item in inputlist:
        print(f"\t{item}")



for line in generated:
    if line not in handmade:
        in_generated.append(line)
    else:
        add_if_not_there(line)

for line in handmade:
    if line not in generated:
        in_handmade.append(line)
    else:
        add_if_not_there(line)


highlight_list(in_generated, "Generated")
highlight_list(in_handmade, "Handmade")
highlight_list(in_both, "Both")




