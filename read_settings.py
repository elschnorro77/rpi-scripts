#!/usr/bin/env python
# This file is part of HoneyPi [honey-pi.de] which is released under Creative Commons License Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0).
# See file LICENSE or go to http://creativecommons.org/licenses/by-nc-sa/3.0/ for full license details.

# read settings.json which is saved by rpi-webinterface
import io
import json
from pathlib import Path
from utilities import backendFolder

def get_settings():
    filename = backendFolder + '/settings.json'
    my_file = Path(filename)
    settings = {}

    try:
        my_abs_path = my_file.resolve()
    except: # FileNotFoundError
        # doesn"t exist => default values
        settings["button_pin"] = 16
        settings["interval"] = 300

    else:
        # exists => read values from file
        with io.open(filename, encoding="utf-8") as data_file:
            settings = json.loads(data_file.read())

    settings = check_vars(settings)
    return settings

def check_vars(settings):
    settingstobewritten = False
    try:
        settings["button_pin"] = int(settings["button_pin"])
        if not settings["button_pin"]:
            raise Exception("button_pin is not defined.")
    except:
        settings["button_pin"] = 16

    try:
        if not 'debug' in settings:
            settings["debug"] = 0
    except:
        settings["debug"] = 0

    try:
        if not 'shutdownAfterTransfer' in settings:
            settings["shutdownAfterTransfer"] = 0
    except:
        settings["shutdownAfterTransfer"] = 0

    try:
        settings['ts_channels'][0]["ts_channel_id"]
        settings['ts_channels'][0]["ts_write_key"]
    except:
        try:
            settings["ts_channel_id"]
            print("Old Channel ID to be imported " + str(settings["ts_channel_id"]))
            settings["ts_write_key"]
            print("Old write key to be imported " + settings["ts_write_key"])
            ts_channel = {}
            ts_channel['ts_channel_id']= settings["ts_channel_id"]
            ts_channel['ts_write_key'] = settings["ts_write_key"]
            ts_channels = [] 
            ts_channels.append(ts_channel)
            settings['ts_channels'] = ts_channels
            settingstobewritten = True
        except:
            settings["ts_channels"] = None

    try:
        settings["offline"]
    except KeyError:
        settings["offline"] = 0

    if settingstobewritten:
        print("Writing updated settings")
        write_settings(settings)
    return settings

# get sensors by type
def get_sensors(settings, type):
    try:
        all_sensors = settings["sensors"]
    except TypeError:
        # doesn't exist => return empty array
        return []
    except KeyError:
        # doesn't exist => return empty array
        return []

    sensors = [x for x in all_sensors if x["type"] == type]
    # not found => return empty array
    if len(sensors) < 1:
        return []
    else:
        return sensors

def write_settings(settings):
    filename = backendFolder + '/settings.json'
    my_file = Path(filename)

    try:
        # write values to file
        data_file =  open(filename, "w")
        json.dump(settings, data_file)
    except Exception as ex:
        print("write_settings " + str(ex))

    return True    
