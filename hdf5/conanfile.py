from conans import ConanFile, CMake, tools
import os
import shutil


class Hdf5Conan(ConanFile):
    name = "hdf5"
    version = "1.10.1"
    license = "BSD-style Open Source or Comercial"
    url = "https://github.com/darcamo/conan-recipes"
    author = "Darlan Cavalcante Moreira (darcamo@gmail.com)"
    description = "HDF5 is a data model, library, and file format for storing and managing data."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    requires = "zlib/1.2.11@conan/stable"

    def source(self):
        # https://bitbucket.hdfgroup.org/scm/hdffv/hdf5.git
        # Tag: hdf5-1_10_2
        git = tools.Git(folder="sources")
        git.clone("https://bitbucket.hdfgroup.org/scm/hdffv/hdf5.git",
                  "hdf5-{0}".format(self.version.replace(".", "_")))

        tools.replace_in_file("sources/CMakeLists.txt", "PROJECT (HDF5 C CXX)",
                              '''PROJECT(HDF5 C CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def configure(self):
        self.options["zlib"].shared = self.options.shared

    def build(self):
        cmake = CMake(self)

        if self.options["shared"]:
            cmake.definitions["BUILD_SHARED_LIBS"] = "ON"
        cmake.definitions["HDF5_BUILD_EXAMPLES"] = "OFF"
        cmake.definitions["HDF5_BUILD_TOOLS"] = "ON"
        cmake.definitions["HDF5_BUILD_HL_LIB"] = "OFF"
        cmake.definitions["HDF5_BUILD_CPP_LIB"] = "OFF"
        cmake.definitions["HDF5_ENABLE_Z_LIB_SUPPORT"] = "ON"
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = self.package_folder
        os.mkdir("build")
        shutil.move("conanbuildinfo.cmake", "build/")
        cmake.configure(source_folder="sources", build_folder="build")
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["hdf5"]
