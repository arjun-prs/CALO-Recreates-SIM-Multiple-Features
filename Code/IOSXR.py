import re
import json

print("""calo.py""")
__copyright__ = "Copyright (c) 2018-2021 Cisco Systems. All rights reserved."
print("\n" + __copyright__)


def prettify(result) -> list:
    master_result = []
    for line in result:
        lines = line.split("\n")
        master_result.append(lines[1])
    return master_result


def exbridgedomain(result) -> list:
    domain_list = []
    for segments in result:
        segment = segments.split("\n")
        for line in segment:
            if re.search("BDI", line):
                line = line.strip()
                temp = line[-3:]
                domain_list.append("bridge-domain " + temp)
    return domain_list


def exbdiinterface(lines, result, slist) -> list:
    scount = 0
    shcount, dhcount = exreq(lines, "show running-config")
    for i in range(shcount, dhcount):
        if re.search("!", lines[i]):
            scount = i
        for sparam in slist:
            if re.search(sparam, lines[i]):
                tresult = "!\n"
                for j in range(scount + 1, dhcount):
                    if re.search("!", lines[j]):
                        break
                    tresult += lines[j]
                if tresult not in result and re.search("interface", tresult):
                    result.append(tresult)
    return result


def resfilterin(result, keyword) -> list:
    master_result = []
    for lines in result:
        flag = True
        for ele in keyword:
            if not re.search(ele, lines):
                flag = False
        if flag:
            master_result.append(lines)
    return master_result


def resfilterout(result, keyword) -> list:
    master_result = []
    for lines in result:
        flag = True
        for ele in keyword:
            if re.search(ele, lines):
                flag = False
        if flag and lines not in master_result:
            master_result.append(lines)
    return master_result


def exfilter(lines, result) -> list:
    scount = 0
    shcount, dhcount = exreq(filename, "show running-config")
    vlist = []
    for ele in result:
        if re.search("route-map", ele):
            temp = ele.split(" ")
            i = [index for index, value in enumerate(temp) if value == "route-map"]
            for j in i:
                route = temp[j + 1]
                route = route.strip()
                vlist.append("route-map " + route)
    for i in range(shcount, dhcount):
        if re.search("!", lines[i]):
            scount = i
        for sparam in vlist:
            if re.search(sparam, lines[i]):
                tresult = "!\n"
                for j in range(scount + 1, dhcount):
                    if re.search("!", lines[j]):
                        break
                    tresult += lines[j]
                if tresult not in result:
                    result.append(tresult)

    return result


def exumplsbgp(lines, result) -> list:
    scount = 0
    shcount, dhcount = exreq(lines, "show running-config")
    slist = ["neighbour", "session-group", "community", "community-list"]
    for i in range(shcount, dhcount):
        if re.search("!", lines[i]):
            scount = i
        for sparam in slist:
            if re.search(sparam, lines[i]) and not re.search("snmp", lines[i]) and not re.search("aaa", lines[i]):
                tresult = "!\n"
                for j in range(scount + 1, dhcount):
                    if re.search("!", lines[j]):
                        break
                    tresult += lines[j]
                if tresult not in result:
                    result.append(tresult)
    return result


def exmplsbgp(lines) -> list:
    count = 0
    result = []
    slist = ["neighbour", "session", "community", ]
    for line in lines:
        count = count + 1
        for sparam in slist:
            if re.search(sparam, line) and re.search("!", lines[count - 2]):
                for lineno in range(count - 1, len(lines)):
                    if re.search("!", lines[lineno]):
                        break
                    result.append(lines[lineno])
                result.append("!")
    return result


def rexunifiedmpls(lines) -> list:
    result = []
    umpls = rexmpls(lines)
    fil = exfilter(lines, umpls)
    ibgp = exumplsbgp(lines, fil)
    result = result + umpls + fil + ibgp
    return result


def exreq(lines, reqs):
    scount = 0
    count = 0
    dcount = 0
    for line in lines:
        count += 1
        if re.search(reqs, line):
            scount = count
            break
    for i in range(scount + 1, len(lines)):
        if re.match(r'^end', lines[i]):
            dcount = i
            break
    return (scount, dcount)


def rxreq(lines, reqs) -> list:
    scount = 0
    count = 0
    dcount = 0
    master_result = []
    for line in lines:
        count += 1
        if re.search(reqs, line):
            scount = count
    for i in range(scount + 1, len(lines)):
        if re.search('!', lines[i]):
            count = dcount
            dcount = i
            tresult = "!\n"
            for j in range(count + 1, dcount):
                tresult += lines[j]
            if tresult != "!\n":
                master_result.append(tresult)
    return master_result


def exbgp(lines, result) -> list:
    scount = 0
    shcount, dhcount = exreq(filename, "show running-config")
    slist = ["bgp", "vpnv"]
    for i in range(shcount, dhcount):
        if re.search("!", lines[i]):
            scount = i
        for sparam in slist:
            if re.search(sparam, lines[i]) and not re.search("bgp-community", lines[i]) and not re.search("snmp",
                                                                                                          lines[i]):
                tresult = "\n!"
                for j in range(scount + 1, dhcount):
                    if re.search("!", lines[j]):
                        break
                    tresult += lines[j]
                if tresult not in result and not re.search("MGMT", tresult):
                    result.append(tresult)
    return result


def exospf(lines) -> list:
    result = []
    scount = 0
    shcount, dhcount = exreq(lines, "show running-config")
    slist = ["ospf"]
    for i in range(shcount, dhcount):
        if re.search("!", lines[i]):
            scount = i
        for sparam in slist:
            if re.search(sparam, lines[i]) and not re.search("snmp", lines[i]):
                tresult = "!\n"
                for j in range(scount + 1, dhcount):
                    if re.search("!", lines[j]):
                        break
                    tresult += lines[j]
                if tresult not in result:
                    result.append(tresult)
    return result


def exisis(lines) -> list:
    result = []
    scount = 0
    shcount, dhcount = exreq(lines, "show running-config")
    slist = ["isis"]
    for i in range(shcount, dhcount):
        if re.search("!", lines[i]):
            scount = i
        for sparam in slist:
            if re.search(sparam, lines[i]) and not re.search("snmp", lines[i]):
                tresult = "!\n"
                for j in range(scount + 1, dhcount):
                    if re.search("!", lines[j]):
                        break
                    tresult += lines[j]
                if tresult not in result:
                    result.append(tresult)
    return result


def exeigrp(lines) -> list:
    result = []
    scount = 0
    shcount, dhcount = exreq(lines, "show running-config")
    slist = ["eigrp"]
    for i in range(shcount, dhcount):
        if re.search("!", lines[i]):
            scount = i
        for sparam in slist:
            if re.search(sparam, lines[i]) and not re.search("snmp", lines[i]):
                tresult = "!\n"
                for j in range(scount + 1, dhcount):
                    if re.search("!", lines[j]):
                        break
                    tresult += lines[j]
                if tresult not in result:
                    result.append(tresult)
    return result


def exstatic(lines) -> list:
    result = []
    scount = 0
    shcount, dhcount = exreq(lines, "show running-config")
    slist = ["ip route"]
    for i in range(shcount, dhcount):
        if re.search("!", lines[i]):
            scount = i
        for sparam in slist:
            if re.search(sparam, lines[i]) and not re.search("snmp", lines[i]):
                tresult = "!\n"
                for j in range(scount + 1, dhcount):
                    if re.search("!", lines[j]):
                        break
                    tresult += lines[j]
                if tresult not in result:
                    result.append(tresult)
    return result


def exigp(lines) -> list:
    result = []
    scount = 0
    shcount, dhcount = exreq(lines, "show running-config")
    slist = ["ospf", "isis", "eigrp", "ip route"]
    for i in range(shcount, dhcount):
        if re.search("!", lines[i]):
            scount = i
        for sparam in slist:
            if re.search(sparam, lines[i]) and not re.search("snmp", lines[i]):
                tresult = "!\n"
                for j in range(scount + 1, dhcount):
                    if re.search("!", lines[j]):
                        break
                    tresult += lines[j]
                if tresult not in result:
                    result.append(tresult)
    return result


def exmpls(lines, result):
    scount = 0
    shcount, dhcount = exreq(lines, "show running-config")
    slist = ["mpls"]
    for i in range(shcount, dhcount):
        if re.search("!", lines[i]):
            scount = i
        for sparam in slist:
            if re.search(sparam, lines[i]) and not re.search("snmp", lines[scount + 2]):
                tresult = "!\n"
                for j in range(scount + 1, dhcount):
                    if re.search("!", lines[j]):
                        break
                    tresult += lines[j]
                if tresult not in result and not re.search("encapsulation", tresult) and not re.search("MGMT", tresult) and not re.search( "qos", tresult):
                    result.append(tresult)
    return result


def rexmpls(lines) -> list:
    igp = exigp(lines)
    bgp = exbgp(lines, igp)
    mpls = exmpls(lines, bgp)
    mplsf = exvrfint(lines, mpls)
    bdi = exbridgedomain(mplsf)
    mplsf = exbdiinterface(lines, mplsf, bdi)
    result = []
    for r in mplsf:
        result.append(r)
    return result


def exvrfint(lines, result) -> list:
    scount = 0
    shcount, dhcount = exreq(filename, "show running-config")
    vlist = []
    for ele in result:
        if re.search("vrf forwarding", ele):
            temp = ele.split(" ")
            i = temp.index("vrf")
            vlist.append("vrf definition " + temp[i + 2])
    for i in range(shcount, dhcount):
        if re.search("!", lines[i]):
            scount = i
        for sparam in vlist:
            if re.search(sparam, lines[i]):
                tresult = "!\n"
                for j in range(scount + 1, dhcount):
                    if re.search("!", lines[j]):
                        break
                    tresult += lines[j]
                if tresult not in result and not re.search("MGMT", tresult) and not re.search("mgmt", tresult):
                    result.append(tresult)
    return result


def ospf_json(lines) -> list:
    i = 10
    dictionary = []
    while i < len(lines):
        line = lines[i].split()
        if line[0] == "O":
            temp = {"dest": line[1], "exit": line[-1]}
            dictionary.append(temp)
        i += 1
    return dictionary


def eigrp_json(lines) -> list:
    i = 10
    dictionary = []
    while i < len(lines):
        line = lines[i].split()
        if line[0] == "D":
            temp = {"dest": line[1], "exit": line[-1]}
            dictionary.append(temp)
        i += 1
    return dictionary


def bgp_json(lines) -> list:
    i = 13
    neighbor_list = []
    while i < len(lines):
        line = lines[i].split()
        neighbor_list.append(line[0])
        i += 1
    return neighbor_list


def mpls_json(lines) -> list:
    i = 10
    dictionary = []
    while i < len(lines):
        word = lines[i].split()
        if word[0] == "*>":
            temp = {"dest": word[1], "exit": word[2]}
            dictionary.append(temp)
        i += 1
    return dictionary


def multicast_json(lines) -> list:
    i = 18
    dictionary = []
    temp = {"dest": [], "exit": []}
    while i < len(lines):
        line = lines[i].split()
        if len(line) > 5:
            if line[5] == "flags:":
                dictionary.append(temp)
                temp = {"dest": [], "exit": []}
                if line[0] == "(*,":
                    temp["dest"].append("Rendezvous Point")
                else:
                    temp["dest"].append(line[0])
                temp["dest"].append(line[1])
        if len(line) > 1:
            if line[1] == "Forward/Sparse-Dense,":
                temp["exit"].append(line[0])
        i += 1
    return dictionary[1:]


u = "y"
while u == "y":
    result = []
    flag = True
    user_input0 = input("Do you need to filter running configurartion or ip route configuration (run/route): ")
    if user_input0 == "run":
        user_input1 = input("Do you need IOSXR or IOSXE configuration filter (xe/xr): ")
        filename = 'Input\\ios' + user_input1 + ' config.txt'
        f = open(filename, 'r')
        lines = f.readlines()
        if user_input1 == "xr":
            user_input2 = "bgp"
            result = rxreq(lines, "Show run router bgp")
        elif user_input1 == "xe":                                                                                         
            user_input2 = input("Which running configuration do you need: (igp/eigrp/static/ospf/isis/mpls/unified_mpls) ")
            if user_input2 == "igp":
                result = exigp(lines)
            elif user_input2 == "eigrp":
                result = exeigrp(lines)
            elif user_input2 == "ospf":
                result = exospf(lines)
            elif user_input2 == "isis":
                result = exisis(lines)
            elif user_input2 == "static":
                result = exstatic(lines)
            elif user_input2 == "mpls":
                result = rexmpls(lines)
            elif user_input2 == "unified_mpls":
                result = rexunifiedmpls(lines)
            elif user_input2 == "multicast":
                result.append("Feature still under development")
                flag = False
            else:
                result.append("Invalid Input")
                flag = False
        filename = 'Output\\' + user_input1 + ' show run (filtered) ' + user_input2 + '.txt'
        with open(filename, 'w+') as fout:
            for lines in result:
                fout.write(lines)
    elif user_input0 == "route":
        user_input2 = input("Which routes do you want to display: (eigrp/ospf/bgp/mpls/multicast) ")
        filename = 'Input\\show ip route ' + user_input2 + '.txt'
        f = open(filename, 'r')
        lines = f.readlines()
        if user_input2 == "ospf":
            result = ospf_json(lines)
        elif user_input2 == "eigrp":
            result = eigrp_json(lines)
        elif user_input2 == "bgp":
            result = bgp_json(lines)
        elif user_input2 == "mpls":
            result = mpls_json(lines)
        elif user_input2 == "multicast":
            result = multicast_json(lines)
        else:
            result.append("Invalid Input")
            flag = False
        filename = 'Output\\show ip route ' + user_input2 + '.json'
        with open(filename, 'w+') as fout:
            json.dump(result, fout)
    else:
        result.append("Invalid Input")
        flag =False
    if flag == True and user_input0 == "run":
        pretty_result = prettify(result)
        # print(*pretty_result, sep="\n")
        print("Size of filtered Output: ", end='')
        print(len(result))
        user_input3 = input("Do you want to filter the result further (y/n): ")
        if user_input3 == "y":
            keyword = input("Please enter keywords to include in space seperated format: ")
            filtered_result = resfilterin(result, keyword.split())
            keyword = input("Please enter keywords to exclude in space seperated format: ")
            filtered_result = resfilterout(filtered_result, keyword.split())
            # print(*filtered_result, sep="\n")
            print("Size of further filtered Output: ", end='')
            print(len(filtered_result))
            with open('Output\\' + user_input1 + ' show run ' + user_input2 + ' filtered result.txt', 'w+') as fout:
                for lines in filtered_result:
                    fout.write(lines)
    else:
        print(*result, sep="\n")   
    u = input("Do you want to continue (y/n): ")
f.close()
fout.close()
