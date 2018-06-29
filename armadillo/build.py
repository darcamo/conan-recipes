from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="darcamo", channel="stable")

    # builder.add(options={"armadillo:shared": True,
    #                      "armadillo:use_system_libs": True})
    # builder.add(options={"armadillo:shared": False,
    #                      "armadillo:use_system_libs": True})
    # builder.add(options={"armadillo:shared": True,
    #                      "armadillo:use_system_libs": False})
    # builder.add(options={"armadillo:shared": False,
    #                      "armadillo:use_system_libs": False})
    builder.add_common_builds(pure_c=False)

    filtered_builds = []
    for settings, options, env_vars, build_requires, reference in builder.items:
        print(options)
        if settings['compiler.libcxx'] == 'libstdc++11':
            # options1 = options.copy()
            # options1["armadillo:use_system_libs"] = True
            # filtered_builds.append([settings, options1, env_vars, build_requires])
            options2 = options.copy()
            options2["armadillo:use_system_libs"] = False
            filtered_builds.append([settings, options2, env_vars, build_requires])

    builder.run()
