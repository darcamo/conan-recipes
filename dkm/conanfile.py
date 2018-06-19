from conans import ConanFile, CMake, tools


class DkmConan(ConanFile):
    name = "dkm"
    version = "master"
    license = "MIT"
    author = "Darlan Cavalcante Moreira (darcamo@gmail.com)"
    url = "https://github.com/darcamo/conan-recipes"
    description = ("This is a k-means clustering algorithm written in C++, "
                   "intended to be used as a header-only library. Requires "
                   "C++11. See https://github.com/genbattle/dkm")
    no_copy_source = True
    homepage = "https://github.com/genbattle/dkm"

    def source(self):
        self.run("git clone https://github.com/genbattle/dkm")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        # tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)",
#                               '''PROJECT(MyHello)
# include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
# conan_basic_setup()''')

    def package(self):
        self.copy("include/*.hpp", src="dkm")
