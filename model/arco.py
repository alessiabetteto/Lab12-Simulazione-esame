from dataclasses import dataclass

from model.actor import Actor


@dataclass

class Arco:
    a1: Actor
    a2: Actor
    peso: int