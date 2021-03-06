import os
import shutil

from component import pcolors as pcolor
from component import Config

class Generator():
    def __init__(self):
        self.name = None
        self.path = None
        self.project = None
        self.config = None
        self.lib_choosen = []

    def cp_lib(self, lib_choosen):
        self.lib_choosen = lib_choosen
        for file_name in lib_choosen:
            shutil.copy("Data/lib/" + file_name, self.project + "/lib")

    def add_makefile(self):
        fd = open("Data/Makefile", 'r')
        content = fd.read().split("\n")
        fd.close()
    
        nb_line = 0
        for line in content:
            if (line == None or line == ""):
                content[nb_line] = ""
            elif (line[0] == '#'):
                content[nb_line] = None
            elif (line.find("SRC\t=") != -1):
                content[nb_line] = line + "\t" + self.config.get_main_file() + ".c"
            elif (line.find("FLAGS\t=") != -1):
                content[nb_line] = line + "\t" + self.config.get_flags()
            elif (line.find("$(MAKE_LIB)") != -1 and self.config.get_lib() == 0):
                content[nb_line] = None
            elif (line.find("$(LDFLAGS)") != -1 and self.config.get_lib() == 0):
                content[nb_line] = content[nb_line].replace("$(LDFLAGS)", "")
                print(content[nb_line])
            nb_line += 1
        fd = open(self.project + "/Makefile", "x")
        for line in content:
            if (line != None):
                fd.write(line + "\n")
        fd.close()

        if (self.config.get_lib() == 1):
            fd = open("Data/Makefile_lib", 'r')
            content = fd.read().split("\n")
            fd.close()
            
            nb_line = 0
            for line in content:
                if (line == None or line == ""):
                    content[nb_line] = ""
                elif (line[0] == '#'):
                    content[nb_line] = None
                elif (not line.find("SRC\t=")):
                    tmp = line + "\t"
                    for file_lib in self.lib_choosen:
                        tmp += file_lib + " \\\n\t\t"
                    content[nb_line] = tmp
                nb_line += 1
            fd = open(self.project + "/lib/Makefile", "x")
            for line in content:
                if (line != None):
                    fd.write(line + "\n")
            fd.close()
    
    def add_include(self, lib_choosen):
        name_lib = []
        for lib_file in lib_choosen:
            name_lib.append(lib_file.replace(".c", ""))
    
        fd = open("Data/Include.h", 'r')
        content = fd.read().split("\n")
        fd.close()

        nb_line = 0
        new_content = []
        for line in content:
            if (line == ""):
                new_content.append(line)
            elif (line.find("#include") != -1):
                new_content.append(line)
            elif (line.find('//') == -1):
                for lib_file in name_lib:
                    if (line.find(" " + lib_file + "(") != -1):
                        new_content.append(line)
            nb_line += 1

        fd = open(self.project + "/include/" + self.config.get_include()[0] + ".h", "x")
        if (self.config.get_include()[1] == 1):
            fd.write("#ifndef " + self.config.get_include()[0].upper() + "_H_\n")
            fd.write("#define " + self.config.get_include()[0].upper() + "_H_\n\n")
        for line in new_content:
            fd.write(line + "\n")
        if (self.config.get_include()[1] == 1):
            fd.write("\n#endif /* !" + self.config.get_include()[0].upper() + "_H_ */")
        fd.close()

    def add_main(self):
        fd = open(self.project + "/" + self.config.get_main_file() + ".c", "x")
        fd.write("int main(void)\n{\n\treturn (0);\n}")
        fd.close()

    def create_all_directories(self):
        if (self.path[len(self.path) - 1] != '/'):
            self.path += "/"
        try:
            os.mkdir(self.path + self.name)
            self.project = self.path + self.name
            if (self.config.get_src_folder() == 1):
                os.mkdir(self.project + "/src")
            if (self.config.get_lib() == 1):
                os.mkdir(self.project + "/lib")
            if (len(self.config.get_include()) != 0):
                os.mkdir(self.project + "/include")
        except OSError:
            print(pcolor.red + "Creation of folder failed" + pcolor.white)
            print(pcolor.yellow + "Try to change Location" + pcolor.white)
            exit(0)

    def init_generator(self, name, path, config):
        self.name = name
        self.path = path
        self.config = config