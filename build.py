from conan.packager import ConanMultiPackager
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="bzip2:shared", pure_c=True)
    if platform.system() == "Windows": # Library not prepared to create a .lib to link with (only dll)
        # Remove shared builds in Windows
        filtered_builds = []
        for settings, options, env_vars, build_requires in builder.builds:
            if not options["bzip2:shared"]:
                filtered_builds.append([settings, options, env_vars, build_requires])
        builder.builds = filtered_builds

    builder.run()

