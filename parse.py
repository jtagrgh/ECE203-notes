from json import dump
from os import walk
from os import path
from os import chdir
from os import listdir
from os import getcwd

terms = {}

# Get list of all directoring without any ignore keywords
d_ignore = ["git", "scripts", "templates"]
all_dirs = [d[0] for d in walk("./") if not any(i in d[0] for i in d_ignore)];

header = open(path.join(all_dirs[0], "templates", "header.html"), "r");
middle = open(path.join(all_dirs[0], "templates", "middle.html"), "r");
footer = open(path.join(all_dirs[0], "templates", "footer.html"), "r");

root_dir = all_dirs[0]
next_dir = all_dirs[0]

for i in range(len(all_dirs)):
    chdir(next_dir)
    depth = len([x for x in all_dirs[i].split("/") if x != '']) - 1
    root_dir = "../" * depth + all_dirs[0]
    next_dir = "../" * depth + all_dirs[(i+1) % len(all_dirs)]

    cwd_dirs = [i for i in next(walk("./"))[1] if not any(k in i for k in d_ignore)]

    unparsed_lines = []
    parsed_lines = [f"\t\t<!-- {all_dirs[i]} -->\n"]
    toc_lines = []

    if (len(cwd_dirs) > 0):
        toc_lines = [
            "<h3>table-of-contents</h3>\n", 
            "<ul>\n", 
        ]

        for d in cwd_dirs:
            sub_path = path.join(all_dirs[i], d, "index.html")
            toc_lines.append(f"\t<li><a href=\"{sub_path}\">{d}</a></li>\n")

        toc_lines += [
            "</ul>"
        ]

    parsed_lines += toc_lines

    if "unparsed_index.html" not in listdir("./"):
        continue

    with open("unparsed_index.html", "r") as f:
        for line in f:
            unparsed_lines.append(line)

    for line in unparsed_lines:
        line_split = line.split("$")
        if len(line_split) <= 1:
            parsed_lines.append("\t\t" + line)
            continue
        for i in range(1, len(line_split), 2):
            obj = line_split[i].replace("$", "")
            for d in all_dirs:
                if obj in d: # Object name is in directory name
                    html = "<a href=\"" + path.join(d, "index.html")  + "\">" + obj + "</a>"
                    line_split[i] = html
                    break
        line = "".join(line_split)
        parsed_lines.append("\t\t" + line)

    with open("index.html", "w") as f:
        for line in header:
            f.write(line);
        header.seek(0);

        f.write(f"\t\t<base href=\"{root_dir}\">\n")

        for line in middle:
            f.write(line);
        middle.seek(0);

        for line in parsed_lines:
            f.write(line)

        for line in footer:
            f.write(line);
        footer.seek(0);


header.close()
middle.close()
footer.close()

print("Done parsing")
