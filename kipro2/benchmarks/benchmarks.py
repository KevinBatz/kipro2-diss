import os
import subprocess
from os.path import exists
import pickle

#--post
#"[c=i] + [not (c=i)]*0"
#--pre
#"[elow+4=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh)]*(1/5) + [not (elow+4=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh))]*\\infty"
#1,2,3,4


benchmarks = [(1,"brp1", "brp.pgcl", "totalFailed", "[toSend <= 4]*(totalFailed + 1) + [not (toSend <= 4)]*\\infty", "kind"),
(2,"brp2", "brp.pgcl", "totalFailed", "[toSend <= 6]*(totalFailed + 3) + [not (toSend <= 6)]*\\infty", "kind"),
(3,"brp3", "brp.pgcl", "totalFailed", "[toSend <= 8]*(totalFailed + 3) + [not (toSend <= 8)]*\\infty", "kind"),
(4,"brp4", "brp.pgcl", "totalFailed", "[toSend <= 20]*(totalFailed + 8) + [not (toSend <= 20)]*\\infty", "kind"),
(5,"brp5", "brp.pgcl", "totalFailed", "totalFailed + 0.25","bmc"),
(6,"brp6", "brp.pgcl", "totalFailed", "totalFailed + 0.5","bmc"),
(7,"brp7", "brp.pgcl", "totalFailed", "totalFailed + 0.75","bmc"),
(8,"brp8", "brp.pgcl", "totalFailed", "totalFailed + 1","bmc"),
(1,"geo1", "geo.pgcl", "x", "[c<=0]*(x+1) + [not (c<=0)]*x", "kind"),
(2,"geo2", "geo.pgcl", "x", "x+1", "kind"),
(3,"geo3", "geo.pgcl", "x", "x","bmc"),
(4,"geo4", "geo.pgcl", "x", "x+0.9","bmc"),
(5,"geo5", "geo.pgcl", "x", "x+0.9999999999999","bmc"),
(1,"rabin1", "rabin.pgcl", "[not (1=i)] + [(1=i)]*0", "[1<i & i<3 & phase=0] * (1/3) + [not (1<i & i<3 & phase=0)]*\\infty", "kind"),
(2,"rabin2", "rabin.pgcl", "[not (1=i)] + [(1=i)]*0", "[1<i & i<4 & phase=0] * (1/3) + [not (1<i & i<4 & phase=0)]*\\infty", "kind"),
(3,"rabin3", "rabin.pgcl", "[not (1=i)] + [(1=i)]*0", "[1<i & i<5 & phase=0] * (1/3) + [not (1<i & i<5 & phase=0)]*\\infty", "kind"),
(4,"rabin4", "rabin.pgcl", "[not (1=i)] + [(1=i)]*0", "[1<i & i<6 & phase=0] * (1/3) + [not (1<i & i<6 & phase=0)]*\\infty", "kind"),
(5,"rabin5", "rabin.pgcl", "[not (1=i)] + [(1=i)]*0", "[1<i & phase=0] * (0.2) + [not (1<i & phase=0)]*\\infty","bmc"),
(6,"rabin6", "rabin.pgcl", "[not (1=i)] + [(1=i)]*0", "[1<i & phase=0] * (0.225) + [not (1<i & phase=0)]*\\infty","bmc"),
(7,"rabin7", "rabin.pgcl", "[not (1=i)] + [(1=i)]*0", "[1<i & phase=0] * (0.25) + [not (1<i & phase=0)]*\\infty","bmc"),
(1,"fdr1", "fdr.pgcl", "[c=i] + [not (c=i)]*0", "[elow+1=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh)]*(1/2) + [not (elow+1=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh))]*\\infty", "kind"),
(2,"fdr2", "fdr.pgcl", "[c=i] + [not (c=i)]*0",
               "[elow+2=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh)]*(1/3) + [not (elow+2=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh))]*\\infty", "kind"),
(3,"fdr3", "fdr.pgcl", "[c=i] + [not (c=i)]*0",
               "[elow+3=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh)]*(1/4) + [not (elow+3=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh))]*\\infty", "kind"),
(4,"fdr4", "fdr.pgcl", "[c=i] + [not (c=i)]*0",
               "[elow+4=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh)]*(1/5) + [not (elow+4=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh))]*\\infty", "kind"),
(5,"fdr5", "fdr.pgcl", "[c=i] + [not (c=i)]*0",
               "[elow+2=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh)]*(1/4) + [not (elow+2=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh))]*\\infty","bmc"),
(6,"fdr6", "fdr.pgcl", "[c=i] + [not (c=i)]*0",
               "[elow+3=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh)]*(1/5) + [not (elow+3=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh))]*\\infty","bmc"),
(7,"fdr7", "fdr.pgcl", "[c=i] + [not (c=i)]*0",
               "[elow+4=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh)]*(1/6) + [not (elow+4=ehigh & n=ehigh-elow+1 & v=1 & c=0 & running=0 & (not (i < elow)) & (i <= ehigh))]*\\infty","bmc"),
              ]

dirname = os.path.dirname(__file__)
cmd_dir = dirname + "/../../"
pickle_dir = cmd_dir+"kipro2/benchmarks/"

timeout = 300

def run_benchs():
    success = []
    for (var, name, prog, post, pre, engine) in benchmarks:
        print(name)
        prog = cmd_dir + "kipro2/benchmarks/wp/" + prog
        to_exec = "cd " + cmd_dir + ('; poetry shell; python3 -m kipro2.cmd %s --post "%s" --pre "%s" --safestatistics "%s" --engine %s' % (prog, post, pre,pickle_dir+name+".pickle", engine))
        try:
            subprocess.call(to_exec, shell=True, timeout=timeout, executable='/bin/bash')
            success.append(name)
        except Exception as e:
            print("TO")

    print("successfull:")
    print(success)

def get_latex():

    res = ""
    first = True
    for (var, name, prog, post, pre, engine) in benchmarks:
        if var == 1:
            res += "%\n%\n%\n \hline \n"
            first = True
        pickle_file = pickle_dir + name + ".pickle"
        if exists(pickle_file):
            with open(pickle_file, 'rb') as picklef:
                statistics = pickle.load(picklef)

                ftime = str(statistics.formula_time).split(" ")[0]
                if ftime == "0.0":
                    ftime = "<0.01"

                stime = str(statistics.sat_time).split(" ")[0]
                if stime == "0.0":
                    stime = "<0.01"

                ttime = str(statistics.total_time).split(" ")[0]
                if ttime == "0.0":
                    ttime = "<0.01"

                res += "& " + str(var) + " & " + statistics.result + " & " + str(statistics.k) + " & " + str(statistics.final_size) + " & " + ftime + " & " + stime + " & " + ttime
                if first:
                    res += "\\rule{0pt}{2.3ex}"
                res += " \\\\ \n"
        else:
            res+= "& " + str(var) + " & TO & -- & -- & -- & -- & -- \\\\ \n"

        first = False

    print(res)

run_benchs()
get_latex()


