#
# This file is part of Zhockon Platform project.
# 
# Copyright (C) 2009-2011 William Oliveira de Lagos <william.lagos1@gmail.com>
#
# Zhockon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zhockon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zhockon.  If not, see <http://www.gnu.org/licenses/>.
#

import sys,os,ConfigParser,pickle
from optparse import OptionParser
from subprocess import Popen

try:
    import pygame
    import OpenGL
    # Module not implemented already.
    # import OpenAL
    from pygame.locals import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except ImportError, i:
    print("Some libraries weren't installed correctly.")
    print("Check PyOpenGL, PyOpenAL and Pygame to run Euphoria")
    print i; sys.exit()

parser = OptionParser()
parser.add_option("-p","--program",dest="program",help="Execute the selected program with Euphoria", metavar="FILE")
parser.add_option("-a","--core-activate",dest="cactive",action="store_true",help="Activate one or more Euphoria micro-modules")
parser.add_option("-d","--core-deactivate",dest="cdeactive",action="store_true",help="Deactivate one or more Euphoria micro-modules")
parser.add_option("-i","--information",dest="info",action="store_true",help="Show information about the engine.")
(options,args) = parser.parse_args()

def main(*argv):
    """Execute the tools for Euphoria Core."""
    z = Core(True)
    if options.cactive:
        z.configure_core(1)
    elif options.cdeactive:
        z.configure_core()
    elif options.info:
	z.test_libs()
    elif options.program:
	cmd = "python %s" % options.program
	exct = Popen(cmd.split())
	rtrn = exct.wait()
    else:
        print ("Unrecognized option. Digit -h for help.")

class Version():
    def __init__(self,v,m,y):
        self.vers = v
        self.year = y
        self.month = m

class Core():
    """Euphoria Core Class"""
    def __init__(self,boolean=False):
        """Initialize the Core switch"""
        self.zkready = boolean
    def create_info(self,v,m,y):
        verfile = open("ver.dat","w")
        versnow = Version(v,m,y)
        pickle.dump(versnow, verfile)
        verfile.close()
    def show_info(self):
        """Show information about the platform"""
        verfile = open("ver.dat","r")
        versnow = pickle.load(verfile)
        version = versnow.vers
        month = versnow.month
        year = versnow.year
        print("Zhockon Platform Alpha %s")%(version)
        print("Updated in %s/%s.")%(month,year)
        verfile.close()
    def configure_core(self,option=0):
        """Configure the Euphoria Core with ZConf"""
        cfg = Config()
        if option == 0:
            cfg.change_conf()
        else:
            cfg.change_conf("activate")
    def test_libs(self,times = 0):
        """Do some tests with embedded libs on Zhockon"""
        while times < 3:
            print("What do you want to do?\n"
                  "1. Verify if Pygame is installed.\n"
                  "2. Test animation with Euphoria.\n"
                  "3. Draw a cube with PyOpenGL.\n")
            choice = raw_input("Select one of the options:")
            if(choice == "1"):
                try:
                    print("Pygame : "+pygame.version.ver)
                    print("Pygame is now installed.")
                except ImportError, i:
                    print("Pygame isn't installed.")
                break
            elif(choice == "2"):
                import game
                game.Game([640,480])
                break
            elif(choice == "3"):
                import depth
                depth.cube_demo()
                break
            else:
                print "Invalid option. Try again."
                times = times + 1
class Config():
    """Euphoria Configuration Class"""
    def __init__(self):
        """Prepare the configuration of Euphoria"""
        conf = ConfigParser.ConfigParser()
        try:
            conf.read("euph.cfg")
        except ConfigParser.NoSectionError:
            print "Problems with ZConf. Check the euph.cfg file."
    def change_conf(self,option="deactivate"):
        """Turn off or on the switches on Euphoria"""
        conf = ConfigParser.ConfigParser()
 
        try:
            conf.read("euph.cfg")
            file = open("euph.cfg","w")
            items = conf.items("Core")
        except ConfigParser.NoSectionError:
            print "Problems with ZConf. Check the euph.cfg file."

        if option == "deactivate":
            for i in items:
                if i[1] == "True": 
                    print i[0]+": "+i[1]
            choice = raw_input("Select the sector to deactivate:")
            conf.set("Core", choice, False)
            conf.write(file)
        elif option == "activate":
            for i in items:
                if i[1] == "False":
                    print i[0]+": "+i[1]
            choice = raw_input("Select the sector to activate:")
            conf.set("Core",choice,True)
            conf.write(file)

if __name__ == "__main__":
    sys.exit(main(*sys.argv))
