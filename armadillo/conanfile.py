from conans import ConanFile, CMake, tools
from conans.errors import ConanException
import os


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
               "use_wrapper": [True, False]}
    default_options = "shared=True", "use_wrapper=True"
    generators = "cmake"
    source_folder_name = "armadillo-{0}".format(version)
    source_tar_file = "{0}.tar.xz".format(source_folder_name)

    def system_requirements(self):
        blas_package_name = None
        lapack_package_name = None
        hdf5_package_name = None
        if tools.os_info.linux_distro == "ubuntu":
            blas_package_name = "libblas-dev"
            lapack_package_name = "liblapack-dev"
            hdf5_package_name = "libhdf5-dev"
        elif tools.os_info.linux_distro == "arch":
            blas_package_name = "blas"
            lapack_package_name = "lapack"
            hdf5_package_name = "hdf5"

        installer = tools.SystemPackageTool()
        if blas_package_name and lapack_package_name:
            installer.install(blas_package_name)
            installer.install(lapack_package_name)

        if hdf5_package_name:
            installer.install(hdf5_package_name)

    def source(self):
        tools.download("http://sourceforge.net/projects/arma/files/{0}".format(
            self.source_tar_file),
                       self.source_tar_file)
        self.run("tar -xvf {0}".format(self.source_tar_file))
        os.remove(self.source_tar_file)
        os.rename(self.source_folder_name, "sources")
        config_filename = "sources/include/armadillo_bits/config.hpp"
        config_file = tools.load(config_filename)
        tools.save(config_filename, "#ifndef CONFIG_HPP\n#define CONFIG_HPP\n\n{0}\n#endif".format(config_file))

    def build(self):
        cmake = CMake(self)

        if self.options.use_wrapper:
            tools.replace_in_file(
                file_path="sources/include/armadillo_bits/config.hpp",
                search="// #define ARMA_USE_WRAPPER",
                replace="#define ARMA_USE_WRAPPER")
            cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        else:
            # Since wrapper is not used, then no library will be created. In
            # that case, shared option is not useful and we delete it
            del self.options.shared

        cmake.configure(source_folder="sources")
        cmake.build()

    def package(self):
        self.copy("armadillo", dst="include", src="sources/include")
        self.copy("*.hpp", dst="include/armadillo_bits",
                  src="sources/include/armadillo_bits")

        if self.options.use_wrapper:
            self.copy("*armadillo.dll", dst="bin", keep_path=False)
            self.copy("*armadillo.lib", dst="lib", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.so.*", dst="lib", keep_path=False)
            self.copy("*.a", dst="lib", keep_path=False)
            self.copy("*.dylib", dst="lib", keep_path=False)

    def _get_libraries_for_linking(self):
        """
        Get the correct libraries for linking providing the blas and lapack
        interface, as well as the hdf5 library.
        """
        if tools.os_info.linux_distro == "arch":
             return ["blas", "lapack", "hdf5"]
        else:
            return []

    def package_info(self):
        if self.options.use_wrapper:
            self.cpp_info.libs = ["armadillo"]
            if not self.options.shared:
                self.cpp_info.libs.extend(self._get_libraries_for_linking())
        else:
            self.cpp_info.libs = self._get_libraries_for_linking()

    def package_id(self):
        if not self.options.use_wrapper:
            # Without the wrapper armadillo is a header-only library
            self.info.header_only()
