from cpt.packager import ConanMultiPackager

# if __name__ == "__main__":
#     # This dummy builder will be used only to generate all common builds. From
#     # there we will get the ones we are interested in and add them to another builder
#     builder_dummy = ConanMultiPackager(username="darcamo", channel="stable")

#     # Builder that we will actually run
#     builder = ConanMultiPackager(username="darcamo", channel="stable")
#     builder_dummy.add_common_builds(pure_c=False)

#     all_builds = builder_dummy.items
#     for settings, options, env_vars, build_requires, reference in all_builds:
#         options1 = options.copy()
#         options1["armadillo:use_system_libs"] = True
#         options2 = options.copy()
#         options2["armadillo:use_system_libs"] = False

#         builder.add(settings=settings, options=options1, env_vars=env_vars,
#                     build_requires=build_requires)
#         builder.add(settings=settings, options=options2, env_vars=env_vars,
#                     build_requires=build_requires)

#     builder.run()


if __name__ == "__main__":
    builder = ConanMultiPackager(username="darcamo", channel="stable")
    builder.add_common_builds(pure_c=False)
    builder.run()
