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
