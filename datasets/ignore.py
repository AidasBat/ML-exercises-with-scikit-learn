# -*- coding: utf-8 -*-

from __future__ import division

from builtins import range
from psychopy import visual, core, event
from psychopy.tools.coordinatetools import cart2pol

from numpy.random import random, shuffle

win = visual.Window([1024, 768], units='pix', monitor='testMonitor')

N = 500
fieldSize = 500
elemSize = 40
coherence = 0.5

xys = random([N, 2]) * fieldSize - fieldSize / 2.0  # numpy vector
globForm = visual.ElementArrayStim(win,
    nElements=N, sizes=elemSize, sfs=3,
    xys=xys, colors=[180, 1, 1], colorSpace='hsv')

def makeCoherentOris(XYs, coherence, formAngle):
    nNew = XYs.shape[0]
    newOris = random(nNew) * 180
    possibleIndices = list(range(nNew))
    shuffle(possibleIndices)
    coherentIndices = possibleIndices[0: int(nNew * coherence)]
    theta, radius = cart2pol(XYs[: , 0], XYs[: , 1])
    newOris[coherentIndices] = formAngle - theta[coherentIndices]
    return newOris

globForm.oris = makeCoherentOris(globForm.xys, coherence, 45)

lives = random(N) * 10
while not event.getKeys():
    newXYs = globForm.xys
    newOris = globForm.oris
    deadElements = (lives > 10)
    lives[deadElements] = 0
    newXYs[deadElements, : ] = random(newXYs[deadElements, : ].shape) * fieldSize - fieldSize/2.0
    new = makeCoherentOris(newXYs[deadElements, : ], coherence, 45)
    newOris[deadElements] = new
    globForm.xys = newXYs
    globForm.pris = newOris
    globForm.draw()
    win.flip()
    lives = lives + 1
    event.clearEvents('mouse')

win.close()
core.quit()
