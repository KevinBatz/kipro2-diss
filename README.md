# kipro2-diss: k-Induction and Bounded Model Checking for Probabilistic Programs



## Contents

 1. Installation
 2. Usage
 3. Accepted Syntax for Loops
 4. License

## 1. Installation


We use [poetry](https://github.com/python-poetry/poetry) for dependency management.
See [here](https://python-poetry.org/docs/) for installation instructions for poetry.

In the root directory of this repository, run `poetry install` to install the dependencies in a new virtual environment. You are now ready to run cegispro2.

## 2. Usage

kipro2 is a Python 3 application using [pysmt](https://github.com/pysmt/pysmt) and [probably](https://github.com/Philipp15b/probably).
probably is a library built at the Software Modeling and Verification Group of RWTH Aachen to parse and work with pGCL programs and expectations.
Its internals are [quite extensively documented](https://philipp15b.github.io/probably/), so if there are questions about the input language of cegispro2, you might want to look there.

In the root directory of this repository, run `poetry shell` to enter the virtual environment. kipro2 can then be run via 

`python3 -m kipro2.cmd PROGRAM --post POST --pre PRE --engine ENG`

where
- PROGRAM is a path to a pgcl program parsed by the tool Probably (https://philipp15b.github.io/probably/) (you can find examples in the directories kipro2/benchmarks/wp)
- POST is a postexpectation in Guarded Normal Form (run python3 -m cegispro2.cmd --help for more info). Examples are given in the comments of the files contained in the above directories.
- POST is a preexpectation in Guarded Normal Form (run python3 -m cegispro2.cmd --help for more info). Examples are given in the comments of the files contained in the above directories.
- ENG is either kind (for k-induction) or bmc (for bounded model checking)


## 3. Accepted Syntax for Loops

Parsing of pGCL programs and expectations is done by the [probably](https://philipp15b.github.io/probably/) library.
There are many examples in the `benchmarks` directory.

An excerpt from the [Lark](https://github.com/lark-parser/lark) grammar for pGCL programs used in the probably library:
```
declaration: "nat" var bounds? -> nat

bounds: "[" expression "," expression "]"

instruction: "skip"                                      -> skip
           | "while" "(" expression ")" block            -> while
           | "if" "(" expression ")" block "else"? block -> if
           | var ":=" rvalue                             -> assign
           | block "[" expression "]" block              -> choice
           | "tick" "(" expression ")"                   -> tick

rvalue: "unif" "(" expression "," expression ")" -> uniform
      | expression

literal: "true"  -> true
       | "false" -> false
       | INT     -> nat
       | FLOAT   -> float
       | "∞"     -> infinity
       | "\infty" -> infinity
```

Expressions in programs and expectations can be built from the following operators, grouped by precedence:

1. `||`, `&`
2. `<=`, `<`, `=`
3. `+`, `-`
4. `*`, `:`
5. `/`
6. `not `, `( ... )`, `[ ... ]`, `literal`, `var`

Whitespace is generally ignored.

## 8. License

We provide cegispro2 under the Apache-2.0 license (see `LICENSE` file).

