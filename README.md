# corpus-utils

### Corpus File Specification
Corpus file manages basic information of projects in the corpus.

A project should have below basic information:

- project name
- url linked to the project git repository
- build command
- clean command

A corpus file is wrriten in YAML/JSON format, and it is a dictionary which key is the project name, and value is a dictionary of the given project's attributes. See below concrete specification:

In YAML:

```yaml
---
projects:
  first project:
    giturl: first project's url
    build: first project's build command
    clean: first project's clean command
  second project:
    giturl: second project's url
    build: second project's build command
    clean: second project's clean command
```

or in JSON:

```
{
  "projects": {
    "first project": {
      "giturl": "first project's url",
      "build": "first project's build command",
      "clean": "first project's clean command"
    },
    "second project": {
      "giturl": "second project's url",
      "build": "second project's build command",
      "clean": "second project's clean command"
    }
  }
}
```

### Run corpus util script
`run-corpus.py` is a util script that helps you running your tool on a benchmark defined by a benchmark file.

Given a benchmark file, it fetching the projects in benchmark into your local machine, and then running your tool on these projects.

Usage:

```
run-corpus.py --corpus-file <your-benchmark-file> --executable <path-to-your-executable>
```

By running above command, it will fetching all projects in the benchmark file into a directory named as same as your benchamrk file name (e.g. into a dir named `xxx-corpus` if your corpus file name is `xxx-corpus.yml`). This directory will also located under the same directory where your benchmark file located in. Then it will running your tool on these projects.

An example of running this script:

```
run-corpus.py --corpus-file my-corpus.yml --executable jsr308/ReadChecker/run-dljc.sh
```

### TODO Works
#### Ideas on running experiment util
Motivation: During the work on my master thesis, I found running experiment and collecting results is a painful and tedious procedure. As a programmer, I naturely come up with this idea: "Why not let machine do the experiment and just give me the result as I desired?" Therefore I wish to have a util script that can automatically perform experiment and collect result. Here is a draft of the desire shape of that script:

- Input:
  - A configuration file, indicates (multiple) configuration setting of launching the tools (CF & CFI).
    It would has a similar format like below:
 ```yaml
 # in yaml
 # General setting that shared with all rounds of experiment.
 general-setting:
   -classpath:"appending customize classpath when launching CF & CFI. Useful for external type systems, default is empty."
   -cfArgs:
     #... detail cf args. describes as a dictionary.
   -cfiArgs:
     #... detail of cfi args. describes as a dictionary.
     -solverArgs:
       #... detail of solverArgs. describes as a dictionary.
 
 experiments:
   - with-preference:
     -cfiArgs:
       -enablePreference:true
   - without-preference:
       -enablePreference:false
```
  - A table description file, indicates what latex tables should be generated:
```yaml
basic_info_table:
  basic_data: [ "nFiles", "blank", "comment", "code"]
  
table1:
  use_built_in_table_format: "whether generate a latex table wrapper, or only table data is generated, default is false."
  basic_data: [ "constraint_size", "slot_size"]
  compare_data: ["total_inferred", "TOP", "BOTTOM", "SEQUENCE"]
```

- Output:
  A file stores all the latex table data I want.

Benifit of having this script:

- Focus on setting experiemnt configuration once, then I can run it multiple times with the confidence of getting results with same configuration. (it is very upset to found after running an experiment that one parameter is missing/set to wrong value, e.g. expect run Ontology with preference but forget passing preference=true).
- Get rid of manually collecting the table data, which is very tedious and time-exhuasting.
 
 
 

