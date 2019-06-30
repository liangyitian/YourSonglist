from enum import Enum
import pygame

class playStatus(Enum):
    IDLE=0
    PLAYING=1
    PAUSED=2

class player:
    def __init__(self):
        pass
        self.__status=playStatus.IDLE
        self.__position=None
        self.__progress=None
        self.__songID=None
        self.__duration=None
        self.__volume=0.5

        pygame.mixer.init(frequency=44100)
        pygame.mixer.music.set_volume(self.volume)

    def getVolume(self):
        return self.__volume

    def setVolume(self,volume):
        self.__volume=volume

    def getPosition(self):
        return self.__position

    def setPosition(self,position):
        self.__position=position
        self.__progress=position/self.__duration

    def getProgress(self):
        return self.__progress

    def setProgress(self, progress):
        self.__progress = progress
        self.__position=progress*self.__duration


