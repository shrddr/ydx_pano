import math

import numpy as np

import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from fetch import get_pano

g_quadratic = gluNewQuadric()
# gluQuadricOrientation(g_quadratic, GLU_INSIDE)
gluQuadricOrientation(g_quadratic, GLU_OUTSIDE)
gluQuadricNormals(g_quadratic, GLU_SMOOTH)
gluQuadricDrawStyle(g_quadratic, GLU_FILL)
gluQuadricTexture(g_quadratic, GL_TRUE)


def loadTexture(loc):
    get_pano(loc)
    textureSurface = pg.image.load(f'cache/{loc}.jpg')
    textureData = pg.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texid


def main(loc):
    pg.init()
    display = (800, 600)
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)

    loadTexture(loc)

    # glShadeModel(GL_FLAT)
    # glEnable(GL_LIGHT0)
    # glEnable(GL_LIGHTING)

    gluPerspective(45, (display[0] / display[1]), 0.1, 150.0)
    glTranslatef(0, 0, 0)
    glScalef(-1, 1, 1)

    x, y, z = (0, 0, 0)
    rx, ry, rz = (90,180,0)
    vel = 0.1
    rvel = 1
    dragging = False
    drag_x, drag_y = (0, 0)
    drag_sensitivity = 0.075

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if dragging:
            rx -= mouse_dy * drag_sensitivity
            rz += mouse_dx * drag_sensitivity

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            x -= vel
        if keys[pg.K_RIGHT]:
            x += vel
        if keys[pg.K_UP]:
            y -= vel
        if keys[pg.K_DOWN]:
            y += vel
        if keys[pg.K_PAGEUP]:
            z += vel
        if keys[pg.K_PAGEDOWN]:
            z -= vel

        if keys[pg.K_KP7]:
            rx += rvel
        if keys[pg.K_KP4]:
            rx -= rvel
        if keys[pg.K_KP8]:
            ry += rvel
        if keys[pg.K_KP5]:
            ry -= rvel
        if keys[pg.K_KP9]:
            rz += rvel
        if keys[pg.K_KP6]:
            rz -= rvel

        glPushMatrix()
        glTranslate(x, y, z)
        glRotatef(rx, 1, 0, 0)
        glRotatef(ry, 0, 1, 0)
        glRotatef(rz, 0, 0, 1)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        gluSphere(g_quadratic, 22, 36, 36)
        glPopMatrix()

        pg.display.flip()
        pg.time.wait(10)


if __name__ == "__main__":
    # main('vy8tf6hnwZX9')
    # main('eTHmtcFyYk2V')
    main('yGUcr9xJT564')
