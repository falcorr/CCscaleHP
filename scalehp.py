# TODO: 
# - have reference backup values, backup / revert functionality
# - confirm operating in correct directory
# - store skipNames externally

import os
import sys
import datetime
import math
import re
import msvcrt

patternFilename = re.compile("(.*)\..{1,4}$")
patternName = re.compile("^.*\"anims\": \"(.*)\".*$")
patternHP = re.compile("^.*\"hp\": ([\d|\.]{1,}).*$")

def log(text, append = True):
    try:
        if append:
            log = open(rootDir + '\\' + logFilename + '.log', 'a')
        else:
            log = open(rootDir + '\\' + logFilename + '.log', 'wt')
    except:
        print("Error writing to log file")
    finally:
        log.write("[%s] %s\n" % (datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'), text))
        log.close

def scan(dir): # pro-tip: avoid os.walk in future - absolute pain, issues, didn't work properly
    items = os.listdir(dir)
    for item in items:
        if os.path.isfile(os.path.join(dir, item)):
            if os.path.splitext(item)[1] == ".json":
                lineNum = None
                file = os.path.join(dir + '\\' + item)
                
                # excluded 'enemies.buffalo-fire'
                skipNames = ['boss.cargo-crab', 'boss.cargo-crab-extra', 'enemies.turret-rhombus', 'boss.hedgehag-king', 'enemies.hedgehog-boss', 'enemies.frobbit-miniboss-gallant', 'enemies.frobbit-miniboss-femme', 'enemies.gray-frobbit', 'enemies.snowman-jungle-1', 'enemies.snowman-jungle-2', 'enemies.snowman-xmas', 'enemies.snowman-sand', 'enemies.meerkat-special-command-1', 'enemies.turret-arid-boss', 'enemies.megamoth', 'enemies.jungle-sloth-black', 'enemies.boss-samurai', 'boss.glitch-boss', 'enemies.sandworm-boss', 'enemies.jungle-ape', 'enemies.jungle-shockboss', 'boss.whale', 'enemies.jungle-waveboss', 'enemies.panda-alt', 'boss.scorpion-boss', 'enemies.turret-large', 'enemies.guards', 'enemies.guard-mustache', 'enemies.pillar-large', 'enemies.jungle-fish-boss', 'enemies.goat-father', 'npc.designer', 'enemies.sandshark-special', 'enemies.sandshark-ghost', 'boss.fish-mega-gear', 'enemies.henry', 'henry-prop', 'enemies.panda-alt', 'enemies.penguin-rapper', 'boss.scorpion-boss', 'enemies.jungle-shockcat-black', 'boss.snow-megatank', 'enemies.snow-megatank-orb', 'enemies.spider-alt', 'boss.elephant', 'enemies.elboss-core', 'boss.driller', 'enemies.default-bot', 'enemies.icewall', 'enemies.aircon', 'enemies.oven', 'enemies.turret-baki-mortar-1', 'enemies.dummy', 'enemies.target-bot-2']
                
                linesToReplace = []
                HP = []
                newHP = []
                
                try:
                    with open(file, 'rt', encoding = "utf8") as original:
                        lines = original.readlines()
                        for i, line in enumerate(lines):
                            for match in re.finditer(patternName, line):
                                name = match.group(1)
                            for match in re.finditer(patternHP, line):
                                lineNum = i + 1
                                if float(match.group(1)) > 10:
                                    linesToReplace.append(lineNum)
                                    HP.append(match.group(1))
                                    newHP.append(math.ceil(float(HP[-1]) * float(scalePercentage) / 100))
                                    
                    if name not in skipNames:
                        if len(linesToReplace) > 0:
                            for i, lineNum in enumerate(linesToReplace):
                                lines[lineNum - 1] = lines[lineNum - 1].replace(str(HP[i]), str(newHP[i]))
                                log("[Changed] \"%s\" changed HP from %s to %s (%s)" % (name, int(HP[i]), int(newHP[i]), file))
                                print ("%s (%s) [line %s]: %shp --> %shp" % (name, file, lineNum, int(HP[i]), int(newHP[i])))
                                
                            with open(file, 'wt', encoding = "utf8") as edited:
                                edited.writelines(lines)
                        else:
                            log("[Ignored] \"%s\" has token or no HP (%s)" % (name, file))
                            
                            
                    else:
                        log("[Skipped] \"%s\" has been skipped (%s)" % (name, file))
                except:
                    log("[Error] File inaccessible %s" % (file))
                    
        elif os.path.isdir(os.path.join(dir, item)):
            scan(os.path.join(dir, item))

rootDir = os.getcwd()
scalePercentage = None

logFilename = 'scalehp_' + datetime.datetime.now().strftime('%Y%m%d_%H%M')
#logFilename = 'scalehp'
log("scaleHP log", False)

try:
    scalePercentage = sys.argv[1]
except:
    print("Invalid scale percentage provided")
    print("Usage: scaleHP [percentage]")
    log("[Error] Scale percentage not provided")
    sys.exit()
scaleValidate = re.compile("^\d{1,2}%?$")
if scaleValidate.match(scalePercentage) is None:
    print("Please enter a scale of 1-99%")
    print("Usage: scaleHP [percentage]")
    log("[Error] Invalid scale percentage provided")
    sys.exit()
scalePercentage.strip('%')

print("Scale HP of enemies in CrossCode")
print("Ensure this program is run in the \data\enemies\ directory")
print("Scale chosen is %s%%" % (scalePercentage))
print("Press any key to begin\n")
msvcrt.getch()
log("[Begin]")

scan(rootDir)
log("[End]")