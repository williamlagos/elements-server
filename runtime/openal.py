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

import pyopenal as OpenAL

class Handler(BaseHandler):
    def __init__(self):
        pass
    def load_sound(self,archive):
        try:
            raise NotImplementedError
        except NotImplementedError, e:
            print "Option not already implemented."
    def stop_sound(self,archive):
        try:
            raise NotImplementedError
        except NotImplementedError, e:
            print "Option not already implemented."
    def benchmark():
        try:
            raise NotImplementedError
        except NotImplementedError, e:
            print "Option not already implemented."        
        # device = openal.alcOpenDevice(None)
        # device = openal.alcOpenDevice("'( ( devices '( native waveout esd sdl alsa arts null ) ) )")
        # context = openal.alcCreateContext (device, (openal.ALC_FREQUENCY, 22050, openal.ALC_INVALID))
        # openal.alcMakeContextCurrent (context)
            
        # openal.alListenerfv (openal.AL_POSITION, (0.0, 0.0, 0.0))
        # openal.alListenerfv (openal.AL_ORIENTATION, (0.0, 0.0, 1.0, 0.0, 1.0, 0.0))
        # stereo = openal.alGenBuffers (1)
        
        # file = open('./sword.wav', 'r')
        # data = file.read()
        # openal.alBufferData (stereo, openal.AL_FORMAT_WAVE_EXT, data, 0)
        # moving_source = openal.alGenSources (1)
        
        # openal.alSource3f (moving_source, openal.AL_POSITION, 0.0, 0.0, 20.0)
        # openal.alSourcefv (moving_source, openal.AL_VELOCITY, (0.0, 0.0, 0.0))
        # openal.alSourcei  (moving_source, openal.AL_BUFFER, stereo)
        # openal.alSourcei  (moving_source, openal.AL_LOOPING, openal.AL_FALSE)
        
        # openal.alSourcePlayv (moving_source)
        # openal.alSourcei (moving_source, openal.AL_SOURCE_STATE, openal.AL_INITIAL)
        
        # print "Using OpenAL", openal.alGetString(openal.AL_VERSION), "by", openal.alGetString(openal.AL_VENDOR)
        
        # while(1): pass        
    def test():
        OpenAL.init()
        try:
            l = OpenAL.Listener(22050)
            l.position = (0.0, 0.0, 0.0)
            l.at = (0.0, 0.0, 1.0)
            l.up = (0.0, 1.0, 0.0)
            
            b = OpenAL.WaveBuffer(os.path.join(os.path.dirname(sys.argv[0]), "sword.wav"))
            #b = OpenAL.OggVorbisBuffer("/home/jiba/src/slune/sounds/summum_of_the_light.ogg")
            
            s = OpenAL.Source()
            s.position = (0.0, 0.0, 0.0)
            s.velocity = (0.0, 0.0, 0.0)
            s.buffer  = b
            s.looping = 1
            
            s.play()
            
            # Move the source further
            
            z = 0.0
            while 1:
                z += 0.5
                s.position = (0.0, 0.0, z)
                time.sleep(0.1)
                
            print 'ok'
        except RuntimeError, e: print "Unavailable device."