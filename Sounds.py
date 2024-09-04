import pygame, time

masterVolume = 1


# (run before pygame.init()) initializes the sound mixer (pre-init is better in general it seems)
def preInit(maxChannels: int=8) -> None:
    pygame.mixer.pre_init(channels=maxChannels)


# initializes the sound mixer
def init(maxChannels: int=8) -> None:
    pygame.mixer.init()
    pygame.mixer.set_num_channels(maxChannels)


# a base class for managing sounds
class SoundManager:
    def __init__(self, sound: pygame.mixer.Sound, volume: float = 1, channel: int = 1, loops: int = 0, max_time: int = 0, fade_ms: int = 0) -> None:
        self.sound = sound
        self.volume = volume
        self.channel = channel
        self.loops = loops
        self.max_time = max_time
        self.fade_ms = fade_ms
        self.channel = pygame.mixer.Channel(self.channel)
        self.channel.set_volume(self.volume)
        self.ended = False
        self.start = time.time()
    def play(self) -> None:
        self.channel.set_volume(self.volume*masterVolume)
        self.channel.play(self.sound, loops = self.loops, maxtime = self.max_time, fade_ms = self.fade_ms)
    def stop(self, fade_out: int = 0) -> None:
        self.channel.fadeout(fade_out)
    def __mul__(self, v: float) -> None:
        self.channel.set_volume(v)
    def pause(self) -> None:
        self.channel.pause()
    def resume(self) -> None:
        self.channel.unpause()


# a class for loading a sound file and playing it
class Sound (SoundManager):
    def __init__(self, sound_file: str, volume: float = 1, channel: int = 1, loops: int = 0, max_time: int = 0, fade_ms: int = 0) -> None:
        self.sound = pygame.mixer.Sound(sound_file)
        self.file = sound_file
        self.start_time = None
        super().__init__(self.sound, volume=volume, channel=channel, loops=loops, max_time=max_time, fade_ms=fade_ms)
    def play(self) -> None:
        super().play()
        self.start_time = time.time()


