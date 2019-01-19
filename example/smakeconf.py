import smake

sm = Smake()
sm.name = "app"
sm.source_dirs = ["src", "src/module_1", "src/module_2"]
sm.compiler = "gcc"
sm.dependencies = ["sdl"]
sm.target = "build/" + sm.name

def post_compile():
    if sm.util.get_platform() == "linux":
        target = "/usr/bin/" + sm.name
        sm.copy_executable_to(target)


sm.post_compile_script = post_compile
sm.compile()