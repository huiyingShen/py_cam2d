import simpleaudio as sa


wave_obj = sa.WaveObject.from_wave_file("hello_again.wav")
wave_obj.play().wait_done()