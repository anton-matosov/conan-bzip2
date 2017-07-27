from conans import ConanFile, tools
import os, shutil
from conans.tools import download, unzip, replace_in_file, check_md5
from conans import CMake
from conans.util import files

class Bzip2Conan(ConanFile):
    name = "bzip2"
    version = "1.0.6"
    branch = "master"
    ZIP_FOLDER_NAME = "bzip2-%s" % version
    generators = "cmake"
    settings =  "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    exports = ["CMakeLists.txt"]
    url="http://github.com/lasote/conan-bzip2"
    license="BSD-style license"

    def config(self):
        del self.settings.compiler.libcxx

    def source(self):
        zip_name = "bzip2-%s.tar.gz" % self.version
        download("http://www.bzip.org/%s/%s" % (self.version, zip_name), zip_name)
        check_md5(zip_name, "00b516f4704d4a7cb50a1d97e6e8e15b")
        unzip(zip_name)
        
        os.unlink(zip_name)

    def build(self):
        shutil.move("CMakeLists.txt", "%s/CMakeLists.txt" % self.ZIP_FOLDER_NAME)

        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        fpic = "-DFPIC=ON" if self.options.fPIC else ""

        with tools.chdir(self.ZIP_FOLDER_NAME):
            files.mkdir("_build")
            with tools.chdir("_build"):
                cmake = CMake(self)
                cmake.configure(build_dir=".", source_dir="../", args=[shared, fpic])
                cmake.build()

    def package(self):
        # Copying zlib.h, zutil.h, zconf.h
        self.copy("*.h", "include", "%s" % (self.ZIP_FOLDER_NAME), keep_path=False)
        self.copy("*bzip2", dst="bin", src=self.ZIP_FOLDER_NAME, keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="%s/_build" % self.ZIP_FOLDER_NAME, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="%s/_build" % self.ZIP_FOLDER_NAME, keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="%s/_build" % self.ZIP_FOLDER_NAME, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['bz2']
