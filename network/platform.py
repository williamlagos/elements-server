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

compat = {
		'audio': 	('sdl',['openal']),
		'graphics': ('sdl',['opengl']),
		'elements': ('sdl',['opengl']),
		'physics': 	('sdl',['opencl']),
		'network': 	('sdl',['']),
		}

def select(package,library):
	choices = compat[package][1]
	antique = compat[package][0]
	choices.insert(0,antique)
	choices.remove(library)
	compat[package] = [library,choices]
def save():
	pass
def load(package):
	library = compat[package][0]
	if library is 'sdl':
		from libs.sdl import Handler
	elif library is 'opengl':
		from libs.opengl import Handler
	elif library is 'openal':
		from libs.opengl import Handler
	#elif library is 'opencl':
	#	from libs.opencl import Handler
	else:
		from libs.base import BaseHandler as Handler
	handler = Handler()
	return handler