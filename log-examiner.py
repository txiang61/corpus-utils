# Examine logs to see if there were exceptions.
# If found exceptions in logs, trigger test minimizer
# to produce a test case.

# Assumptions:
# 0. Already has DLJC deployed in the pre-defined relative location.
# 1. Corpus alredy downloaded.
# 2. Has knowledge about common corpus file structure.

# Inputs:
# - corpus location
# - corpus file location #TODO: how to combine this with corpus location?
# - list of projects need to be examined
# - log file pattern: a relative path to the log file in each project
# - error pattern: a regex string represents the interesting error in logs
# - tool executable: a driver script for running test minimizer with the configuration of the target tool.
#                    e.g. ontology/dataflow/etc.
#                    this tool executable should takes following input:
#                      $1: exception pattern $* build cmd
#                       e.g. tool_exec 'an exception regex pattern' build cmd

# Two modes:
# 1. Given a location of corpus, examine whole corpus.
# 2. Given a location of corpus, and a list of projects,
#    examine these projects in the corpus.

# TODO:
# 1. Extract common logic from corpus scripts. Build them as a python module.
# 2. Improve run-dljc.sh, maybe rewrite it in python, to be more flexible on receiving parameters.

from multiprocessing import Pool
import sys, os
import yaml
import re
import subprocess
import shlex

CORPUS_FILE = "$jsr308/ontology/apache-common.yml"
CORPUS_LOCATION = "$jsr308/ontology/corpus"
LOG_FILE = "logs/infer.log"
CORPUS = None
EXCEPTION_PATTERN = None
TOOL_EXECUTABLE = "$jsr308/ontology/run-test-minimizer.sh"

def main(argv):
 
    global EXCEPTION_PATTERN, CORPUS
    EXCEPTION_PATTERN = re.compile("^\s*Exception: .*")
    with open (CORPUS_FILE) as corpus:
        CORPUS = yaml.load(corpus)["projects"]

    examined_projects = ["commons-compress", "commons-lang"]

    pool = Pool(4)
    pool.map(check_log, examined_projects)

def check_log(project_name):
    exceptions_context = list()
    exceptions = list()
    project = CORPUS[project_name]
    with open(os.path.join(CORPUS_LOCATION, project_name, LOG_FILE)) as log_file:
        log_content = log_file.readlines()
        for i, line in enumerate(log_content):
            if bool(re.search(EXCEPTION_PATTERN, line)):
                exceptions.append(re.escape(line.strip()))
                exceptions_context.append("".join(log_content[i - 2 : i + 3]))


    if len(exceptions) > 0:
        # TODO: extract this logic to a common module, share with run-tool-on-corpus.
        project_dir = os.path.join(CORPUS_LOCATION, project_name)
        os.chdir(project_dir)
        print "Enter directory: {}".format(project_dir)
        if project["clean"] == '' or project["build"] == '':
            print "Error: there were no build/clean cmd in project {}.".format(project_name)
        print "Cleaning project..."
        subprocess.call(shlex.split(project["clean"]))
        print "Cleaning done."

        cmd = [TOOL_EXECUTABLE, exceptions[0], project["build"]]

        print "Running test minimizer: {}".format(" ".join(cmd))
        rtn_code = subprocess.call(cmd)

if __name__ == "__main__":
    main(sys.argv)