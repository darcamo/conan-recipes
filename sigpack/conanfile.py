from conans import ConanFile, CMake, tools
import os
import shutil

class SigpackConan(ConanFile):
    name = "sigpack"
    version = "1.2.4"
    license = "Mozilla Public License 2.0"
    author = "Darlan Cavalcante Moreira (darcamo@gmail.com)"
    url = "https://github.com/darcamo/conan-recipes"
    description = "SigPack is a C++ signal processing library using the Armadillo library as a base."
    generators = "cmake"
    source_zip_filename = "sigpack-{0}.zip".format(version)
    requires = ("armadillo/8.500.1@darcamo/stable",)

    def source(self):
        tools.download("https://sourceforge.net/projects/sigpack/files/sigpack-{0}.zip/download".format(self.version), self.source_zip_filename)
        tools.unzip(self.source_zip_filename)

        os.rename("sigpack-1.2.4/sigpack/", "sigpack")
        os.unlink(self.source_zip_filename)
        shutil.rmtree("sigpack-1.2.4/")

    def package(self):
        self.copy("*.h", dst="include", src="sigpack")
