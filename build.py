#!/usr/bin/python

conf = {}
link_template = "link-template.html"
link_directory = "docs"


def getConf(filename):
    import json
    global conf
    conf = json.loads(open(filename, "r").read())
    fo = open(filename, "w")
    fo.write(json.dumps(conf, indent=3, sort_keys=True))
    fo.close()

def shorter_url(url):
    # https://docs.google.com/forms/d/e/1FAIpQLScrQiV8_L550zqlyAKxsExL2ZZS7bQlK5kItu-S2U8PdK6nTg/viewform?usp=sf_link
    uriIndex = url.index("/", 8)
    uri = url[uriIndex:]
    if len(uri) > 10:
        uri = "..." + uri[-8:]
        return url[:uriIndex+1]+uri
    return url

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
    s = s.replace("{{LINK:TO_SHORT}}", str(shorter_url(to)))
    s = s.replace("{{LINK:TIME}}", str(time))
    
    fo.write(s)
    fo.close()

    print("Created: "+name)

def update_version(msg):
    from datetime import datetime

    fo = open(link_directory + "/VERSION", "w")
    ver = conf.get("version", "")
    time = datetime.now()

    fo.write("--- gonyyi.a ---\n")
    fo.write("Version: " + ver+"\n")
    fo.write("Updated: " + str(time)+"\n")
    if msg != "":
        fo.write("\n--- Change(s) --- \n" +msg+ "\n")

    fo.close()


def main():
    import sys

    getConf("conf.json")

    clean(conf.get("directory", ""),
          conf.get("link", {}).get("excludes", []))

    if len(sys.argv) > 1:
        update_version(" ".join(sys.argv[1:]))
        # ${{ github.event.head_commit.message }}
    else:
        update_version("")

    for link in conf.get("link", {}).get("links", []):
        create(link.get("link", ""), link.get("name", ""), link.get("to", ""), link.get("sec", ""))


if __name__ == "__main__":
    main()
