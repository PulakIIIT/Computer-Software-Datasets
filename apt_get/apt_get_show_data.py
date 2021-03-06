import subprocess
import json

with open("./list_of_all_apt_packages.txt", "r") as f:
    data = f.readlines()

def toJson(details):
    details = details.split("\n")
    dic = {}
    desc_flag = 0
    for line in details:
        if line=='':
            break
        elif desc_flag==0:
            field = line.split(":",1)[0]
            desc = line.split(":",1)[1]
            dic[field] = desc[1:]
            if field=="Description":
                desc_flag=1
        else:
            dic[field] += line
    return dic


package_dct = {}

for i, x in enumerate(data):
    if i % 3 == 2:
        package = x.split("/")[0]
        bashCommand = "apt show " + package
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        details = output.decode("utf-8")
        details = toJson(details)
        package_dct.update({package: details})

f = open('./processed_data.json', 'w')
f.write(json.dumps(package_dct))
f.close()
