from conans import ConanFile, CMake, tools


class EzprogressbarConan(ConanFile):
    name = "ezprogressbar"
    version = "2.1.1"
    license = "MIT"
    author = "Darlan Cavalcante Moreira (darcamo@gmail.com)"
    url = "https://github.com/darcamo/conan-recipes"
    description = "Provides some simple headers for progress bars in software"
    no_copy_source = True
    homepage = "https://github.com/spaulaus/ezprogressbar"

    def source(self):
        self.run("git clone https://github.com/spaulaus/ezprogressbar")
        # Note: This commit hash is one commit after v2.1.1. There was no
        # release after that but this commit removes a compiler warning. We
        # keep this recipe is 'version 2.1.1' even though it is one commit
        # after that.
        self.run("cd ezprogressbar && git checkout f8d1d72c69b31f5b9dcb82725bc7828844b2a7b3")

    def package(self):
        self.copy("ez*.hpp", dst="include/ezProgressBar", src="ezprogressbar")
