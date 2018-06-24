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
               # "use_wrapper": [True, False],
               "use_system_libs": [True, False]  # If true the recipe will use blas and lapack from system
    }
    default_options = "shared=True", "use_system_libs=True"
    # default_options = "shared=True", "use_wrapper=True", "use_system_libs=True"
    generators = "cmake_find_package", "cmake_paths"
    source_folder_name = "armadillo-{0}".format(version)
    source_tar_file = "{0}.tar.xz".format(source_folder_name)

    def requirements(self):
        if self.settings.os == "Windows":
            self.options.use_system_libs = False

        if not self.options.use_system_libs:
            self.requires("lapack/3.7.1@darcamo/stable")

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("7z_installer/1.0@conan/stable")
            self.build_requires("cmake_installer/3.11.3@conan/stable")

    def system_requirements(self):
        # We will put the names of the system libraries to be installed here
        system_lib_names = []
        if tools.os_info.linux_distro == "ubuntu":
            system_lib_names.append("libhdf5-dev")
            if self.options.use_system_libs:
                system_lib_names.extend(["libblas-dev", "liblapack-dev"])
        elif tools.os_info.linux_distro == "arch":
            system_lib_names.append("hdf5")
            if self.options.use_system_libs:
                system_lib_names.extend(["blas", "lapack"])

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

        # config_filename = "sources/include/armadillo_bits/config.hpp"
        # config_file = tools.load(config_filename)
        # tools.save(
        #     config_filename,
        #     "#ifndef CONFIG_HPP\n#define CONFIG_HPP\n\n{0}\n#endif".format(
        #         config_file))

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
        # if self.options.use_wrapper:
        #     tools.replace_in_file(
        #         file_path="sources/include/armadillo_bits/config.hpp",
        #         search="// #define ARMA_USE_WRAPPER",
        #         replace="#define ARMA_USE_WRAPPER")
        #     cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        # else:
        #     # Since wrapper is not used, then no library will be created. In
        #     # that case, shared option is not useful and we delete it
        #     del self.options.shared
        #     del self.settings

        # shutil.move("conanbuildinfo.cmake", "sources/")
        shutil.move("conan_paths.cmake", "sources/")

        cmake.configure(source_folder="sources", build_folder="sources")
        cmake.build()
        cmake.install()

    # def _get_libraries_for_linking(self):
    #     """
    #     Get the correct libraries for linking providing the blas and lapack
    #     interface, as well as the hdf5 library.
    #     """
    #     if tools.os_info.linux_distro == "arch":
    #         return ["blas", "lapack", "hdf5"]
    #     else:
    #         return []

    def package_info(self):
        # TODO: test for self.settings.arch == "x86_64"
        self.cpp_info.libdirs = ["lib", "lib64"]
        self.cpp_info.libs = ["armadillo"]
        if not self.options.shared:
            self.cpp_info.libs = ["armadillo", "hdf5", "lapack", "blas"]

        # # self.cpp_info.libs = ["armadillo", "hdf5", "openblas", "lapack"]

        # if self.options.use_wrapper:
        #     self.cpp_info.libs = ["armadillo"]
        #     if not self.options.shared:
        #         self.cpp_info.libs.extend(self._get_libraries_for_linking())
        # else:
        #     self.cpp_info.libs = self._get_libraries_for_linking()

    # def package_id(self):
    #     if not self.options.use_wrapper:
    #         # Without the wrapper armadillo is a header-only library
    #         self.info.header_only()
