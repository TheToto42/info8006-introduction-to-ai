# My two cents (Samy Aittahar)
# Agents (intelligents ?) that can control walls


from .game import Agent
from .game import Actions
from . import util
import numpy as np

SWITCH_FROM_OPEN_P = 0.7
SWITCH_FROM_CLOSE_P = 0.3


class Waller(Agent):
    def __init__(self, index, seed=-1):
        self.index = index
        if seed == -1:
            self.rng = np.random.RandomState()
        else:
            self.rng = np.random.RandomState(seed)
        self.switch_from_open_p = SWITCH_FROM_OPEN_P
        self.switch_from_close_p = SWITCH_FROM_CLOSE_P

    def get_action(self, state):
        raise NotImplementedError()


class MDPWaller(Waller):
    def get_action(self, state):
        if state.getWallState(self.index):
            proba = 1 - self.switch_from_close_p
        else:
            proba = self.switch_from_open_p
        return self.rng.choice([True, False], 1, p=[proba, 1 - proba])[0]


class PerturbedMDPWaller(MDPWaller):
    def getPerturbations():
        return NotImplementedError()

    def __init__(self, index, seed=-1):
        Waller.__init__(self, index, seed)
        perturb_1, perturb_2 = self.getPerturbations()
        self.switch_from_open_p += self.rng.choice(
            [-1, 1], 1)[0] * perturb_1 * self.switch_from_open_p
        self.switch_from_close_p += self.rng.choice(
            [-1, 1], 1)[0] * perturb_2 * self.switch_from_close_p


class SlightlyPerturbedMDPWaller(PerturbedMDPWaller):

    def getPerturbations(self):
        return [self.rng.uniform(0, 0.2) for i in range(2)]


class HighlyPerturbedMDPWaller(PerturbedMDPWaller):

    def getPerturbations(self):
        return tuple([self.rng.uniform(0.2, 0.5) for i in range(2)])
