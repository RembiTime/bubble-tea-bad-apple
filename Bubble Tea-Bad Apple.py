# Plays the songs "Bubble Tea" and "Bad Apple" each with their own little thing going on in the console
# Rhyder Swen
# 8/29/21

# Bubble Tea by Dark Cat
# Sheet music by Canine Helicopter at https://musescore.com/user/28327927/scores/5247003
# Bad Apple from Touhou Project by Huw Lewis-Jones
# Sheet music by Rinnosuke at https://musescore.com/user/166080/scores/359836
# Video to ASCII conversion by CalvinLoke at https://github.com/CalvinLoke/bad-apple

import pysine
import time
import sys
import threading
import fpstimer
from audioplayer import AudioPlayer

# Stores the frequencies of each note in a variable so it's easier to read and program
G3 = 208
A3 = 220
B3 = 247
C4 = 277
D4 = 294
E4 = 330
F4reg = 349
F4 = 370
G4reg = 392
G4 = 415
A4 = 440
B4 = 494
C5reg = 523
C5 = 554
D5 = 587
E5 = 659
F5reg = 698
F5 = 740
G5 = 831
A5 = 880
B5 = 988
C6 = 1109
D6 = 1175
E6 = 1319
F6 = 1480

# Stores the length of each note in variables and automatically changes the other variables based off the length of the whole note
whole = 1.5
half = whole/2
quarter = half/2
eight = quarter/2
sixteen = eight/2
n32 = sixteen/2
dotQuarter = quarter+eight
dotEight = eight+sixteen
reg = 0

# The notes in order
BTMelody = [
    C4, 
    B3, 
    E4, A4, 
    B4, C5,
    B4,
    F4reg,
    A4, A4,
    E5, C5,

    # 12

    A4, E5, B5, C6, E5,
    B4, C5, E5, F5,
    E5,F5,C5,E5,B4,
    C5,A4,B4,A4,B4,C5,E5,C5,
    B4,A4,E5,D5,E5,F5,A5,C6,

    # 42

    F5reg,C5,F5reg,G5,F5reg,C5,B4,C5,
    C5,A4,C5,C5reg,G4,C5reg,B4,G4reg,
    B4,C5,B4,A4,E5,C5,B4,A4,
    A4,F4,E5,F5,A4,

    # 71

    B4,C5,B4,A4,
    E5,F5,C5,E5,B4,
    C5,A4,B4,A4,B4,C5,E5,C5,
    B4,A4,E4,D4,E4,F4,A4,C5,

    # 96

    F4reg,C4,F4reg,G4,F4reg,C4,B3,C4,
    C5,A4,C5,C5reg,G4,C5reg,B4,G4reg,
    B4,C5,B4,A4,E5,C5,B4,A4,

    # 120 / Page 2

    F5,E5,C5,B4,
    A4,E5,C5,B4,A4,
    F5,E5,C5,B4,A4,
    B4,A4,B4,A4,E5,C5,B4,A4,
    F5,E5,C5,B4,

    # 146

    A4,E5,C5,B4,A4,
    F5,E5,C5,B4,A4,
    B4,A4,B4,A4,E5,C5,B4,A4,
    E4,F4,C5,B4,

    # 168

    F5,E5,C5,A4,
    F5,E5,C5,C5reg,A4,
    B4,A4,B4,A4,E5,C5,B4,A4,
    E4,F4,C5,B4,

    # 189

    F5,E5,C5,A4,
    F5,E5,C5,C5reg,A4,
    B4,A4,B4,A4,E5,C5,B4,A4,
    E4,A4,E5,E5,F5reg,
 
    # 211

    F4reg,B4,C5,F5reg,C5,F5reg,F5,
    A4,A5,G5,F5,B4,C5reg,
    B4,E5,C5,B4,A4,
    A4,F4,E4,D4,E4,F4,A4,C5,

    # 237 / Page 3

    F4reg,C4,F4reg,G4,F4reg,C4,B3,C4,
    C5,A4,C5,C5reg,G4,C5reg,B4,G4reg,
    B4,C5,B4,A4,E5,C5,B4,A4,
    A5,F5,E5,D5,E5,F5,A5,C6,

    # 269

    B4,C5,F5reg,G5,F5reg,B4,A4,B4,
    C5,A4,C5,C5reg,G4,C5reg,B4,G4reg,
    B4,C5,B4,A4,E5,C5,B4,A4,
    F6,A5,B5,B5,C6,

    # 298

    C6,E6,C6,F6,
    C6,E6,F6,C6,E6,B5,
    C6,A5,B5,A5,E5,C5,B4,A4,
    A4,F4,E4,D4,E4,F4,A4,C5,

    # 324

    B3,C4,F4reg,G4,F4reg,C4,B3,C4,
    F4,A4,C5,E5,F5,C5,E5,B4,
    C5,A4,B4,A4,E5,C5,B4,A4,

    # 348 / Page 4 (After skipping a bit)

    E5,C5,A4,E5,C5,A4,B4,
    B4,A4,E5,C5reg,B4,A4,
    F4,E5,C5,A4,E5,C5,A4,B4,
    B4,A4,E5,C5reg,B4,A4,
    A4,E5,E5,F5reg,

    # 381

    G4,B4,C5,F5reg,C5reg,F5reg,F5,
    C5,A5,G5,F5,B4,C5reg,
    B4,B4,A4,

    # 397 / Back to coda part I'm ignoring because long

    A4, E5, B5, C6, E5,
    B4, C5, E5, F5,
    E5,F5,C5,E5,B4,
    C5,A4,B4,A4,B4,C5,E5,C5,
    B4,A4,E5,D5,E5,F5,A5,C6,

    # 42

    F5reg,C5,F5reg,G5,F5reg,C5,B4,C5,
    C5,A4,C5,C5reg,G4,C5reg,B4,G4reg,
    B4,C5,B4,A4,E5,C5,B4,A4,
    A4,F4,E5,F5,A4,

    # 71

    B4,C5,B4,A4,
    E5,F5,C5,E5,B4,
    C5,A4,B4,A4,B4,C5,E5,C5,
    B4,A4,E4,D4,E4,F4,A4,C5,

    # 96

    F4reg,C4,F4reg,G4,F4reg,C4,B3,C4,
    C5,A4,C5,C5reg,G4,C5reg,B4,G4reg,
    B4,C5,B4,A4,E5,C5,B4,A4,

    # 505

    A4,B4,C5
]

# How long each note should play
BTLengths = [
    whole,
    whole,
    half,
    half,
    dotQuarter, eight+half,
    whole,
    whole,
    dotQuarter, half,
    dotQuarter, eight+half,

    eight,eight,eight,eight,eight,
    eight,eight,eight,eight,
    eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,

    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,

    eight,eight,eight,eight,
    eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,

    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,

    eight,quarter,quarter,eight+eight,
    quarter,quarter,eight,eight,eight+quarter,
    eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight+quarter,
    eight,quarter,quarter,eight+eight,

    quarter,quarter,eight,eight,eight+quarter,
    eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,dotQuarter,
    eight,quarter,quarter,eight+eight,

    quarter,quarter,quarter,eight+quarter,
    eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight+quarter,
    eight,quarter,quarter,quarter,

    quarter,quarter,quarter,eight+quarter,
    eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight+quarter,
    quarter,eight,eight,eight,eight,

    eight,eight,eight,quarter,eight,eight,eight,
    quarter,eight,quarter,quarter,sixteen,eight+quarter,
    quarter,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,

    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,

    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    quarter,eight,eight,eight,eight,

    eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,

    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,quarter,

    eight,eight,eight,eight,eight,eight,eight+eight,
    eight,eight,quarter,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,quarter,
    eight,eight,quarter,eight,eight,eight+quarter,
    eight,eight,eight,eight,

    eight,eight,eight,quarter,eight,eight,eight,
    quarter,eight,quarter,quarter,sixteen,eight+quarter,
    quarter,eight,eight,

    eight,eight,eight,eight,eight,
    eight,eight,eight,eight,
    eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,

    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,

    eight,eight,eight,eight,
    eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,

    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,eight,eight,

    whole,whole,whole*2
]

# If there's any rests in between the notes (reg means no break)
BTRests = [ 
    reg,
    reg,
    reg, reg,
    reg, reg,
    reg,
    reg,
    eight, reg,
    reg, reg,

    reg,reg,reg,quarter,eight+quarter,
    reg,quarter,reg,quarter+eight,
    reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,

    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,quarter,eight+quarter,

    reg,quarter,reg,quarter+eight,
    reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,

    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,quarter,

    reg,reg,reg,reg,
    reg,reg,reg,reg,eight,
    reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,

    reg,reg,reg,reg,eight,
    reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,

    reg,reg,reg,eight,
    reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,

    reg,reg,reg,eight,
    reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,quarter,reg,reg,

    reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,

    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,

    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,quarter,reg,quarter,

    reg,quarter,reg,quarter,
    reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,

    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,

    reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,
    reg,quarter,reg,reg,

    reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,
    quarter,reg,reg,

    reg,reg,reg,quarter,eight+quarter,
    reg,quarter,reg,quarter+eight,
    reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,

    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,quarter,eight+quarter,

    reg,quarter,reg,quarter+eight,
    reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,

    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,
    reg,reg,reg,reg,reg,reg,reg,reg,

    reg,reg,reg
]

# Contains each frame of the tea graphic
teaGraphic = [
    """






    _________
 .-'---------|  
( C|/\/\/\/\/|
 '-./\/\/\/\/|
   '_________'
    '-------'""",
    """






    _____o___
 .-'---------|  
( C|/\/\/\/\/|
 '-./\/\/\/\/|
   '_________'
    '-------'""",
    """





         O
    _o_____o_
 .-'---------|  
( C|/\/\/\/\/|
 '-./\/\/\/\/|
   '_________'
    '-------'""",
    """




         O
     O     o
    __o_o____
 .-'---------|  
( C|/\/\/\/\/|
 '-./\/\/\/\/|
   '_________'
    '-------'""",
    """



         X
     O     O
      O o  
    _______o_
 .-'---------|  
( C|/\/\/\/\/|
 '-./\/\/\/\/|
   '_________'
    '-------'""",
    """


         +
     O     X
      X o  
           o
    _o_______
 .-'---------|  
( C|/\/\/\/\/|
 '-./\/\/\/\/|
   '_________'
    '-------'""",
    """

      +
     X     +
      + O  
           O
     o
    _________
 .-'---------|  
( C|/\/\/\/\/|
 '-./\/\/\/\/|
   '_________'
    '-------'""",
    """

     +    
        X  
           O
     O

    _________
 .-'---------|  
( C|/\/\/\/\/|
 '-./\/\/\/\/|
   '_________'
    '-------'""",
    """
          
        +  
           X
     X


    _________
 .-'---------|  
( C|/\/\/\/\/|
 '-./\/\/\/\/|
   '_________'
    '-------'""",
    """
          
           +
     +
           


    _________
 .-'---------|  
( C|/\/\/\/\/|
 '-./\/\/\/\/|
   '_________'
    '-------'"""
]

# Contains each frame of the tree graphic
treeGraphic = [
    """
                  v .   ._, |_  .,
           `-._\/  .  \ /    |/_
               \\\\  _\, y | \//
         _\_.___\\\\, \\\\/ -.\||
           `7-,--.`._||  / / ,
           /'     `-. `./ / |/_.'
                     |    |//
                     |_    /
             /       |-   |
                 \   |   =|
                     |    |
--------------------/ ,  . \--------._""",
    """
                  v .   ._, |_  .,
           `-._\/  .  \ /    |/_
               \\\\  _\, y | \//
         _\_.___\\\\, \\\\/ -.\||
           `7-,--.`._||  / / ,
           /'  \  `-. `./ / |/_.'
                     |    |// \\
                     |_    /
                     |-   |
             -       |   =|
                 |   |    |
--------------------/ ,  . \--------._""",
 """
                  v .   ._, |_  .,
           `-._\/  .  \ /    |/_
               \\\\  _\, y | \//
         _\_.___\\\\, \\\\/ -.\||
           `7-,--.`._||  / / ,
           /'     `-. `./ / |/_.'
               |     |    |//
                     |_    /  -
                     |-   |
                     |   =|
             \       |    |
--------------------/ ,  . \--------._""",
 """
                  v .   ._, |_  .,
           `-._\/  .  \ /    |/_
               \\\\  _\, y | \//
         _\_.___\\\\, \\\\/ -.\||
           `7-,--.`._||  / / ,
           /'     `-. `./ / |/_.'
           -         |    |//
               /     |_    /
                     |-   |   /
                     |   =|
                     |    |
--------------------/ ,  . \--------._""",
 """
                  v .   ._, |_  .,
           `-._\/  .  \ /    |/_
               \\\\  _\, y | \//
         _\_.___\\\\, \\\\/ -.\||
           `7-,--.`._||  / / ,
           /'     `-. `./ / |/_.'
                     |    |//
           /         |_    /
               -     |-   |
                     |   =|   |
                     |    |
--------------------/ ,  . \--------._""",
 """
                  v .   ._, |_  .,
           `-._\/  .  \ /    |/_
               \\\\  _\, y | \//
         _\_.___\\\\, \\\\/ -.\||
           `7-,--.`._||  / / ,
           /'-    `-. `./ / |/_.'
                 |   |    |//
                     |_    /
           |         |-   |
               \     |   =|
                     |    |   \\
--------------------/ ,  . \--------._""",
"""
                  v .   ._, |_  .,
           `-._\/  .  \ /    |/_
               \\\\  _\, y | \//
         _\_.___\\\\, \\\\/ -.\||
           `7-,--.`._||  / / ,
           /'     `-. `./ / |/_.'
             \       |    |//
                 /   |_    /
                     |-   |
           \         |   =|
               |     |    |
--------------------/ ,  . \--------._""",
"""
                  v .   ._, |_  .,
           `-._\/  .  \ /    |/_
               \\\\  _\, y | \//
         _\_.___\\\\, \\\\/ -.\||
           `7-,--.`._||  / / ,
           /'     `-. `./ / |/_.'
                     |    |//
             |       |_    /
                 -   |-   |
                     |   =|
           -         |    |
--------------------/ ,  . \--------._"""
]

# The little dancing man
dance1 = "♪┏(・o･)┛  ♪"
dance2 = "♪┗ ( ･o･) ┓♪"


# Contains the lyrics of the song, seperated per syllable to be able to put together to the rhythm
lyrics = [
    "\nLet's","\u200b go"," to"," see"," the"," stars"," and"," the"," moon",
    "\nI'd"," fly"," far"," in","to"," space"," as"," long"," as"," I"," am"," with"," you",
    "\nThe"," light"," in"," my"," bright"," eyes"," when"," you're"," near",
    "\nThe"," flut","ter","ing"," I"," feel"," in"," my"," chest"," when"," you"," are"," here",
    "\nI"," can't"," ex","plain"," this"," kind"," of"," love",
    "\nIt"," pulls"," me"," to"," you",", I"," want"," it",", I"," can't"," get"," e","nough",
    "\nSo"," share"," this"," pre","cious"," life"," with"," me",
    "\nJus","t take"," my"," hand"," and"," let's"," en","joy"," the"," things"," that"," we'll"," see\n\n"
    # 85
]

# Adds a bunch of new lines to block out what was previously in the console so new frames can be shown
whitespace = "\n\n\n\n\n\n\n"

# Create a thread so it can run smoothly instead of changing every note
showTea = True
def tea_updater():
    currentTea = 0
    # This will keep looping forever until showTea is set to false
    while showTea:
        # There is no frame 17, so this loops the animation
        if currentTea == 17: currentTea = 0
        # The first 7 frames keeps the animation still with no bubbles
        if currentTea < 8: 
            print(whitespace + teaGraphic[0])
        else:
            print(whitespace + teaGraphic[currentTea-7])
        time.sleep(0.2)
        currentTea += 1

# Same thing as the tea, but it always loops instead of having still frames
showTree = True
def tree_updater():
    currentTree = 0
    while showTree:
        # Loop the animation for as long as it's active, playing one frame per .2 seconds
        if currentTree == 8: currentTree = 0
        print(whitespace + treeGraphic[currentTree])
        time.sleep(0.2)
        currentTree += 1

def show_lyrics(i):
    j = 0
    # The lyrics start 120 notes behind, and adding 120 blank strings is just dumb, so we subtract!
    while j < len(lyrics[i-120]):
        print((lyrics[i-120])[j:j+1],end="",flush=True)
        # Find the length of the note that and divide that by the number of characters + 2 so there's space in between, so we can print out the characters 1 by 1 because why not!
        time.sleep(BTLengths[i]/(len(lyrics[i-120])+2))
        j += 1

def play_bubble_tea():
    global showTea
    global showTree
    showTea = True
    showTree = True
    vocals = AudioPlayer("Bubble Tea Vocals.mp3")
    teaTime = threading.Thread(target=tea_updater)
    treeTime = threading.Thread(target=tree_updater)
    teaTime.start()

    state = 0
    i = 0
    while i < 506:
        # Stop the tea animation and start displaying the lyrics
        if i == 116: vocals.play()
        if i >= 120 and i <= 205:
            showTea = False
            lyricThread = threading.Thread(target=show_lyrics, args=[i])
            lyricThread.start()
            # print(lyrics[i-120],end="",flush=True)

        # Once the lyrics are done, switch between the frames of the dancing guy to the rhythm
        if i > 206 and i < 395: 
            if state == 0:
                # This replaces the last line of text in the console
                sys.stdout.write("\r%s" % dance1)
                state = 1
            else:
                sys.stdout.write("\r%s" % dance2)
                state = 0

        # Once the little dude is done dancing, start the tree animation
        if i == 395: treeTime.start()
        # Stop the tree and display the credits once the song is done
        if i == 505: 
            showTree = False
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nThank you!\nSong: Bubble Tea by Dark Cat\nProject by Rhyder Swen")

        # time.sleep() is multiplied by 1.2 because for some reason, it is slightly shorter than the notes
        pysine.sine(BTMelody[i], BTLengths[i])
        time.sleep(BTRests[i]*1.2)
        i += 1

    select_song()


# BAD APPLE

# Redefine the variables to work with bad apple (it's in a different key)
E2 = 78
F2 = 87
G2 = 93
A2 = 104
B2 = 117
C3 = 123
D3 = 139
E3 = 156
F3 = 175
G3 = 185
A3 = 208
B3 = 233
C4 = 247
D4reg = 294
D4 = 277
E4reg = 330
E4 = 311
F4reg = 349
F4 = 349
G4reg = 392
G4 = 370
A4 = 415
B4 = 466
C5reg = 523
C5 = 494
D5 = 554
E5reg = 659
E5 = 622
F5reg = 698
F5 = 698
G5 = 740
A5 = 831
B5 = 932
C6 = 988
D6 = 1109
E6reg = 1319
E6 = 1245
F6 = 1397
G6 = 1480

# Again, redefine the lengths because Bad Apple is slightly slower than Bubble Tea
whole = 1.739
half = whole/2
quarter = half/2
eight = quarter/2
triplet = quarter/3
sixteen = eight/2
n32 = sixteen/2
dotQuarter = quarter+eight
dotEight = eight+sixteen
reg = 0

BAMelody = [
    E3,B3,E3,B3,E3,B3,E3,B3,E3,B3,
    E3,B3,E3,B3,E3,B3,E3,E3,
    E3,B3,E3,B3,E3,B3,E3,B3,E3,B3,
    E3,B3,E3,B3,E3,B3,E3,E3,
    E3,B3,E3,B3,E3,B3,E3,B3,E3,B3,
    E3,B3,E3,B3,E3,B3,E3,E3,
    E3,B3,E3,B3,E3,B3,E3,B3,E3,B3,
    E3,B3,E3,B3,E3,
    E5reg,E4reg,

    # 71

    E3,E3,B3,B3,D4,E4,E3,E3,B3,B3,D4,E4,
    E3,E3,B3,B3,D4,E4,E3,E4,G4,G3,G4,A4,
    E3,E3,B3,B3,D4,E4,E3,E3,B3,B3,D4,E4,
    E3,E3,B3,B3,D4,E4,A3,G4,A4,G3,E4,G4,
    E3,E3,B3,B3,D4,E4,E3,E3,B3,B3,D4,E4,
    E3,E3,B3,B3,D4,E4,E3,E4,G4,G3,G4,A4,
    E3,E3,B3,B3,D4,E4,E3,E3,B3,B3,D4,E4,
    E3,E3,B3,B3,D4,E4,A4,G4,A4,G4,E4,G4,

    # 167

    E4,F4,G4,A4,B4,E5,D5,
    B4,E4,B4,A4,G4,F4,
    E4,F4,G4,A4,B4,A4,G4,

    # 187

    F4,E4,F4,G4,F4,E4,D4reg,F4,
    E4,F4,G4,A4,B4,E5,D5,
    B4,E4,B4,A4,G4,F4,
    E4,F4,G4,A4,B4,A4,G4,

    # 215

    F4,G4,A4,B4,
    E4,F4,G4,A4,B4,E5,D5,
    B4,E4,B4,A4,G4,F4,
    E4,F4,G4,A4,B4,A4,G4,

    # 239

    F4,E4,F4,G4,F4,E4,D4reg,F4,
    E4,F4,G4,A4,B4,E5,D5,
    B4,E4,B4,A4,G4,F4,
    E4,F4,G4,A4,B4,A4,G4,

    # 267 // Page 3

    F4,G4,A4,B4,
    D5,E5,B4,A4,B4,A4,B4,
    D5,E5,B4,A4,B4,A4,B4,
    A4,G4,F4,D4,E4,D4,E4,

    # 292

    F4,G4,A4,B4,E4,B4,D5,
    D5,E5,B4,A4,B4,A4,B4,
    D5,E5,B4,A4,B4,A4,B4,
    A4,G4,F4,D4,E4,D4,E4,
    F4,G4,A4,B4,E4,B5,D6,

    # 327

    D6,E6,B5,A5,B5,A5,B5,
    D6,E6,B5,A5,B5,A5,B5,
    A5,G5,F5,D5,E5,D5,E5,
    F5,G5,A5,B5,E5,B5,D6,
    D6,E6,B5,A5,B5,A5,B5,

    # 362

    D6,E6,B5,A5,B5,E6,F6,
    G6,F6,E6,D6,B5,A5,B5,
    A5,G5,F5,D5,E5,B4,D5,

    # 383 - Repeat that

    D5,E5,B4,A4,B4,A4,B4,
    D5,E5,B4,A4,B4,A4,B4,
    A4,G4,F4,D4,E4,D4,E4,

    # 404 note not found

    F4,G4,A4,B4,E4,B4,D5,
    D5,E5,B4,A4,B4,A4,B4,
    D5,E5,B4,A4,B4,A4,B4,
    A4,G4,F4,D4,E4,D4,E4,
    F4,G4,A4,B4,E4,B5,D6,

    # 439

    D6,E6,B5,A5,B5,A5,B5,
    D6,E6,B5,A5,B5,A5,B5,
    A5,G5,F5,D5,E5,D5,E5,
    F5,G5,A5,B5,E5,B5,D6,
    D6,E6,B5,A5,B5,A5,B5,

    # 474

    D6,E6,B5,A5,B5,E6,F6,
    G6,F6,E6,D6,B5,A5,B5,
    A5,G5,F5,D5,E5

    # 493
]

BALengths = [
    eight,eight,eight,eight,eight,eight,sixteen,sixteen,sixteen,sixteen,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,sixteen,sixteen,sixteen,sixteen,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,sixteen,sixteen,sixteen,sixteen,
    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,eight,eight,sixteen,sixteen,sixteen,sixteen,
    eight,eight,eight,eight,quarter,eight,eight,

    eight,sixteen,eight,sixteen,sixteen,sixteen,eight,sixteen,eight,sixteen,sixteen,sixteen,
    eight,sixteen,eight,sixteen,sixteen,sixteen,eight,sixteen,sixteen,eight,sixteen,sixteen,
    eight,sixteen,eight,sixteen,sixteen,sixteen,eight,sixteen,eight,sixteen,sixteen,sixteen,
    eight,sixteen,eight,sixteen,sixteen,sixteen,eight,sixteen,sixteen,eight,sixteen,sixteen,
    eight,sixteen,eight,sixteen,sixteen,sixteen,eight,sixteen,eight,sixteen,sixteen,sixteen,
    eight,sixteen,eight,sixteen,sixteen,sixteen,eight,sixteen,sixteen,eight,sixteen,sixteen,
    eight,sixteen,eight,sixteen,sixteen,sixteen,eight,sixteen,eight,sixteen,sixteen,sixteen,
    eight,sixteen,eight,sixteen,sixteen,sixteen,triplet,triplet,triplet,triplet,triplet,triplet,

    eight,eight,eight,eight,quarter,eight,eight,
    quarter,quarter,eight,eight,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,

    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    quarter,quarter,eight,eight,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,

    quarter,quarter,quarter,quarter,
    eight,eight,eight,eight,quarter,eight,eight,
    quarter,quarter,eight,eight,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,

    eight,eight,eight,eight,eight,eight,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    quarter,quarter,eight,eight,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,

    quarter,quarter,quarter,quarter,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,

    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,

    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,

    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,

    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,

    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,

    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,

    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,quarter,eight,eight,
    eight,eight,eight,eight,half,

    # Ending bit after key change:

    eight,sixteen,eight,sixteen,eight,eight,sixteen,eight,sixteen,eight,
    eight,sixteen,eight,sixteen,eight,eight,sixteen,eight,sixteen,eight,
    eight,sixteen,eight,sixteen,eight,eight,sixteen,eight,sixteen,eight,
    eight,sixteen,eight,sixteen,eight,eight,sixteen,eight,sixteen,eight
]

# Redefine notes for the key change in Bad Apple
D4 = 294
E4 = 330
F4 = 370
G4 = 392
A4 = 440
B4 = 494
C5flt = 494
C5 = 523
D5 = 587
E5 = 659
F5 = 740
G5 = 784
A5 = 880
B5 = 988
C6 = 1047
D6 = 1175
E6 = 1319
F6 = 1480
G6 = 1568

BAMelodyKC = [
    C5flt,D5,
    D5,E5,B4,A4,B4,A4,B4,
    D5,E5,B4,A4,B4,A4,B4,
    A4,G4,F4,D4,E4,D4,E4,

    # 23

    F4,G4,A4,B4,E4,B4,D5,
    D5,E5,B4,A4,B4,A4,B4,
    D5,E5,B4,A4,B4,A4,B4,
    A4,G4,F4,D4,E4,D4,E4,
    F4,G4,A4,B4,E4,B5,D6,

    # 58

    D6,E6,B5,A5,B5,A5,B5,
    D6,E6,B5,A5,B5,A5,B5,
    A5,G5,F5,D5,E5,D5,E5,
    F5,G5,A5,B5,E5,B5,D6,
    D6,E6,B5,A5,B5,A5,B5,

    # 93

    D6,E6,B5,A5,B5,E6,F6,
    G6,F6,E6,D6,B5,A5,B5,
    A5,G5,F5,D5,E5,

    # 112

    A4,A4,B4,A4,B4,A4,A4,B4,A4,B4,
    A4,A4,B4,A4,B4,A4,A4,B4,A4,B4,
    A4,A4,B4,A4,B4,A4,A4,B4,A4,B4,
    A4,A4,B4,A4,B4,A4,A4,B4,A4,B4

    # 152
]

def play_bad_apple_video():
    # Open read-only database file that stores all the frames
    database = open("Bad Apple Frames.txt", "r")
    # Split each frame into its own entry in an array
    frames = database.read().split("-")
    # Ensures that it plays at 30fps
    timer = fpstimer.FPSTimer(30)

    # Plays the video
    for frame in frames:
        print(frame)
        timer.sleep()

def play_bad_apple():
    BAVideo = threading.Thread(target=play_bad_apple_video)
    BAVideo.start()

    i = 0
    while i < 493:
        pysine.sine(BAMelody[i], BALengths[i])
        # There are literally no rests in bad apple, and I don't wanna type reg 5 million times for nothing, so having time.sleep() would be unnecessary here
        i += 1
    
    # Loop notes 71-380
    i = 71
    while i < 381:
        pysine.sine(BAMelody[i], BALengths[i])
        i += 1
    
    # KEY CHANGE TIME BAYBEEEEEE
    i = 0
    while i < 152:
        pysine.sine(BAMelodyKC[i], BALengths[i+381])
        # Adds 381 to the index of the length array because the lengths of the notes in the key change are the same as in the regular, and I don't wanna make another variable
        i += 1

    BAVideo.join()
    select_song()


# Song Selector
def select_song():
    choice = input("""\n==============================================================
Choose a song: 
1) Bubble Tea
2) Bad Apple
3) Exit
==============================================================\n""")

    while True:
        if choice == "1": play_bubble_tea()
        elif choice == "2": play_bad_apple()
        elif choice == "3": quit()
        else: choice = input("That is not a valid input! Please try again!\n")

select_song()