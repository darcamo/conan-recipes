from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(username="darcamo", channel="stable")
    builder.add(options={"imgui-sfml:shared": True})
    builder.add(options={"imgui-sfml:shared": False})
    builder.run()
