from conans import ConanFile, CMake, tools


class ConfiguruConan(ConanFile):
    name = "configuru"
    version = "0.4.1"
    license = "Public Domain"
    author = "Darlan Cavalcante Moreira (darcamo@gmail.com)"
    url = "https://github.com/darcamo/conan-recipes"
    description = "Configuru, an experimental JSON config library for C++x"
    no_copy_source = True
    homepage = "https://github.com/emilk/Configuru"

    def source(self):
        self.run("git clone https://github.com/emilk/Configuru")
        self.run("cd Configuru && git checkout v0.4.1")

    def package(self):
        self.copy("configuru.hpp", dst="include", src="Configuru")
