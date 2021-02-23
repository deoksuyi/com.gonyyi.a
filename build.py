#!/usr/bin/python

conf = {}
link_template = "link-template.html"
link_directory = "docs"


def getConf(filename):
    import json
    global conf
    conf = json.loads(open(filename, "r").read())


def clean(dst, excludes):
    import os
    files = os.listdir(dst)
    for fname in files:
        if fname.endswith(".html") and fname not in excludes:
            print("Delete: " + dst + "/" + fname)
            os.remove(dst + "/" + fname)


def create(link, name, to, time):
    if link == "" or name == "" or to == "" or time == "":
        print("Not created: "+name)
        return
    templ = open(link_template, "r")
    fo = open(link_directory + "/" + link + ".html", "w")

    s = templ.read()
    s = s.replace("{{LINK:NAME}}", str(name))
    s = s.replace("{{LINK:TO}}", str(to))
    s = s.replace("{{LINK:TIME}}", str(time))
    fo.write(s)
    fo.close()
    print("Created: "+name)

def main():
    getConf("conf.json")

    clean(conf.get("directory", ""),
          conf.get("link", {}).get("excludes", []))

    for link in conf.get("link", {}).get("links", []):
        create(link.get("link", ""), link.get("name", ""), link.get("to", ""), link.get("sec", ""))


if __name__ == "__main__":
    main()
