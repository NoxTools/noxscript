# Nox Script Compiler

_nsc_ is a compiler written in Python for Nox Script. The compiler generates an _obj_ file that can be loaded into Nox maps.


## How to use

First, download the [compiler](https://github.com/NoxTools/noxscript/releases/latest) from releases. Download `nsc.exe` for Windows and `nsc.linux` for Linux. Make sure you also download `builtins.h` into the same directory.

### Usage

```
>nsc -h
Usage: nsc [OPTIONS] SOURCE
    
  NoxScript 3.0 Compiler - By Andrew Wesie (zoaedk) and Brian Pak (cai)

Options:
  -o, --out TEXT  Output file path.
  -v, --verbose   Verbose mode. Displays script information.
  -h, --help      Show this message and exit.

```

Simply pass in the script source file name as an argument to the compiler.


## Screenshots
![demo](http://i.imgur.com/tna9eTz.png)

![wrong](http://i.imgur.com/IoJzMsX.png)
