# SMake
Simple Make replacement for lazy developers that like Python.

## Requirements
`Python 3.6+`

## What is it for?
You think that Makefiles are confusing or unreadable? 
You're too lazy to go through CMake or Autotools? If so, SMake is for you.
It's simply a Python module that used in .py file links and compiles your C/C++ project.

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

## What compilers are available?

For now only 3 compilers are supported: gcc (`gcc`), g++ (`gcc_cpp`) and clang (`clang`).
In this example we will use `g++` compiler because we want to compile C++ files.

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

For Linux it's easy to install libraries via the package manager.
But what if you want specifically for Windows to add SFML `include/` and `lib/` directories?
With help comes `Smake.get_platform()`:

## Platform checking

```python
# SFML 2
if sm.get_platform().startswith('win'): # win32, win64
    sm.gcc_cpp.include_dirs.append('C:\\SFML2\\include')
    sm.gcc_cpp.library_dirs.append('C:\\SFML2\\lib')
```

## Linking and compiling

Now the easiest ones are left: linking and compiling. 
For this you use `Smake.link()` and `Smake.compile()` method, respectively.

```python
sm.gcc_cpp.link()
sm.gcc_cpp.compile()
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
       
    sm.gcc_cpp.link()
    sm.gcc_cpp.compile()
    
    # post-compile stuff
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
