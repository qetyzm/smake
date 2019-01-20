import smake

sm = smake.Smake()
sm.name = 'app'
sm.obj_dir = 'obj'
sm.bin_dir = 'build'
sm.gcc.sources = sm.merge(
    sm.wildcard('src/*.c'), 
    sm.wildcard('src/module/*.c'))
sm.gcc.compiler_flags = ['pedantic']
sm.gcc.warning_flags = ['all']
sm.gcc.linker_flags = ['sdl2']

if sm.get_platform().startswith("win"):
    sm.gcc.include_dirs.append("C:\\SDL2\\include")
    sm.gcc.library_dirs.append("C:\\SDL2\\lib")

sm.gcc.link()
sm.gcc.compile()

# post compile stuff
if sm.get_platform().startswith("linux") or sm.get_platform() == "darwin":
    target_path = sm.make_path('usr', 'bin', sm.name)
    sm.copy_executable_to(target_path)