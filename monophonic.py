#!/usr/bin/env python

"""Transcribe melodies.

A really small (one function) python library to get a music21 representation 
of a melody from audio.  Given an audio file containing a monophonic melody 
(a single melodic line with no accompaniment), use the Echo Nest audio analysis tools 
(http://developer.echonest.com/docs/v4/_static/AnalyzeDocumentation_2.2.pdf)
to segment the audio into notes and identify each note's pitch and duration.  
Then make a representation of the melody in music21 (http://mit.edu/music21/)
to easily analyse, make notation, or make midi.

Example usage:
>>> import monophonic
>>> local_audio_file = <Full path to a local mp3 or wav file> 
>>> stream = monophonic.transcribe(local_audio_file)
>>> stream.show()

NOTE:
*It doesn't work very well.*  The pitch data isn't particularly accurate, the 
rhythm quantization could improve a lot, it doesn't even try to get the octave 
of each pitch, and of course noisy audio screws it up completely.

Also, if you're using a Mac, and Echo Nest doesn't already have an analysis of your audio, you'll need to first run this once using the factory installed instance of Python.

Dependencies:
music21: http://mit.edu/music21/
echo-nest-remix: http://code.google.com/p/echo-nest-remix/


Jonathan Marmor
2011-02-12, Music Hack Day New York

"""

import echonest.audio
import music21

def _get_quarter_duration(track):
   # TODO: do this better
   return 60.0 / track.analysis.tempo['value']

def _chroma_to_pitch_class(chroma):
   # TODO: do this better
   most_likely = max(chroma)
   pitch_class = chroma.index(most_likely)
   return pitch_class

def _milliseconds_to_quarter_durations(segment, quarter_duration):
   # TODO: do this better
   return segment.duration / quarter_duration

def _quantize(stream):
   # TODO: do this better
   stream.quantize([4], processOffsets=True, processDurations=True)
   for note in stream:
      if note.duration.quarterLength == 0.0:
         note.duration.quarterLength = 0.25

def transcribe(local_audio_file):
   track = echonest.audio.LocalAudioFile(local_audio_file)
   quarter_duration = _get_quarter_duration(track)
   segments = track.analysis.segments
   stream = music21.stream.Stream()
   for segment in segments:
      note = music21.note.Note()
      note.pitchClass = _chroma_to_pitch_class(segment.pitches)
      # TODO: set octave
      note.duration = music21.duration.Duration()
      note.duration.quarterLength = _milliseconds_to_quarter_durations(segment, quarter_duration)
      stream.append(note)
   _quantize(stream)
   return stream

def test():
   base_path = '/Users/jmarmor/Desktop/analyse/TalkAboutSuffering.mp3'
   pray_path = '/Users/jmarmor/Desktop/analyse/doc_watson_down_in_the_valley_to_pray.mp3')
   pray = transcribe(pray_path)
   talk = transcribe(talk_path)
   return pray, talk

if __name__ == '__main__':
   test()