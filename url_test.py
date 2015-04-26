#!/usr/bin/env python
import re
import os
import requests
cmd = "dir /A-D /B url"
files_list = os.popen(cmd).readlines()
url_files = []
for i in files_list:
    i = i.strip("\n")
    url_files.append(i)
urls_for_next_test = {}
urls_counter = {}
for url_file in url_files:
    urls_for_next_test[url_file] = []
    urls_counter[url_file] = {"S":0,"F":0}
    with file("url\\" + url_file,"r") as url_read:
        url_list = url_read.readlines()[4:]
        url_list_fixed = []
        for i in url_list:
            i = i.strip("\n")
            url_list_fixed.append(i)
        for url in url_list_fixed:
            print url
            try:
                r = requests.get("http://"+ url, timeout=1)
            except Exception, e:
                print type(e)
                urls_counter[url_file]["F"] = urls_counter[url_file]["F"] + 1
            else:
                if r.status_code >= 400:
                    print r.status_code
                    urls_counter[url_file]["F"] = urls_counter[url_file]["F"] + 1
                else:
                    print "OK"
                    urls_for_next_test[url_file].append(url)
                    urls_counter[url_file]["S"] = urls_counter[url_file]["S"] + 1
for i in urls_for_next_test:
    with file("test_" + i + ".html","w") as url_test:
        url_test.write("<!DOCTYPE html>\n<html>\n<head>\n<title>test url</title>\n</head>\n<body>\n")
        counter_file = "S:%d,F:%d" % (urls_counter[i]["S"],urls_counter[i]["F"])
        url_test.write(counter_file+"</br>\n")
        for j in urls_for_next_test[i]:
            link = """<a href="%s" target="_blank">%s</a></br>\n""" % ("http://"+j,j)
            url_test.write(link)
        url_test.write("</body>\n</html>")