from conans import ConanFile, CMake, tools
# from conans.errors import ConanException
import os
import shutil


class ArmadilloConan(ConanFile):
    build_policy = "missing"
    name = "armadillo"
    version = "8.500.1"
    license = "Apache License 2.0"
    author = "Darlan Cavalcante Moreira (darcamo@gmail.com)"
    url = "https://github.com/darcamo/conan-recipes"
    description = "C++ library for linear algebra & scientific computing"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "use_system_libs": [True, False]  # If true the recipe will use blas and lapack from system
    }
    default_options = "shared=True", "use_system_libs=True"
    generators = "cmake_find_package", "cmake_paths"
    source_folder_name = "armadillo-{0}".format(version)
    source_tar_file = "{0}.tar.xz".format(source_folder_name)

    def requirements(self):
        if self.settings.os == "Windows":
            self.options.use_system_libs = False

        if not self.options.use_system_libs:
            self.requires("lapack/3.7.1@darcamo/stable")
            self.requires("hdf5/1.10.1@darcamo/stable")

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("7z_installer/1.0@conan/stable")
            self.build_requires("cmake_installer/3.11.3@conan/stable")

    def system_requirements(self):
        if self.options.use_system_libs:
            # The 'system_lib_names' variable will have the names of the system
            # libraries to be installed
            if tools.os_info.linux_distro == "ubuntu":
                system_lib_names = (["libhdf5-dev", "libblas-dev", "liblapack-dev"])
            elif tools.os_info.linux_distro == "arch":
                system_lib_names = (["hdf5", "blas", "lapack"])
            else:
                system_lib_names = []

            installer = tools.SystemPackageTool()
            for lib in system_lib_names:
                installer.install(lib)

    def source(self):
        tools.download(
            "http://sourceforge.net/projects/arma/files/{0}".format(
                self.source_tar_file),
            self.source_tar_file)
        if self.settings.os == "Windows":
            self.run("7z x %s" % self.source_tar_file)
            tar_filename = os.path.splitext(self.source_tar_file)[0]
            self.run("7z x %s" % tar_filename)
            os.unlink(self.source_tar_file)
        else:
            self.run("tar -xvf {0}".format(self.source_tar_file))
        os.remove(self.source_tar_file)
        os.rename(self.source_folder_name, "sources")

        if not self.options.use_system_libs:
            tools.replace_in_file("sources/CMakeLists.txt", "project(armadillo CXX C)",
                                  '''project(armadillo CXX C)
                                  include(${CMAKE_SOURCE_DIR}/conan_paths.cmake)''')

    def config_options(self):
        # Armadillo warns shared lib doesn't work on MSVC
        if self.settings.compiler == "Visual Studio":
            self.options.shared = False

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        # Prevent cmake from stripping non-standard build paths -> cmake does
        # this o ensure the executable will use the system libraries and work
        # on any system it is deployed on. However, when armadillo is linked
        # with mkl cmake will strip the mkl path (since it is non-standard) and
        # then when we link with the generated armadillo library mkl will not
        # be found.
        cmake.definitions["CMAKE_INSTALL_RPATH_USE_LINK_PATH"] = True

        shutil.move("conan_paths.cmake", "sources/")
        cmake.configure(source_folder="sources", build_folder="sources")
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libdirs = ["lib", "lib64"]
        self.cpp_info.libs = ["armadillo"]
        if not self.options.shared:
            self.cpp_info.libs = ["armadillo", "hdf5", "lapack", "blas"]
