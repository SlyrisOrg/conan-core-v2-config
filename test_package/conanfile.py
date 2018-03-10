from conans import ConanFile, CMake, tools
import os
import shutil


def get_parent(path):
    return os.path.dirname(path)


class CoreconfigTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    requires = "gtest/1.8.0@bincrafters/stable"

    def build(self):
        directory = get_parent(get_parent(os.getcwd()))
        self.run("git clone https://github.com/SlyrisOrg/core-v2")
        shutil.copy(os.getcwd() + "/core-v2/tests/config-test/config-test.cpp", directory + "/config-test.cpp")
        shutil.rmtree(os.getcwd() + "/core-v2", ignore_errors=True)

        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            self.run(".%sexample" % os.sep)
