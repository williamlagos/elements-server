#
# This file is part of Zhockon Foundation.
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

import platform

class Sound:
    def __init__(self):
        self.zkn = platform.load('audio')
        self.sounds = []
    def archive(self,file):
        self.sounds.append(zkn.load_sound(file))
    def play(self,namefile):
        for s in sounds:
            if namefile is s:
                zkn.play_sound(file)
    def stop_one(self,namefile):
        for s in sounds:
            if namefile is s:
                zkn.stop_sound(file)
    def stop(self):
        for s in sounds:
            zkn.stop_sound(file)

class Music:
    def __init__(self):
        pass
    
class Effects:
    def __init__(self):
        pass