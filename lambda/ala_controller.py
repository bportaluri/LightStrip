"""
Alexa Smart Home Lambda function for LiveLights project.

Note that this example does not deal with user authentication, only uses virtual devices, omits
a lot of implementation and error handling to keep the code simple and focused.
"""

import logging
import time
import json

import math
import random

import boto3


THING_NAME = 'LL01'


# Animations and palettes for ALA library
# https://github.com/bportaluri/ALA/blob/master/src/Ala.h

ANIM_ON=101
ANIM_OFF=102
ANIM_BLINK=103
ANIM_BLINKALT=104
ANIM_SPARKLE=105
ANIM_SPARKLE2=106
ANIM_STROBO=107

ANIM_CYCLECOLORS=151

ANIM_PIXELSHIFTRIGHT=201
ANIM_PIXELSHIFTLEFT=202
ANIM_PIXELBOUNCE=203
ANIM_PIXELSMOOTHSHIFTRIGHT=211
ANIM_PIXELSMOOTHSHIFTLEFT=212
ANIM_PIXELSMOOTHBOUNCE=213
ANIM_COMET=221
ANIM_COMETCOL=222
ANIM_BARSHIFTRIGHT=231
ANIM_BARSHIFTLEFT=232
ANIM_MOVINGBARS=241
ANIM_MOVINGGRADIENT=242
ANIM_LARSONSCANNER=251
ANIM_LARSONSCANNER2=252

ANIM_FADEIN=301
ANIM_FADEOUT=302
ANIM_FADEINOUT=303
ANIM_GLOW=304

ANIM_FADECOLORS=351
ANIM_FADECOLORSLOOP=352
ANIM_PIXELSFADECOLORS=353
ANIM_FLAME=354

ANIM_FIRE=501
ANIM_BOUNCINGBALLS=502
ANIM_BUBBLES=503

PAL_NONE=0
PAL_RGB=1
PAL_RAINBOW=2
PAL_PARTY=3
PAL_HEAT=4
PAL_FIRE=5


anim_relaxing = []
anim_relaxing.append({'animation': ANIM_PIXELSFADECOLORS, 'palette': PAL_PARTY,   'duration': 2000 })
anim_relaxing.append({'animation': ANIM_SPARKLE2,         'palette': PAL_PARTY,   'duration': 2000 })
anim_relaxing.append({'animation': ANIM_SPARKLE,          'palette': PAL_RAINBOW, 'duration': 1000 })
anim_relaxing.append({'animation': ANIM_FADECOLORSLOOP,   'palette': PAL_RGB,     'duration': 8000 })
anim_relaxing.append({'animation': ANIM_COMET,            'palette': PAL_RGB,     'duration': 1000 })
anim_relaxing.append({'animation': ANIM_LARSONSCANNER2,   'palette': PAL_NONE,    'color':  'FF0000',     'duration': 1000 })

anim_exciting = []
anim_exciting.append({'animation': ANIM_PIXELSFADECOLORS, 'palette': PAL_HEAT,   'duration': 200 })
anim_exciting.append({'animation': ANIM_SPARKLE2,         'palette': PAL_HEAT,   'duration': 200 })
anim_exciting.append({'animation': ANIM_SPARKLE,          'palette': PAL_HEAT, 'duration': 100 })
anim_exciting.append({'animation': ANIM_FADECOLORSLOOP,   'palette': PAL_HEAT,     'duration': 800 })
anim_exciting.append({'animation': ANIM_COMET,            'palette': PAL_HEAT,     'duration': 100 })


client = boto3.client('iot-data')

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Sets the power: on/off
def animation_relaxing():
    #logger.info(">>>>>>>>>>>>>" + state)
    response = client.update_thing_shadow(
        thingName = THING_NAME, 
        payload = json.dumps({
            'state': {
                'desired': random.choice(anim_relaxing)
            }
        })
    )

# Sets the power: on/off
def animation_exciting():
    #logger.info(">>>>>>>>>>>>>" + state)
    response = client.update_thing_shadow(
        thingName = THING_NAME, 
        payload = json.dumps({
            'state': {
                'desired': random.choice(anim_exciting)
            }
        })
    )

# Display a glowing animation
def thingshadow_start():
    #logger.info(">>>>>>>>>>>>>" + state)
    response = client.update_thing_shadow(
        thingName = THING_NAME, 
        payload = json.dumps({
            'state': {
                'desired': {
                    'animation': 304,
                    'color': '000055',
                    'duration': 2000
                }
            }
        })
    )

# Sets the power: on/off
def thingshadow_turn_on():
    #logger.info(">>>>>>>>>>>>>" + state)
    response = client.update_thing_shadow(
        thingName = THING_NAME, 
        payload = json.dumps({
            'state': {
                'desired': {
                    'animation': 101,
                    'color': 'FFFFFF',
                    'palette': 0
                }
            }
        })
    )

# Sets the power: on/off
def thingshadow_turn_off():
    #logger.info(">>>>>>>>>>>>>" + state)
    response = client.update_thing_shadow(
        thingName = THING_NAME, 
        payload = json.dumps({
            'state': {
                'desired': {
                    'animation': 102
                }
            }
        })
    )

# Sets the brigthness in range [0-100]
def thingshadow_set_brightness(brightness):
    response = client.update_thing_shadow(
        thingName = THING_NAME, 
        payload = json.dumps({
            'state': {
                'desired': {
                    'brightness': brightness
                }
            }
        })
    )


# Sets RGB color, each component must be an integer in the [0-255] range
def thingshadow_set_color(rgb_color):
    response = client.update_thing_shadow(
        thingName = THING_NAME, 
        payload = json.dumps({
            'state': {
                'desired': {
                    'color': rgb_color
                }
            }
        })
    )
