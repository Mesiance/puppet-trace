# Puppet class tracer
___
This tool can be handy in case when you have a realy huge puppet manifests base and serching for puppet class calls (includes) becomes to pain.

**Current features:**
- Search for all includes of class with all levels of subincludes and print it as a tree, json or yaml
- Search if one class is in some of levels of includes of another class and print it as a chain


### Installing
`pip install puppet-trace --index-url https://gitlab.com/api/v4/projects/53420056/packages/pypi/simple`
### Usage
`puppet-trace [options] classname`

`classname` - class name which you want to check for includes

**options:**

  `--env-file <path to .env file>`
  Environments file. You can set it for some permanent params like path to puppet manifests directory.
  
  `-s, --seek <class to seek>`
  Seek the class in includes tree of onother class. Specify here class name that will be seeked.
  
  `-p, --path <path to manifests directory>`
  Path to puppet manifests directory. Default: your current directory
  
  `--format <format>`
  Output format. Available options '**tree**', '**json**', '**yaml**'