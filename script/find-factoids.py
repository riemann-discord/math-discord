import itertools
text = []
setup_line = 600
with open("../math-discord/preamble.tex") as f:
    for line in itertools.islice(f, setup_line, None):
        if ("DeclareFactoid" in line) or ("NewEntry" in line):
            factoid_name = line.split("{")[1][:-1]
            text.append(f"`\.{factoid_name}`")
        s = ",\n".join(text)
print(s)
