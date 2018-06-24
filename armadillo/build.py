from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="darcamo", channel="stable")
    # builder.add(options={"armadillo:use_wrapper": True,
    #                      "armadillo:shared": True})

    builder.add(options={"armadillo:shared": True,
                         "armadillo:use_system_libs": True})
    builder.add(options={"armadillo:shared": False,
                         "armadillo:use_system_libs": True})
    builder.add(options={"armadillo:shared": True,
                         "armadillo:use_system_libs": False})
    builder.add(options={"armadillo:shared": False,
                         "armadillo:use_system_libs": False})
    builder.run()
