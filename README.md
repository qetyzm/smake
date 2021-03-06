# SMake
Simple Make replacement for lazy developers that like Python.

## What is it for?
You think that Makefiles are confusing or unreadable? 
You're too lazy to go through CMake or Autotools? If so, SMake is for you.
It's simply a Python module that used in .py file links and compiles your C/C++ project.


## Requirements
- [Python](http://python.org) 3.6+
- Click (optional)

## Supported compilers

+ gcc
+ g++
+ clang

# Example code

Example for Hello world example:

`src/hello.c`:
```C
#include <stdio.h>

int main() {
    printf("Hello, SMakefile!\n");
    return 0;
}
```

`Smakefile.py`:
```python
import smake_buildtools
import click

sm = smake_buildtools.Smake()
sm.name = 'hello'
sm.obj_dir = 'obj'
sm.bin_dir = 'build'

@click.group()
def cli():
    pass
    
@cli.command()
def install():
    sm.gcc.sources = ['src/hello.c']
    sm.gcc.compiler_flags.append('pedantic')
    sm.gcc.warning_flags.append('all')       
    sm.gcc.link()
    sm.gcc.compile()

@cli.command()
def clean():
    sm.remove_dir(sm.obj_dir)
    sm.remove_dir(sm.bin_dir)

if __name__ == "__main__":
    cli()
```

## Running the script

`$ python ./SMakefile.py install`

# How to install

Using pip:

`$ pip install smake_buildtools`

# Okay, how to use it?
First you need to import SMake:

```python
import smake_buildtools
```

## Defining project
Then define your SMake project:

```python
sm = smake_buildtools.Smake()
sm.name = 'app'
sm.obj_dir = 'obj'
sm.bin_dir = 'build'
```

## Adding source files

You need to add some source files for compiler.
For example, we have sources in `src/` and `src/module` directories.
For this we can use two SMake methods: `Smake.wildcard` and `Smake.merge`. 

```python
sm.gcc_cpp.sources = sm.merge(
    sm.wildcard('src/*.cpp'),
    sm.wildcard('src/module/*.cpp')
)
```

## Compiler flags

Then add some flags (here we can use some SFML libs):

```python
sm.gcc_cpp.compiler_flags = ['pedantic', 'static']
sm.gcc_cpp.warning_flags = ['all']

# SFML 2
sm.gcc_cpp.linker_flags.append('sfml-graphics')
sm.gcc_cpp.linker_flags.append('sfml-window')
sm.gcc_cpp.linker_flags.append('sfml-system')
sm.gcc_cpp.linker_flags.append('sfml-audio')
```

## Platform checking

For Linux it's easy to install libraries via the package manager.
But what if you want specifically for Windows to add SFML `include/` and `lib/` directories?
With help comes `Smake.get_platform()`:

```python
# SFML 2
if sm.get_platform().startswith('win'): # win32, win64
    sm.gcc_cpp.include_dirs.append('C:\\SFML2\\include')
    sm.gcc_cpp.library_dirs.append('C:\\SFML2\\lib')
```

## Compiling and linking

Now the easiest ones are left: compiling and linking. 
For this you use `Smake.compile()` and `Smake.link()` method, respectively.

```python
sm.gcc_cpp.compile()
sm.gcc_cpp.link()
```

## Summary

As you can see, for normal user every line is very clear.
If someone wants to compile your code it's easy for them to see what values are used for what.

Example code:

```python
import smake_buildtools
import click

sm = smake_buildtools.Smake()
sm.name = 'app'
sm.obj_dir = 'obj'
sm.bin_dir = 'build'

@click.group()
def cli():
    pass
    
@cli.command()
def install():
    sm.gcc_cpp.sources = sm.merge(
        sm.wildcard('src/*.cpp'),
        sm.wildcard('src/module/*.cpp'))
    sm.gcc_cpp.compiler_flags = ['pedantic', 'static']
    sm.gcc_cpp.warning_flags = ['all']

    # SFML 2
    sm.gcc_cpp.linker_flags.append('sfml-graphics')
    sm.gcc_cpp.linker_flags.append('sfml-window')
    sm.gcc_cpp.linker_flags.append('sfml-system')
    sm.gcc_cpp.linker_flags.append('sfml-audio')
    if sm.get_platform().startswith('win'): # win32, win64
        sm.gcc_cpp.include_dirs.append('C:\\SFML2\\include')
        sm.gcc_cpp.library_dirs.append('C:\\SFML2\\lib')

    sm.gcc_cpp.compile()
    sm.gcc_cpp.link()
    
    # post-linking stuff
    if sm.get_platform().startswith('linux') or sm.get_platform() == 'darwin':
        target_path = sm.make_path('usr', 'bin', sm.name)
        sm.copy_executable_to(target_path)

@cli.command()
def clean():
    sm.remove_dir(sm.obj_dir)
    sm.remove_dir(sm.bin_dir)

if __name__ == '__main__':
    cli()
```

Save this as SMakefile.py in project root directory and run:

`$ python ./SMakefile.py install`
