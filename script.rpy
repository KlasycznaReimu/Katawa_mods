## The script of the game goes in this file.

## Declare characters used by this game. The color argument colorizes the name
## of the character.

##Niji me fecit 2016-2020
##Communism or barbarism. Only communism will have a chance of mitigating the ongoing climate catastrophe.
##Arm the workers. Arm the homeless. Hang the bankers from the lampposts. Guillotine the billionaires.
##Pour molten gold down Bezos' throat. The only good fascist is a dead one. Free Palestine.
##Trans rights are human rights. No one is illegal. John Brown was right. Lilly and Miki are Best Girls.
##nijidoggo@gmail.com

init -1 python:
    renpy.music.register_channel("ambient", "sfx", True)


init python:

#naughty stuff.
    if persistent.adultmode is False:
        persistent.adultmode = False

#various moves
    define.move_transitions("charamove", 1.0, _ease_time_warp, _ease_in_time_warp, _ease_out_time_warp)
    define.move_transitions("charamovefast", 0.5, _ease_time_warp, _ease_in_time_warp, _ease_out_time_warp)
    define.move_transitions('charamove_slow', 2.0, _ease_time_warp, _ease_in_time_warp, _ease_out_time_warp)
    def Dissolvemove(time, time_warp=_ease_time_warp):
        top = Dissolve(time)
        before = MoveTransition(time, factory=MoveFactory(time_warp=time_warp), old=True)
        after = MoveTransition(time, factory=MoveFactory(time_warp=time_warp))
        return ComposeTransition(top, before=before, after=after)

    dissolvecharamoveslowish = Dissolvemove(2.0)
    dissolvecharamove = Dissolvemove(1.0)
    dissolvecharamoveslow = Dissolvemove(3.0)
    dissolvecharamovefast = Dissolvemove(0.75)
    dissolvecharamovereallyfast = Dissolvemove(0.15)

#this is needed for the kslogo clockwipe, also uses stuff further down (WORKS! -Niji)
    def start_music(track,f=1.0):
        renpy.music.play(track, fadein=f)
        return
    def stop_music(f=1.0):
        renpy.music.stop(fadeout=f)
        return

#steam (WORKS! -Niji)
    steam = anim.TransitionAnimation("vfx/steam1.png", 1.5, Dissolve(0.5, alpha=True),
                                     "vfx/steam2.png", 1.5, Dissolve(0.5, alpha=True),
                                     "vfx/steam3.png", 1.5, Dissolve(0.5, alpha=True))
    steam2 = anim.TransitionAnimation("vfx/steam3.png", 0.75, Dissolve(0.5, alpha=True),
                                     "vfx/steam1.png", 1.5, Dissolve(0.5, alpha=True),
                                     "vfx/steam2.png", 1.5, Dissolve(0.5, alpha=True),
                                     "vfx/steam3.png", 0.75, None)

    renpy.image("steam", steam)
    renpy.image("steam2", steam2)

#constructors (openeyeslow works, rest assumed to work - Niji)
    dotwipe_down = ImageDissolve(im.Tile("ui/tr-dots_col.png"), 0.5, 32, ramptype="mcube") #this is needed after you click load, options or jukebox -Niji
    dotwipe_up = ImageDissolve(im.Tile("ui/tr-dots_col.png"), 0.5, 32, ramptype="mcube", reverse = True) #this is needed after you click to start the game -Niji
    slowfade = Fade(1.0, 0.5, 1.0)
    openeye = ImageDissolve('vfx/tr_eyes.png', 2.0, 64, ramptype='cube')
    openeyeslow = ImageDissolve('vfx/tr_eyes.png', 3.5, 64, ramptype='cube')
    shuteye = ImageDissolve('vfx/tr_eyes.png', 2.0, 64, ramptype='mcube', reverse=True)
    openeyefast = ImageDissolve('vfx/tr_eyes.png', 0.5, 64, ramptype='cube')
    shuteyefast = ImageDissolve('vfx/tr_eyes.png', 0.20000000000000001, 64, ramptype='mcube', reverse=True)
    shuteyemed = ImageDissolve('vfx/tr_eyes.png', 1.00000000000000001, 64, ramptype='mcube', reverse=True)
    openeye_shock = ImageDissolve('vfx/tr-openshock.png', 0.80000000000000004, 64, ramptype='cube')

#this is the code to make soundtransition work, wich we need to make delayblindsfade work wich is shorttimeskip -Niji
    def is_glrenpy():
        if (int(renpy.version().split('.')[1])) > (10):
            return True
        else:
            return False

    class SoundTransitionClassCompat(renpy.display.transition.Transition):
        __doc__ = '\n        A transition that does nothing but play a sound.\n        To be used in MultipleTransitions, obviously.\n        '
        def __init__(self, sound, time=0.0001, channel='sound', old_widget=None, new_widget=None, **properties):
            super(SoundTransitionClassCompat, self).__init__(time, **properties)
            self.time = time
            self.old_widget = old_widget
            self.new_widget = new_widget
            self.events = False
            self.sound = sound
            self.channel = channel
        def render(self, width, height, st, at):
            if (st) >= (self.time):
                self.events = True
                return render(self.new_widget, width, height, st, at)
            if (st) < (self.time):
                renpy.display.render.redraw(self, 0)
            renpy.sound.play(self.sound, channel=self.channel)
            return renpy.display.render.Render(width, height, opaque=True)
    def disp_size(disp):
        if isinstance(disp, str):
            disp = im.Image(disp)
        return disp.load().get_size()
    def quasiblur(disp_in, factor, bilinear_out=True, bilinear_in=True):
        disp_down = im.FactorScale(disp_in, width=(1.0) / (factor), bilinear=bilinear_in)
        if bilinear_out:
            (in_w, in_h) = disp_size(disp_in)
            disp_up = im.Scale(disp_down, width=int((in_w) + (factor)), height=int((in_h) + (factor)), bilinear=True)
            disp_up = im.Crop(disp_up, 0, 0, in_w, in_h)
        else:
            disp_up = im.FactorScale(disp_down, width=factor, bilinear=False)
        return disp_up
    class SoundTransitionClassGL(renpy.display.transition.Transition):
        __doc__ = '\n        A transition that does nothing but play a sound.\n        To be used in MultipleTransitions, obviously.\n        '
        def __init__(self, sound, delay=0.0001, channel='sound', old_widget=None, new_widget=None, **properties):
            super(SoundTransitionClassGL, self).__init__(delay, **properties)
            self.old_widget = old_widget
            self.new_widget = new_widget
            self.events = True
            self.sound = sound
            self.channel = channel
            self.played = False
        def render(self, width, height, st, at):
            if not (self.played):
                renpy.sound.play(self.sound, channel=self.channel)
                self.played = True
            return renpy.display.transition.null_render(self, width, height, st, at)
    if is_glrenpy():
        SoundTransition = renpy.curry(SoundTransitionClassGL)
    else:
        SoundTransition = renpy.curry(SoundTransitionClassCompat)
    def transition_attach_sound(tr_in, sound):
        return MultipleTransition([False, SoundTransition(sound), False, tr_in, True])

    delayblinds = ImageDissolve("vfx/tr-delayblinds.png", 1.0)

    delayblindsfade = MultipleTransition([False, SoundTransition('sfx/time.ogg'), False, delayblinds, Solid('#000'), delayblinds, True])


# effect abstractions (shorttimeskip works, others assumed to work - Niji)
    menueffect = dissolve
    charaenter = dissolve
    charaexit = dissolve
    charachange = dissolve
    characlose = dissolve
    charadistant = dissolve
    locationchange = dissolve
    locationskip = fade
    shorttimeskip = delayblindsfade

    clockwipe = ImageDissolve(im.Tile("ui/tr-clockwipe.png"), 2.0, 8)

#crowd (works - Niji)
    crowd = anim.TransitionAnimation("vfx/crowd1.png", 1.0, Dissolve(0.2, alpha=True),
                                     "vfx/crowd2.png", 1.0, Dissolve(0.2, alpha=True),
                                     "vfx/crowd3.png", 1.0, Dissolve(0.2, alpha=True))



    renpy.image("crowd", crowd)


    ##crowd_ss = anim.TransitionAnimation(sunset("vfx/crowd1.png"), 1.0, Dissolve(0.2, alpha=True),
                                        ##sunset("vfx/crowd2.png"), 1.0, Dissolve(0.2, alpha=True),
                                        ##sunset("vfx/crowd3.png"), 1.0, Dissolve(0.2, alpha=True))

    ##renpy.image("crowd_ss", crowd_ss)

    ##crowd_ni = anim.TransitionAnimation(night("vfx/crowd1.png"), 1.0, Dissolve(0.2, alpha=True),
                                        ##night("vfx/crowd2.png"), 1.0, Dissolve(0.2, alpha=True),
                                        ##night("vfx/crowd3.png"), 1.0, Dissolve(0.2, alpha=True))

    ##renpy.image("crowd_ni", crowd_ni)

# Fireworks (works -Niji)
    def fw_constructor(image, sparkle=True, normalprob = 1):
        sparklebase = anim.Blink(image, high=1.0, low=10.0, on=0.2, off=0.0, set=3.0)
        sparkleprob = 1
        if not sparkle:
            sparklestate = image
            onstate = image
        elif str(sparkle) == "True":
            sparklestate = sparklebase
            onstate = sparklebase
        else:
            sparklestate = sparklebase
            onstate = image
            sparkleprob = sparkle
        return anim.SMAnimation("blank",
                                anim.State("blank", Solid("#00000000")),
                                anim.Edge("blank", 0.1, "blank", prob=30),
                                anim.Edge("blank", 0.1, "flash", trans = Dissolve(0.04, alpha=True)),
                                anim.State("flash", Solid("#FFFFFF66")),
                                anim.Edge("flash", 0.1, "on", trans = Dissolve(0.04, alpha=True), prob=normalprob),
                                anim.Edge("flash", 0.1, "sparkle", trans = Dissolve(0.04, alpha=True), prob=sparkleprob),
                                anim.State("on", onstate),
                                anim.Edge("on", 6.0, "blank", trans = Dissolve(3.0, alpha=True)),
                                anim.State("sparkle", sparklestate),
                                anim.Edge("sparkle", 6.0, "blank", trans = Dissolve(3.0, alpha=True)),
                                showold=True)

    fireworks = LiveComposite((800,600),
                              (0,0), fw_constructor("vfx/fw1.png"),
                              (0,0), fw_constructor("vfx/fw2.png"),
                              (0,0), fw_constructor("vfx/fw3.png"),
                              (0,0), fw_constructor("vfx/fw4.png"),
                              (0,0), fw_constructor("vfx/fw5.png"),
                              (0,0), fw_constructor("vfx/fw6.png"),
                              (0,0), fw_constructor("vfx/fw7.png"),
                              (0,0), fw_constructor("vfx/fw8.png", sparkle=1),
                              (0,0), fw_constructor("vfx/fw9.png", sparkle=1))

    renpy.image("fireworks",fireworks)

# display tools (works -Niji)
    twoleft = Position(xanchor=0.5, xpos=0.3, yanchor=0.5, ypos=0.5)
    tworight = Position(xanchor=0.5, xpos=0.7, yanchor=0.5, ypos=0.5)

    oneleft = Position(xanchor=0.5, yanchor=0.5, xpos=0.4, ypos=0.5)
    oneright = Position(xanchor=0.5, xpos=0.6, yanchor=0.5, ypos=0.5)

    twoleftsit = Position(xanchor=0.5, yanchor=1.0, xpos=0.3, ypos=1.15)
    tworightsit = Position(xanchor=0.5, yanchor=1.0, xpos=0.7, ypos=1.15)
    leftsit = Position(xanchor=0.5, yanchor=1.0, xpos=0.15, ypos=1.15)
    rightsit = Position(xanchor=0.5, yanchor=1.0, xpos=0.85, ypos=1.15)
    centersit = Position(xanchor=0.5, yanchor=1.0, xpos=0.5, ypos=1.15)
    centersit2 = Position(xanchor=0.5, yanchor=1.0, xpos=0.5, ypos=1.07)
    centersitlow = Position(xanchor=0.5, yanchor=1.0, xpos=0.5, ypos=1.25)
    twoleftsitlow = Position(xanchor=0.5, yanchor=1.0, xpos=0.3, ypos=1.25)
    oneleftsitlow = Position(xanchor=0.5, yanchor=1.0, xpos=0.4, ypos=1.25)
    onerightsitlow = Position(xanchor=0.5, yanchor=1.0, xpos=0.6, ypos=1.25)
    tworightsitlow = Position(xanchor=0.5, yanchor=1.0, xpos=0.7, ypos=1.25)

    closeleft = Position(xanchor=0.5, xpos=0.25, yanchor=0.5, ypos=0.5)
    closeright = Position(xanchor=0.5, xpos=0.75, yanchor=0.5, ypos=0.5)
    closeleft2 = Position(xanchor=0.5, xpos=0.20,yanchor=0.5, ypos=0.5)

    rightedge = Position(xanchor=0.5, xpos=0.92, yanchor=0.5, ypos=0.5)
    leftoff = Position(xanchor=0.5, xpos=0.13, yanchor=0.5, ypos=0.5)
    centeroff = Position(xanchor=0.5, xpos=0.52, yanchor=0.5, ypos=0.5)

    twoleftoff = Position(xanchor=0.5, xpos=0.32, yanchor=0.5, ypos=0.5)
    tworightoff = Position(xanchor=0.5, xpos=0.68, yanchor=0.5, ypos=0.5)
    centeroff = Position(xanchor=0.5, xpos=0.52, yanchor=0.5, ypos=0.5)
    twocenteroff = Position(xanchor=0.5, xpos=0.39, yanchor=0.5, ypos=0.5)
    twocenteroff2 = Position(xanchor=0.5, xpos=0.41, yanchor=0.5, ypos=0.5)
    twocenteroff3 = Position(xanchor=0.5, xpos=0.59, yanchor=0.5, ypos=0.5)

    tworightstagger = Position(xanchor=0.5, xpos=0.6, yanchor=0.5, ypos=0.5)

    leftdoor = Position(xanchor=0.5, xpos=0.10, yanchor=0.5, ypos=0.5)
    leftdooropen = Position(xanchor=0.5, xpos=-0.1, yanchor=0.5, ypos=0.5)
    rightwallopen = Position(xanchor=0.5, xpos=0.85, yanchor=0.5, ypos=0.5)
    roomopen = Position(xanchor=0.5, xpos=0.45, yanchor=0.5, ypos=0.5)

    bgleft = Position(xanchor=0.5, xpos=0.4, yanchor=0.5, ypos=0.5)
    bgright = Position(xanchor=0.5, xpos=0.6, yanchor=0.5, ypos=0.5)

    leftoffsit = Position(xanchor=0.5, xpos=0.13, yanchor=1.0, ypos=1.15)
    rightedgesit = Position(xanchor=0.5, xpos=0.92, yanchor=1.0, ypos=1.15)

    oneleftsit = Position(xanchor=0.5, yanchor=1.0, xpos=0.4, ypos=1.15)
    onerightsit = Position(xanchor=0.5, yanchor=1.0, xpos=0.6, ypos=1.15)

    leftsitlow = Position(xanchor=0.5, yanchor=1.0, xpos=0.15, ypos=1.25)
    rightsitlow = Position(xanchor=0.5, yanchor=1.0, xpos=0.85, ypos=1.25)

    rightedgetsu = Position(xanchor=0.5, xpos=0.92, yanchor=0.45, ypos=0.5)
    tworighttsu = Position(xanchor=0.5, xpos=0.7, yanchor=0.45, ypos=0.5)
    leftoffmiyu = Position(xanchor=0.5, xpos=0.01, yanchor=0.17, ypos=0.5)


#logo clockwipe, also uses stuff at the top (WORKS -Niji)

define fadeslow = Fade(0.7, 0.3, 0.7)
define kslogowords = "kslogowords.png"
define kslogoheart = "kslogoheart.png"
image solid_black = Solid("#000")
define passingoftime = ImageDissolve("ui/tr-clockwipe.png", 2.0)

#this causes the blinky arrow in the nvl box, need to figure out how get it to show up after every paragraph -Niji
define config.nvl_page_ctc = anim.Filmstrip("ui/ctc_strip.png", (16,16), (8,8), 0.03, ypos=560, xpos=772) #This MAY be more efficient...
define config.nvl_page_ctc_position = "fixed"


#this causes the blinky arrow in the say box -Niji
image ctc_blink:
        xpos 0.98 ypos 0.95
        xanchor 1.0 yanchor 1.0
        "ui/ctc.png"
        linear 1.0 alpha 1.0
        "ui/ctc_blank.png"
        linear 1.0 alpha 1.0
        repeat

#flashes
define flash = Fade(0.25, 0,.75, color="#FFFFFF")
define shortflash = Fade(0.25, 0, 0.4, color="#FFFFFF")
define whiteout = Fade(0.5, 0.2, 2.0, color="#FFFFFF")
define blackflash = Fade(0.75, 0,.75, color="#000000")

#shake character
transform flinch:
        linear 0.096 xoffset -10 #move left 20 pixel in 0.2 seconds
        linear 0.096 xoffset +10 #move right 20 pixel in 0.2 seconds
        repeat 2 #repeat the above 5 times

#Characters
define n = nvl
define hi = Character("Hisao", color=(200, 255, 200, 255), ctc="ctc_blink", ctc_position="fixed")
define mk = Character("Miki", color=(173, 115, 94, 255), ctc="ctc_blink", ctc_position="fixed")
define har = Character("Haru", color=(249, 234, 160, 255), ctc="ctc_blink", ctc_position="fixed")
define suz = Character("Suzu", color=(114, 173, 238, 255), ctc="ctc_blink", ctc_position="fixed")
define yuk = Character("Yukio", color=(137, 124, 191, 255), ctc="ctc_blink", ctc_position="fixed")
define yu = Character("Yuuko", color=(44, 158, 49, 255), ctc="ctc_blink", ctc_position="fixed")
define ke = Character("Kenji", color=(204, 124, 42, 255), ctc="ctc_blink", ctc_position="fixed")
define jun = Character("Dad", color=(235, 36, 59, 255), ctc="ctc_blink", ctc_position="fixed")
define mu = Character("Mutou", color=(255, 255, 255, 255), ctc="ctc_blink", ctc_position="fixed")
define mot = Character("Mrs Suzuki", color=(221, 221, 211, 255), ctc="ctc_blink", ctc_position="fixed")
define dad = Character("Mr Suzuki", color=(241, 241, 241, 255), ctc="ctc_blink", ctc_position="fixed")
define tsu = Character("Tsubasa", color=(233, 78, 119, 255), ctc="ctc_blink", ctc_position="fixed")
define yam = Character("Yamada", color=(255, 141, 124, 255), ctc="ctc_blink", ctc_position="fixed")
define shi = Character("Shizune", color=(114, 137, 238, 255), ctc="ctc_blink", ctc_position="fixed")


#sprites and backgrounds
image generic_missing = "generic_missing.png"
image hisao_blank = "hisao_blank.png"
image hisao_erm = "hisao_erm.png"
image hisao_erm_u = "hisao_erm_uniform.png"
image hisao_talk_big = "hisao_talk_big.png"
image hisao_talk_big_u = "hisao_talk_big_uniform.png"
image hisao_smile = "hisao_smile.png"
image hisao_smile_u = "hisao_smile_uniform.png"
image hisao_wtf = "hisao_wtf.png"
image hisao_wtf_u = "hisao_wtf_uniform.png"
image hisao_biggrin = "hisao_biggrin.png"
image hisao_biggrin_u = "hisao_biggrin_uniform.png"
image hisao_disappoint = "hisao_disappoint.png"
image hisao_disappoint_u = "hisao_disappoint_uniform.png"
image hisao_frown = "hisao_frown.png"
image hisao_frown_u = "hisao_frown_uniform.png"
image hisao_heh = "hisao_heh.png"
image hisao_heh_u = "hisao_heh_uniform.png"
image hisao_smile_teeth = "hisao_smile_teeth.png"
image hisao_smile_teeth_u = "hisao_smile_teeth_uniform.png"
image hisao_talk_small = "hisao_talk_small.png"
image hisao_talk_small_u = "hisao_talk_small_uniform.png"
image hisao_hmpf = "hisao_hmpf.png"
image hisao_hmpf_u = "hisao_hmpf_uniform.png"
image hisao_closed = "hisao_closed.png"
image hisao_closed_u = "hisao_closed_uniform.png"
image hisao_declare = "hisao_declare.png"
image hisao_declare_u = "hisao_declare_uniform.png"
image hisao_blush = "hisao_blush.png"
image hisao_blush_u = "hisao_blush_uniform.png"
image hisao_beach_blush = "hisao_beach_blush.png"
image hisao_beach_frown = "hisao_beach_frown.png"
image hisao_beach_smile = "hisao_beach_smile.png"
image hisao_beach_erm = "hisao_beach_erm.png"
image hisao_beach_disappoint = "hisao_beach_disappoint.png"
image hisao_beach_talk = "hisao_beach_talk.png"
image hisao_beach_grin = "hisao_beach_grin.png"
image hisao_beach_declare = "hisao_beach_declare.png"
image hisao_topless = "hisao_topless.png"
image hisao_pale = "hisao_pale.png"
image hisao_wtf_close = "hisao_wtf_close.png"
image hisao_wtf_close_u = "hisao_wtf_close_uniform.png"
image hisao_erm_close = "hisao_erm_close.png"
image hisao_erm_close_u = "hisao_erm_close_uniform.png"
image hisao_smile_close = "hisao_smile_close.png"
image hisao_smile_close_u = "hisao_smile_close_uniform.png"
image hisao_topless_smile = "hisao_topless_smile.png"
image rin = "rin.png"
image haru_annoyed = "haru_annoyed.png"
image haru_basic = "haru_basic.png"
image haru_sad = "haru_sad.png"
image haru_serious = "haru_serious.png"
image haru_smile = "haru_smile.png"
image haru_yo = "haru_yo.png"
image suzu_angry = "suzu_angry.png"
image suzu_angry_d = "suzu_angry_dress.png"
image suzu_concerned = "suzu_concerned.png"
image suzu_concerned_d = "suzu_concerned_dress.png"
image suzu_embarrassed = "suzu_embarrassed.png"
image suzu_embarrassed_d = "suzu_embarrassed_dress.png"
image suzu_grin = "suzu_grin.png"
image suzu_grin_d = "suzu_grin_dress.png"
image suzu_happy = "suzu_happy.png"
image suzu_happy_d = "suzu_happy_dress.png"
image suzu_invis = "suzu_invis.png"
image suzu_normal = "suzu_normal.png"
image suzu_normal_d = "suzu_normal_dress.png"
image suzu_side = "suzu_side.png"
image suzu_smile = "suzu_smile.png"
image suzu_smile_d = "suzu_smile_dress.png"
image suzu_speak = "suzu_speak.png"
image suzu_speak_d = "suzu_speak_dress.png"
image suzu_surprised = "suzu_surprised.png"
image suzu_surprised_d = "suzu_surprised_dress.png"
image suzu_veryangry = "suzu_veryangry.png"
image suzu_veryangry_d = "suzu_veryangry_dress.png"
image suzu_unhappy = "suzu_unhappy.png"
image suzu_unhappy_d = "suzu_unhappy_dress.png"
image suzu_sleepy = "suzu_sleepy.png"
image suzu_sleepy_d = "suzu_sleepy_dress.png"
image suzu_asleep = "suzu_asleep.png"
image suzu_asleep_d = "suzu_asleep_dress.png"
image suzu_veryembarrassed = "suzu_veryembarrassed.png"
image suzu_veryembarrassed_d = "suzu_veryembarrassed_dress.png"
image suzu_beach_normal = "suzu_beach_normal.png"
image suzu_beach_annoyed = "suzu_beach_annoyed.png"
image suzu_beach_angry = "suzu_beach_angry.png"
image suzu_beach_smile = "suzu_beach_smile.png"
image suzu_beach_small_em = "suzu_beach_small_em.png"
image suzu_beach_sad = "suzu_beach_sad.png"
image suzu_beach_surprised = "suzu_beach_surprised.png"
image suzu_cry = "suzu_cry.png"
image suzu_cry_d = "suzu_cry_dress.png"
image suzu_cry_smile = "suzu_cry_smile.png"
image suzu_cry_smile_d = "suzu_cry_smile_dress.png"
image suzu_despair = "suzu_despair.png"
image suzu_despair_d = "suzu_despair_dress.png"
image suzu_neutral = "suzu_neutral.png"
image suzu_neutral_d = "suzu_neutral_dress.png"
image suzu_glare = "suzu_glare.png"
image suzu_glare_d = "suzu_glare_dress.png"
image yukio_angry = "yukio_angry.png"
image yukio_blush = "yukio_blush.png"
image yukio_eeh = "yukio_eeh.png"
image yukio_huh = "yukio_huh.png"
image yukio_notimpressed = "yukio_notimpressed.png"
image yukio_smile = "yukio_smile.png"
image yukio_punched = "yukio_punched.png"
image yukio_punched_defiant = "yukio_punched_defiant.png"
image yukio_punched_angry = "yukio_punched_angry.png"
image yuukoshang_happy_down = "yuukoshang_happy_down.png"
image yuukoshang_happy_up = "yuukoshang_happy_up.png"
image yuuko_neurotic_up = "yuuko_neurotic_up.png"
image yuuko_cry_up = "yuuko_cry_up.png"
image yuuko_worried_up = "yuuko_worried_up.png"
image yuuko_neutral_down = "yuuko_neutral_down.png"
image kenji_neutral = "kenji_neutral.png"
image kenji_tsun = "kenji_tsun.png"
image kenji_happy = "kenji_happy.png"
image kimono_normal = "kimono_normal.png"
image kimono_unhappy = "kimono_unhappy.png"
image kimono_embarrassed = "kimono_embarrassed.png"
image kimono_grin = "kimono_grin.png"
image kimono_happy = "kimono_happy.png"
image tsu_tooth_smile = "tsu_tooth_smile.png"
image tsu_annoyed = "tsu_annoyed.png"
image tsu_smile = "tsu_smile.png"
image tsu_tongue = "tsu_tongue.png"
image tsu_deadpan = "tsu_deadpan.png"
image tsu_ooh = "tsu_ooh.png"
image tsu_sad = "tsu_sad.png"
image tsu_question = "tsu_question.png"
image tsu_hmm = "tsu_hmm.png"
image tsu_erm = "tsu_erm.png"
image tsu_dumps = "tsu_dumps.png"
image tsu_beach_deadpan = "tsu_beach_deadpan.png"
image tsu_beach_erm = "tsu_beach_erm.png"
image tsu_beach_closed = "tsu_beach_closed.png"
image tsu_beach_tooth_smile = "tsu_beach_tooth_smile.png"
image mother_normal = "mother_normal.png"
image mother_soften = "mother_soften.png"
image mother_angry = "mother_angry.png"
image mother_yell = "mother_yell.png"
image mother_tight = "mother_tight.png"
image mother_murder = "mother_murder.png"
image mother_closed = "mother_closed.png"
image mother_smile = "mother_smile.png"
image miyu_happy = "miyu_happy.png"
image miyu_normal = "miyu_normal.png"
image AGirl = "AGirl.png"
image phone = "mobile-sprite.png"
image junko_question = "junko_question.png"
image junko_smile = "junko_smile.png"
image junko_frown = "junko_frown.png"
image junko_grin = "junko_grin.png"
image junko_embarrassed = "junko_embarrassed.png"
image shizu_basic_normal2 = "shizu_basic_normal2.png"
image shizu_behind_blank = "shizu_behind_blank.png"
image shizu_basic_angry = "shizu_basic_angry.png"
image shizu_cross_angry = "shizu_cross_angry.png"
image shizu_behind_frown = "shizu_behind_frown.png"
image dad_smile = "dad_smile.png"
image dad_smirk = "dad_smirk.png"
image dad_laugh = "dad_laugh.png"
image dad_talk = "dad_talk.png"
image dad_grump = "dad_grump.png"
image dad_normal = "dad_normal.png"
image dad_frown = "dad_frown.png"
image dad_unhappy = "dad_unhappy.png"
image dad_smile_close = "dad_smile_close.png"
image muto_irritated = "muto_irritated.png"
image muto_normal = "muto_normal.png"
image muto_smile = "muto_smile.png"
image aoi_smile = "aoi_smile.png"
image aoi_surprised = "aoi_surprised.png"
image saki = "saki.png"
image saki_frown = "saki_frown.png"
image haru_conehead = "haru_conehead.png"
image suzu_angry_lift = "suzu_angry_lift.png"
image suzu_speak_close = "suzu_speak_close.png"
image suzu_speak_close_d = "suzu_speak_close_dress.png"
image kimono_happy_close = "kimono_happy_close.png"
image suzu_veryembarrassed_close = "suzu_veryembarrassed_close.png"
image suzu_veryembarrassed_close_d = "suzu_veryembarrassed_close_dress.png"
image suzu_smile_close = "suzu_smile_close.png"
image suzu_smile_close_d = "suzu_smile_close_dress.png"
image suzu_father_happy = "suzu_father_happy.png"
image suzu_father_unhappy = "suzu_father_unhappy.png"
image suzu_father_normal = "suzu_father_normal.png"
image suzu_father_shock = "suzu_father_shock.png"
image kid_laugh = "kid_laugh.png"
image kid_mimic = "kid_mimic.png"
image kid_staring = "kid_staring.png"
image waiter_neutral = "waiter_neutral.png"
image waiter_happy = "waiter_happy.png"
image pills = "pills.png"
image bg school_gardens_ss = "school_gardens_ss.jpg"
image bg school_track_ss = "school_track_ss.jpg"
image bg suburb_shanghaiext_ss = "suburb_shanghaiext_ss.jpg"
image bg suburb_shanghaiint = "suburb_shanghaiint.jpg"
image bg school_gardens3 = "school_gardens3.jpg"
image bg city_karaokeint = "city_karaokeint.jpg"
image bg school_library = "school_library.jpg"
image bg school_cafeteria = "school_cafeteria.jpg"
image bg school_scienceroom = "school_scienceroom.jpg"
image bg school_gate = "school_gate.jpg"
image bg school_road = "school_road.jpg"
image bg suburb_shanghaiext = "suburb_shanghaiext.jpg"
image bg school_road_ss = "school_road_ss.jpg"
image bg school_girlsdormhall = "school_girlsdormhall.jpg"
image bg city_street4 = "city_street4.jpg"
image bg city_cafe = "city_cafe.jpg"
image bg school_track_running = "school_track_running.jpg"
image bg school_track = "school_track.jpg"
image bg school_dormext_start = "school_dormext_start.jpg"
image bg school_dormhallground = "school_dormhallground.jpg"
image bg school_dormhallway = "school_dormhallway.jpg"
image bg school_dormhisao = "school_dormhisao.jpg"
image bg school_dormkenji = "school_dormkenji.jpg"
image bg suburb_konbiniext_ni = "suburb_konbiniext_ni.jpg"
image bg school_dormmiki = "school_dormmiki.jpg"
image bg city_street2 = "city_street2.jpg"
image bg arcade = "arcade.jpg"
image bg dormsuzu = "dormsuzu.jpg"
image bg school_hallway3 = "school_hallway3.jpg"
image bg suburb_roadcenter_ni = "suburb_roadcenter_ni.jpg"
image bg hatsune = "hatsune.jpg"
image bg iwanako_letter = "iwanako_letter.png"
image bg 4265edited = "4265edited.png"
image bg suburb_tanabata_ni = "suburb_tanabata_ni.jpg"
image bg tanabata_game = "tanabata_game.jpg"
image bg misc_sky_ni = "misc_sky_ni.jpg"
image bg 4317 = "4317.png"
image bg city_trainstation = "city_trainstation.jpg"
image bg city_houseext = "city_houseext.jpg"
image bg city_houseint = "city_houseint.jpg"
image bg city_housekitchen = "city_housekitchen.jpg"
image bg suzu_bedroom = "suzu_bedroom.jpg"
image bg 4399 = "4399.png"
image bg 4150 = "4150.jpg"
image bg city_street1 = "city_street1.jpg"
image bg suburb_road = "suburb_road.jpg"
image bg road = "road.jpg"
image bg ishigaki_day = "ishigaki_day.jpg"
image bg ishigaki_evening = "ishigaki_evening.jpg"
image bg ishigaki_sea = "ishigaki_sea.jpg"
image bg izakaya = "izakaya.jpg"
image bg 4337 = "4337.jpg"
image bg 4361 = "4361.jpg"
image bg sushi = "sushi.png"
image bg city_street3_ni = "city_street3_ni.jpg"
image bg 4237 = "4237.png"
image bg misc_ceiling_ni = "misc_ceiling_ni.jpg"
image bg school_track_on = "school_track_on.jpg"
image bg misc_ceiling_ss = "misc_ceiling_ss.jpg"
image bg school_nurseoffice_ss = "school_nurseoffice_ss.jpg"
image bg mp3 = "mp3.png"
image bg school_dormbathroom = "school_dormbathroom.jpg"
image bg 4255 = "4255.png"
image bg 4258 = "4258.png"
image bg cinema = "cinema.jpg"
image bg ital_res = "ital_res.jpg"
image bg food = "food.jpg"
image bg school_road_ni = "school_road_ni.jpg"
image bg school_staircase2 = "school_staircase2.jpg"
image bg school_lobby = "school_lobby.jpg"
image bg school_gardens = "school_gardens.jpg"
image bg school_dormext_full = "school_dormext_full.jpg"
image bg school_dormext_full_ni = "school_dormext_full_ni.jpg"
image bg suburb_park = "suburb_park.jpg"
image bg bench = "bench.png"
image bg 4561 = "4561.png"
image bg topless = "topless.jpg"
image bg countryside = "countryside.jpg"
image bg countryroad = "countryroad.jpg"
image bg boar_sign = "boar_sign.jpg"
image bg farm = "farm.jpg"
image bg farm_interior = "farm_interior.jpg"
image bg farm_interior2 = "farm_interior2.jpg"
image bg farm_mikiroom = "farm_mikiroom.jpg"
image bg fields = "fields.jpg"
image bg school = "school.jpg"
image bg countryschool_hallway = "countryschool_hallway.jpg"
image bg countryside_classroom = "countryside_classroom.jpg"
image bg apple = "apple.jpg"
image bg creek = "creek.jpg"
image bg farm_porch = "farm_porch.jpg"
image bg countryside_night_sky = "countryside_night_sky.jpg"
image bg 4211 = "4211.png"
image bg rice = "rice.jpg"
image bg farm_porch_day = "farm_porch_day.jpg"
image bg onsen = "onsen.jpg"
image bg pitch = "pitch.jpg"
image bg misc_sky = "misc_sky.jpg"
image bg sobarestaurant = "sobarestaurant.jpg"
image bg trail = "trail.jpg"
image bg edge = "edge.jpg"
image bg trail2 = "trail2.jpg"
image bg camp = "camp.jpg"
image bg trail3 = "trail3.jpg"
image bg village = "village.jpg"
image bg school_gate_ni = "school_gate_ni.jpg"
image bg school_gate_ni_running = "school_gate_ni_running.jpg"
image bg school_courtyard_ni = "school_courtyard_ni.jpg"
image bg school_courtyard_ni_running = "school_courtyard_ni_running.jpg"
image bg school_hallway2 = "school_hallway2.jpg"
image bg burgerk = "burgerk.jpg"
image bg aquarium = "aquarium.jpg"
image bg manta = "manta.jpg"
image bg giftshop = "giftshop.jpg"
image bg plushie = "plushie.jpg"
image bg school_dormext_full_ss = "school_dormext_full_ss.jpg"
image bg school_dormhisao_ss = "school_dormhisao_ss.jpg"
image bg cap = "cap.jpg"
image bg school_room34 = "school_room34.jpg"
image bg school_forestclearing = "school_forestclearing.jpg"
image bg doggy_edited = "doggy_edited.png"
image bg roadside = "roadside.jpg"
image bg busstop = "busstop.jpg"
image bg cake = "kurisumasu_keiki.jpg"
image bg hotdo1 = "HOTDO1.jpg"
image bg hotdo2 = "HOTDO2.jpg"
image bg arcadeint = "arcadeint.jpg"
image bg ishigaki_sea_run = "ishigaki_sea_run.jpg"
image bg ishigaki_day_run = "ishigaki_day_run.jpg"
image bg tanabata_bamboo = "tanabata_bamboo.jpg"
image bg doggo = "doggo.jpg"
image bg uniform = "uniform.jpg"
image bg track_team_photo = "track_team_photo.jpg"
image bg fields_fast = "fields_fast.jpg"
image bg hole = "hole.jpg"
image bg lewd = "lewd.jpg"
image bg bed = "bed.png"
image bg school_gardens_running = "school_gardens_running.jpg"

#music and SFX
define music_miki = "Carefree_Days.ogg"
define music_daily = "Daylight.ogg"
define music_soothing ="Air_original.ogg"
define music_best_shot = "benatar.ogg"
define music_grease = "grease.ogg"
define music_running = "Hokabi.ogg"
define music_jazz = "Red_Velvet.ogg"
define music_tragic = "Cold_Iron.ogg"
define music_pearly = "Stride.ogg"
define music_night = "Nocturne.ogg"
define music_moonlight = "Breathlessly.ogg"
define music_innocence = "Innocence.ogg"
define music_credits = "Romance_in_Andante.ogg"
define music_drama = "Moment_of_Decision.ogg"
define music_Out_of_the_Loop = "Out_of_the_Loop.ogg"
define music_lullaby = "Lullaby_of_Open_Eyes.ogg"
define music_ease = "Ease.ogg"
define music_timeskip = "Passing_of_Time.ogg"
define music_tranquil = "Afternoon.ogg"
define music_fripperies = "Fripperies.ogg"
define music_tension = "High_Tension.ogg"
define music_normal = "School_Days.ogg"
define music_suzu = "Autumn.ogg"
define music_everyday_fantasy = "Everyday_Fantasy.ogg"
define music_caged_heart = "Caged_Heart.ogg"
define music_raindrops = "Raindrops_and_Puddles.ogg"
define music_painful = "Painful_History.ogg"
define music_ah = "Ah_Eh_I_Oh_You.ogg"
define music_friendship = "Friendship.ogg"
define music_heart = "Letting_my_Heart_Speak.ogg"
define music_shadow = "Shadow_of_the_Truth.ogg"
define music_to_become_one = "To_Become_One.ogg"
define music_aria = "Aria_de_l'Etoile.ogg"
define music_comfort = "Comfort.ogg"
define music_generic_happy = "Generic_Happy.ogg"
define sfx_can_clatter = "can_clatter.ogg"
define sfx_park = "parkambience.ogg"
define sfx_crowd_indoors = "crowd_indoors.ogg"
define sfx_normalbell = "carillon.ogg"
define sfx_crowd_outdoors = "crowd_outdoors.ogg"
define sfx_storebell = "storebell.ogg"
define sfx_blop = "blop.mp3"
define sfx_fireworks = "fireworks.ogg"
define sfx_running = "running.ogg"
define sfx_birdstakeoff = "birdstakeoff.ogg"
define sfx_traffic = "traffic.ogg"
define sfx_pillow = "pillow.ogg"
define sfx_broken_plate = "broken_plate.ogg"
define sfx_sitting = "sitting.ogg"
define sfx_dooropen = "dooropen.ogg"
define sfx_impact = "wumph.ogg"
define sfx_splash = "splash.ogg"
define sfx_void = "void.mp3"
define sfx_doorclose = "doorclose.ogg"
define sfx_rain = "rain.ogg"
define sfx_doorknock = "doorknock.ogg"
define sfx_doorknock_soft = "doorknock2.ogg"
define sfx_shower = "shower.ogg"
define sfx_alarmclock = "alarm.ogg"
define sfx_switch = "switch.ogg"
define sfx_hammer = "hammer.ogg"
define sfx_rustling = "rustling.ogg"
define sfx_whiteout = "whiteout.ogg"
define sfx_car_driving = "car_driving.ogg"
define sfx_cycling = "cycling.ogg"
define sfx_can = "can.ogg"
define sfx_tray_rattling = "tray_rattling.mp3"
define sfx_bat_hit = "bat_hit.ogg"
define sfx_kick_machine = "kick_machine.ogg"
define sfx_snap = "snap.ogg"
define sfx_doorslam = "doorslam.ogg"
define sfx_tcard = "tcard.ogg"
define sfx_rumble = "rumble.ogg"
define sfx_cicadas = "cicadas.ogg"
define sfx_cellphone = "cellphone.ogg"
define sfx_cutlery = "cutlery.ogg"
define sfx_car_drive_off = "car_drive_off.ogg"
define sfx_car_door = "car_door.ogg"
define sfx_beach = "beach.ogg"
define sfx_photo = "shutterfilm.ogg"
define sfx_kei_arrive = "kei_arrive.ogg"
define sfx_clap = "clap.ogg"
define sfx_pothole = "pothole.ogg"
define sfx_sliding_door = "sliding_door.ogg"
define sfx_creaking_door = "creaking_door.ogg"
define sfx_wood_floor = "wood_floor.ogg"
define sfx_footsteps_hard = "footsteps_hard.ogg"
define sfx_brook = "brook.ogg"
define sfx_crickets = "crickets.ogg"
define sfx_twig_snap = "twig_snap.ogg"
define sfx_forest = "forest.ogg"

#this is for the chapter title cards
#image bg act1card= "ui/act1card.png"
define act1card = "act1card.png"
define act1 = "act1.png"
define neutral = "neutral.png"
define act2suzu = "act2suzu.png"
define act2hisao = "act2hisao.png"
define passingact = ImageDissolve("ui/tr-tcard-act1.png", 3.0)
define passingactsuzu = ImageDissolve("ui/tc-act2suzu.png", 3.0)
define passingacthisao = ImageDissolve("ui/tc-act2hisao.png", 3.0)

#this is for the splash screen and disclaimer at the start
define lsaudiologo = "4lsaudiologo.ogg"
image bg splash = "splash.jpg"

#The credits
label credits:
    $ credits_speed = 65 #scrolling speed in seconds
    scene black #replace this with a fancy background
    with dissolve
    show theend:
        yanchor 0.5 ypos 0.5
        xanchor 0.5 xpos 0.5
    with dissolve
    with Pause(3)
    hide theend
    show cred at Move((0.5, 5.0), (0.5, 0.0), credits_speed, repeat=False, bounce=False, xanchor="center", yanchor="bottom")
    with Pause(credits_speed)
    show disclaim1:
        yanchor 0.5 ypos 0.5
        xanchor 0.5 xpos 0.5
    with dissolve
    with Pause(4)
    hide disclaim1
    show disclaim2:
        yanchor 0.5 ypos 0.5
        xanchor 0.5 xpos 0.5
    with dissolve
    with Pause(4)
    hide disclaim2
    show thanks:
        yanchor 0.5 ypos 0.5
        xanchor 0.5 xpos 0.5
    with dissolve
    with Pause(3)
    hide thanks
    show mail:
        yanchor 0.5 ypos 0.5
        xanchor 0.5 xpos 0.5
    with dissolve
    with Pause(5)
    hide mail
    return

init python:
    credits = ('Head Writer', 'Suriko'), ('Music', 'Nicol Armarfi'), ('Music', 'Blue123'), ('Backgrounds', 'Katawa Shoujo Team'), ('Backgrounds', 'Niji'), ('Sprites', 'Katawa Shoujo Team'), ('Sprites', 'Sharp-o'),('Sprites', 'Konett'), ('Sprites', 'Suzumiya Haruhi no Gyakuten'), ('Sprites', 'KSAlpha Rebuild'), ('Sprites', 'GGSalmon'), ('Sprites', 'Tropical Kiss'), ('Sprites', 'Yonyonyon'), ('Sprites', 'Deji'), ('Sprites', 'Coming Out On Top'), ('Sprites', 'Dream Daddy'), ('Sprites', 'Paradisuu'), ('Sprites', 'Senji4.Ujin'), ('Sprites', 'tokudaya.net'), ('Sprites', 'Bunnyvoid'), ('Sprites', 'Jean Valjean'), ('Sprites', 'Higurashi'), ('Sprites', 'Angel Beats!'), ('CG', 'rtil'), ('CG', 'Raemz/Weee'), ('CG', 'Tentakl'), ('CG', 'event7'), ('CG & sprite editing', 'Niji'), ('Text editing', 'Niji'), ('Programming', 'StanR'), ('Programming', 'Kickaha'), ('Programming', 'Niji'), ('Sound Effects', 'Katawa Shoujo Team'), ('Sound Effects', 'Niji'), ('Karaoke Music', 'Hit me with your best shot - Schwartz/Benatar'), ('Karaoke Music', 'Summer Nights - Jacobs/Casey/Travolta/Newton-John'), ('Special Thanks', 'StanR and the original Summer\'s Clover team'), ('Special Thanks', 'Four Leaf Studios')
    credits_s = "{size=50}Credits\n\n"
    c1 = ''
    for c in credits:
        if not c1==c[0]:
            credits_s += "\n{size=50}" + c[0] + "\n"
        credits_s += "{size=30}" + c[1] + "\n"
        c1=c[0]
    credits_s += "\n{size=30}Engine\n{size=30}Ren'py\n7.3.5" #Don't forget to set this to your Ren'py version

init:
#   image cred = Text(credits_s, font="myfont.ttf", text_align=0.5) #use this if you want to use special fonts
    image cred = Text(credits_s, text_align=0.5)
    image theend = Text("{size=80}The end", text_align=0.5)
    image disclaim1 = Text("{size=30}This game's story, assets and part of the code were used without permission from any of the involved parties", text_align=0.5)
    image disclaim2 = Text("{size=30}Not affiliated with Four Leaf Studios or Katawa Shoujo in any way", text_align=0.5)
    image thanks = Text("{size=80}Thanks for Playing!", text_align=0.5)
    image mail = Text("{size=80}nijidoggo@gmail.com", text_align=0.5)







## The game starts here.

label start:

    stop music fadeout 2.0

    scene black
    $renpy.pause(1)

    show text "An unauthorised Katawa Shoujo spin off" with dissolve
    #play sound lsaudiologo
    $renpy.pause(3)
    hide text with dissolve
    $renpy.pause(1)
    scene bg splash with dissolve
    $renpy.pause(5)
    scene black with dissolve
    $renpy.pause(2)

    scene black

    n "{cps=60}I've always believed that there are many kinds of people.{/cps}"

    n "{cps=60}Those who calmly stroll through their uneventful lives, the ones who meander from this interest to another, they who walk in the shadow of others more notable than themselves, and so on.{/cps}"

    n "{cps=60}As for me... I was the type who ran. The people I wanted to be with, what I wanted to do with my life, where I wanted to be, I knew the answers to all those questions.{/cps}"

    n "{cps=60}I had my worries and concerns, of course, but those meant nothing when living with such purpose. My ambition was what set me free. For those fleeting years of my childhood, I was unstoppable.{/cps}"

    n "{cps=60}Three years ago, that world ended.{/cps}"


    nvl hide dissolve

    nvl clear

    #this works! need to figure out how to ge the heart and text to show up too: probbaly by editing the black/white image that immagedissolves and using act1card -Niji
    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(sfx_tcard)
    show neutral with fade
    show act1card with passingact
    $renpy.pause(10.0)
    $renpy.music.stop(fadeout=2.0)


label en_C1:

    #scene bg act1card with dissolve
    #pause 10.0
    #play sound sfx_tcard #why will this not play? Will not work with music or sound. Is pause to blame? -Niji

    scene bg school_gardens_ss #black
    with dissolve

    play music music_tranquil fadein 6.0 ##was Miki's theme in original script # start with Miki's theme

    window show

    play sound sfx_can_clatter

    "The rattle of a can hitting the vending machine rings out across the empty school grounds. With the orange of sunset settling over the campus, everyone's retreated to their dormitories and homes for an early start to their studying and various hobbies."

    "Without much else to do, I wander through the gardens while drinking to make the best of the unusually quiet surrounds."

    "Summer's biting particularly hard this year. At least, that's what everybody's been complaining about lately. I don't really see the problem, but I've always been more used to hot weather than others."

    "With little around me to think about, beyond the occasional sip from the can, my mind turns to something that has been bugging me."

    "Every day feels the same. The school week begins, I attend classes, school week ends. Laze around for the weekend, and then it all repeats once more. 'Stagnant' is probably the best word for it."

    "It's not that I hate such a life. Compared to how I've lived before now, it's something I feel I should probably treasure."

    "But my life is also finite. No matter how blissfully unaware I am of it, time still passes. Maybe it's summer holidays that've focused my thinking, or maybe the exams beforehand. Either way, this way of living will end."

    scene bg school_track_ss
    with locationchange

    play ambient sfx_park fadein 1.5
    $ renpy.music.set_volume(0.5, 1.5, channel="music")

    "Emerging through the line of trees separating the track from the main grounds, the movement of a lone person immediately catches my eye."

    "His figure casts a long shadow in the evening's light as he slowly runs along the far side of the track. Looks like it's hard going, with his arms swaying to and fro as he valiantly pushes himself onwards."

    "I idle up to the side of the track and take another swig. It's a welcome distraction from my troubling thoughts."

    "As he comes around the corner, it's possible to finally get a good look at him."

    "I'd recognise those disheveled locks of Hisao's anywhere. While his natural habitat may be the classroom, I've seen him spluttering around the track alongside Emi a couple of times before."

    "Dressed, as always, in his shirt without the bothersome jacket, it's clear that he has a nice build. That said, despite his solid chest and broad shoulders, there's an unassuming air to him. Perhaps it's due to his rather plain face, or just his subdued nature from having recently changed schools."

    "Without anything in particular to say to the boy, I just take another sip of my drink as he continues up the track."

    "Maybe the normal thing to do here would be to cheer him on for throwing himself at the track with such gusto, but it really doesn't look like he's enjoying the ordeal."

    "His running form is becoming worse and worse, and his speed is noticeably slowing. Even the bird that's swooped down to peck at something left in the grass doesn't bother moving as he runs by."

    "It reminds me of how I used to throw myself at the track, running however many laps I could before I broke from exhaustion."

    "I move to take another swig from my can as he comes back around, only to find it lacking. With my attention briefly diverted from Hisao to my sadly empty drink, I'm take mildly off guard as he stumbles off the track and comes to a haphazard stop just ahead of me."

    #stop music fadeout 2.0

    $ renpy.music.set_volume(1.0, 4.0, channel="music") # restoring music volume

    show hisao_talk_small_u with dissolve
    $ renpy.music.set_volume(0.5, 1.5, channel="music")
    #play music music_pearly fadein 1.0 #this is so loud it drowns out the park sfx :/ ##was afternoon music in original script

    hi "Can I... help you...?"

    "Not knowing if he'd even be able to hear me past his panting, I let him collect himself for a few seconds before answering."

    mk "Just watchin'."

    hi "Yeah... I can see that."

    show hisao_wtf_u with charachange
    hide hisao_talk_small_u

    stop music fadeout 1.0
    stop ambient fadeout 1.0

    "He clutches at his knees and tries his best to regulate his breathing, but it's in vain. It's when he clutches at his chest and his breathing noticeably rises in pitch that I start to get a bit worried."

    mk "You okay? Looks like you kinda overdid it, there."

    hi "I'm fine. Totally fine."

    "If he's going to be like that, all that I can do is take a step back and let him recuperate."

    "Beyond his breathing and a slight breeze in the trees, there's nothing to be heard. It reminds me just how alone we are, likely being the only two people in the entire school grounds right now."

    show hisao_erm_u with charachange
    hide hisao_wtf_u

    play music music_pearly fadein 1.0
    play ambient sfx_park fadein 1.0

    "After who knows how much time, he finally manages to compose himself and stand upright, sweat still tricking down the side of his face. There's a sickly wheeze to his breathing, but I don't think he wants to be reminded of it."

    hi "Miura, right? I'm Hisao Nakai."

    mk "The mysterious transfer student himself. Pleased to meet ya."

    hi "What brings you out here, anyway?"

    mk "Just grabbin' a drink. You?"

    hi "Missed my morning run. E... I mean, Ibarazaki, said I should run in the evening to make up for it."

    mk "Don't worry, I know Emi. Damn near all the school does."

    "I nod towards the track, the bird still out there trying to drag a left over food packet away."

    mk "Just how long have you been out here?"

    hi "A while. I should probably just cut my losses and get dinner, but she'd kill me if I skipped out."

    mk "Man, just give up."

    "Come to think of it, this might be a good chance. Dinner alone is boring, and if I can twist him into paying for a meal, all the better."

    mk "If you're hungry, I know a good place if you're up for it."

    show hisao_talk_small_u with charachange
    hide hisao_erm_u

    "He looks a little startled by the suggestion, running a hand through his hair as he tries to settle himself down and think things through. I can practically see the gears turning in his head as he selects his choice."

    mk "C'mon, a hot girl's asking you to eat with her. You're gonna refuse that?"

    show hisao_heh_u with charachange
    hide hisao_talk_small_u

    hi "They say modesty is a virtue."

    mk "Never said I was a virtuous person."

    "May as well wait things out as he continues with his deliberation, as I'm pretty confident I know what the reply will be. Sure enough, he finally comes up with an answer."

    show hisao_smile_u with charachange
    hide hisao_heh_u

    hi "Fine, I'll go along with you."

    stop ambient fadeout 2.0
    stop music fadeout 2.0

    $ renpy.music.set_volume(1.0, 4.0, channel="music") # restoring music volume

    #centered "~ Timeskip ~" with dissolve
    scene bg suburb_shanghaiext_ss
    with shorttimeskip #locationchange

    "The Shanghai's location within the nearby town has always been convenient. I had thought even this might be too much for Hisao given his exhaustion, but he managed to drag himself here just fine."

    play sound sfx_storebell

    scene bg suburb_shanghaiint
    with locationchange

    play music music_miki fadein 1.0

    $ renpy.music.set_volume(0.5, .5, channel="ambient")
    play ambient sfx_crowd_indoors fadein 1.0

    show hisao_erm_u at centersit
    with dissolve
    hide hisao_heh_u

    "I like the uniforms they have here, even if they do strike me as a little unconventional. Our meals placed before us, the waitress takes her leave to attend to a handful of other customers at the opposite end of the cafe."
    "Not being especially hungry, my meal's just a slice of pie and a drink. Hisao's pack of sandwiches don't look like it'll last for long, one of them already having disappeared into his mouth."

    "He catches me staring, awkwardly holding the next midair while looking mildly embarrassed."

    hi "Sorry, I just..."

    mk "It's normal to be hungry after exercise, man. Go ahead and stuff your face."

    show hisao_talk_small_u at centersit with charachange
    hide hisao_erm_u at centersit

    "Hisao obediently does so, though with a touch more delicacy than before."

    mk "So what's the story with Emi, anyway?"

    hi "She just pushes me to exercise with her sometimes. Guess she enjoys the company. I mean, like you do now."

    mk "Doesn't seem like you enjoy the experience much."

    hi "Well, I do want to get back into shape. As much as I can, anyway."

    show hisao_frown_u at centersit with charachange
    hide hisao_talk_small_u at centersit

    "He pulls his cuff up his arm a little, taking a loose flab of skin from his forearm and giving it a pinch as he frowns. He sure is pale under his shirt, though maybe I'm not the best judge of that."

    mk "You sure found the right person if you want to be whipped into shape. Just make sure she doesn't kill you first."

    hi "Believe me, she's come close."

    "His tone is way too serious for a throwaway joke. Surely she's not that much of a slave driver."

    "Taking a bite into my own food, it turns out I'm surprisingly hungry myself. The two of us end up stuffing down our food in no time, crumbs littering the table in the aftermath."

    show hisao_erm_u at centersit with charachange
    hide hisao_frown_u at centersit

    "With dinner finished, Hisao leans back in his seat and contentedly pats his stomach. I run my finger around the inside of my mouth to work out the remnants stuck to my teeth, savouring the taste of the last little bits I manage to find."

    "At first I take Hisao's staring out the window to be a sign of boredom, but one careless glance gives his game away. He's trying to distract himself from the bandaged stump resting on the table."

    "I'd hardly think worse of someone for looking at it; being distracted by something out of the ordinary is completely normal. I just give a smile, hoping to make him relax a bit."

    hi "Sorry."

    mk "Believe me, you're not the first to notice. It's not like a missing hand is exactly subtle."

    "Hoping, and succeeding, to defuse the situation a bit, I grin and waggle my stump in the air a little to emphasise the point. It's delightfully easy to read Hisao's emotions, even when he's trying his best to suppress them."

    hi "I still have no idea what to make of this place."

    mk "Town, or Yamaku?"

    "He just raises an eyebrow."

    mk "What's the problem with it?"

    hi "Hmm... I think 'confronting' would probably be the right word."

    hi "It's not every day you see someone with half their face heavily scarred, or have to try and communicate with someone who can't hear. Then there's the obvious example of Emi."

    mk "Well, I mean, you're not wrong. Being a transfer student would make that a lot worse, too."

    mk "Try coming at that from another angle, though - what're we doing now?"

    hi "Chatting at a cafe?"

    mk "And what'd you do today before that?"

    hi "Woke up, got dressed, went to classes, had lunch and tea in a club room, more classes, went to run on the track, and then started chatting with you."

    mk "Isn't that a pretty normal high school day?"

    show hisao_talk_small_u at centersit with charachange
    hide hisao_erm_u at centersit
    show hisao_erm_u at centersit with charachange #followed by hisao_erm to make an opne-close mouth animation
    hide hisao_talk_small_u at centersit

    "He moves to protest, but finds himself searching for words. However reluctantly it may be, he backs down once he realises that I have a point."

    mk "You'll get used to it soon enough. If everyone else at school seems cool with it, that's only because we all had a head start of years."

    show hisao_talk_small_u at centersit with charachange
    hide hisao_erm_u at centersit

    hi "And if I accidentally offend someone? I almost did just then, remember?"

    mk "Then... so what? Just find someone else to talk to. There's hundreds of people here to pick from. Hell, you're talking to me easily enough."

    show hisao_erm_u at centersit with charachange
    hide hisao_talk_small_u at centersit

    hi "A pretty normal high school, huh..."

    mk "Exactly. Just pick up some friends, find your groove, and ride the rest of the year out. You'll be fine."

    "He turns to look out the window, reflecting on the conversation. That expression of contemplation suits him well."

    "Evidently coming to a conclusion, he gives a nod before turning back to me."

    show hisao_smile_u at centersit with charachange
    hide hisao_erm_u at centersit

    hi "Thanks. I'll keep that in mind."

    stop music fadeout 1.0

    "The smile he gives me is kinda sweet. Weak, but terribly sincere. All I can do in response is give a satisfied grin back."

    "Such a chance meeting might not change much for me, but if I can help Hisao get on the right track, at least I'll have been useful to someone."

    "The weather really is nice today."

    ##stop music fadeout 2.5

    stop ambient fadeout 2.5
    $ renpy.music.set_volume(1.0, .5, channel="ambient")

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_C2:

    scene bg school_gardens3
    with dissolve
    $ renpy.music.set_volume(0.5, 1.5, channel="music")
    play music music_soothing fadein 0.25 # [str]

    window show

    "I find myself lazily sitting at the base of a particularly tree in the school gardens, making the most of its shade while watching the goings on ahead."

    "With the events over and medals dispensed, the people gathered for the track meet have now fanned out over the grounds. Runners excitedly talk with their friends and parents, with the handful who have romantic interests in the other participating school using the opportunity to catch up on more affectionate matters."

    "It's nice. In fact, I prefer this atmosphere to the competitive nature of the track meet itself. People just catching up with others, having a nice time as the importance of who won or lost whichever race fades away."

    "Without much else to do, I idly toy with the medal on my chest. First place was a lost cause; Emi's in another league when it comes to sprinting, after all. Silver still ain't bad, especially given that I'm hardly the competitive type to begin with."

    "I wonder what metal this thing is actually made of. Tin, maybe. I flick it a couple of times to try and gauge the sound, but it's no use."

    show rin with moveinleft
    hide rin with moveoutright

    "A shadow crossing my vision grabs my attention, but I needn't have bothered looking. The owner just keeps on walking towards the main building, her empty sleeves swaying in the breeze."

    "Looking back to where she came from, I see a familiar face slowly strolling around the grounds. Given that he isn't in gym uniform, he's probably only here because of Emi."

    "I feel a little bad for him. Sure, he's around the student council and Emi a lot, but that feels more like he's being bossed around than actually choosing to hang out with friends. Not that I'm innocent, I guess."

    "The thought of something some of the guys in the club had hastily arranged comes to mind as I mull over the situation."

    "I come to my feet after making my decision, striding past a gaggle of gossiping girls and calling out to him."

    show hisao_talk_small_u with charachange

    hi "Oh, Miura. Hey."

    mk "Got dragged here by the shortie, eh?"

    show hisao_disappoint_u with charachange

    "Hisao just hangs his head as I saunter up to him. He's pretty transparent."

    "It's always struck me how out of place Hisao seems around the track club and other sports stuff. He said he liked soccer when he introduced himself in class, but it's kinda hard to imagine such a passive and subdued lad running around a field and being boisterous."

    "It makes me wonder what he'd be doing with himself if Emi weren't dragging him around by the scruff of the neck."

    mk "Least she put on a show for you."

    show hisao_erm_u with charachange

    hi "Has she always been that good at sprinting?"

    mk "Yep. She puts in the hours on the track, so it ain't no surprise that it pays off. Fastest thing on no legs, and all that."

    hi "Still, it looks like you did fine yourself."

    mk "It's something. You hang around the club and look decently built; I'm surprised you didn't run in some race or another."

    show hisao_frown_u with charachange

    hi "You saw me the other day on the track, didn't you?"

    "The face he pulls makes me feel bad for bringing it up. This being Yamaku, it isn't hard to think up reasons why he might have problems in that area."

    mk "Forget I asked. There is another reason I wanted to talk with you, actually."

    mk "Most of the track club's going to a karaoke place this evening to hang out. There's space for you, if you wanna come."

    show hisao_wtf_u with charachange

    "Hisao looks genuinely startled, but I think it's in a good way."

    hi "I was going to study..."

    mk "C'mon, it'll be fun. Some of the other guys want to know who you really are too, y'know."

    show hisao_disappoint_u with charachange

    hi "I somehow doubt I'm that interesting."

    mk "Mysterious transfer student who keeps hanging around the track with Emi? What's there not to be curious about?"

    "He wavers a little, but eventually throws his arms up in surrender."

    show hisao_heh_u with charachange

    hi "Alright, you got me. I'll come."

    stop music fadeout 1.5

    scene bg city_karaokeint
    with shorttimeskip
    play music music_best_shot fadein 1.0
    $ renpy.music.set_volume(0.5, .5, channel="ambient")
    play ambient sfx_crowd_indoors fadein 1.0

    "The moment we all entered the dimly-lit room, we started acting as if it were home. People laid on the couches, draped themselves over the arms and backs to talk to friends, threw snacks and drink bottles to each other, and generally made a din from all the arguing over the day's events."

    "Now that some time has passed, with the excitement and adrenaline of the track meet ebbing, things have finally settled down a little. The dozen people around make-do with gossiping while lounging around on the garishly coloured seats, occasionally cheer or jeer at whoever's up front belting out some crappy song or another, and busily chat the night away."

    "Not that I'm excluded, with Hisao seated to my right and speaking up to be heard over the atrocious number being sung to a chorus of laughs and teasing."

    show hisao_talk_big_u at centersit with dissolve

    hi "If you don't mind me asking, where are the girls from club? I'm sure I saw a couple besides Emi at the track meet, but only the guys are here."

    mk "What, you lookin' to pick up?"

    hi "I just transferred in, I don't move that quickly."

    mk "Come on, you could do worse than the girls in the track club. Fitness does wonders for you-know-what, after all..."

    show hisao_blush_u at centersit with charachange
    hide hisao_talk_big_u at centersit

    "He gives me a flat face, but I detect a hint of embarrassment in it. Guess he's a bit of a prude."

    mk "They're just busy. Supposedly. Maybe it was too much of a sausage fest for them."

    stop music fadeout 4.0

    "He moves to say something, but as the guy singing ends his round, the next beckons for Hisao to join him as he walks up to the mic. Yukio Hasegawa, nothing less than perhaps the most popular guy in track club. He's always cut graceful figure for a man, bearing slim, refined eyes, impeccably groomed hair, and a gentle face. "
    "Far from my type, but other girls seem to gush over him."

    "The others in the room, whether out of curiosity, friendliness, or teasing, quickly join in to try and make Hisao perform. The guy himself doesn't look enthused, but I suspect that's as much due to the pressure as the actual act."

    mk "You should do it. What've you got to lose?"

    show hisao_hmpf_u at centersit with charachange
    hide hisao_blush_u at centersit

    hi "My dignity. I can't sing, you know."

    mk "What, you think any of us can? Stop being lame and just have some fun."

    #show hisao_frown at centersit with charachange
    #hide hisao_hmpf
    with vpunch
    show hisao_hmpf_u at left with charamovefast

    "I put my hand on his back and give him a sharp push off his ass, jolting him into the center of the room."

    show hisao_wtf_u at left with charachange
    hide hisao_hmpf_u at left
    pause (0.5)
    show hisao_frown_u at left with charachange
    hide hisao_wtf_u at left

    "It's only momentary, but as he recovers, he throws an odd glance back to me afterwards. His anxious, almost scared, face leaves me speechless."

    hide hisao_frown_u with dissolve

    "Everything returns to normality in a flash, the boy taking a breath before marching around the table and up to the mic with back hunched and feet dragging, waving down the cheers of those around him as he does. Whatever was going on in his head, it was far beyond just being shy."

    "With nobody else seemingly having noticed, all I can do is sit back puzzled in my seat and take a swig from the soft drink in front of me."

    play music music_grease fadein 1.0

    "As the music starts up and the vocals kick in, it becomes obvious that the two are far from practiced at this. Their voices might not be bad, but they're horrendously out of key. Hisao's shyness is getting the better of him too, which only looks worse next to Yukio's confident demeanor."

    "From the corner of my eye, I notice the guy to my left leaning forward, his face turning to mine."

    show haru_basic at centersit with dissolve

    "Named Haruhiko, though everyone calls him Haru, he's a follow classmate who also had the misfortune of being stuck on the first row of tables. While he may be quite gifted physically, being decently tall and strong, he's far from the sharpest tool in the shed. "
    "It matters little, though, as his endearing cheerful nature and eternal optimism cover for whatever shortcomings he may have."

    show haru_smile at centersit with charamove
    hide haru_basic at centersit

    har "So, what's the over/under on the new guy?"

    "I set the drink back on the table, my hand rubbing my neck as I lean back. I don't know what answers he's expecting, but I doubt I'll be able to give him any."

    mk "You're asking me?"

    show haru_serious at centersit with charamove
    hide haru_smile at centersit

    har "You're the one who invited him, you know."

    mk "He paid for my lunch, so I felt like I owed him. That's all there is to it."

    show haru_basic at centersit with charamove
    hide haru_serious at centersit

    "The corner of his mouth tugs upwards. Just a little."

    har "You being honorable. There's a first."

    mk "Prick."

    mk "So do you know anything about him? All I know is that he's a nerd who gets bossed around by the shortie and the student council."

    har "Heard he used to play soccer. Not half bad at it, either."

    mk "Used to?"

    show haru_serious at centersit with charamove
    hide haru_basic at centersit

    har "Somethin' wrong with this."

    "Haru glances to the two at the front of the room, both of them being far too distracted with their attempts to make something resembling a decent song to pay us much heed. Satisfied that we're communicating in private, he jabs at his chest with his thumb a couple of times."

    har "He had a heart attack. Real bad, too. Emi'd probably know more. Or the guy himself."

    "He adds the last suggestion as an afterthought, though understandably so. Plenty in Yamaku have their bugbears about what's happened to them in the past, though I'd be damn hypocritical to complain about it."

    mk "Come on, a heart attack? At that age?"

    har "It happens."

    "I expect him to admit that what he heard was some vague rumour or something, but he just shrugs and looks at me matter-of-factly."

    "What would Hisao be, 17? 18? That's the kind of thing you hear taking out frail old folks. Natural causes, and all that. Now that I think of it, maybe that explains why he got puffed so easily back when I saw him at the track."

    mk "Shit..."

    show haru_sad at centersit with charamove
    hide haru_serious at centersit

    "It's kind of pathetic, but that's all the response I can muster as I lean back in my seat. Haru just lets out a dissatisfied sigh, equally put off by the idea."

    hide haru_sad at centersit with dissolve

    "Looking back at the duo finishing up their song at the front of the room, I can't help but see him in a new light."

    stop music fadeout 2.0
    stop ambient fadeout 2.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_C3:

    scene bg school_library
    with dissolve
    $ renpy.music.set_volume(0.5, 1.5, channel="music")
    play music music_fripperies fadein 1.0

    window show

    "If I had to choose which room embodied the feeling of this school the most, it'd have to be the library."

    "It looks normal, at a glance. Large, sure, but otherwise normal. It's only when you start walking through the aisles that you realise the odd little allowances for the students. Audiobooks, braille books, wider passages, and the like. Then there's the cane or two propped against the desks of reading students."

    "There's also the old-fashioned stuffiness, too. Doesn't help that the literature club students are all quiet as mice, but it's something more than that. The furniture, staff, and general mustiness of the older books are all stifling."

    show suzu_neutral at centersit
    with dissolve

    "My eyes eventually fall on the girl across the table from me. 'Unremarkable' would perhaps be the best description of how she appears, save for the bags under her eyes and brace on her knee. For Yamaku, though, that's doing pretty well."

    "If I had to choose which pose embodied the personality of Suzu the most, it'd have to be her chin resting on her hand as her eyes lazily scan the manga magazine in front of her."

    "The girl looks up, her eyes meeting my own. Her reaction, or lack thereof, is about what I'd expect."

    show suzu_speak at centersit with charamove
    hide suzu_neutral at centersit

    suz "Staring is rude."

    mk "I dunno how you put up with this place. Don't you have anything more exciting to do with yourself?"

    show suzu_neutral at centersit with charamove
    hide suzu_speak at centersit

    "She sighs as I start to rock back and forth on my chair to occupy myself. With nobody else willing to brave the heat, the track club's been largely abandoned for the day. I can think of better things to do than throw myself around an empty track."

    "Then again, the literature club sure makes a dull sight. The closest thing I can see to an actual club activity is half a dozen students sitting around a table quiet discussing some book or another."

    mk "Why don't you join them?"

    "Following my nod, she glances to her side and back with a minimum of effort, not even bothering to lift her head from her hand."

    show suzu_surprised at centersit with charamove
    hide suzu_neutral at centersit

    suz "Because I'm busy reading this."

    mk "Isn't literature club for discussing literature?"

    show suzu_concerned at centersit with charamove
    hide suzu_surprised at centersit

    suz "Most of us just read whatever. As long as we're quiet and in the library, nobody really cares."

    mk "So that's all you're gonna do? Read manga?"

    "I was sincerely hoping she'd suggest something for us to do, or maybe even socialise, but she simply shrugs and goes back to reading. It's hard to say whether it's out of apathy or being too tired to do much more than this."

    "Then again, I'd be more surprised if I could gauge her feelings. The kind way to describe her would be 'ambivalent', but after a year of being around her, I've settled on a diagnosis of 'possible lobotomy'. That air of quiet disapproval never seems to leave her."

    "As she slowly turns the page and continues her reading, a familiar voice draws my attention to the end of the library."

    "The tense voice of Ikezawa, hunched over on a beanbag in her usual little corner, isn't difficult to distinguish. Hisao sits on the floor beside her, a disarming smile on his face as he softly tries to chat."

    "I can't quite pick out their conversation, but the fact that they're having one at all is pretty impressive."

    "Suzu turns back around as I stop my gawking, her own interest apparently having been piqued."

    show suzu_surprised at centersit with charamove
    hide suzu_concerned at centersit

    suz "She seems to like him."

    mk "Yeah, they get on well."

    "I might say that, but I have my misgivings. There's more than one story of when girls have tried getting close to her, only for things to go bad for all involved. How much of that is actually true or just gossip, I have no idea, but it's plainly obvious she has a lot of baggage."

    "It might be rather hypocritical, but I don't have much want to get involved. With the way I am, it could only go badly."

    #show hisao _invis at rightedge
    #with None

    "Hisao comes to his feet as their conversation apparently ends, returning from their sanctuary at the end of the library. As he walks by us, a couple of thick novels held to his side, I give a short whistle and motion for him to come over."

    show suzu_surprised at twoleftsit with charamove
    #hide suzu_concerned at twoleftsit
    show suzu_concerned at twoleftsit with charamove
    hide suzu_surprised at twoleftsit

    show hisao_talk_small_u at right with moveinright

    hi "Odd to see you here."

    mk "Well aren't you quick on the uptake?"

    mk "C'mon, take a seat. I need someone for company who has still some life left in them."

    show hisao_talk_small_u at tworightsit with charachange

    "Hisao obediently does so, taking a seat and plopping his books down in front of him. A couple of sci-fi novels, by the looks of them. Not terrible taste. An improvement over Suzu's girly stuff, anyway."

    show suzu_surprised at twoleftsit with charamove
    hide suzu_concerned at twoleftsit

    "Suzu briefly takes her head from her chin to see the new face. I decide to seize the chance."

    mk "Hisao, this is Suzu Suzuki."

    show hisao_smile_u at tworightsit with charachange
    hide hisao_talk_small_u at tworightsit

    "He gives a warm greeting, to which Suzu simply gives a quiet nod, having reverted to her more shy self. He seems a little more sedate than the other friends from track club, so hopefully she'll open up to him a little more than them. Given time."

    show hisao_talk_small_u at tworightsit with charachange
    hide hisao_smile_u at tworightsit

    hi "So you're into manga?"

    show suzu_speak at twoleftsit with charamove
    hide suzu_surprised at twoleftsit

    suz "Are you?"

    hi "A little. To be honest, I don't really follow any of the serialised stuff anymore."

    suz "I see."

    show hisao_disappoint_u at tworightsit with charachange
    hide hisao_talk_small_u at tworightsit
    show suzu_concerned at twoleftsit with charachange
    hide suzu_speak at twoleftsit

    "With Suzu leaving no opening for the conversation to continue, Hisao leans back from the table in disappointment and reaches for one of his books. It's a little sad to see things end this way, and I have told her not to be so antisocial."

    show suzu_speak_close at twoleftsit with charamove
    hide suzu_concerned at twoleftsit

    "Frustrated, I lean over the table, close my fist, and begin rubbing my knuckles into the top of her head."

    #show suzu_speak_close at twoleftsit with charamove
    with vpunch
    #hide suzu_concerned at twoleftsit

    suz "Ow. Ow. Ow."

    show hisao_wtf_u at tworightsit with charachange
    hide hisao_disappoint_u at tworightsit

    hi "Uh, Miki..."

    mk "What have I told you about being like that?"

    "I'm not using much force at all, but her reaction's enough to make me back off rather quickly. The point's been made in any case."

    show suzu_angry at twoleftsit with charamove
    hide suzu_speak_close at twoleftsit
    show hisao_talk_small_u at tworightsit with charachange
    hide hisao_wtf_u at tworightsit

    hi "So you're into shoujo, then?"

    show suzu_embarrassed at twoleftsit with charachange
    hide suzu_angry at twoleftsit

    suz "Is that bad?"

    hi "It's normal enough. Watch the shows?"

    show suzu_normal at twoleftsit with charachange
    hide suzu_embarrassed at twoleftsit

    suz "Yeah. This one's getting an adaptation soon which I'll have to catch."

    hi "Doesn't that stuff air pretty late?"

    suz "My sleep schedule's all over the place anyway."

    show hisao_heh_u at tworightsit with charachange
    hide hisao_talk_small_u at tworightsit

    "He's clearly resisting snark given how tired she visibly looks, but wisely thinks better of it."

    mk "Didn't get much of that stuff on TV back where I came from."

    mk "So you used to read it, Hisao?"

    show hisao_erm_u at tworightsit with charachange
    hide hisao_heh_u at tworightsit

    hi "It was good for killing time while wandering town. Didn't spend much time at home."

    show suzu_concerned at twoleftsit with charachange #why is this not showing up?
    hide suzu_normal at twoleftsit

    suz "Your parents didn't mind?"

    hi "Both of them worked long hours, so not really."

    "There's a gulf between their concepts of what parents would allow, but it's understandable. For someone as pampered as Suzu, being let to wander so much must be a pretty strange idea. I suppose Hisao's a bit like me in that regard."

    mk "Well, at least someone's familiar with the scene. Had practically none of that stuff back home, so it's largely foreign to me."

    mk "Speaking of people's homes... I see you were visiting Hanako's little corner. Tryin' to make inroads with her?"

    show hisao_frown_u at tworightsit with charachange
    hide hisao_erm_u at tworightsit

    hi "'Trying' is the key word, there."

    mk "Don't look so beaten. You can hold a conversation with her, right? That's more than anyone else in the class has managed so far."

    hi "That's more to her friend's credit than mine."

    mk "You really need to learn how to accept praise."

    "My reply is a bit crabby, and admittedly not only because it's a bad habit. 'Hanako's friend' could only be referring to one person; the pretty blonde that she often meets after class. I'm a little jealous of him for getting so close to her so easily."

    mk "You know, you say it's weird to see me here, but what about you?"

    show hisao_smile_teeth_u at tworightsit with charachange
    hide hisao_frown_u at tworightsit

    hi "Reading's my main hobby."

    mk "And running?"

    show hisao_hmpf_u at tworightsit with charachange
    hide hisao_smile_teeth_u at tworightsit

    hi "That's... more like a sentence."

    show suzu_grin at twoleftsit with charachange
    hide suzu_concerned at twoleftsit

    "It's only because we're in the library that I stifle a laugh. Suzu might try to hide it, but the flicker of a smirk flashes on her face as well. True bonding, though the misery of others."

    show suzu_concerned at twoleftsit with charachange
    hide suzu_grin at twoleftsit

    mk "I guess you're all set for exams, then."

    show hisao_talk_small_u at tworightsit with charachange
    hide hisao_hmpf_u at tworightsit

    hi "Why do you say that?"

    mk "You're with Mutou all the time, you know. Guy's got high hopes. You get ridiculous marks for most of your subjects, too."

    show hisao_biggrin_u at tworightsit with charachange
    hide hisao_talk_small_u at tworightsit

    hi "That's because I work for them."

    "This guy catches on way, way too quickly. I might not pay attention in class, but he doesn't have to burn me like that. Suzu's attention is finally wrested from her reading material, looking genuinely impressed. As much as her stony face can, anyway."

    mk "That's harsh, man."

    suz "You're strongest in math and science, correct?"

    show hisao_talk_small_u at tworightsit with charachange
    hide hisao_biggrin_u at tworightsit

    hi "Yeah."

    suz "Could you look at something I couldn't get when we go back to class?"

    show hisao_smile_u at tworightsit with charachange

    hi "Sure, no problem. Doesn't hurt to work it all out before exams come up."

    "Exams. I hate that word. The mood of the class has already begun to sour thanks to the anxiety and stress they cause, and it's only going to get worse in the weeks ahead."

    "At least they're useful for something. If studying's going to be how she expands her social circle, then all the better. Given how hard she works for her rather average marks, maybe he can help turn things around."

    stop music fadeout 2.0
    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_C4:

    scene bg school_cafeteria
    #with shorttimeskip
    $ renpy.music.set_volume(0.5, 1.5, channel="music")
    play music music_ease fadein 1.0
    $ renpy.music.set_volume(0.5, .5, channel="ambient")
    play ambient sfx_crowd_indoors fadein 0.5

    window show

    "I've always found the cafeteria to be a fun place to watch people."

    "Deftly manoeuvring through the rapidly filling room after being among the first to have their tray filled by the old ladies behind the counter, I can't help but glance around at the other students on my way to a free table."

    "By rights, the cafeteria should be a melting pot. Students from every club, class, condition, and year level are here, and with everyone in their uniforms, the differences between rich and poor, country and city, fashionable and unfashionable, fades to nothing."

    "But, people being people, they still find a way to stick to their cliques. The track club members form a clump as they playfully jostle one another, as do a bunch of the deaf students, huddling together in their impenetrable little social circle while signing in their silent second language."

    "There are the gaggles of popular girls with their posses, and the odd trio of less popular girls who stick to their few friends. The rowdy class clowns who loudly joke and act out, and the softly-spoke academics who keep to themselves while shuffling along. Everyone has their niche, even if that niche consists of only one."

    "Setting down my tray at an empty table, I separate the disposable chopsticks using the tips of my fingers as always. Strength comes in surprisingly useful when you largely rely on one hand for manipulation, with the two conjoined sticks easily splitting apart."

    "While I'd hesitate to say it's great, the food here is still pretty good. Filling, and by far satisfying enough to live on for quite a while. Can't complain about the price, either."

    show suzu_neutral at centersit with dissolve

    "It doesn't take long for company to arrive after I've started eating, a familiar figure silently seating herself across the table from me."

    "Suzu simply begins to eat without a word. Such things aren't unusual with her, so I simply look down and continue with my own lunch."

    "As I shovel rice into my mouth, I find myself especially pleased with how they've cooked it today. Not too dry, not too sticky. Ditching the chopsticks and gulping down some soup, it turns out that they've done a good job on that too."

    "Whether Suzu's enjoying her lunch as much as I is, as always, a mystery."

    "Looking past her, two of the three stooges come into sight. With my hand taken, I end up waving my stump around in the air to get their attention. It does the job, with the duo changing course and heading our way."

    #show suzu_concerned at leftoffsit with charamove
    show haru_yo at right
    with moveinright

    har "'Afternoon Miki, Suzuki."

    show haru_yo at leftoff with charamove
    show haru_basic at leftoff with charamove
    show hisao_smile_u at rightedge with moveinright
    show hisao_smile_u at rightedgesit with charamove

    "Suzu pauses her eating to nod to the both of them, as do I. Hisao moves around to take a seat beside me with his juice and a packet of bread, while Haru manoeuvres himself to the end of the table holding a suspicious plain cardboard box with equally suspicious care."

    mk "What's with that?"

    show hisao_heh_u at rightedgesit with charachange
    hide hisao_smile_u at rightedgesit
    show haru_smile at leftoff with charamove
    hide haru_basic at leftoff

    "Hisao just shrugs as I lean over and ask him. Haru just gleams a smile in response, setting down the mystery box and lifting the top off with practiced ease."

    scene bg cake with dissolve

    "As the sides fall away, a gorgeous looking red and white sponge cake is revealed. A thick layer of cream separates the two layers of sponge, and another sits atop the cake. Big, succulent strawberries circle the outer rim, each sitting on its own further blob of cream. "
    "Finally, a light dusting of frosting covers the cake, like a thin shower of snow."

    "It's... beautiful. As expected of Haru."

    scene bg school_cafeteria with dissolve

    show hisao_smile_teeth_u at rightedgesit
    show suzu_grin at centersit
    show haru_smile at leftoff
    with dissolve

    hi "You're drooling."

    mk "Don't care, gimme that thing."

    "He might be criticizing me, but Suzu's attention is just as focused. Her sweet tooth is getting the better of her as the cafeteria food before her languishes."

    show haru_serious at leftoff with charamove
    hide haru_smile at leftoff

    har "Right, right, just hold on a moment."

    "He takes the plastic knife cunningly carried inside the box, and sets about cutting a few slices. Looks like the cake's already had a good third eaten."

    mk "So what's the story?"

    show hisao_talk_small_u at rightedgesit with charachange
    hide hisao_smile_teeth_u at rightedgesit

    hi "Who's?"

    mk "Let's start with the cake."

    show haru_basic at leftoff with charamove
    hide haru_serious at leftoff

    har "Made too much during home ec class. The teacher doesn't mind me baking my own stuff there as long as she gets some."

    hi "So you're into baking?"

    har "Sure am. Might not have many talents, but I'm good at the ones I have."

    "As he gets back to cutting it up, I look around for an answer to the second question on my mind; where the third stooge has gotten himself to."

    "As my eyes fall on him, I can't help but give a weak grin. Suzu notices my staring and twists her head around to see, but turns back to the cake in short measure."

    show suzu_concerned at centersit with charachange
    hide suzu_grin at centersit

    scene black with dissolve
    scene bg school_cafeteria

    #put in some girl sprites for Yukioto talk to
    show yukio_smile
    show aoi_smile at twoleft
    show saki at tworight

    "Sure enough, he's standing around chatting up a couple of girls. I might not see the appeal in his appearance, but I can admit that he pulls off an air of confidence well, even without hearing what he's saying."
    "Going by the bashful smile of the long-haired girl as she toys with her hair, and the other's excited chatting, he's making good progress with both."

    scene black with dissolve
    scene bg school_cafeteria

    #some kind of fade again
    #hide yukio_smile
    show hisao_talk_small_u at rightedgesit
    show suzu_neutral at centersit
    show haru_basic at leftoff
    with dissolve

    hi "Is he always like that? I swear he was with a couple of other girls last week."

    mk "Believe me, you have no idea."

    "Some people bake, some run, some study, and some pick up women."

    scene black with dissolve
    scene bg school_cafeteria

    #fade again and add girls
    #hide hisao_talk_small
    show yukio_huh
    show aoi_smile at twoleft
    show saki at tworight

    "As if he'd heard me, Yukio looks up from his companions to see Hisao and I staring. Sensing an escape, he nods to us and seemingly explains that he wants to come our way."

    #make a sad/worried saki maybe in previous shots flip eyes to look at yukio, and in this keep eyes like they were but flip mouth to make frown
    show aoi_surprised at twoleft with charachange
    hide aoi_smile at twoleft
    show saki_frown at tworight with charachange
    hide saki at tworight

    "The girl with longer hair is about to follow him over before her friend stops her, gesturing at me while frowning. It's hard to be hurt by something you deserve, and as they both quickly decide to walk off, I can take solace in that at least my reputation's helped Yukio."

    hide aoi_surprised with easeoutright
    hide saki_frown with easeoutright


    scene black with dissolve
    scene bg school_cafeteria


    #fade again and also find out of to move everyone a bit so 4 people can be onscreen
    show suzu_concerned at onerightsit
    show haru_basic at oneleftsit
    show hisao_erm_u at rightedgesit
    with dissolve
    show yukio_smile at leftoff
    with moveinleft

    yuk "And how are we today, ladies and gents?"

    hi "Good."

    har "Good."

    mk "Good."

    suz "Good."

    show yukio_notimpressed at leftoff with charachange

    yuk "Don't be too enthusiastic, now."

    show haru_basic at leftoffsit with charamove
    hide yukio_notimpressed at leftoff
    show yukio_smile at oneleftsit with charamove
    show suzu_unhappy at onerightsit with charachange
    hide suzu_concerned at onerightsit

    "He takes a seat beside Suzu, giving her a brief disarming smile as he does. She visibly wilts, despite doing her best to avoid doing so."

    show haru_serious at leftoffsit with charamove

    "Haru looks back to the cake, but frowns as he begins to cut another slice."

    har "Hmm. We'll have one more slice than we have people. Should've worked that out first."

    mk "Dibs on the double portion."

    show haru_annoyed at leftoffsit with charamove
    hide haru_serious at leftoffsit

    har "Piss off. Suzuki gets double."

    show suzu_embarrassed at onerightsit with charachange
    hide suzu_unhappy at onerightsit

    suz "Uh... thank you."

    mk "Hold on, what's the criteria here? Is it because she's a girl?"

    show haru_basic at leftoffsit with charamove
    hide haru_annoyed at leftoffsit

    har "A polite young girl, yes."

    mk "What about me? I'm a girl too."

    stop music fadeout 0.5
    play music music_tension fadein 0.5

    show yukio_notimpressed at oneleftsit with charachange
    hide yukio_smile at oneleftsit

    yuk "Only when it suits you."

    "I get up out of my chair to get some height over him, which he responds to in kind."

    #get yukio closer/bigger somehow?
    hide yukio_notimpressed at oneleftsit
    show yukio_huh at oneleft with charachange

    mk "Oh yeah? How about you try having periods?"

    show yukio_angry at oneleft with charachange
    hide yukio_huh at oneleft

    yuk "Piss off, we have to-{w=.5}{nw}"

    mk "Look at me, I'm a man, oh no I have to shave my face, I have dreams that give me orgasms, how terrible~!"

    yuk "Well maybe you'd be treated like a girl if you actually acted like one!"

    mk "Huh? What's that? I can't hear you over bleeding from my genitals and feeling like I've been sucker-punched in the gut once a month!"

    yuk "You're making my point for me! If you didn't go on about your bloody periods while we're eating, we'd-!{w=.95}{nw}"

    mk "Maybe I'd act more like a girl once I got free crap for being one!"

    show hisao_frown_u at rightedgesit with charachange
    hide hisao_erm_u at rightedgesit
    show suzu_concerned at onerightsit with charachange
    hide suzu_embarrassed at onerightsit
    show haru_sad at leftoffsit with charamove
    hide haru_basic at leftoffsit

    hi "Miki, Yukio, please..."

    "Hisao looks to Suzu for help as we snarl at each other, but all she's doing is burying her face in her palm and trying not to exist."

    stop music fadeout 0.5
    stop ambient fadeout 0.5

    #shrink yukio back down

    "I want to thump Yukio for being an ass, but in contrast to the busy hum of students of before, the sudden silence around us reminds me that we're in the cafeteria."

    #hide yukio_angry at oneleft
    show yukio_angry at oneleftsit with charachange

    "Submitting to Hisao's begging, we both fall back into our seats, neither of us admitting that the argument is over."

    show haru_basic at leftoffsit with charamove
    hide haru_sad at leftoffsit
    show suzu_embarrassed at onerightsit with charachange
    hide suzu_concerned at onerightsit

    play ambient sfx_crowd_indoors fadein 1.0

    "As if the altercation had never happened, Haru passes the extra slice to Suzu, earning a shy nod of thanks. It only serves to make Yukio all the more pissed for some reason, but before I can step in to defuse the situation, Hisao does the job for me."

    show hisao_talk_small_u at rightedgesit with charachange
    hide hisao_frown_u at rightedgesit

    hi "What brings you here anyway, Yukio?"

    show yukio_notimpressed at oneleftsit with charachange
    hide yukio_angry ay oneleftsit
    play music music_ease fadein 1.5

    yuk "Oh, it's a woeful tale. A terrible curse has struck me yet again. Day after day this happens, and only so rarely can I find refuge from its grip."

    "He's totally making an ordeal out of it, clutching at his chest and emoting as hard as he can. Even if it's for an audience of one, he still likes to play the orator. It's a shame he stopped acting, really."

    yuk "I'm just... too popular."

    show hisao_erm_u at rightedgesit with charachange
    hide hisao_talk_small_u at rightedgesit

    hi "What."

    yuk "Girls just fall over themselves for me. It's been like this ever since high school started, and if anything it's only become worse."

    show yukio_blush at oneleftsit with charachange
    hide yukio_notimpressed at oneleftsit

    yuk "Oh, what I would do to get those women off me! I tell them I'm not interested, but it only makes them try all the harder."

    hi "You can't be serious."

    "Haru begins to come around each of our seats, setting down a slice before each of us before sitting beside Hisao. I quickly tuck into mine as soon as I can, the wonderful taste of cream and strawberries filling my mouth. Befriending this guy was one of the best decisions ever."

    show haru_smile at leftoffsit with charamove
    hide haru_basic at leftoffsit

    har "It's true. He ended up quitting drama and switching to the track club just to lower his profile." #changed this Mor to Har cause it makes sense -Niji [str]

    show hisao_smile_teeth_u at rightedgesit with charachange
    hide hisao_erm_u at rightedgesit
    play audio sfx_snap

    "Hisao suddenly clicks his fingers in a flash of insight."

    hi "Ah, that explains it! I knew that face on the posters was yours. You must still work for them sometimes, right?"

    show yukio_smile at oneleftsit with charachange
    hide yukio_blush at oneleftsit

    yuk "Yeah, though it's mostly organizing new recruits and helping with behind the scenes stuff. They probably just use my face to draw in a bigger crowd..."

    show yukio_eeh at oneleftsit with charachange
    hide yukio_smile at oneleftsit

    "His smile fails him as he looks down at his dessert, a cloud of despair hanging overhead. I wonder how many girls he'd get if he let this side of himself show through more often."

    yuk "Man, it really is a pain. Those girls are so loud and obnoxious, I can't stand any of them."

    mk "I might not the best judge, but I don't really understand your appeal. Physically, at least."

    show haru_basic at leftoffsit with charamove
    hide haru_smile at leftoffsit

    har "You don't?"

    mk "You do?"

    "I see an opportunity to both tease him and stroke my own ego, and so take it without hesitation."

    mk "Hmm... who do you think is hotter? Me, or Yukio?"

    show yukio_huh at oneleftsit with charachange
    hide yukio_eeh at oneleftsit

    "I lean around Hisao and stare intently at Haru, with Yukio reluctantly doing the same."

    show haru_serious at leftoffsit with charamove
    hide haru_smile at leftoffsit
    show hisao_erm_u at rightedgesit with charachange
    hide hisao_smile_teeth_u at rightedgesit
    show suzu_concerned at onerightsit with charachange
    hide suzu_embarrassed at onerightsit

    "Haru's taking this surprisingly seriously, his head moving between our faces with a look of total concentration as he brings his fingers to his stubbled chin. Seconds pass, with Hisao and Suzu's interest obviously piqued as they stare and eat at the same time."

    "Everybody's on tenterhooks as we await his judgment, with Yukio's face slowly moving further and further back."

    show yukio_eeh at oneleftsit with charachange
    hide yukio_huh at oneleftsit

    har "I'd have to say Yukio."

    "I'm a little disappointed in the answer, but the look on Yukio's face more than makes up for it."

    yuk "That's a joke... right?"

    show haru_basic at leftoffsit with charamove
    hide haru_serious at leftoffsit

    har "Not at all. I can definitely see why girls like you."

    show yukio_angry at oneleftsit with charachange
    hide yukio_eeh at oneleftsit

    yuk "You're the last person I wanted that kind of praise from."

    show hisao_smile_u at rightedgesit with charachange
    hide hisao_erm_u at rightedgesit

    "Smiling at his discomfort, Hisao finishes his cake and gives due compliments to Haru, which I hurriedly second."

    mk "Come to think of it, haven't you got lots of female friends, Hisao? Maybe you could give the stud here some tips on how to friendzone like a pro."

    show hisao_hmpf_u at rightedgesit with charachange
    hide hisao_smile_u at rightedgesit

    hi "Thanks..."

    yuk "I'm not interested in keeping them as friends, I just want them to piss off."

    show yukio_smile at oneleftsit with charachange
    hide yukio_angry at oneleftsit

    yuk "Here."

    "He plucks the strawberry off his dessert and plops it on top of Suzu's uneaten slice. She doesn't even notice, given her attention being focused on trying to get through the first without dropping crumbs everywhere."

    show yukio_huh at oneleftsit with charachange
    hide yukio_smile at oneleftsit

    "He waits for a reaction to his act of kindness before giving up and hanging his head in defeat. I don't think Yukio is having a good day."

    mk "Well, there you have it, Hisao. These are the losers I hang out with."

    show hisao_smile_u at rightedgesit with charachange
    hide hisao_hmpf_u at rightedgesit

    hi "They're not so bad."

    show haru_smile at leftoffsit with charamove
    hide haru_basic at leftoffsit

    "Haru clamps onto Hisao's shoulder and gives him a playful shake. It's nice to see Hisao loosening up, even if it is just a little."

    stop ambient fadeout 1.0
    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_C5:

    scene bg school_scienceroom
    #with shorttimeskip
    play music music_normal fadein 1.0

    window show

    "Walking into class, my gaze immediately falls to Suzu's desk. Each and every morning she enters class long before I do, and though I might have hoped to catch her out, today is no different than any other."

    "It's one of life's small wonders; I never did understand how someone in a perpetual state of sleep deficiency manages to get here on time every day. Well, it's not that I don't understand how, so much as why."

    "I suppose it's a lie to say that nothing at all is different, though. Her head may be resting in her hand as it always is, but rather than looking out the window, her eyes are on the guy casually speaking with her in front of her desk."

    "Suzu and Hisao took to each other surprisingly quickly. She doesn't seem particularly interested in actually conversing, but just giving him the time of day is more than she gives the other guys in the track and field club. 'Boorish', she calls them."

    "Which isn't wrong, really."

    mk "Yo."

    show hisao_talk_big_u at twoleft #make a surprised face for Hisao
    show suzu_surprised at tworight
    with charaenter

    "The two of them react in unison to the sound of my voice, Hisao turning his body towards me as Suzu moves little more than her eyes. Their normal morning greetings come to a halt almost as soon as they begin."

    hide suzu_surprised

    show hisao_erm_u at twoleft
    hide hisao_talk_big_u at twoleft
    show suzu_neutral at tworight
    hide suzu_surprised at tworight
    with charachange

    "Suzu just sighs as Hisao's face, as it so often does, turns to mild concern."

    hi "Are you... okay?"

    mk "Huh?"

    "He motions to his left cheek, my own fingers mirroring his out of reflex. It takes me a second to realize what he's referring to. I haven't looked in the mirror, but there'd no doubt be a nice big bruise there right about now."

    mk "Haha, this? I kinda got a bit rough with another club guy. We're cool, don't worry."

    show suzu_surprised at tworight with charachange
    hide suzu_neutral at tworight

    suz "Again?"

    hi "...This happens often?"

    show suzu_speak at tworight with charamove
    hide suzu_surprised

    suz "You have no idea."

    show suzu_concerned at tworight with charachange
    hide suzu_speak at tworight

    "I disarm him with a stupid grin as I scratch the back on my neck."

    hi "Both of you seem rather accident-prone."

    hi "Then again, maybe accident isn't the right term to use for you."

    play sound sfx_clap

    "The loud clapping of hands behind me would make me jump if it were less obvious who said hands belonged to. As Mutou clears his throat and tries to shepherd the gossiping class into their seats, Hisao obediently takes his leave of us and I turn to take my seat."

    hide suzu_concerned
    hide hisao_erm_u
    with charaexit

    "The fact he's addressing the class rather than me is cause for a mental sigh of relief. He wouldn't take kindly to casual talk of a scrap between students, and his classroom lectures are boring enough without being subjected to another on the subject."

    show muto_irritated with charaenter

    mu "Oh, and Miura? I'll see you after class."

    "Damn it."

    stop music fadeout 2.0

    scene bg school_gate
    #with shorttimeskip
    show suzu_neutral at twoleft
    show hisao_erm_u at tworight
    with shorttimeskip
    play music music_tranquil fadein 1.0

    "Jogging past the school gates, Suzu and Hisao can be seen patiently waiting for me. By now the main throng of leaving students has passed, reduced to little more than the occasional person or two."

    show suzu_speak at twoleft with charamove
    hide suzu_neutral at twoleft

    suz "Have fun?"

    mk "Detention on Monday. What a pain in the ass."

    show hisao_talk_small_u at tworight with charachange
    hide hisao_erm_u at tworight

    hi "At least it's Saturday, right? You've got a stay of execution for a couple of days."

    mk "Whatever. Let's just get lunch."

    suz "Shanghai?"

    mk "Yeah. You okay with that, Hisao?"

    hi "Sounds good."

    "The decision made, we set off down the hill for the local town."

    scene bg school_road
    with locationchange
    show suzu_concerned at twoleft with charaenter
    hide suzu_speak at twoleft
    show hisao_erm_u at tworight with charaenter
    hide hisao_talk_small_u at tworight

    "I like this time of year. The weather, hot with decent but not overbearing humidity, reminds me of home. It also means being able to wear summer outfits, which are far more comfortable than winter clothing."

    "It's hard to tell if Suzu's fidgeting is because she's uncomfortable around Hisao, or just because she hates the heat. She's a winter kind of person after all, in every way."

    "Even Hisao, the rookie, looks more casual than she does. That said, he has the undeniable air of a tourist about him; eyes flitting about, pace just slightly slower than what looks natural, head turning this way and that."

    mk "Where you come from, anyway? You aren't a local, that's for sure."

    show hisao_talk_small_u at tworight with charachange
    hide hisao_erm_u at tworight

    hi "The city. The quiet of places like this is a big difference."

    mk "Hah, a city boy. Should've known."

    hi "I take it you're from somewhere else, then?"

    show suzu_speak at twoleft with charachange
    hide suzu_concerned at twoleft

    suz "She's a hick from up North."

    mk "Hey."

    show suzu_grin at twoleft with charachange
    hide suzu_speak at twoleft

    suz "Well, aren't you?"

    show hisao_heh_u at tworight with charachange
    hide hisao_talk_small_u at tworight

    "I don't want to let her get away with it, but from the interested face Hisao's making, she's already won this."

    mk "We can't all be dainty spoiled princesses..."

    show hisao_disappoint_u at tworight with charachange
    hide hisao_heh_u at tworight

    hi "You make it sound like you're from out in the sticks or something."

    mk "I am, dude. Tell you what, the first time wandering around the city near here was a big culture shock."

    show hisao_wtf_u at tworight with charachange
    hide hisao_disappoint_u at tworight
    show suzu_surprised at twoleft with charamove
    hide suzu_grin at twoleft

    "His reaction is kind of charming. He has no idea at all what a country life is like, no doubt desperately mining his brain for any images that he can muster."

    "Not that Suzu's any different. I don't really care to explain it to either of them; it's not something I take particular pride in, and bringing her there to visit would only cause problems."

    mk "Oh yeah, I noticed you chatting with the guys in the track club yesterday. You ever going to actually join, or what?"

    show hisao_erm_u at tworight with charachange
    hide hisao_wtf_u at tworight

    hi "Do I have to? I don't remember it being compulsory."

    mk "That's not what I'm asking! Urgh."

    show hisao_smile_teeth_u at tworight with charachange
    hide hisao_erm_u at tworight

    hi "Maybe I should just join the literature club and wash my hands of the whole thing."

    show suzu_grin at twoleft with charamove
    hide suzu_surprised at twoleft

    suz "Yes, do that. The school hardly needs another jock running about."

    mk "Oi, doesn't that make me a jock?"

    show hisao_biggrin_u at tworight with charachange
    hide hisao_smile_teeth_u at tworight

    hi "To be fair..."

    with vpunch
    show hisao_talk_big_u at tworight with charachange
    hide hisao_biggrin_u at tworight

    "I clap the boy over the head, drawing protests from him. The last thing I need is another Suzu on my case."

    show suzu_normal at twoleft with charachange
    hide suzu_grin at twoleft

    suz "So violent."

    show hisao_smile_teeth_u at tworight with charachange
    hide hisao_talk_big_u at tworight

    hi "Very violent."

    "I'm beginning to think I've created a monster by bringing these two together."

    stop music fadeout 2.0

    scene bg suburb_shanghaiext
    with locationchange

    "By the time we reach the Shanghai, I feel like I've run through a gauntlet with the both of them pecking away. Suzu throws the odd snark while alone, but she and Hisao egg each other on."

    "I don't really hate it, though. It's maybe even a little cute."

    play sound sfx_storebell

    scene bg suburb_shanghaiint
    with locationchange

    "The bell above the door gives its trademark rattle as we file in, the waitress's hurried shuffling towards us no less familiar. Look like the place is mostly empty, save for a handful of other patrons."

    "Maybe it's a good thing; if such a place can stay open for this many years and not shut down from the lack of customers, at least the staff aren't going to be too stressed. They keep their jobs, and the town keeps its little odd cafe."

    show yuukoshang_happy_down at center with dissolve
    show yuukoshang_happy_down at centersitlow with charamovefast
    show yuukoshang_happy_down at center with charamovefast

    "When she reaches us, the waitress throws her upper body down in a sharp bow. Hisao flinches from how close she comes to head butting him."

    yu "Welcome to the Shanghai! Please take a seat."

    hide yuukoshang_happy_down with dissolve
    show suzu_neutral at twoleft
    show hisao_erm_u at tworight
    with dissolve
    show suzu_neutral at twoleftsit with charamove
    show hisao_erm_u at tworightsit with charamove
    #looks better if they don't sit at the same time -Niji
    play music music_daily fadein 1.0

    "I give a weak smile as we go, picking an empty window-side table from amongst the many. Suzu shuffles into her seat and I slide in next to her, Hisao being relegated to the other side."

    mk "You've been here a few times now, right? You like it?"

    hi "The fact that Yuuko's here still weirds me out a bit..."

    mk "Haha, yeah. Lots of people say that. She's pretty at least, right?"

    hi "Guess so."

    mk "You gotta loosen up, man. You're a teenage guy, nobody's gonna believe that you don't have an eye for the ladies."

    hi "How should I answer, then?"

    mk "I dunno. 'I like her tits', 'she's got nice thighs'. Whatever."

    show hisao_wtf_u at tworightsit with charachange
    hide hisao_erm_u at tworightsit

    hi "...Is Yuuko looking at us?"

    show suzu_veryembarrassed at twoleftsit with charamove
    hide suzu_neutral at twoleftsit

    suz "No, thank God."

    "I just smile at them. Looks like he's going to be just as easy to tease as Suzu is. Such prim and proper people, they are."

    show hisao_erm_u at tworightsit with charachange
    hide hisao_wtf_u at tworightsit
    show suzu_concerned at twoleftsit with charachange
    hide suzu_veryembarrassed at twoleftsit

    "As they both recover from their fit of modesty, a more important matter comes to mind. I want to help him back on his feet, but if he's going to be around me for any length of time, he'll have to get used to Suzu as well. And vice-versa."

    "I stare to my companion beside me, making her tilt her head."

    mk "Wanna show him your party trick?"

    show suzu_unhappy at twoleftsit with charachange
    hide suzu_concerned at twoleftsit

    "She pauses for a moment to work out what I'm referring to. By her increasingly hesitant face, she's got the right idea."

    "After thinking on it for a good while, with Hisao's face curiously looking on, she comes to the conclusion I'd been hoping for."

    show suzu_speak at twoleftsit with charachange
    hide suzu_unhappy at twoleftsit

    suz "If he's going to be hanging around, I guess we have to."

    hi "Show me what?"

    "I give him a disarming smile for a moment, before suddenly turning beside me."

    stop music

    mk "BOO!"

    show suzu_surprised at twoleftsit with charamove
    hide suzu_speak at twoleftsit

    "All she does is raise an eyebrow. I have to admit I'm holding back a little; my mental block against possibly hurting her isn't that easy to get around."

    suz "That isn't going to work if-"

    #shake the screen here maybe? -Niji
    show hisao_talk_big_u at tworightsit with charachange #and make hisao's and then Suzu's character jump up or something
    hide hisao_erm_u at tworightsit
    show hisao_talk_big_u at tworight with charamovefast
    show hisao_talk_big_u at tworightsit with charamovefast
    with vpunch
    play sound sfx_doorslam

    show suzu_speak at twoleftsit with charachange
    hide suzu_surprised at twoleftsit
    show suzu_speak at twoleft with charamovefast
    show suzu_speak at twoleftsit with charamovefast


    hi "ARGH!"

    "Hisao leaping out of his seat and hitting his fists to the table as he shouts, albeit in a careful way given we're in public, has the intended effect. Suzu immediately jumps in fright, my own heart skipping a beat in sheer startlement."

    show suzu_asleep at twoleftsitlow with charamove
    hide suzu_speak at twoleftsit
    play sound sfx_impact #with bang soundeffect

    "With barely a second's delay, the life seemingly goes out of her. A sigh as the air from her lungs lazily passes her lips is all to be heard as her small body goes limp in her seat. Her head jerks downward as all control goes out of her neck, before her entire upper body falls forwards."

    play music music_suzu

    "With an audible thud, her forehead lands on the table without the slightest resistance. Her arms follow soon after, flopping haphazardly onto the surface. With the show over, the girl beside me now lies seemingly dead, save for the movement of her breathing."

    show hisao_wtf_u at tworightsit with charachange
    hide hisao_talk_big_u at tworightsit

    "Hisao looks mortified, as if he himself had fired a bullet into her. Shock from the sudden nature of what happened, and extreme discomfort from a human moving and remaining limp in such an unnatural way, are written on his face."

    "I have to admit, for all I may be trying to play it cool, it still puts me off a little. I've never truly gotten used to this."

    hi "Is she... okay...?"

    mk "She's fine. Welcome to cataplexy."

    mk "Her muscles stop working when she gets shocked or has big emotions. It's like, bang, you end up a lifeless doll."

    show hisao_talk_small_u at tworightsit with charachange
    hide hisao_talk_big_u at tworightsit

    hi "Part of her narcolepsy?"

    mk "Yep. It ain't always just sleeping, unfortunately."

    show hisao_disappoint_u at tworightsit with charachange
    hide hisao_talk_big_u at tworightsit

    hi "Cataplexy..."

    stop music fadeout 3.0

    "He says the word slowly and carefully, making sure he engraves it onto his mind. He gives the word a lot of weight in the way he says it, which is good to see."

    play music music_raindrops fadein 3.0

    show hisao_erm_u at tworightsit with charachange
    hide hisao_disappoint_u at tworightsit

    hi "Is it always like this?"

    mk "Well, Suzu's case is.... not light, to put it one way. Usually it's just like, weak knees, or not being able to keep your head up."

    "I feel bad for saying it so plainly, even if Suzu would've done just the same if she were able to right now. She got dealt a really shitty hand, and saying so just makes it feel all the more real."

    show hisao_frown_u at tworightsit with charachange
    hide hisao_erm_u at tworightsit

    "He looks back to her for a moment, but doesn't last long before covering his face with his hands to try and recollect himself. I can't say I blame him."

    hi "Sorry, this is just..."

    mk "It's cool; I had the same reaction as you when I first saw it happen. Hell of a trick, eh?"

    hi "Does she need to be snapped out of it somehow?"

    mk "Give her a minute or two and she'll be right as rain."

    show suzu_sleepy at twoleftsitlow with charachange
    hide suzu_asleep at twoleftsitlow
    show suzu_concerned at twoleftsit with charamove_slow
    hide suzu_sleepy at twoleftsitlow

    "No sooner do I say this, than Suzu begins to stir. Groaning slightly, she manages to move her arms to more comfortable positions before ever so slowly levering herself off the table."

    "With a bit of time to reorient herself and rub her eyes, she eventually comes back to the land of the living."

    suz "Don't be sorry about how you reacted. I'm used to it."

    hi "You heard everything?"

    suz "My muscles give out, not my senses. Which can be a pain all on it's own."

    show hisao_erm_u at tworightsit with charachange
    hide hisao_frown_u at tworightsit

    hi "How do you mean?"

    suz "When I get an attack, people often think I've had a seizure, fallen asleep, or fainted. It's not fun to be aware of what people are doing to your body while trying to wake you up, but unable to say anything."

    mk "And that's why it's handy to have someone around who knows all this when you get an attack."

    hi "Makes sense. To be honest, I had no idea narcolepsy included something like that."

    hi "How often does it happen, if you don't mind me asking?"

    "She just shrugs."

    show suzu_speak at twoleftsit with charachange
    hide suzu_concerned at twoleftsit

    suz "It varies."

    "Something's off about her answer. Whenever I've asked her questions about anything, but especially her narcolepsy, she always gives the most specific response she can. Partly because I pressured her into it so I could keep track."

    "Given she has no reason to be vague for his sake, it makes me concerned that her attacks are getting worse and she's trying not to tell me. It's the kind of terrible attempt at secrecy she'd try."

    hi "I'm guessing this is how you got the knee brace?"

    "A nod is her answer. Hisao's simpleminded curiosity is endearing, and Suzu dutifully doles out answers in her usual dull and encyclopedic manner. Talking about it in a generic way doesn't seem to bother her, at least as far as I can tell."

    show suzu_normal at twoleftsit with charachange
    hide suzu_speak at twoleftsit

    "With this, Hisao's line of questioning appears to be at an end. His sits back and thinks for a little, the footsteps of Yuuko approaching our table eventually reaching our ears."

    #move hisoa & suzu to right
    #show hisao_erm at right with charamove
    #show suzu_normal at centersit with charamove
    show yuukoshang_happy_down at left with moveinleft
    #play music music_everyday_fantasy fadein 1.0

    yu "What would you like today?"

    show hisao_smile_u at tworightsit with charachange
    hide hisao_erm_u at tworightsit

    hi "Coffee and a slice of pie, thanks."

    mk "Same as him."

    suz "Just tea, please."

    yu "No problem, coming right up!"

    show yuukoshang_happy_down at leftsit with charamovefast
    show yuukoshang_happy_down at left with charamovefast
    hide yuukoshang_happy_down with moveoutleft
    #move suzu back left

    "With her usual sharp bow, she scuttles off behind the counter. I still can't decide if the uniforms here are dorky or nice, but it suits her somehow. Not only because it shows off her nice legs, either. Her unusually chipper mood today makes her extra cute."

    show hisao_disappoint_u at tworightsit with charachange
    hide hisao_smile_u at tworightsit
    show suzu_neutral at twoleftsit with charamove
    hide suzu_normal at twoleftsit

    "The three of us end up waiting in silence for our drinks. Suzu takes out her phone and begins tapping away at it, the screen held in front of her as she browses whatever site she's on now. Hisao just looks out the window, his expression showing him to be deep in thought."

    "I kind of want to bug him so I can have a conversation partner, but I decide to leave him be. The boy has a lot to think about right now, after all."

    "Looking around the cafe proves about as boring as expected. A few old people who came to this town to live out a quiet retirement sit at a few of the tables, and a handful students from Yamaku populate the others. I think I recognise the back of the class rep's head over the other side of the cafe, but I can't be sure."

    #move hisao and suzu right
    show yuukoshang_happy_up at left with moveinleft

    "After what feels like forever, Yuuko emerges with three drinks and two pie slices on a platter. Suzu may live in her own world sometimes, but at least she's polite, putting down her phone as they're set down on the table in order to thank her."

    show yuukoshang_happy_down at left with charachange
    hide yuukoshang_happy_up at left
    play sound sfx_storebell
    pause
    hide yuukoshang_happy_down with moveoutleft
    #move suzu and hisao back

    "The bell above the door rings out, with Yuuko giving the briefest of nods before quickly scooting off to the entering customers."

    mk "The town's pretty nice, isn't it?"

    show hisao_erm_u at tworightsit with charachange
    hide hisao_disappoint_u at tworightsit

    hi "Hmm? Oh, yeah, it is."

    show suzu_normal at twoleftsit with charamove
    hide suzu_neutral at twoleftsit

    stop music fadeout 1.0

    "Hisao's absentminded reply annoys me a little, but the tinkle of silverware on her teacup draws the attention of both Hisao and I. Suzu ladles teaspoon after teaspoon of sugar into her tea, only stopping after it becomes more a sweet dessert than a drink." #originally said tinker of silverware. Replaced with what I assume Suriko intended -Niji [str]

    show hisao_declare_u at tworightsit with charachange
    hide hisao_erm_u at tworightsit
    play music music_caged_heart fadein 1.0

    "After staring at his coffee for a bit afterwards, Hisao lets out a long breath before speaking up."

    hi "I wasn't going to mention this, but I probably should."

    "He already has the attention of Suzu and I after speaking, but the both of us become a lot more curious after he moves his tie to the side and begins unbuttoning the top of his shirt."

    "I briefly wonder how much of his chest I'm going to get to see, but he stops after undoing several of the topmost buttons. A shame; he looks like he'd have a nice chest on him."

    "Pulling his collar aside, what he intends to show us becomes clear. The top of a vertical line chasing up the very center of his chest, depressed just slightly into his flesh and shaded a little darker than the surrounding skin."

    show suzu_surprised at twoleftsit with charamove
    hide suzu_normal at twoleftsit

    suz "An operation?"

    show hisao_disappoint_u at tworightsit with charachange
    hide hisao_declare_u at tworightsit

    hi "For my heart. A few months ago I had a heart attack caused by arrhythmia. The scar's from when they cracked my chest open for surgery."

    "So what Haru said was true. I do my best to feign mild surprise, as the fact that I learned it before he was ready to do his show and tell makes me feel a little sheepish."

    "Then again, the fact that there's such a visual indication of what he's been through is a real surprise. I always thought of heart attacks as something you don't really see, but his large scar is impossible to miss. It's jarring."

    mk "That's... damn."

    show hisao_heh_u at tworightsit with charachange
    hide hisao_disappoint_u at tworightsit

    "I feel a bit bad for opening my mouth but failing to find something to say. He gives a weak smile to excuse me for it, but I'd have honestly preferred him to be annoyed with me than make a face like that."

    hi "There you have it. The reason I transferred to Yamaku, that is."

    "Hisao buttons up his shirt and blows on his coffee before beginning to drink it, the fact that none of us really have anything more to say about his revelation becoming obvious. Suzu and I briefly look to each other before doing the same."

    "The more I think about it, the more it makes sense. His inability to keep up with Emi at all on the track, constant resting, weirdness around joining in sports... Given his build, he was no couch potato before it happened."

    "I have to admit that it was a smooth move to show us that right now; I can see the gears turning in Suzu's head. Opening himself up to us like that, especially just after Suzu showed her condition to him so vividly, will go a long way in earning her trust."

    "He probably doesn't know it yet, but it looks like he'll be able to handle her just fine. Not many people can."

    stop music fadeout 2.0

    scene bg suburb_shanghaiint
    show suzu_sleepy at twoleftsit
    show hisao_erm_u at tworightsit
    with shorttimeskip

    "As I chow down the last of my pie, I notice a subtle movement from the corner of my eye. Turning to where it came from, I see Suzu's head beginning to slowly nod, her eyelids also having trouble staying up. She might be working to hide it, but the harder she tries, the more obvious it is."

    "If she's already this bad, she's probably been fighting to stay lucid for a while. Silly girl."

    mk "It's fine."

    suz "Sorry."

    "She looks annoyed, but only in the most routine of ways. It's far from the first time this has happened, after all."

    show suzu_asleep at twoleftsitlow with charamove_slow
    hide suzu_sleepy at twoleftsit

    "The world drops from her consciousness as she lowers herself down to the table, this time in a much more careful way than the last. I dutifully take her empty cup of tea and place it a few inches away as her arms come to rest around her head."

    "Hisao silently looks on, doing his best to appear nonplussed as he defers to my experience in dealing with her."

    "And just like that, Suzu's gone."

    mk "Whelp, she's out for the count."

    hi "This is just sleep, right?"

    mk "Yeah, just a nap. She's gonna be out for a while, most likely."

    hi "Do we wait for her, or...?"

    mk "Nah, I'll just carry her back."

    show hisao_talk_small_u at tworightsit with charachange
    hide hisao_erm_u at tworightsit

    hi "You sure? I can do it if you want."

    mk "Your chivalry is cute, but it's fine. There is something else you can do, though."

    hi "Yeah?"

    mk "Spot me the meal? Pretty please?"

    hi "And why should I do that?"

    mk "'Cause I'm cute."

    show hisao_hmpf_u at tworightsit with charachange
    hide hisao_talk_small_u at tworightsit

    "He just grimaces. I knew I should've gone with 'hot' or 'sexy'."

    show hisao_declare_u at tworightsit with charachange
    hide hisao_hmpf_u at tworightwit

    hi "Alright, I'll do it. That will work exactly once, understand?"

    "Excellent. I wonder how many times I can get him to do that with various excuses."

    "Acting fast before he can retract his offer, I smile and call Yuuko over. With the bill paid over Suzu's peacefully sleeping body, our little outing comes to an end."

    scene bg school_road_ss
    show hisao_erm_u
    with shorttimeskip
    play music music_tranquil fadein 1.0

    "The trudge up the hill back up to Yamaku from town is a journey I've made countless times by now. I'm pretty sure I've lost count of the number of times I've made it while carrying a slumbering girl on my back, too."

    "It's not much of a bother, to be honest. She's a light little thing, worryingly so at times, and it's good exercise for my upper body in any case."

    "Hisao tries his best to look like this is a routine thing, but it's in vain. A one-handed girl walking up a hill with her sleeping friend on her back is just too odd a sight to ignore, at least in the beginning."

    show hisao_talk_small_u with charachange
    hide hisao_erm_u

    hi "I've got no idea how you manage that."

    mk "It ain't so bad. I've been working out since forever anyway."

    "The thought of a girl being stronger than he is clearly dents his pride a little. That he's already breathing heavily while I'm not having much trouble at all just makes it worse."

    "At least he has a fair excuse, given what he said back there."

    hi "It's nice, though. You two must be really close."

    mk "Why do you say that?"

    hi "Suzu trusts you enough to be okay with you manhandling her, and you put yourself out to carry her around. You both seem to have a good handle on each other, too."

    "I think to myself a bit about his words. I suppose it's reasonable for an observer to think that, but I wouldn't really way we're close at all. I struggle for a bit to put our relationship into words, as much for me as for him."

    mk "It's... practical. Yeah, I think that's the best way to describe our relationship."

    show hisao_erm_u with charachange
    hide hisao_talk_small_u

    hi "You fell into each other's orbit."

    mk "Yeah, exactly. You're good with those word things."

    "I'm happy with that description, and I think Suzu would be too, if she could hear it. Hisao, on the other hand, looks quite put off even if he did suggest it. He probably made the assumption just because we were both girls."

    "It's not worth getting too attached at this point, anyway. She's going to get into some good university, just like Hisao is given his constant praise from Mutou. That path is closed for me. Things got a lot better when I stopped caring about that fact."

    stop music fadeout 1.0

    "But even now, as I carry her still body up the hill like this, I still feel the slightest bit comforted by her warmth."

    scene bg school_girlsdormhall
    with shorttimeskip

    "Having parted and gone our separate ways, Hisao to the male dormitory building - after telling me his room number, in case I decide to visit - and the two of us to the female one, I find myself shuffling up the hallway to Suzu's room. It's the floor below my own, unfortunately; if we were neighbors, it'd be a lot more convenient."

    "With my left arm holding up Suzu, I manage to retrieve the key to her room from my pocket after some fiddling. Her convincing the staff to let me get a copy of her dorm room key cut for situations like this was one of her better moves."

    play sound sfx_dooropen

    "A quick flick of the hand, and the lock opens with a satisfying click. Manoeuvring around the door as I open it, the familiar smell of her room hits me before the view does."

    scene bg dormsuzu
    with locationchange

    "It's 'girly', for lack of a better word. I don't know exactly what makes up the scent, beyond probably nail polish remover and light perfume, but it's unmistakable and foreign nevertheless."

    "Closing the door behind us and turning to the room ahead, I slowly navigate the way to her bed, taking care to manoeuvre around the multitude of papers, books, clothes, manga, magazines, and toys scattered around the floor. She has a desk, but that's largely dedicated to her big laptop, plus a few other toys around it."

    "My room might be far from spotless, but at least you can see the floor. Then again, maybe that's just because I don't have the money to constantly buy things."

    "Grunting a little, I turn around at the side of her bed and bend down at the knees, slowly lowering Suzu onto her bed. With the weight lifted from my shoulders, I turn back and set about organising the disheveled heap, moving her legs and arms around to whatever looks reasonably comfortable."

    show suzu_asleep with dissolve
    play music music_suzu

    "My work done, I stand back up and admire my work. I can't help but smile at the absurdity of it all, even after all this time. A perfect little spoiled princess, neatly arranged with her plush toys all around her on the bed to keep her company."

    "I reach down and brush a stray hair away from her closed eyes, my gaze lingering a little on her motionless face. It's almost painful how delicate she looks, like a china doll that could crumble any second."

    "She really is a real life Sleeping Beauty."

    "I shouldn't get so sentimental about it. Maybe it's because I've only ever hung around with guys that a girl who actually acts like one feels so strange. It could just be yearning for a side of me I've never had a chance to explore. Who knows."

    hide suzu_asleep with dissolve

    "Well, whatever. I turn and scratch the back of my head as I make to leave, trying to brush the thoughts from my head. It doesn't really matter what Hisao thinks about our relationship; I'm not the kind of person a girl like her should be around."

    scene bg hatsune with dissolve

    "I stop for a moment as I'm distracted by an actual doll on Suzu's shelf. An energetic-looking girl in bright clothes from some show she watched a while ago. She has a lot more at home, but only brought a handful to her dorm. She might call them figures rather than dolls, but I don't really get the difference."

    "I poke at its head for something to do as I mull things over."

    "We really are from two different worlds. For all I try, I can't think of a damn thing we have in common. I'm envious of so many things about her, from her innocence, to her family, to her wealth, but I've never bothered mentioning it."

    "Some people pop out of the right set of legs, and others don't. Some people mess everything up, and others don't. That's life."

    suz "Don't..."

    scene bg dormsuzu
    show suzu_sleepy
    with dissolve

    "Suzu's voice, little more than a faint and mumbled whisper, draws my attention to her as I obediently stop tweaking at her doll. It looks like she's awake, albeit only by the most generous definition."

    "She rubs her eyes, but does little beyond stare at the ceiling. I've always thought it must be hard to constantly be waking up in different places than where you went to sleep, but she's never once complained about it."

    mk "You okay?"

    suz "I'm fine."

    "No, she's not. Her voice has a slightly miffed edge to it, which she's too groggy to try and cover for."

    "She's never worried about being a bother to me before. Not that I mind; being useful to at least one other person in the world is something I need. She's a total idiot socially, but I think even she managed to work that out for herself."

    "That leaves the only other person that was with us."

    "It's kind of cute, really, getting all rattled about her narcolepsy in front of a boy. I shouldn't smile, but it's hard to suppress. Having just transferred, it's unlikely Hisao would have a girlfriend right now, so she's in with a good chance."

    mk "Don't feel bad about it. Hisao's pretty understanding."

    show suzu_concerned with charachange
    hide suzu_sleepy

    suz "He's a total babe in the woods is what he is."

    mk "Haha, you got that right. He's totally helpless right now."

    mk "What do you think of the guy?"

    show suzu_surprised with charamove
    hide suzu_concerned

    "She looks at me a moment trying to ascertain my intentions. That was an amazingly direct way to try and gauge her feelings towards him, after all."

    show suzu_speak with charamove
    hide suzu_surprised

    suz "He's sensible. I don't mind him."

    "Well done, Hisao. That's one of the highest compliments someone could ever hope for from her."

    "She's not wrong, though. He might be a nerd, but he's comfortable dealing with the other club guys as friends. His sensitive side is enough to make Suzu lower her guard around him as well, which is someone none of those guys could ever do."

    "Looks like I'm stuck with him, then. There aren't many that can overcome Suzu's distrust of others, and as far as friends go, I could do a lot worse than Hisao. Having someone around who doesn't know about my past means a lot less baggage to deal with, too."

    suz "What are you smiling about?"

    mk "Nothin'. Just take it easy for today, alright? And eat a snack or something; don't think I missed you skipping lunch."

    show suzu_normal with charachange
    hide suzu_speak

    suz "Only if you promise to do your homework for once."

    mk "Alright, alright, I will. See you tomorrow."

    suz "See you."

    "With that, I give her a parting wave before leaving the room and its girly smell."

    scene bg school_girlsdormhall
    with locationchange
    stop music fadeout 1.0
    play sound sfx_doorclose

    "Entering the hallway and carefully closing her door behind me, all I can do is rest my back against it as I close my eyes and sigh. Looks like the last few months of my time here won't be as simple as I expected."

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_C6:

    scene bg city_street2
    with dissolve
    play music music_ease fadein 1.0

    window show

    "Leaning back against the railing as the multitude of people ahead move to and fro, I do my best to pass the time by watching those who walk by."

    "I had arranged to meet Suzu and Hisao at noon, but it's getting perilously close and there's still no sign of either of them. I probably should have listened to Hisao and taken the same bus as he was going to use after all."

    "Not that I mind all that much. Just leaning back and watching others is entertaining, given the sheer variety in people you see. I suppose when you get enough people in one place, you'll eventually start seeing the odd ones."

    "Of course, badly hidden glances from the occasional person who notices my left arm ending in a stump reminds me that I'm one of the odd ones myself."

    "If I really cared, I could cross my arms, shove the stump in my jean pocket, or just pull down the sleeves of my shirt a little. It's not exactly hard to notice when my sleeves are rolled up, after all."

    "It hardly matters, though. I'm out of their consciousness a minute after they lose sight of me, so I may as well just wear whatever's comfortable. That's one of the advantages of a city over small town life; when you're surrounded by so many people, it's easy to be forgotten."

    "I look to my watch again to see the time, the dark grey digits reading out a time of five minutes to noon. At least I had an early lunch, so I'm hardly starving for food."

    "As soon as I begin to wonder if either of them will actually be here on time, I notice a familiar young man with brown hair manoeuvring through the crowd. It takes a moment to identify him, given that this is the first time I've seen him out of his school uniform."

    show hisao_smile with dissolve

    "Hisao doesn't look fussed by the crowd at all as he walks up, casually strolling through wherever he can see a gap in the people moving around him. Guess he's the punctual type, given how close he cut it."

    hi "Hey. Looks like I made it just in time."

    mk "Getting out of the retirement home took a while, then?"

    show hisao_talk_big with charachange
    hide hisao_smile

    hi "Huh?"

    mk "The vest. It's not a cool look."

    show hisao_hmpf with charachange
    hide hisao_talk_big

    hi "Don't knock the vest; it's smart."

    mk "Whatever you say, gramps."

    "He begins to protest, but turns to the side instead. My own gaze follows his out of curiosity, with the object of his attention becoming quickly obvious."

    "Suzu runs towards us as fast as her legs can take her, her white summer dress billowing out behind her as she tries to hold her bag to her side. It's kinda sad how slow she is despite the fact she's running."

    show hisao_erm with charachange
    hide hisao_hmpf

    hi "Damn..."

    "I turn to see Hisao averting his eyes, holding his balled hand to his mouth to try and hide his expression."

    mk "Hmm?"

    show hisao_blush with charachange
    hide hisao_erm

    hi "She's cute."

    "All I can do is give an amused snort."

    mk "Yup."

    show hisao_blush at tworight with charamove
    show suzu_veryembarrassed_d at twoleft with moveinleft

    "She pants heavily as she reaches us, barely managing to splutter out a greeting as she gasps for air. In the end we all got here on time, even if it was only just barely."

    suz "Sorry... I slept in... I didn't..."

    show hisao_smile at tworight with charachange
    hide hisao_blush

    hi "Just calm down and take a breath. It's fine."

    "The two of us wait for Suzu to settle herself before either continues."

    show suzu_normal_d at twoleft with charachange
    hide suzu_veryembarrassed_d
    show hisao_talk_small at tworight
    hide hisao_smile

    hi "So do we actually have any plan about what we're doing, besides hanging out?"

    suz "I need to buy a couple of new notebooks. I've almost run out."

    mk "Stationery shopping? Really?"

    hi "To be honest, I could probably do with picking up a couple as well."

    mk "You two are the worst."

    "Further protests don't make any difference to either of them, so the three of us end up heading off towards a stationery shop to pick up school supplies. I guess I could buy a pen... or something. Beats waiting outside for them."

    scene bg city_street4
    with locationchange

    "As we walk on, the heat of the summer's day beating down, I find myself distracted by the sights alongside us. It's Hisao who eventually picks up on it."

    show suzu_neutral_d at twoleft
    show hisao_smile at tworight
    with dissolve

    hi "What's up?"

    mk "You know, I can never get used to those huge displays. The ones they use for advertising and stuff."

    "I point upwards the massive screen mounted on the front of a tall store, the logo of some electronics company flashing up and moving about with wild and vivid color. Even in the summer's daylight, the screen is dazzlingly bright and impossible to ignore."

    show hisao_erm at tworight with charachange
    hide hisao_smile

    "Hisao, for his part, looks rather unimpressed. I might as well have pointed to a pebble on the ground for all the interest he takes. The best he can do is tilt his head as he tries to think of something to say about it."

    hi "Yeah, it is pretty big."

    show suzu_speak_d at twoleft with charamove
    hide suzu_neutral_d at twoleft

    suz "He comes from the city. What do you expect?"

    "So Hisao's a city boy. Should've guessed."

    "Images of Tokyo and Osaka I've seen on television spring to mind; a teeming mass of people flowing through streets like gushing rivers of water, the bright blare of storeys-high screens beaming down on their heads."

    mk "Man, I gotta go to Tokyo sometime. It's like living in the future, there."

    show hisao_wtf at tworight with charachange
    hide hisao_erm
    show suzu_surprised_d at twoleft with charamove
    hide suzu_speak_d

    hi "Hold on, you've never been to Tokyo? Not once?"

    "Even Suzu shares Hisao's disbelief, wheeling around to see me as the three of us grind to a halt. All I can do in response is shrug."

    mk "Never needed to."

    "The two of them share a knowing glance before continuing on. I think I just validated a whole bunch of ideas they had about me."

    "With a quick skip up to them, we continue on our way."

    stop music fadeout 1.0

    scene bg arcade
    with shorttimeskip
    play music music_miki

    "I just couldn't hack it. With the Suzu and Hisao dawdling around getting books, folders, and whatever else, I ended up bailing out and hitting the arcade next door."

    scene bg hotdo1
    with locationchange

    "Dancing games are rather pointless without friends, so the choice was largely already made as to what to play. Cheap plastic gun in hand, I plink away at the screen for minutes on end, sending zombies and other undead sprawling to the ground."

    "I wonder if I can get used to the quiet of home after being in a place like this. Fancy amusements like arcades, music stores, and concerts still feel like a novelty to me, but everyone else barely notices how amazing they are."

    "Even as I gun down more monsters in a violent pixilated rampage, a couple at the entrance can be heard deciding to go to the cinema instead of wasting time here. I did see movies before moving to Yamaku, but it was a rare treat back then. Here, it's just a spur of the moment decision."

    "That momentary lapse in concentration is all the excuse the game needs to destroy me, scratch marks suddenly littering the screen. I try to fight back, but my pace is completely gone."

    "As the continue screen comes up, hungry for more coins as always, a familiar voice comes from beside me."

    scene bg arcadeint
    with locationchange
    show hisao_smile_teeth at oneright
    show suzu_normal_d at oneleft
    with dissolve

    hi "You did pretty well. That game's pretty unforgiving."

    "Hisao and Suzu stand side by side, having patiently waited for me to finish. It's kinda funny to see them together like this; they look like they're cosplaying an elderly couple. No sense of fashion, not that I'm one to speak."

    "What he said piques my curiosity, though; I wonder is he's any better than me at this, given that he seems to have played before."

    mk "Fastest lightgun in the West. You any good at this stuff?"

    show hisao_closed at oneright with charachange
    hide hisao_smile_teeth at oneright

    stop music fadeout 0.5

    hi "Start up a 2-player game and I'll show you."

    hide suzu_normal_d at oneleft
    hide hisao_closed at oneright
    with charaexit
    scene bg hotdo2 with dissolve
    play music music_running

    n "Something about the tone of his voice is different than usual. I only realise what it is after he's given Suzu his bag to hold and taken up position with the second lightgun, pulling it from its holster with practiced ease. He's excited. Just a little, but it's there."

    n "I occasionally throw a glance at him as I set up a fresh round, throwing in my last few yen as he looks down the sights. Guess I'll be mooching off someone for dinner again, but my curiosity's demanding to be sated."

    n "The two of us take up our positions as the co-op story mode starts up, going through the same lame intro sequence I've seen so many times before."

    n "And then... it begins."

    n "As undead spring up from the corridors we walk through, the two of us blast away as fast as the guns allow. We get past one level, then two, then three."

    n "I'm starting to have problems as we reach the fourth, with more and more enemies requiring more and more shots start launching themselves at us. One life gets used, then another, and by the time the level's over, I'm sitting on just one left."

    n "I hardly feel bad about it, though. It might only be by the skin of my teeth, but this is the first time I've managed to get to the fifth level. Hisao's quite the comrade, and peering over at his side of the screen, it looks like he's still got two lives left to my one."

    n "He looks like the other runners in the club when they get into the zone, with their eyes narrowed and mind focused. It's a cool look. Perhaps a little too cool, as his focused expression almost makes me miss the first enemies of the new level."

    n "That said, it wouldn't have made of a much difference if it had. My last life disappears in the opening few moments, leaving the rest to Hisao. Not that he seems to mind, as he manages the challenge of two player's worth of enemies at once for some time."

    n "But then it happens. One life is gone by the time the level's wrapped up, and by the time the sixth level has started, it's obvious he's overwhelmed. He puts up a heroic last stand, but in a few minutes, he's taken out by a veritable flood of enemies."

    n "The continue screen returns once again, the both of us well and truly beaten. Hisao lets out a long breath as his shoulders slump, the adrenaline leaving him as he returns the lightgun to its holster."

    nvl hide dissolve

    nvl clear

    scene bg arcadeint
    show suzu_happy_d at oneleft
    show hisao_smile at oneright
    with charaenter

    suz "That was pretty good."

    mk "Thanks. Had a good wingman, though."

    "Hisao just shrugs. He just looks at the screen for a while before turning to us with a cocky smile. I think it's the first time I've seen him genuinely proud of an accomplishment."

    hi "That's how you do it. We heading off?"

    stop music fadeout 1.0

    "Suzu nods and takes the lead, handing Hisao his bag before the three of us file out into the busy street outside."

    scene bg city_street4
    with locationchange

    play music music_ease fadein 1.0

    show suzu_normal_d at twoleft
    show hisao_smile at tworight
    with charaenter

    "The difference between the air-conditioned arcade and sunbaked walkway is like night and day, with the afternoon's heat setting in."

    show suzu_speak_d at twoleft with charachange
    hide suzu_normal_d at twoleft

    suz "You look pleased with yourself."

    hi "Just been a while since I hit the arcades. Kinda happy I can still pull that off."

    mk "You're the only guy I've seen manage to get that far. I thought they rigged those things so you had to keep buying lives to continue."

    hi "They pretty much do. Actually finishing is nearly impossible."

    show suzu_sleepy_d at twoleft with charachange
    hide suzu_speak_d at twoleft

    mk "Well look at Mister Arcade Machine Expert talking big over here."

    stop music fadeout 1.0

    "I turn to Suzu to back me up, only to find her no longer in sight. Both Hisao and I turn to check where she is in confusion."

    "Walking slower and slower behind us, Suzu's eyes remain pinned to the ground ahead of her. I might not be particularly bothered by the heat, but Suzu isn't as hardy as most."

    show hisao_talk_big at tworight with charachange
    hide hisao_smile at tworight

    play music music_tension

    "My heart freezes as she suddenly begins to fall, legs crumpling underneath her and giving no resistance as her body drops downward. A movement from the corner of my vision darts forwards before I even have a chance to react."

    show suzu_asleep_d at twoleftsitlow with charamove
    hide suzu_sleepy_d at twoleft
    show hisao_talk_big behind suzu_asleep_d at twoleftsit with charamovefast

    "It's all over in what must be less than a second. Hisao, hero of the day, stands with his legs bent as he holds Suzu's limp body to his front. Every time he lulls me into thinking he's just another boring studybug, he goes and pulls something like that."

    show hisao_erm behind suzu_asleep_d at twoleftsit with charachange
    hide hisao_talk_big at twoleftsit

    stop music fadeout 1.0

    mk "That was some amazing stuff, dude."

    #show hisao_talk_small behind suzu_asleep at twoleftsit with charachange
    #hide hisao_erm at twoleftsit

    hi "Don't worry about that. Could you take her?"

    mk "Sure, hold on."

    "Back when he first entered Yamaku, everyday conversations tended up put him on guard, but now he's dealing with a public situation without panicking in the least. He might be sweating a little, but I'm still impressed."

    hide suzu_asleep_d at twoleftsitlow with moveoutbottom
    show hisao_erm at center with charamove
    #show hisao_erm at center with charachange

    "I quickly jog up and turn around, Hisao helping manoeuvre her onto my back. The heat alone wouldn't do this, but if she was tired before coming here, it might have finished her off. Whether it's cataplexy or a sudden sleep attack, she's not going to be in a condition to walk much more in either case."

    mk "See anywhere we could rest a bit?"

    "He scans around a little before pointing to a small cafe with some free outdoor tables."

    hi "Let's head over there. We can grab a coffee while she recuperates."

    "Sounds like a plan. I nod in assent as we move off, the slumbering girl on my back drawing more than a few badly hidden glances. I'm kind of glad she isn't awake for this, as she'd no doubt hate the attention."

    "Thankfully it isn't far to the place Hisao pointed out, with him going inside to order a couple of coffees while I deposit Suzu in a chair before taking a seat myself."

    scene bg city_cafe
    show suzu_asleep_d at twoleftsitlow
    with locationchange
    play music music_raindrops

    "It's been a long time since she passed out in public. Now that I think about it, it must look incredibly suspicious to the people around us for two teenagers to be dragging around an unconscious girl. Maybe it's a good thing I'm a girl too, as two guys dragging her around would look even worse."

    "I idly rap my fingers on the table while occasionally glancing to her, arms and head arranged on the table in what's hopefully a comfortable position."

    "Thinking back to when she fell, I reach into the wallet in my back pocket and fish out some yen. I can't really ask Hisao to spot me the coffee after what he did for her; it's incidents like that which gave her that stupid knee brace in the first place."

    show hisao_erm at tworight with moveinright
    show hisao_erm at tworightsit with charamove

    "Eventually he emerges from the glass door of the cafe, setting down a cup in front of me before sitting down. I put several notes on the table and slide them over in return, earning a nod of thanks before he slips them into his pocket."

    mk "Bit of excitement there, eh?"

    show hisao_disappoint at tworightsit with charachange
    hide hisao_erm at tworightsit

    hi "I could do without more excitement in my life, to be honest."

    mk "Where'd you get reflexes like that, anyway?"

    hi "Dunno, probably partly from playing so much soccer. Before the heart attack, anyway."

    show hisao_frown at tworightsit with charachange
    hide hisao_disappoint at tworightsit

    hi "I miss playing that..."

    "He gives a wistful sigh as he looks out to the street."

    "I feel terribly bad for asking. I know that sting all too well, and here I am inflicting it on someone else, albeit accidentally."

    mk "Wanted to go pro, or...?"

    hi "Nah, nothing like that. It's just... it was structure, I guess. Something to dedicate myself to."

    hi "I was good at it, you know. Nothing amazing, but I could keep up with the others easily enough. It was something I could do with friends, see myself improving at, and look forwards to each day."

    hi "I guess I didn't realise how much that meant to me, before I lost it."

    "Ah, I think I understand him a lot better now. The reason he studies so much isn't because he's some nerd, but because he wanted to fill that hole in his life."

    "That's admirable, I think. To deal with such a shock in that particular way is something I can respect."

    show suzu_sleepy_d at twoleftsit with charamove_slow
    hide suzu_asleep_d at twoleftsitlow
    show hisao_erm at tworightsit with charachange
    hide hisao_frown at tworightsit

    "Suzu begins to stir as we talk, mumbling something unintelligible as she tries to sit herself upright. The two of us just wait for her to fully wake, knowing that engaging her while she's so disoriented would be futile."

    show suzu_sleepy_d at flinch

    "After shaking her head and pinching the bridge of her nose, she appears a little more lucid."

    suz "Where...?"

    hi "Just a cafe nearby, don't worry."

    mk "Superman here managed to catch you before you fell, so you're not hurt."

    "She just nods silently, still trying to regain her senses. Where she is and whether she ended up injured should cover just about everything."

    "As if to prove me wrong, she digs around in her bag a little and retrieves her trusty mobile phone, no doubt to check how long she's been out. It wouldn't have been all that much time, so it shouldn't come as a shock."

    show suzu_embarrassed_d at twoleftsit with charamove
    hide suzu_sleepy_d at twoleftsit

    "She pauses a little after doing so, looking to Hisao with a hint of shyness."

    suz "If you want my number..."

    show hisao_declare at tworightsit with charachange
    hide hisao_erm at tworightsit

    hi "Ah, sure. May as well take it."

    "He quickly grabs his phone from his pocket and slides it across the table towards her. Her fingers make short work of the task, adding her number to his phone and vice-versa."

    "Feeling left out, I drag my old phone from my pocket as well. It might be noticeably older than either of their whizz-bang things, but it does the job."

    mk "Yo, gimme."

    show suzu_normal_d at twoleftsit with charachange
    hide suzu_embarrassed_d at twoleftsit
    show hisao_erm at tworightsit with charachange
    hide hisao_declare at tworightsit

    "Suzu glances to Hisao for confirmation, with a shrug being the answer as he busily sips his coffee."

    "With another slide his phone reaches me, and I quickly set about bringing up his contact list. It's difficult to just ignore what's right there, so I scroll a couple of times to see who he's deemed worthy before adding my own details."

    mk "Huh. You've got the student council goons in here?"

    show hisao_talk_small at tworightsit with charachange
    hide hisao_erm at tworightsit

    hi "You make that sound like a bad thing."

    mk "Well... I mean, I'm fine with them, but..."

    show suzu_neutral_d at twoleftsit with charamove
    hide suzu_normal_d at twoleftsit

    "I glance to Suzu, who evades my staring."

    mk "They can be a bit intimidating."

    hi "I suppose I can see that, but they've been a lot of help. They do take their job seriously."

    suz "That's part of the problem."

    mk "You just gotta know how to deal with 'em. Straight back, stiff lip, and tell 'em what you mean."

    hi "You're the last person I expected to defend them."

    mk "Pfft, they're fine. I can appreciate people who take their work seriously, you know."

    show hisao_biggrin at tworightsit with charachange
    hide hisao_talk_small at tworightsit

    hi "Maybe you should try doing that yourself."

    show suzu_surprised_d at twoleftsit with charachange
    hide suzu_neutral_d at twoleftsit

    "Suzu's gaze shifts to me, waiting to see my comeback. I just settle for sticking my tongue out at him."

    "With the argument headed off and his phone returned, we content ourselves with drinking and talking for a good long time."

    stop music fadeout 2.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_C7:

    scene bg school_track_running ##add running sound
    with locationchange
    play sound sfx_running loop
    play music music_miki

    window show

    "Sprinting has never been my thing. I've never managed to hype myself up for the competitive nature of the track meets, either."

    "But the act of running, of putting one foot in front of the other, that's what I've found pleasure in. I couldn't care less if other people are on the track with me or not. That isn't really the point of it."

    "As I jog around the track during lunch, I can feel my mind clearing. Some people do stuff like this to give themselves time to think, to mull things over. For me, it's the opposite. While running, I can just concentrate on the track itself, the breeze blowing past me, the sounds of the birds in the trees."

    "After everything that's happened, this is the one time I can forget it all. No more worries about school, home, or my past. Just me, and the track."

    "I give the others in the club a quick glance as I come around once more. As expected, the dozen that're here are just lazing around chatting between themselves. A few are drinking bottles of water and others are eating snacks, but all of them are on their asses. Too hot for them, probably."

    "Haru raises himself and gestures for me to join him, with Yukio nearby taking his feet also. No reason not to, so I break from the track and head over to the two."

    stop sound fadeout 0.3

    scene bg school_track
    with locationchange

    mk "Yo."

    show haru_yo at twoleft
    show yukio_smile at tworight
    with charaenter

    "He gives a wave as I slow down and walk towards them. With a long breath and a bit of a stretch, I feel the exhaustion from the run ebb away."

    har "You seen Hisao today? He hasn't shown up to club yet."

    mk "Sorry, no idea where he's gotten to. Emi hasn't dragged his ass here?"

    "Thinking back to the end of last class... I think I saw Hisao leave with the main bunch of students, but I've no idea where he went to after that."

    show haru_serious at twoleft with charamove
    hide haru_yo at twoleft
    show yukio_notimpressed at tworight with charachange
    hide yukio_smile at tworight

    "Yamagata snorts in amusement as Haru just crosses his arms and sighs."

    yuk "She's giving him the silent treatment. Think he balked at one too many of her morning runs."

    mk "That's harsh, man."

    "He just shrugs. Not much we can do about it, I suppose."

    mk "I guess one of us'll have to go on a hunt. She's gonna go nuts if she finds he's skipping club completely."

    har "He could just be studying. Exams are soon, you know."

    "He emphasises the last two words, as if Mutou busting my balls wasn't enough. He surrenders the point after the fed up glare I give him in response."

    "Each of us looks at each other, trying to come up with our best excuses to not bother. I just want to get back to running, and it's probably too hot for either of the others to be assed wandering around trying to find him."

    show haru_basic at twoleft with charamove
    hide haru_serious at twoleft

    har "The usual?"

    "We all quickly nod; it's obviously going to be the only way to decide this. Huddling together, the three of us hold our fists out in preparation."

    show haru_serious at twoleft with charamove
    hide haru_basic at twoleft

    har "Paper, scissors... rock!"

    show haru_annoyed at twoleft with charamove
    hide haru_serious at twoleft
    show yukio_huh at tworight with charachange
    hide yukio_notimpressed at tworight

    "We each throw our choices out. One scissor, one rock, and then mine. For some strange reason, the others end up looking at me with flat faces."

    mk "It's rock."

    "I waggle my stump around in the air a little before giving up on the joke. Without further ado, we pump our fists up and down for another round. This time, I throw my choice out with my right hand."

    "...Two papers against my rock. Assholes."

    "I reluctantly slink off after a sympathetic pat on the shoulder, knowing full well that my goose is cooked. Guess I'll hit the library first; where better to find a nerd studying for exams, after all?"

    stop music fadeout 0.5

    scene bg school_dormext_start
    with shorttimeskip

    "After failing to see him in the gardens leading back to the main building, poking my head into the largely empty classroom, and finding the library a bust, I make the trek back down the flights of stairs and across the school grounds to the dormitories."

    scene bg school_dormhallground
    with locationchange

    scene bg school_dormhallway
    with locationchange

    "Strolling through what should be the hallway to Hisao's dorm room, I casually glance around at the near-empty corkboards on either side. All that's there are a couple of old and tatty joke pictures, threatening to fall onto the floor."

    "It's odd to contrast with the sections of the male dorms I've seen, full of official notices, jokes, and messages to other guys in the nearby rooms. Teachers might try their best to keep the more crude ones torn down, but a few occasionally manage to stay up for an evening or two."

    play sound sfx_dooropen

    "Eventually I reach my goal, pressing the door handle and gingerly pushing in to see if it'll open. It obediently opens at my touch, giving me a wave of relief. I'd probably have just given up if he wasn't here, but at least now this wasn't all for nothing."

    scene bg school_dormhisao
    with locationchange

    "Poking my head around the now half-open door, there doesn't seem to be any sign of life inside. Maybe he's in the toilet or something, though that doesn't explain why he retreated to his dorm room during club time. With no desire to wait around bored in the hallway, I decide to step in and indulge my curiosity about what his room is like."

    "Plain. There isn't any other word for it. He did transfer in recently, but it wouldn't kill him to put something on the walls, or some toy or whatever on his desk. All that's here are a bunch of books, his computer, and a few clothes strewn about. For a guy, he's very neat. Frustratingly so."

    "After pacing around a few times out of boredom, I take a quick moment to crouch down and peek under his bed, hoping to see if he's stuffed anything embarrassing underneath."

    "Nothing, except for a couple of misplaced pieces of clothing. Disappointing. I guess he's the type to have that kind of thing on his computer, anyway."

    "It's only after getting back on my feet that I take more careful notice of his desk. Behind a couple of textbooks sits a bunch of bottles, drawing me towards them to see what they are."

    show pills with dissolve

    "Medications. I didn't think they could be, given how many there are; well over a dozen, by my count. I pick up one of the bottles to see the label more clearly, but can't divine anything from the lengthy name. '-ole', -'ine', '-ane', all the same to me. "

    "I gently put it down amongst the others as another item on his desk catches my eye."

    play music music_painful

    scene bg iwanako_letter with dissolve

    "A single piece of paper, obviously a letter sitting atop its opened envelope, adorned with sunflower decorations and cute pink writing. It's obviously to Hisao, rather than from him."

    "By the time my conscience has said to step away, my eyes have already started scanning the letter's contents. I sure wish I had handwriting as neat as this."

    "'How are you? I hope you are well and happy at your new school. Everyone here misses you.' so it's from someone at his old school. I guess the mysterious transfer student does have a past after all."

    "Blah, blah, blah. Just a status update of what's been happening in the lead-up to their set of exams. At least he still has contact with them, I suppose."

    "'The truth is, the times when I visited you at the hospital made me worried about you. I am not talking about your health. You seemed to become more and more distant and disheartened.' Well, yeah, being stuck in a hospital for a while would make you feel shitty."

    "As my eyes keep scanning the page, the penny finally drops."

    "'Now that the distance between us is also physical, it also feels more final, somehow. I wonder if we will meet again. Perhaps it's for the best if we don't?' She... wasn't just a friend, was she?"

    "Now I understand what this is. It's not some buddy writing to another about what's been happening lately. It's a break up, with a bunch of meaningless padding thrown in to distract from what she was really meaning to say."

    "I've made a mistake. I should never have seen this."

    scene bg school_dormhisao with dissolve

    "I step back to the center of the room and take a quick look towards the door, making sure I'm not being watched. My first thoughts are for my own self-preservation. Typical."

    stop music fadeout 1.5

    scene bg school_dormhallway
    with locationchange

    "Deciding that I've had quite enough my prying, I quickly retreat to the hallway outside the room, taking care to quietly close the door just as it had been. There's nothing to be gained by confessing; it's better for everyone if this just never happened."

    "The faint sound of voices catches my ear, though thankfully it sounds more like general chatter than anything directed at me. Sounds like it's coming from one of the nearby dorm rooms."

    "Whether it's out of a desire to distract myself from what I've read, or simply trying to establish an alibi if Hisao comes by, I once again I quietly poke my head through an unlocked door. This time around, I do find somebody inside."

    "Hisao stands with his back to the door, busily chatting with someone else."

    "Everything about the other guy seems a little bit off. His height is a little too short. His hair is a little too scruffy. His glasses are a little too thick. His scarf... well, that's more than just a little off, and not just given that it's summer."

    "The scrawny guy notices me over Hisao's shoulder, their conversation abruptly ending as the two of them turn to their visitor."

    mk "...'Sup?"

    show hisao_disappoint_u with dissolve

    hi "Haven't you heard of knocking?"

    play sound sfx_doorknock_soft

    "I obediently knock a few times on the door. The short guy just raises an eyebrow as Hisao sighs and motions in my direction."

    show hisao_hmpf_u with charachange

    hi "Kenji, this is Miki Miura. Miki, this is Kenji Setou."

    mk "You don't have to make it sound like you're embarrassed to know me."

    "I'm not quite sure how to interpret the awkward face he pulls. Not much point in leaving now anyway, so I wander into the room regardless."

    scene bg school_dormkenji
    with locationchange
    show hisao_erm_u at right
    show kenji_neutral at left
    with dissolve
    play music music_Out_of_the_Loop

    "Unlike Hisao's, this is a room that feels lived in. Bits and bobs that Kenji's collected over the years and brought from home are littered around the room. It's what he has hanging on the walls that particularly catches my eye."

    "I nod to a poster of the local Pacific League baseball team, nestled in a corner next to some... professional bowling posters? I didn't even know they made posters for bowling teams."

    mk "Nice taste."

    ke "You know them?"

    mk "Kinda hard not to know the locals, even if they did flunk last season."

    ke "They're still the best team. It's just their coach."

    mk "Totally. I mean, just look at how well 2005 worked out."

    show kenji_tsun at left with charachange
    hide kenji_neutral at left

    "All he does is frown a little, but I somehow get the feeling I'd have offended him less by insulting his mother."

    mk "Calm down, I follow them too. The sooner they find their groove, the better."

    "The quick save mends his attitude a little, but he still seems suspicious. Whether he knows it or not, Hisao steps in to save the day."

    show hisao_talk_small_u at right with charachange
    hide hisao_erm_u at right

    hi "I had no idea you followed baseball."

    mk "Baseball is the best sport, you know."

    hi "Huh. Play?"

    mk "Used to."

    show hisao_frown_u at right with charachange
    hide hisao_talk_small_u at right

    "Even after all these years, those two words still feel like a punch to the gut. I quickly move to hold my expression, but Hisao sees through it, going by his reaction."

    "An awkward silence follows. I shouldn't blame him, given that I was the one who brought it up. Better to just let it drop, as I feel like telling him one detail or another will make everything eventually unravel. I guess this is what they call 'baggage'."

    show kenji_neutral at left with charachange
    hide kenji_tsun at left

    ke "Do you follow bowling?"

    "This dude has no idea how thankful I am for the change in topic. Even if it is a weird one."

    mk "Bowling... I think I played that once. Is there like, a professional scene or something?"

    show kenji_tsun at left with charachange
    hide kenji_neutral at left

    "All hopes he might have had for engaging me visibly evaporate. I guess the dude puts a lot of stock in bowling."

    ke "Bowling is the best sport. Why does nobody understand this?"

    mk "Wasn't bowling more popular in the 80s or something? It's just something you do to kill time these days."

    show kenji_happy at left with charachange
    hide kenji_tsun at left

    ke "Exactly! The 80s were a golden era. All the best stuff comes from the 80s. Like bowling."

    show hisao_talk_small_u at right with charachange
    hide hisao_frown_u at right

    hi "The economy was booming back then, so maybe you have a point."

    ke "It's not just sport and the economy, either. The 80s gave all the best action movies. The most important and educational media ever made."

    show hisao_erm_u at right with charachange
    hide hisao_talk_small_u at right

    hi "I... don't think those movies were educational. At all."

    ke "They were documentaries on how to be a man, dude. They just don't make them like that anymore."

    mk "You got a point there, actually. The newer action movies are all lacking something."

    show kenji_tsun at left with charachange
    hide kenji_happy at left

    ke "I know, right? We've lost control of Hollywood. There is no hope for them now. We have to retreat and guard the homeland."

    ke "We're alone in this world. Generations will grow up not knowing what true manliness looks like, cowed by their overlords. Soon popular culture will be all chick flicks and shoujo games. Even the action movies will be made for girls."

    "I don't really get what he's on about, but a future full of girly romance movies sounds bad. I saw one once out of curiosity, and nearly threw up from the sentimentality of it. How do people watch that stuff?"

    mk "That would be terrible."

    ke "Yes, terrible."

    show kenji_happy at left with charachange
    hide kenji_tsun at left

    ke "You keep good company, Hisao. I knew I was right to rely on you."

    show hisao_disappoint_u at right with charachange
    hide hisao_erm_u at right

    "I sure said something right. He gives a thumbs-up, but Hisao looks like he'd rather be anywhere other than here right now. He hastily, and pretty blatantly, changes the subject."

    hi "What'd you want me for, anyway?"

    mk "That's... a very good question."

    mk "Oh, right. You didn't show up at club, so I came to drag your ass in."

    show hisao_frown_u at right with charachange
    hide hisao_disappoint_u at right

    "He glances to his watch, its news apparently unpleasant for him."

    hi "She's gonna eat me alive. Sorry Kenji, I gotta go."

    ke "It's cool. We can we can cover the udentstay ouncilcay akeovertay sometime later. I have visual aids and everything."

    hi "Yeah... sometime later. I'll see you around."

    stop music fadeout 2.0

    scene bg school_dormhallway
    with locationchange
    show hisao_heh_u

    "The two of us take our leave, Hisao closing the door behind us before we start down the hallway."

    mk "Seems like a cool dude. Friend?"

    hi "He's... yeah. I guess he is."

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_C8:

    scene bg suburb_konbiniext_ni
    with dissolve #shorttimeskip
    play music music_raindrops

    window show

    show haru_basic at twoleftsit
    show hisao_talk_small_u at tworightsit
    with dissolve

    "With the sun well and truly having set, Haru, Hisao, and I pass the time lazing around in front of the convenience store. The light from the store illuminates the street around us as we sit on the ground, backs propped up against the window."

    "A couple of bags sit between us, holding a late dinner of onigiri, potato croquettes, and some canned drinks. Not exactly five-star cuisine, but it's edible and filling."

    "Aside from the sound of our munching away and occasional chatter, there's little else to be heard. The bulk of school's students have retired to their dorm rooms for the evening by now, leaving us to shoot the breeze in peace."

    hi "Still surprised Yukio's not here."

    mk "Don't believe him when he says he's studying?"

    show hisao_biggrin_u at tworightsit with charachange
    hide hisao_talk_small_u at tworightsit

    hi "About as much as I'd believe you."

    mk "Dick."

    har "Leaving those two aside, I'm surprised you're not studying. You don't seem as careless as they are."

    show hisao_disappoint_u at tworightsit with charachange
    hide hisao_biggrin_u at tworightsit

    hi "I needed the break, to be honest. There's only so much I can do before I'd burn out."

    har "Sounds like you've got a good head on your shoulders."

    show hisao_smile_teeth_u at tworightsit with charachange
    hide hisao_disappoint_u at tworightsit

    "Hisao gives a grin and quick snort to pass off the praise, tucking into a drink afterwards. Praise seems to slide off him, which I've never quite understood. Why work so hard for no reward? I thought academic types lived for a pat on the head."

    show hisao_smile_u at tworightsit with charachange
    hide hisao_smile_teeth_u at tworightsit

    "Haru cares much less than I about the matter, plucking out a familiar magazine from his bag with his free hand while chomping at the onigiri held in the other."

    mk "New issue out?"

    show haru_smile at twoleftsit with charamove
    hide haru_basic at twoleftsit

    har "Yeah. Want to read after me?"

    mk "Sure."

    show hisao_talk_small_u at tworightsit with charachange
    hide hisao_smile_u at tworightsit

    hi "A defence forces magazine? Didn't know you were interested in that stuff."

    show haru_yo at twoleftsit with charamove
    hide haru_smile at twoleftsit

    har "Gotta have something to occupy myself with besides baking cakes."

    hi "You've really got your eye set on working in a bakery, don't you?"

    mk "You make that sounds like a bad thing. Having a purpose to your life is admirable, no matter what it is."

    show hisao_erm_u at tworightsit with charachange
    hide hisao_talk_small_u at tworightsit

    hi "That sounds absolutely bizarre, coming from you."

    "I can't help but glare at him. For him to say that feels like an invalidation of everything that happened before my accident."

    "But on the other side of the coin, that's the front I've been presenting to him to begin with. My dream died. It's gone. What's the point in bringing it up?"

    "Without realising it, I've begun to rub my stump once more. Thankfully, Haru fills the air with more meaningless words to try and liven things back up."

    show haru_serious at twoleftsit with charamove
    hide haru_yo at twoleftsit

    har "What about you, Hisao? You seem to have a good head on your shoulders, unlike her. Surely you have something to apply that brain to."

    show hisao_talk_small_u at tworightsit with charachange
    hide hisao_erm_u at tworightsit

    hi "To be honest, I haven't really given it much thought. Suppose I'll have to, with graduation on the horizon."

    hi "I do agree with Miki, though. It's good to have something to work towards."

    hi "Come to think of it, what are you planning on doing with yourself?"

    "I should've known that would come up."

    mk "I plan on enjoying the springtime of youth."

    show hisao_frown_u at tworightsit with charachange
    hide hisao_talk_small_u at tworightsit

    hi "In other words, nothing."

    mk "You say that like it's a bad thing. We're only young once, man."

    "He looks to the side, but finds no support from Haru. With a magazine in one hand and food in the other, he's made it clear he has no intention of getting involved."

    stop music fadeout 2.0

    "Hisao's eyes linger for a little too long, and as I follow his gaze, I see why. Even Haru looks up from his magazine after noticing the lull in the discussion."

    hide haru_serious at twoleftsit
    hide hisao_frown_u at rightrightsit
    with dissolve
    ##make girl move from left to right
    show AGirl with moveinleft

    "A girl in the Yamaku uniform comes striding up the street in the direction of school, the three of us watching her as she strolls past. Quite a pretty thing, and carries herself well."

    "Whether she's noticed our glances is answered by the flirtatious flick she gives her hair, showing a brief flash of her cute earrings. I guess that's the way the game is played."

    show AGirl
    hide AGirl with moveoutright

    "All too soon, she disappears into the night."

    show hisao_blush_u at tworightsit
    show haru_serious at twoleftsit
    with dissolve

    "With the three of us thoroughly distracted, the previous discussion is hard to return to. Hisao and I take a few more gulps of our drinks, but Haru evidently has other ideas as he takes to his feet and passes me his reading material."

    #show haru_yo at twoleftsit with charachange
    show haru_yo at twoleft with charamovefast
    hide haru_serious at twoleftsit
    play music music_running

    "Standing bolt upright and looking up the street, he looks like a man on a mission. I think I know what's gotten into his head."

    show hisao_talk_small_u at tworightsit with charachange
    hide hisao_blush_u at tworightsit

    hi "What's wrong?"

    har "Something came up. I have to go."

    mk "Go get 'em, tiger."

    hide haru_yo with moveoutright

    "He gives us a nod before heading off, running a hand through his hair before putting them in his pockets to appear as casual as he can."

    #hide hisao_talk small at right
    show hisao_smile_teeth_u at centersit with charamove
    hide hisao_talk_small_u at tworightsit

    hi "The springtime of youth, huh?"

    mk "Just as I said."

    show hisao_disappoint_u at centersit with charachange
    hide hisao_smile_teeth_u at centersit

    "With the two of us left to our own devices, I pick up the can next to me and give it a swirl to check if it's empty, Hisao digging around in the bag between us for a croquette. As he pulls one out, he makes a disappointed face."

    hi "Aww, last one."

    mk "Mine!"

    show hisao_talk_big_u at centersit with charachange
    hide hisao_disappoint_u at centersit

    hi "What? No."

    "Hisao fearfully twists to the side, clutching it with both hands as if it were a pearl or diamond. Without a second thought, I drop the magazine and can, jumping onto his back to try and snatch it from his grasp."

    show hisao_wtf_u at centersit with hpunch
    hide hisao_talk_big_u at centersit

    hi "Miki!?"

    mk "I said mine! Give it!"

    "I throw my left arm around his neck to pin myself to him as I swipe at the food, Hisao frantically holding it out as far as he can with his right hand while jabbing me repeatedly with his left elbow."

    mk "I need sustenance!"

    show hisao_talk_big_u at centersit with hpunch
    hide hisao_wtf_u at centersit

    hi "So what? I got it out! It's mine!"

    "We struggle some more as he tries in vain to throw me off, the two of us probably looking like utter idiots to any passerby. He suddenly changes tack and thrusts the croquette towards his mouth, but I manage to get an iron grip on his wrist."

    "He frantically tries to move his arm, but it's hopeless. I'm taken off guard by how little effort it takes to manhandle him, as he looked quite well built at a glance. I push further into his back and squeeze my hand to make him drop it, drawing further protests as my grip gets tighter and tighter."

    "Our growling and grunting gets louder and louder, before eventually the pain becomes too much for him. Hisao's fingers snap open with the food promptly dropping to the pavement. I quickly reach out and grab it before he has the chance, before pulling back and returning to my seat as he rubs his sore wrist."

    "The both of us take a breather after the scuffle, the conquered casting a distinct frown towards the conqueror. I don't care; I got my food."

    stop music fadeout 2.0

    show hisao_frown_u at centersit with charachange
    hide hisao_talk_big_u at centersit

    hi "That's been on the ground, you know..."

    mk "Five second rule."

    "I give it a little dusting before jamming the item into my mouth in one go. It's a bit cold by now, but still worth the effort."

    "All Hisao's left to do as I munch away is heave a sigh and deposit our bags into the nearby bin, taking care to retrieve the can I threw away and dump that in too."

    "With dinner finished, I give my stomach a hearty pat and lean back against the window. It doesn't look like Hisao has any intentions of leaving as he retakes his seat beside me, making it obvious that he still has something he wants talk about."

    mk "So, what's eating you?"

    show hisao_erm_u at centersit with  charachange
    hide hisao_frown_u at centersit
    play music music_night

    "He looks surprised that I picked up on it for a moment, but eventually acquiesces."

    hi "I'm not really sure. I guess with the summer holidays around the corner after exams, I'm just getting a bit reflective."

    hi "I've been here for a month, but still feel like the ground's moving under my feet. Stuff's just happening around me, sort of thing."

    mk "Isn't that normal? You didn't live alone before, right?"

    hi "Technically not, but both my parents worked. Spent most of my time either at practice or roaming around the city with friends, so I wasn't home much to begin with."

    "Spoke like a true urbanite."

    mk "Dude, living on your own for the first time is bloody hard. Handling laundry, feeding yourself for every meal, doing your chores out of need rather than being asked, being separated from your parents for months and sometimes years... it's a pretty huge change."

    hi "I had help, though. Shizune and Misha put themselves out for me more than once, and much as I hate to say it, you've been around too."

    mk "And what, that makes me wrong? You're living on your own, and got help when you needed it. Sounds to me like you're doing pretty well for yourself."

    mk "Even by Yamaku's standards you've been dealt a shit hand. I'm honestly pretty surprised you've managed so well, considering everything you've been through."

    show hisao_frown_u at centersit with charachange
    hide hisao_erm_u at centersit

    "His expressions drops, and after a brief moment of thought, it becomes all too obvious why."

    hi "You were in my room, weren't you?"

    "I rapidly prepare to lie me ass off, but his dead serious expression leaves me speechless. I've never seen him so stony-faced. Awkwardly shrugging is all I can do."

    mk "A bit?"

    "What am I doing, I can lie better than that. What does that even mean, anyway?"

    "Well, there's no use denying it now."

    mk "Sorry."

    mk "How did you know?"

    hi "After I take a particular pill, I turn the bottle around. Helps keep track of whether I've had my daily medications that day or not."

    mk "And I didn't put one back the right way..."

    mk "I do mean what I said, though. You've done well for yourself."

    mk "To be honest, it makes me kinda jealous. I was a real piece of work when I first entered Yamaku, but here you are, skirting death and just rolling with the punches."

    show hisao_disappoint_u at centersit with charachange
    hide hisao_frown_u at centersit

    "I leave an opening for him to ask about me, but he doesn't take it. Instead, he just looks... tired. Like an old man reflecting as his eyes slowly close."

    hi "I wonder about that."

    mk "What's wrong?"

    "He slowly shakes his dreary head, still looking at the ground."

    hi "You wouldn't understand."

    "Moments pass in silence, frustration at his sudden change in demeanor welling up."

    "He's right, of course, but that doesn't make it any easier. Hisao isn't just taking pills to suppress some medical issue or another. He's taking pills to not die. I think about how to do two things at once, or how to do up a button with one hand. He thinks about mortality and how his end might come."

    "We're eighteen. Kids. We can't even drink. That's too young to think about death. Of course I can't understand that crap, and neither can he, no matter how much he might pretend to."

    play sound sfx_clap

    stop music

    show hisao_wtf_u at centersit with vpunch

    "I end up responding the only way I know how. By hitting him around the back of his head."

    #show hisao_wtf at centersit with charachange
    hide hisao_disappoint_u at centersit

    hi "Ow! What was that for!?"

    mk "You're a real pain in the ass, you know that!?"

    mk "I thought Suzu was hard enough to deal with, and then you go and start getting all mopey. We're teenagers; we're allowed to not think about that crap."

    show hisao_smile_u at centersit with charachange
    hide hisao_wtf_u at centersit
    play music music_pearly

    "Hisao's reaction to my frustrated appearance is both simple and unexpected. He laughs. At first a simpering chuckle, but in seconds he's escalated to a deep laugh right from the chest he appears to relish my pain. I should probably find it annoying for him to laugh at my expense, but it's more of a relief."

    mk "So you can laugh. I was beginning to wonder."

    hi "I was just thinking about how ridiculously blunt you are. You don't know the meaning of tact, do you?"

    hi "But that's fine. I like that about you."

    "All I can do is smile and give a halfhearted shrug at the compliment, and a bit out of relief that he didn't take too much offense. Hisao seems the type to appreciate honesty, after all, even if it is delivered in a frank way."

    hi "This is probably going to get me beaten, but... it's honestly hard to think of you as a girl. You certainly don't act like any I've been around."

    mk "Believe me, I've heard that more than once."

    hi "You don't mind?"

    mk "Couldn't care less. People can think what they like, doesn't harm me."

    hi "You're pretty weird, you know."

    mk "I don't want to hear that from you."

    #show hisao_smile at centersit
    with vpunch

    "I hit him around the back of his head with my stump, drawing another chuckle from him. I can't help but get caught up in it, launching into laughter myself."

    "Maybe it's from how curious a person Hisao is, the both of us laughing off such morbid thoughts of mortality and death, or simply two overly tired people getting caught up in the stresses of exams and school life..."

    "But in any case, the both of us end up laughing together for a good, long while."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_C9:

    scene bg school_scienceroom
    with locationchange
    show suzu_asleep at oneleftsitlow
    with charaenter

    window show

    play sound sfx_normalbell

    play music music_tranquil fadein 3.0

    "The ringing of the school bell heralds the end of yet another school day."

    "With the exams finally over and the wait until summer break down to days rather than weeks, the mood of the class has lifted immeasurably. Even for those that don't care particularly about their marks, the stress felt by everyone else is contagious."

    "Even Mutou looks a little more sedate, and he hasn't been quite as hard on me as he usually is. He wastes little time in declaring an end to the class and beginning to clean up his desk, knowing full well that trying to teach us any further would be futile."

    "I can't help but relish the sound of the class as people put away their things and begin to chat amongst themselves. Books, hobbies, movies, music, they talk about all the usual wastes of time students would be into, released from the Hell of algebra and physics."

    "As some hang around to gossip and others skip out into the hall to make phone calls and check their messages, I hop up onto my desk with practiced ease."

    "Looks like I might be here a while, so I might as well make myself comfortable. With her head on its side resting in her arms, Suzu silently sleeps away as people move around her table paying her little heed. I used to think it painfully cute, but it's become a wholly normal sight nowadays."

    "My vision of her is momentarily broke as Hanako skitters past me to the door, the blonde Amazon waiting for her outside as she so often is. Least she has someone to attach herself to, I suppose. There are worse lives than that of a limpet."

    "The main attraction finally makes his way towards me, having carefully gone over his notes and finally packed his stuff away."

    show hisao_smile_u at rightedge with moveinright

    mk "Nerd."

    hi "Uh huh. So how well did you do in your exams?"

    mk "Fine."

    mk "...Probably."

    show hisao_erm_u at rightedge with charachange
    hide hisao_smile_u at rightedge

    "Hisao just grimaces before briefly looking to the slumbering girl ahead of me."

    "It's been interesting to watch him slowly become more used to Yamaku's oddities, with the way he treats Suzu perhaps being the clearest sign of it. Her falling asleep or having cataplexy attacks is just a thing that happens, and all you can do is make sure she doesn't hurt herself."

    "But it isn't just her he treats that way. On the track he casually talks with the others from the club, and he occasionally helps out the student council without confusion over whether to address the impossibly busty taskmaster or her ever-bubbly accomplice."

    "He's standing on his own two feet as a member of the class, now. I take a small amount of satisfaction from that, even if my help might not have been much in the scheme of things."

    show hisao_talk_small_u at rightedge with charachange
    hide hisao_erm_u at rightedge

    hi "How'd Suzu do, anyway? She seems to study hard enough."

    mk "Some people have to try harder than others, unfortunately."

    hi "She just finds it hard, or what?"

    mk "It's not that. She's got a pretty good brain up there, actually."

    mk "How would you do in school if you always felt as tired as she does, though? Plus there are the classes she accidentally naps through."

    show hisao_hmpf_u at rightedge with charachange
    hide hisao_talk_small_u at rightedge

    hi "That's a good point."

    "As the conversation lulls, a glance aroud the classroom proves we're the last ones here. I wonder when Mutou managed to slip out so quietly."

    show hisao_talk_small_u at rightedge with charachange
    hide hisao_hmpf_u at rightedge

    hi "So what're your plans for the holidays?"

    mk "Just messin' about at Suzu's place. Pretty nearby, and there's a beach and everything. You?"

    hi "Going home, I guess."

    mk "Catching up with friends and all that, yeah?"

    show hisao_erm_u at rightedge with charachange
    hide hisao_talk_small_u at rightedge

    hi "I don't really have any left there. Beyond meeting my mother and father, I don't really know what I'll do."

    "Hisao has a habit of delivering difficult news with a terribly stilted smile. I can't help but feel a little bit of pity for him, despite how little he may want that. He might do well in class, but I'd know better than most how school isn't everything."

    "An idea forms in my head, which only seems better the more I think about it."

    mk "Hey, why don't you come with me to Suzu's!?"

    show hisao_disappoint_u at rightedge with charachange
    hide hisao_erm_u at rightedge

    hi "You sure about that? I'm not even sure she likes me."

    mk "Believe me, she's cool with you. It'll be fun, don't worry about it so much!"

    show hisao_erm_u at rightedge with charachange
    hide hisao_disappoint_u at rightedge

    hi "If she's okay with it..."

    mk "C'mon man, lighten up. You survived exams, now's your time to enjoy yourself."

    mk "Besides, shouldn't a man be pleased to spend a summer with two girls? We could do this, and we could do that..."

    "He tries his best not to look interested as I wildly grin and move my hand suggestively."

    stop music fadeout 2.0

    ##move hisao left next to suzu, move yukio and haru in from right
    show hisao_erm_u at leftoff with charamove
    show yukio_notimpressed at oneright with moveinright
    show haru_sad at rightedge with moveinright

    yuk "You shouldn't talk like that, Miki; people might think you're serious. Especially with you being you."

    "Haru's eyes flit to the side for just a second. I just smirk before addressing Yukio."

    mk "Who says I'm joking?"

    yuk "You're not seriously thinking of hanging out with this loser, are you?"

    show hisao_talk_small_u at leftoff with charachange
    hide hisao_erm_u at leftoff

    hi "I don't see anything wrong with the offer."

    show haru_serious at rightedge with charamove
    hide haru_sad at rightedge

    har "I'll keep an eye on the obituaries."

    hi "Come on, she's not that rough is she?"

    show haru_sad at rightedge with charamove
    hide haru_serious at rightedge

    "Yukio and Haru both snort, shaking his head and looking away respectively. All I do is give a flat face, but the possibility of them telling him is there. Hisao doesn't seem the type to hold a grudge, especially after his forgiving me for poking around his room, but he equally seems concerned for those weaker than he."

    play music music_tension

    "It's only now that Yukio notices Suzu in front of me, walking past my desk to get closer. He reaches out towards her, but I quickly intervene."

    mk "Oi, hands off."

    show yukio_angry at oneright with charachange
    hide yukio_notimpressed at oneright

    yuk "Since when were you in charge of her?"

    "I think Hisao's getting a sense of when Yukio and I are about to start going off at one another; he quickly steps in before things escalate once again, making his friend - however reluctantly - back away from Suzu."

    show hisao_disappoint_u at leftoff with charachange
    hide hisao_talk_small_u at leftoff

    stop music fadeout 0.5

    hi "So uh, I'm guessing you guys came for a reason?"

    show haru_smile at rightedge with charamove
    hide haru_sad at rightedge
    show yukio_huh at oneright with charachange
    hide yukio_angry at oneright

    har "Just wanted to see if you lot wanted to come to the Shanghai with us."

    show hisao_smile_u at leftoff with charachange
    hide hisao_disappoint_u at leftoff

    hi "Don't see why not. Miki?"

    mk "I'll stay here, go on and have your fun."

    show hisao_frown_u at leftoff with charachange
    hide hisao_smile_u at leftoff

    hi "But..."

    mk "It's fine! See you guys tomorrow."

    hide hisao_frown_u with moveoutright
    hide yukio_huh with moveoutright
    hide haru_smile with moveoutright

    "Hisao doesn't look pleased with the idea of leaving a comrade behind, but Yukio swings an arm around his neck and drags him out with he and Haru. I give an unseen wave as they leave the classroom, before turning back to my charge."

    "And so, the classroom goes quiet. All I'm left to do is idly gaze out the window."

    play music music_ah

    mk "Summer holidays..."

    "The words roll off my tongue with ease. I'm excited for them... I think. I know I've been looking forward to them, that's for sure. The topic's been on my mind for a good long time. Now that they're actually here, though, I can't quite pin down my feelings about them."

    "Maybe it's less the holidays themselves giving me cold feet, so much as what they signify. This is the last summer holiday before we graduate high school, after all."

    "I should be happy with how things are right now. My carefree days with Suzu, Haru, Hisao, Yukio, and the other guys in track club and class have been some of the best I've had since the accident, after all."

    "But those days will be over in a few months."

    "A movement from Suzu's desk catches my attention, the girl finally stirring from her long nap."

    show suzu_sleepy at oneleftsit with charamove
    hide suzu_asleep at oneleftsitlow

    "Blinking heavily and obviously still dazed, she picks herself up a little and groggily glances around while still half-asleep. It's only after scanning the room that she catches sight of my legs, following them up to my gently grinning face."

    "She simply turns to look out the window as I'd been before. Maybe she's still disoriented from her sleeping, apathetic towards my presence, or simply has nothing to say. In any case, she doesn't bother to say a word as she gazes at the bright summer scene outside, head resting in her hand as always."

    "I should be annoyed with her apathy for my sticking around here for her sake, but I can't even pretend to be. Maybe this is what it's like to be a doting parent, forgiving their daughter's impoliteness as lovable quirks. The more simple answer is that I'm just used to being treated like this by her."

    "I wonder what she'll do with her life. Suzu's terribly shy, but that isn't unheard of; it's not like she's anywhere near Ikezawa's level. She's never expressed any kind of ambition though, nor does she have any particular talents beyond a good work ethic."

    mk "You know how I'm coming over to your place for the holidays, right?"

    show suzu_concerned at oneleftsit with charachange
    hide suzu_sleepy at oneleftsit

    suz "Yes?"

    mk "I kinda invited Hisao."

    show suzu_neutral at oneleftsit with charamove
    hide suzu_concerned at oneleftsit

    "Suzu just sighs. She briefly turns back to check my reaction, before going to looking outside. I can't even read her expression like this."

    suz "I guess it's fine."

    mk "Yay! It'll be great, I promise. He's a cool dude."

    suz "Is that really why you invited him?"

    mk "How do you mean?"

    suz "He doesn't like being pitied. Nobody does."

    "She really knows how to put me in my place, sometimes."

    "Is it really that bad to try and do the right thing by someone, though? I just want to make him happy, just like I want Suzu, Haru, and Yukio to be happy. That's normal for friends, right?"

    mk "Don't worry about it. Summer holidays are for relaxing, remember? We should make the most of them while they last."

    suz "'While they last'..."

    "Ah, I see now. She's been pondering the same things I have."

    "It pains me a little how I can't give her any advice on the matter. If I could find any answers, I'd give them."

    "All I can do is stay beside her as I've always done. Given that she's stayed at my side all this time, she must think the same."

    stop music fadeout 1.0

    scene bg school_girlsdormhall
    with shorttimeskip

    "I give a quick nod to a passing first-year girl as I make my way back to my dormitory room, my hand occupied by a soft drink can. She returns the greeting as we pass, her eyes momentarily lingering on the arms bared by my tank top before we pass each other. At least that's one thing I can be proud of."

    "Another girl stands not far from my room, leaning against the wall and tapping away frantically on her phone. I might as well have not existed for all the attention she gives me as I pass by her and enter my dorm room, closing the door with a push from my foot."

    scene bg school_dormmiki
    with locationchange
    queue sound [ sfx_sitting, sfx_rustling, sfx_can ]
    play music music_miki

    "The bed gives a soft thump as I fall onto it, sitting up and opening the can afterwards."

    "I try to focus on things I need to do, such as packing a bag for my outing to Suzu's, but I can't get my mind off what I was pondering earlier."

    "Nothing lasts forever. If I've learned anything in my life, that'd be it. That's not inherently a good or bad thing; it just is. Might as well ask why winters are cold and summers are hot."

    play sound sfx_impact

    "I give the upturned cardboard box in the center of my room - a makeshift table that ended up just the right size for the job - a kick out of boredom. My aging phone falls off with a clunk, but I'm hardly worried; the thing's practically indestructible, which has been proven many times over."

    "Some of us will go on to great universities, others to menial jobs, and a few will go into family businesses. Most of the students here have long stories ahead of them, of which high school is but one small chapter. For me, graduation is as final as the period at the end of a sentence."

    "They might not say it, but I suspect the same thing has run through the minds of Suzu and Hisao. Yukio and Haru have their futures planned out, as a politician and baker respectively. The other two, not so much."

    "But I'm sure they'll both be fine. They're both good people, and know how to work hard once their hearts are set to a task. I had my shot, and I blew it."

    "Eventually, our carefree days will end. These summer holidays will be our last distraction from that looming future."

    play sound sfx_cellphone

    "A sudden ringing breaks me from my thoughts. Setting the can on the corner of my desk, I hurriedly got off the bed and scavenge the noisy phone from the floor as it skitters about vibrating away."

    show phone

    "The number on the display is instantly recognisable."

    mk "Hi, dad."

    "I always feel like I'm on tenterhooks when I talk to him like this. Not at all when I'm talking to him face to face, but something about yakking away to a disembodied voice always put me off."

    "His deep voice is warm and boisterous as always, and entirely too loud for what's appropriate over the phone."

    jun "Miki! What'd I tell ya 'bout callin' me sometimes?"

    mk "I know, I know. It's just been busy."

    jun "Ah, exams, right? I hope you've done better than last year's effort."

    mk "So what's going on?"

    "Yeah, real smooth. I bet he didn't catch that diversion at all."

    "Thankfully, he just grumbles a bit before moving on. I'll get an earful once the results come in, no doubt."

    jun "Just wonderin' if you wanted to come up here. Finally got some of the rooms cleared, so we actually 'ave some space if you want to bring anyone."

    "Thinking back, a good half of the house has tended to be a complete mess. Since we never used the rooms, they ended up filled with this and that and rarely ever even dusted, let alone properly organised."

    "A summer at home. I've already made arrangements with Suzu, but I could probably twist her arm into coming with me. Same goes for Hisao."

    "It's been so long since I've been there. Simply no point, really; it's quite some way from here to travel, and beyond my father, there was nobody to meet or play with. If I had Hisao and Suzu for company, though, it might not be so boring."

    "But I'd agreed to go to Suzu's, which has always been a fun experience. An opportunity to show Hisao the country, though..."

    # Choice point

    window hide

    ##return


menu:
    #with menueffect
    "Follow existing plan.":
        jump SuzuRoute

    "Agree to go.":
        jump HisaoRoute

label SuzuRoute:
    # Follow existing plan

    window show
    "As much as the idea may tempt me, I told Suzu that I'd stay with her family."

    mk "I kinda already promised Suzuki I'd stay with her. Sorry."

    jun "Don't worry! Long as you're spendin' the time with someone, it's fine! Drop around at some point, though. It's been too long since I've seen you."

    mk "I will, don't worry. I'll give you a call later, okay?"

    jun "Just take it easy, Miki. I love you."

    mk "I know. I love you too."

    "I hate saying that over the phone."

    jun "And your exam result had better be better than you last ones, you hear me?"

    "All that can be heard afterwards is the phone's beeping."

    "Son of a bitch."

    # Continue onto Suzu branch
    window hide
    ##return

label en_S1:

    ##start with suzu route chapter card
    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(sfx_tcard)
    show neutral with fade
    show act2suzu with passingactsuzu
    $renpy.pause(10.0)
    $renpy.music.stop(fadeout=2.0)

    scene bg school_track with dissolve

    play music music_miki

    window show

    "With classes over for the day and most club activities winding up for the semester, the long process of pre-holiday cleanup has begun. With most of the track club members having fled using various terrible excuses, a half dozen of us are left to finish the job."

    "That said, we make good progress even with the reduced manpower. A couple of students are dedicated to organising the mess in the storage shed, and another to fossicking around for litter. Equipment collection duty ended up assigned to Hisao, Haru, and I, though I can't remember agreeing to it."

    show haru_conehead with charaenter

    mk "Haru, stop being a moron."

    har "Hmph. Kids these days just don't understand good fashion."

    hide haru_conehead with moveoutright

    "He reluctantly plucks the large orange cone off his head after pouting a little, stacking it on top of the others before picking them up and heading for the shed. Satisfied that he's pulling his weight, I reach down to grab another running block off the track. It's dull work, but the sooner we get it done, the sooner we can leave."

    "With Hisao being so uptight, I'm surprised he didn't call Haru out. Righting myself and slipping the block into the bundle held in the crook of my other arm, I glance around to check what he's up to."

    "I'd expected him to be distracted with his own work, but instead, he stands a good few yards away bouncing a soccer ball he's found on his head. Doesn't look half bad at it, either. Occasionally he tilts his head this way or that, sometimes bouncing the ball on his shoulder or foot, but he never seems to need much concentration to do so."

    "Rather than yell at him to cut it out, I decide to let him be. He deserves what little enjoyment he can still get from his old hobby, even if he can't play for real anymore."

    suz "He's enjoying himself."

    stop music

    with hpunch

    mk "Woah!"

    "I nearly drop my whole bundle in startlement at the voice suddenly piping up to my right."

    show suzu_neutral at right with moveinright

    "The girl simply stands there looking at Hisao with her usual disinterested face, barely acknowledging the jump she's given me."

    "Wait... has she been waiting until I was alone to approach me? Her timing sure feels coincidental."

    play music music_suzu

    mk "What's up?"

    suz "Just bored. I see you're keeping yourself busy."

    mk "There was something I wanted to tell you, though. Dad invited me home to spend the holidays."

    suz "Are you going?"

    "I just shrug."

    mk "Might've been funny to see how Hisao dealt with country life, but nah."

    show suzu_normal at right with charamove
    hide suzu_neutral at right

    suz "It's not like you to pass up a chance to tease him."

    mk "Oh no, I've been caught out."

    mk "But seriously, I like going to your place. It's our last summer holiday together, so I wanted to spend it with you and your family."

    "Though that brings the question of what I'll do afterwards. I'm sure as hell not taking up the family business, but I'd get eaten alive trying to enter any of the bigger universities."

    "Suzu's marks might not be fantastic, but she's bull-headed enough to have a good chance at the exams. Hisao... well, he'd probably do fine no matter which university he tried for."

    "The boy himself finally notices our staring, dropping the soccer ball and kicking it towards the shed before walking over."

    show hisao_smile_u at twoleft with moveinleft

    hi "Hey, Suzu."

    hi "I can take some of those if you need a rest."

    mk "C'mon, who do you take me for?"

    stop music fadeout 1.0

    play music music_Out_of_the_Loop

    ##lift up suzu's sprite a bit if possible?
    show suzu_angry at right with charachange
    hide suzu_normal at right
    show suzu_angry_lift at oneright with charamove_slow
    hide suzu_angry at right

    "I reach beside me and firmly grab Suzu's blouse, hand gripping the back of the neck. With a slight grunt I pull my arm upward, the slight girl following."

    "The act is made a little harder than usual thanks to her being beside me, but I manage to get her a good couple of inches off the ground, her feet hovering in the air. Being a little short and having no muscle to speak of, her low weight makes Suzu easier to manhandle than some weights I use."

    #hide suzu_normal at right
    #show suzu_angry at right

    "Her head just hangs drearily, with no effort on her behalf to try and escape from my grasp. Given the difference in our strengths, even with one of my arms occupied, she knows all it'd do is make this look more ridiculous."

    mk "See? Still good to go."

    show hisao_erm_u at twoleft with charachange
    hide hisao_smile_u at twoleft

    hi "Are you really okay with her doing this to you, Suzu?"

    #hide suzu_angry at right
    #show suzu_concerned at right

    suz "You get used to it."

    "Hisao just sighs. If she really didn't like it, I'm sure she'd say so. Perhaps she enjoys being my plaything from time to time, given that it's one of the few things we can do together."

    "That might be wishful thinking, though."

    show suzu_concerned at oneright with charamove_slow
    hide suzu_angry_lift at tworight
    #hide suzu_concerned at right
    #show suzu_concerned at center with move
    show haru_annoyed at rightedge with moveinright

    #stop music fadeout 1.0

    "Haru emerges from the shed and begins to head over, with Suzu beginning to swing her legs as he does. Taking my cue, I gently lower her back down to the ground. Other than adjusting her uniform back to her liking, she doesn't seem perturbed."

    har "You're going off at me about not working, and here you lot are horsing around."

    "He's not very good at feigning frustration, but that's more due to his personality than ability in acting. He's the type that's hard to imagine being angry, or even particularly serious, towards anyone."

    show hisao_talk_small_u at twoleft with charachange
    hide hisao_erm_u at twoleft

    hi "Fine, I'm going. Miki?"

    mk "Yeah, I-{w=.25}{nw}"

    stop music

    suz "I have business with her."

    "Suzu's sharp rebuke takes us all off guard. It's odd to hear such an authoritative tone out of her."

    "Shrugging in deference to her instructions, I pass the bundle of running blocks to Hisao before leaving with her. Neither of the two seem to mind as they get back to work with the others."

    scene bg school_road with shorttimeskip

    #centered "~ Timeskip ~" with dissolve

    play music music_daily

    show suzu_concerned

    "A mighty yawn rings out as we descend down the hill into town, a good stretch loosening up my muscles a bit."

    suz "Tired?"

    mk "Just bored as shit. Thanks for bailing me out, there."

    show suzu_smile with charachange
    hide suzu_concerned

    suz "You only agreed to get out of work, didn't you?"

    mk "Duh."

    suz "You have the worst work ethic."

    mk "Least I'm not a terrible person like you are."

    show suzu_surprised with charamove
    hide suzu_smile

    suz "Where did that come from?"

    mk "I was thinking about what you said about Hisao. How I only invited him out of pity."

    suz "Isn't it true?"

    mk "No, and I think that the fact you think so says more about you than me."

    mk "You gotta stop being so cynical about people. Sometimes others do have their fellow man's best interests in mind."

    mk "Maybe this kind of thing is why you don't get more people hanging around you."

    show suzu_angry with charamove
    hide suzu_surprised

    "Rather than protesting the point, she simply sighs and turns away. I don't really get it; she usually doesn't mind when I take a harsh tone with her."

    "That said, I'm not willing to retreat from the point, either. After we graduate, she isn't going to be able to rely on my company. Hisao was a first good step out of her comfort zone, but that isn't enough."

    stop music fadeout 1.0

    scene bg suburb_shanghaiint with shorttimeskip

    #centered "~ Timeskip ~" with dissolve

    #show yuuko bow
    show suzu_unhappy at centersit with dissolve
    show yuukoshang_happy_down at left
    show yuukoshang_happy_down at leftsit with charamovefast
    show yuukoshang_happy_down at left with charamovefast
    hide yuukoshang_happy_down with moveoutleft

    "With a deep bow, Yuuko takes her leave after setting down our drinks. A coffee for me, and tea for Suzu."

    "After that conversation, there wasn't really much for us to say to each other, the rest of the walk down being in silence. Unusually, it's her who speaks first."

    play music music_friendship

    suz "Do you really think I'm a bad person?"

    "So she was dwelling on that comment. I suppose it is normal to be wounded by such a comment."

    mk "Don't look at me like that..."

    mk "Look, maybe I was using a little bit of hyperbole. I like hanging with you, don't get me wrong, but you have to learn to trust others."

    suz "I got used to Hisao."

    mk "That's good, but you need to do more. Be more proactive. Put yourself out there."

    suz "You make it sound so easy."

    mk "It is! People aren't hard. It's like a snowball; once you talk to a couple of new people, you'll get more used to it and strike up conservation with a few others. Keep that going, and you'll be fine with talking to whoever you bump into."

    mk "There's a whole world of people out there, Suzu. So what if you've had to deal with a few assholes, just move on and change the crowd you hang with."

    suz "What if I'm fine with the crowd I have now?"

    "Struck out by her monotone reply, I fall back and scratch my head to try and work out a new approach."

    "We really are two totally different people. She knows Hisao, and she knows me. Two people. How can anyone be happy with that number of friends? How can you just shut yourself off from a whole world of other new and interesting people, each with their own life story, interests, and personalities?"

    "Introverts are weird. Time and time again, this girl reminds me of that fact."

    "Exasperated, I throw my hand up in surrender and let it fall on the table."

    mk "So what's up, anyway? It's not like you to grab me out of the blue."

    show suzu_speak at centersit with charachange
    hide suzu_unhappy at centersit
    pause(0.5)
    show suzu_unhappy at centersit with charachange

    stop music fadeout 2.0

    "She moves to speak, but quickly brings her hand to her mouth in order to more carefully consider her words. I wonder if she's picking that habit up from Hisao."

    "Before long, she places both hands in her lap and forces out what she wants to say."

    show suzu_veryembarrassed at centersit with charachange

    play music music_heart

    suz "You might have helped me find words for this."

    suz "You said I should be more proactive, right?"

    "Oh, she's going to suggest something? I quickly lean forwards in interest, but her upper body moves back as far as my face has moved forwards."

    show suzu_unhappy at centersit with charachange
    hide suzu_veryembarrassed at centersit

    "As if I'd stolen the words from her lips, she suddenly goes silent once more."

    mk "C'mon, what is it? Tell me! Tell me!"

    show suzu_veryembarrassed at centersit with charachange
    hide suzu_unhappy at centersit

    suz "You're like a child..."

    "I grin in full agreement. All it does is make her quickly turn away. Something's with her today."

    suz "Just... put your arms out in front of you."

    "Without any reason not to, I obediently do as she asks. My hand lies palm-down on the table, with my stump laying beside it. I'd probably feel a bit antsy about people staring like this, if there were anyone hovering around."

    mk "Okay, now...?"

    suz "Now close your eyes."

    mk "What?"

    suz "Just do it."

    "She's starting to look flustered. Given what she's telling me to do, shouldn't I be the one feeling put off?"

    scene black with shuteyemed

    "Regardless, I give a sigh and close my eyelids. She's not the type to pull magic tricks, nor the type to do a dumb prank, so all I can do is wait for whatever's coming in darkness."

    "Seconds pass. The Shanghai's pretty quiet today, now that I think of it."

    "A long, shaky breath comes from before me. One soft hand presses to the top of my own, and the tips of her other fingers settle on my stump."

    suz "...Don't make me regret this."

    "Regret what? What's she planning to-{w=.35}{nw}"

    scene bg suburb_shanghaiint with openeye_shock

    "My eyes flash open in shock as realisation dawns on me, but it's far too late."

    scene bg 4265edited with dissolve

    "A set of lips press to mine, soft and trembling. Suzu's body cranes over the table to reach me, her own eyes closed as she presses her mouth to mine."

    scene black with shuteye

    "All I can do is close my eyes in response."

    "My heart stops. Everything around us falls away. Even my feelings of shock and startlement seem to disappear. My mind is emptied, save for the feeling of those lips pressed to mine."

    "I don't know what I'm supposed to say, or what to do. All I know, is that the life I, no, we, had led until just a few minutes ago... has disappeared forever."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_S2:

    scene bg school_scienceroom with dissolve

    window show

    play music music_caged_heart

    "I wonder how long it's been since Suzu missed a class. At least a good few months, I think."

    "Carefully scheduled naps, along with her meds, allow her to drag her feet to class every morning. Even if she sometimes doesn't quite last out the whole day, she makes damned sure she's at least present and accounted for."

    "But that's Suzu all over; she tries hard at every little thing she does. I've no doubt that it makes me look a lot worse in comparison, though to be fair, I've been skipping class pretty rarely in the last year."

    "Mutou drones on with yet another lecture, but even as we scrawl in our notebooks, it's obvious people's minds are elsewhere. It's the last day of the semester, after all. I can't help but glance over at the empty desk beside mine every now and again, as if she might suddenly be there the next time I look."

    "Why she's missing is hardly a mystery. I get a knot in my stomach just thinking about how it happened, and it must no doubt be much worse for her. Suzu might be stubborn as a mule, but even she has her breaking point."

    $ renpy.music.set_volume(0.4, 0.0, channel="sound")
    play sound sfx_normalbell

    "I barely even register the bell signalling the start of lunch, only beginning to shuffle out of the classroom as I see the other students moving past me."

    scene bg school_hallway3 with locationchange

    "Filing into the hallway with those who'd rather escape the stuffy room rather than chat and eat at their desks, the thought of what I should eat floats vaguely into my mind. Bread, I suppose. Cheap, and I could easily force it down."

    "A hand grabs my shoulder, gentle, but firm. I turn to face its owner, but I know who it is without even looking."

    show hisao_smile_u with charaenter

    hi "Hey."

    show hisao_frown_u with charachange
    hide hisao_smile_u

    "His expression, a thoughtful but carefully rehearsed cheerfulness, is the norm for him. It drops the moment he sees my face, the dots all too easy to connect."

    hi "Are you okay?"

    mk "I'm fine, I just... didn't get much sleep last night."

    "I scrunch up my face and pinch the bridge of my nose, trying to pull myself together. This is the result of just one night's bad sleeping; I can't imagine the kind of sleep deprivation Suzu must feel every day."

    "As I look back at Hisao, I can see he wants to say something but doesn't quite have the will to do so. He's a nice enough person, but the way he so often visibly thinks things over before speaking irritates me."

    mk "What is it?"

    hi "...Come with me."

    stop music fadeout 1.0

    scene bg school_cafeteria with shorttimeskip

    play music music_fripperies

    #centered "~ Timeskip ~" with dissolve

    "The cafeteria is humming with activity already, but the two of us thankfully managed to score a free table by getting in before the rush."

    "While Hisao farts around getting food for the both of us, I try to work out what he knows, and what he doesn't."

    "I wouldn't call him an idiot, but Hisao isn't particularly sharp when it comes to others. That said, he and Suzu have been around each other a fair bit lately. Not that she's the talkative type anyway, even with her friends."

    "He's far from the assertive type, too, yet dragged me here of his own accord. There's no doubt about it; The way Hisao's acting today is out of character. I shouldn't be so immediately suspicious, but..."

    show hisao_erm_u with charaenter

    hi "Here."

    show hisao_erm_u at centersit with charamove

    "He sits a juice box and a large piece of bread in a wrapper on the table in front of me. Mangling the thin plastic before finally getting it open with my hand and teeth as he takes a seat, I shovel the bland-tasting bread into my mouth for simple nourishment."

    "I hadn't realised just how hungry I'd gotten, the food almost evaporating as I take mouthful after mouthful."

    "Looking to Hisao, he's stopped as he was about to start on his own, instead opting to watch me pigging out. Whether it's in amusement or startlement, I can't say."

    "I rip off a large chunk of bread before forcefully swallowing it and setting the rest down, my curiosity getting the better of my hunger."

    mk "So, what'd you drag me all the way here for?"

    show hisao_disappoint_u at centersit with charachange
    hide hisao_erm_u at centersit

    hi "I was just wondering if you knew why Suzu wasn't in class today. And why you're in such a state, now that I've seen you."

    "I take a long breath as I think back to when it all happened. I have to tell him, as much for my sake as his."

    "I quickly glance around me to make sure nobody's listening in."

    mk "Can you promise not to tell anybody about this?"

    hi "I promise."

    "Anyone would say that. I believe Hisao more than most, though."

    mk "Suzu..."

    mk "Suzu confessed to me yesterday."

    show hisao_declare_u at centersit with charachange
    hide hisao_disappoint_u at centersit

    "He lets out a long, drawn-out breath, almost seeming to deflate as he sits back and stares at the table ahead of him. It takes him a while to formulate a response beyond scratching the back of his head. I can't blame him."

    show hisao_disappoint_u at centersit with charachange
    hide hisao_declare_u at centersit

    hi "I wouldn't have picked it. The fact that she..."

    mk "Yeah. I didn't know either."

    "We both sit in silence for a bit to mull over our interactions with her. Sure, she never came out to either of us, but she's a private person about practically everything. She's distrustful of others, too, though not without reason."

    "It's impossible to work out whether she was dropping hints, or actively trying to hide it. Let alone whether she was hiding it because she feared our reactions, was worried about word getting out, or was simply confused herself."

    "In any case, she never told me, and obviously didn't tell Hisao. She doesn't talk with anybody beyond us, so the next question is how long did she keep this bottled up inside of her?"

    "Hisao is the first to speak, breaking my train of thought."

    hi "How did you react?"

    mk "I... I guess I didn't."

    show hisao_talk_big_u at centersit with charachange
    hide hisao_disappoint_u at centersit

    hi "Huh?"

    mk "I just mumbled how we should get back to school, and the two of us walked back. That's all that happened."

    show hisao_erm_u at centersit with charachange
    hide hisao_talk_big_u at centersit

    hi "Miki..."

    mk "I was confused, alright!?"

    mk "I had no idea that was coming! I didn't even know she-!{w=.55}{nw}"

    "Hisao quickly waves his hand downwards to make me lower my volume. I quickly do so."

    mk "I didn't even know she liked girls, man. We've been friends for over a year, and I never had a bloody clue."

    mk "I thought things were going well, and now everything's completely messed up..."

    "Here I was thinking I'd managed to keep my emotions under control, but even as I speak, I can feel a lump forming in my throat. It's one thing to mull all this over in my head, but saying it to someone else is a lot harder."

    mk "What am I meant to do?"

    show hisao_talk_small_u at centersit with charachange
    hide hisao_erm_u at centersit

    hi "To be honest, I'm not really sure. You do need to answer her, at least."

    hi "Please don't take this the wrong way, but: are you scared of giving her an answer because you're confused about your feelings, or because you don't want to hurt Suzu by rejecting her?"

    mk "The first."

    "He gives a nod, satisfied with the answer."

    show hisao_erm_u at centersit with charachange
    hide hisao_talk_small_u at centersit

    hi "I guess being the same gender does make that harder. It's not really a position I'd want to be in."

    mk "It's not really that. How should I put this... there's a difference between getting off on that kind of stuff, and a relationship."

    mk "I mean, I like looking at girls as well as guys. I can appreciate a girl's body, you know? But that's pretty different to this."

    mk "I'd a lot less freaked out if it was anybody but Suzu, to be honest. It's like everything I knew just got turned upside down."

    "I think to myself about what I'd just said. I think I'm happy with that explanation. Hisao nods as though he understands, but that's only half the story."

    "Why would Suzu be interested in me, after all? So she's into girls, sure. A surprise, but plenty of people out there are. Why me, though? She isn't like Hisao; she's known me at my worst, not just as I am now."

    "It's just baffling on every level."

    hi "I know this isn't what you want to hear, but I'm pretty sure I'm not going to be much help with this. I don't envy you, that's for sure."

    hi "But in a way... what you're saying makes me kind of glad."

    mk "I'm glad someone's happy."

    hi "It's just good that you're thinking this through. I don't think it's controversial that you can be pretty rash sometimes."

    mk "Prick."

    show hisao_smile_u at centersit with charachange
    hide hisao_erm_u at centersit

    "We both smile, deciding to move on. He's not wrong that he'll be of little help in my decision, but just getting this off my chest has helped a lot. With the shock wearing off, it's easier to think clearly about everything."

    hi "Are you still on for visiting Suzu's home during the holidays?"

    "I briefly think before giving a shrug. Neither of us said anything about the visit being cancelled or otherwise."

    mk "I guess so?"

    show hisao_talk_small_u at centersit with charachange
    hide hisao_smile_u at centersit

    hi "Then you're going to need this sorted out by then. Holidays start tomorrow, and Suzu deserves an answer."

    mk "I know, I know."

    "A deadline would help, now that I think of it. Something to force me into making a decision. I carefully go through the year's events and holidays in my head, soon coming to one that'd be perfect."

    mk "Tanabata's soon, right?"

    mk "Yeah, I'll have an answer by Tanabata."

    show hisao_smile_u at centersit with charachange
    hide hisao_talk_small_u at centersit

    hi "That sounds good. Should I tell her that?"

    mk "Sure. I'd tell her myself, but..."

    hi "I understand."

    "So that's my deadline. Whatever I decide, I need to be careful about how I proceed{w} - Suzu is a fragile person, and moreover, I don't want to lose the only female friend I've ever had."

    "She really is a troublesome girl."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##think I need a hart transition here
    ##return

label en_S3:

    #Custom fadein and fadeout animations. Fades for 4 seconds WHILE text is displayed, can also be used in other places. [AHA]
    transform crowdgather:
        on show:
            alpha 0.0
            easein 4.0 alpha 1.0

    transform crowddisperse:
        on hide:
            easeout 4.0 alpha 0.0


    scene bg suburb_roadcenter_ni with dissolve
    play music music_ease fadein 1.0

    "The air is pleasantly cool tonight, with a gentle breeze and cloudless sky. You couldn't ask for better weather, given the occasion."

    "The sleeves of the bright red kimono hide my missing left hand pretty well. At least it's useful for something; the fact that I can barely move in this thing reminds me why I don't like wearing them."

    "The sandals, too, are terrible. Given the tight fabric around my legs and the danger of putting a foot wrong and slipping out of them, there's little option but to take dainty little steps. Clothes like this make you act ladylike, whether you want to or not."

    "After putting Shizune and Misha through the trouble of doing my makeup for me and helping me put on the kimono, plus paying actual money to get my hair done, Suzu had better appreciate this."

    "I run my hand through my hair, partly to take in the feeling of how smooth and silky it is thanks to the barber's careful work, and partly to distract myself. I've taken care not to move around suddenly or work up a sweat, so everything should still look about right. Hopefully."

    show crowd at crowdgather

    $ renpy.music.set_volume(0.5, 0.0, channel="ambient")
    play ambient sfx_crowd_outdoors fadein 4

    "Walking down the path towards the park where we'd agreed to meet, the crowds get bigger as bigger as I near the main festivities. The scent of grilled food wafts in the air, as does the faint perfume of passing women."

    "It's a nice atmosphere, with people cheerful and happy as they walk along the path brightly lit by paper lanterns and stall lights. The pavement, trees, and everything around me almost seems to glow as the multicoloured lights dance off them."

    "Following the stream of festival-goers, the backs of two familiar figures come into sight ahead of me. One in his dorky sweater, and the other in a cute kimono of her own."

    "As I walk up to the two of them, it's Hisao who notices me first, having glanced back to see if I was coming. He gives a smile as he taps Suzu on the shoulder to turn her around."

    show hisao_smile at tworight
    show kimono_normal at left
    with charaenter

    "And then... we meet."

    "I open my mouth to say something, but the words catch in my throat. It takes me a couple of tries before I give up saying anything casual or witty, instead giving some pathetic excuse at my own expense."

    mk "Guess I was a bit late, huh?"

    hi "It's fine. Going by the looks of you, I can see why you took a while."

    show hisao_smile_teeth at tworight with charachange
    hide hisao_smile at tworight

    hi "I'd never have guessed you could be so ladylike."

    mk "Don't get used to it."

    "Hisao snorts, but my attention soon shifts to Suzu. She simply looks at me, still, silent, and unassuming. With her hair carefully groomed, hands daintily pursed in front of her, and cheeks rosy, she looks like a dainty doll. It's only now that I notice the cute little clip in her hair."

    "I feel my chest tighten as I stare at her. Suzu's always been an oddball, but for once, I feel like we have an understanding that we've never shared before. The look in those eyes could only possibly be one thing."

    "Nobody's ever looked at me like that before. I don't know why I'm so awkward about it; this is what all the fuss over how I looked in front of her was meant to achieve, after all. Despite all the time we've been friends, she's finally managed to leave me speechless."

    "So this is how it feels like to hold someone's heart in your grasp..."

    "The movement of Hisao draws me back into the real world, the sounds, smells, and bright lights around us suddenly re-entering my consciousness. We both look on as he quietly turns and begins to walk away."

    suz "Where are you-?{w=.25}{nw}"

    show hisao_biggrin at tworight with charachange
    hide hisao_smile_teeth at tworight

    hi "I'm going to run on ahead and have a poke around the festival. Enjoy yourselves."

    hide hisao_biggrin with moveoutright
    #show hisao_biggrin with moveoutright

    "He gives a churlish grin as he waves goodbye, skipping backwards with his hands in his pockets before blending into the thickening crowd ahead. Hisao might make for a mightily dorky cupid, but he's done alright. I owe him for this. We both do."

    "And so.... we're alone."

    show kimono_unhappy at left with charachange
    hide kimono_normal

    "I quickly begin to walk forward, or at least, as quickly as the kimono's tight wrapping around my legs allows. Suzu's mouth practically quivers as she tries to work out what to say or do, but I know she's not going to come up with anything."

    "Moving past her, I take her hand in mine as I go, not looking at her nor saying a word. She’s not the only one stuck for how to act in this situation. All I know, is that right now I'm the one who has to take the lead."

    scene bg suburb_tanabata_ni
    show crowd
    with locationchange
    show kimono_unhappy with dissolve ##check if in KS when walking side by side they show the character!!!

    $ renpy.music.set_volume(0.9, 3.0, channel="ambient")

    "Hand in hand, the two of us walk side by side into the heart of the festivities. The noise and laughter levels off as we enter, with people busying themselves eating food, playing games at the stalls, and chatting with their friends and partners."

    "Being two girls limits how intimate we can get, but right now, it doesn't really matter; Just holding hands is intense for both of us."

    "Suzu's hand feels soft, far removed from my rough and poorly cared-for skin, and her fingers lightly clutch at mine. They're warm, and only now do I notice the slight scent of perfume."

    "Just a few days ago we were friends, yet now she acts as a lovestruck maiden. Is it because she'd always held these feelings for me, and just stuffed them down until now? Or is it desperation, a frantic grasping at something precious that she feels might fly away at any moment?"

    "It's a little sad, in a way. Right now she appears more fragile than ever, and it's all because of me."

    "I spot a toffee apple stall a small distance ahead. Longing to break the silence and help the girl enjoy herself, I decide to use her sweet tooth against her."

    mk "Want a toffee apple? My treat."

    "This is where she should be giving me some probably deserved snark about how much I ask her for money. Instead, all she can manage is a subdued nod."

    hide crowd with dissolve

    $ renpy.music.set_volume(0.66, 1.0, channel="ambient")

    "I give a sigh as I lead us to the counter, taking my hand from hers to remove my purse. You pick up a few tricks after being one-handed for so long, with the stall owner raising an eyebrow at how efficiently I flick a few notes from my wallet using the same hand that's holding it."

    "I can't say I share Suzu's taste for sweet things, so after buying one and handing to her, I thank the stall owner and take my leave."

    show kimono_embarrassed with charachange
    hide kimono_unhappy

    suz "Thanks."

    mk "It's fine."

    "She begins to lick at her sweet, but only after reaching out her hand. I take it without question, and the two of us continue onward."

    show crowd behind kimono_embarrassed with dissolve

    $ renpy.music.set_volume(0.9, 1.0, channel="ambient")

    "Suzu's grip is looser than before, which I count as a small victory. While I appreciate her reaction to me being all dolled up, the last thing I want is for her cataplexy to play up. Besides, the calmer she is, the easier things will be."

    "As we move from stall to stall, I keep an eye out for anything that might be fun to do. Little by little her toffee apple whittles away as we walk, the food making the silence between us a little less stressful."

    "Despite my scanning around, it's Suzu who finds something first."

    "She might not have said it, but the way her gaze lingers on a stuffed panda is unmistakable. A quick glance at the stall it's sitting in shows it to be a game involving shooting some cups arranged in a pyramid with a cork gun to win a prize. Simple enough."

    mk "Wanna try it?"

    suz "The gun thing?"

    mk "Yeah."

    show kimono_grin with charachange
    hide kimono_embarrassed

    suz "You just want to shoot something, don't you?"

    "That's more like it. Her sardonicism, both in her voice and her expression, are for once a welcome sight."

    mk "Yup. You can keep the prize."

    hide crowd with dissolve
    hide kimono_grin with dissolve
    scene bg tanabata_game with locationchange

    $ renpy.music.set_volume(0.55, 1.0, channel="ambient")

    "I drag her over to the stall, and ask the owner what the prices are. A handful of yen for three shots is reasonable enough, so I fork over a few coins to the frail old man sitting on his tatty fold-up chair."

    "Suzu patiently stands back as I take the gun from the counter, testing its heft and loading the cork before shaking my left arm upwards to draw the sleeve away from my stump. The owner looks more amused than shocked as I take up position, pressing the stock to my shoulder and resting the barrel on my uncovered forearm."

    "The stance works well at stabilising my aim, even if I can feel the glances of a few passing people on me. A tall, tanned girl in a bright red kimono taking aim with a bare stump where her left hand should be would look pretty weird."

    "I silently will myself to hit the centre cup of the pyramid that's been carefully arranged. This is my chance to look super slick in front of Suzu, and although she's trying to hide it, she really wants that panda. I just need to concentrate, and..."

    play sound sfx_blop

    "The trigger gives little resistance as I pull it, the cork leaving the gun with a soft pop. With that, I lower the gun a little to see the result."

    "I needn't have bothered, as the sound of plastic cups falling to the ground is perfectly obvious. It was only just enough force to do it, but the pyramid toppled over with a single shot."

    mk "Yes!"

    ##show suzu upclose
    show kimono_happy_close with charaenter

    "I don't even get a chance to put the gun down before I find a pair of arms wrapped around me, my stump reflexively coming around Suzu's back as she wraps me in an excited embrace."

    "I can't wipe the dumb grin off my face as I rest the gun's barrel against my shoulder. I must look so cool right now. The coolest."

    suz "Thank you!"

    mk "Piece o' cake."

    "The old man reaches to his side and quietly rings the little bell to signify a winner, knowing that any verbal congratulations would pale compared to her reaction."

    show kimono_happy with charamove
    hide kimono_happy_close
    ##move suzu back

    "I look to him and nod to the bear as the prize I want, Suzu gently breaking off as he comes over with the stuffed item. She gives her earnest thanks to the man, the gun replaced on the counter as he passes it into her eager hands."

    scene bg suburb_tanabata_ni with locationchange
    show crowd at crowddisperse with dissolve
    show kimono_happy with charaenter

    $ renpy.music.set_volume(0.9, 1.0, channel="ambient")

    "We take our leave of the stall hand in hand, my own in her left, and the bear in her right. I can't help but smile at her as she inspects her new friend, glad to see a childish side of her she so rarely allows to be seen."

    "I'm pretty comfortable in calling tonight a success already. It's difficult to get past Suzu's mental reflex of avoiding emotions, but she's finally letting herself go. There's still a chance of cataplexy, or a sudden bout of sleepiness, but we'll take that as it comes."

    stop music fadeout 1.0

    $ renpy.music.set_volume(1.0, 0.0, channel="sound") #setting volume back to default

    play sound sfx_fireworks
    with Pause(0.0)

    stop sound fadeout 2.5

    "A trademark whistle echoes across the air, everyone's eyes suddenly turning to the bright green streak of light slowly chasing upwards into the night."

    "The first firework of the night explodes with a thunderous clap, its bright payload filling the sky above with vivid sparkles. A collective whoop resounds from the crowd, a few children begging to be raised onto their parent's shoulders to see."

    "Everyone begins to move at once towards the main viewing area a good distance ahead. Like two rocks in the middle of a vast stream, Suzu and I find ourselves surrounded by a flow of people all moving towards the one direction."

    suz "We're going to miss the fireworks if we stay here!"

    hide kimono_happy with moveoutright

    play sound sfx_running loop

    "Her hand breaks from mine as she runs ahead as fast as her getup allows, clutching her new panda to her chest."

    "After a moment's thought I quickly take chase, outpacing her with little effort."

    scene bg tanabata_bamboo with dissolve
    show crowd at crowddisperse with dissolve
    stop sound fadeout 0.3
    show kimono_embarrassed with dissolve
    play music music_lullaby fadein 1.0

    "The moment I reach Suzu, I push my arms forward and bring them over her shoulders to take hold of her. She comes to a dead stop the moment she feels my body pressing to hers, her arms dropping to her sides."

    "She way she stopped so suddenly, without a single word being spoken, shows her lie. She never truly pushed the thought of her confession out of her mind, instead trying to distract herself the entire time. It's the sort of thing she'd do."

    stop ambient fadeout 4.0

    hide crowd at crowddisperse

    "The two of us stand still for seconds, maybe minutes. I lose track of the time as we stay there, the area around us slowly draining of people as everyone leaves the stalls to get the best view of the coming fireworks show."

    "And then, it starts."

    hide kimono_embarrassed with dissolve
    scene bg misc_sky_ni with dissolve #maybe dotwipe_down as transition?

    show fireworks

    $ renpy.music.set_volume(1.0, 0.0, channel="ambient") #setting volume back to default

    play ambient sfx_fireworks

    "One by one, the little rockets shoot up into the sky, exploding above into all different colours of the rainbow. The view from here isn't so bad, the glow of the paper lanterns and the haphazardly run strings overhead doing little to block the lightshow above."

    "I carefully rehearsed what I was going to say to Suzu just for this moment, but it's all completely gone. No matter how much I try to remember those words, they never come back."

    "Well, whatever. Rehearsing a lovely little speech doesn't suit me anyway."

    mk "I'm proud of you, Suzu."

    mk "Here I was thinking I was the one with all the guts, but in the end, it turned out to be you."

    mk "I'm sorry for not giving you an answer until now. I... had to sort out a few things in my head, I guess."

    "I take a long breath and close my eyes. I can't take back the next words I'll say, but I know I have to speak them."

    mk "You're a good girl, Suzu. You don't deserve a terrible person like me."

    mk "But if you really do like me... then I'll walk beside you. Wherever you go, I'll go. Wherever I go, I'll take you."

    mk "I'll go out with you, Suzu."

    "I always thought confessions were supposed to make your heart race... but mine feels completely at peace. Things will change, but I know that this is what I want. Suzu deserves happiness, and if I can give that to her, then I can be truly happy as well."

    hide fireworks

    "Her body shudders a little, making me step back."

    scene bg tanabata_bamboo with dissolve
    show kimono_happy with dissolve

    "As she turns to face me, her face is a delicate mix of disbelief and hope. All I can do in response to that delicate face, its owner looking more fragile than she ever has, is give a reassuring smile."

    "Without regard for anyone around us, she closes her eyes and lifts her chin just slightly, standing on her toes. By now everyone's left for the fireworks display, the two of us standing alone in the bright lights bathing the path."

    "With one hand on her left shoulder and my forearm resting on her right, I close my eyes and gently lower myself towards her."

    scene bg 4317 with dissolve

    "And so, I press my lips to those of my precious Sleeping Beauty."

    stop music fadeout 2.0
    stop ambient fadeout 0.5
    with Pause(1.0)

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_S4:

    #scene bg city_trainstation with dissolve
    #with Pause(0.2)

    scene bg city_street4 with locationskip

    window show

    show suzu_normal_d at twoleft
    show hisao_smile at tworight
    with charaenter

    play music music_normal

    "Suzu, Hisao and I make our way along the city street after leaving the train station, the bright summer sun beating down on our heads and the sea's salty smell wafting in the air."

    "It's a nice atmosphere here. When I first learned she lived in the city, images of Tokyo and Osaka flashed to my mind, but instead it ended up being a fairly relaxed place bordering the ocean. It isn't a surprise why Suzu's family decided to make their home here, rather than living in the middle of the big smoke."

    $ renpy.music.set_volume(0.8, 0.0, channel="sound")

    play sound sfx_birdstakeoff fadein 0.2

    "A couple of distracted seagulls resting on a guardrail take flight as we stroll past, squawking in protest."

    mk "I'm telling you, you didn't need to buy those."

    show hisao_talk_small at tworight with charachange
    hide hisao_smile at tworight

    "I point to the small box carried by Hisao, the confectionery shop's cheery logo adorning the plain white container. He raises an eyebrow as he adjusts the duffel bag of clothes and meds carried over his other shoulder."

    hi "Is it so bad to offer a gift when visiting someone?"

    mk "When you're coming with people who've been before, it's a bit much."

    hi "I'm just being polite. I know this might be a foreign concept."

    mk "There's a fine line between good manners and brown-nosing..."

    show suzu_speak_d at twoleft with charachange
    hide suzu_normal_d at twoleft

    suz "Would you two stop fighting?"

    mk "Yes, mother."

    $ renpy.music.set_volume(1.0, 0.0, channel="sound") #setting volume back to default

    play ambient sfx_traffic fadein 3

    "The shimmering of heated air above the road ahead is broken up by a car whizzing past, with a pretty bright red sports car following soon after. While the attention of Hisao and I is drawn by the latter, Suzu's mind is elsewhere."

    "I put my hand on her head and give it a little rub, partly to reassure her, but mostly because I just wanted to. Given that she doesn't protest, I assume she likes it."

    stop ambient fadeout 4

    "It is good to see her in higher spirits, though. The last few days must've taken their toll on her emotionally, but she seems to be largely back to normal. Well, Suzu's normal."

    hi "Is there going to be anybody there when we arrive?"

    show suzu_smile_d at twoleft with charachange
    hide suzu_speak_d at twoleft

    suz "Miyu would be, at least."

    hi "Miyu?"

    mk "Yeah. She's cute; I think you'd get on well with her."

    show hisao_erm at tworight with charachange
    hide hisao_talk_small at tworight

    hi "That sounds like you're trying to set me up."

    mk "We'll see."

    show suzu_asleep_d at twoleft with charachange
    hide suzu_smile_d at twoleft

    "Suzu grimaces, but I manage to hide my reaction. I can't miss a chance to screw with him like this, after all."

    stop music fadeout 1.0

    scene bg city_houseext with locationskip
    show suzu_concerned_d at left
    show hisao_erm at center
    with charaenter

    play music music_fripperies fadein 1.0

    "The three of us finally come within sight of the Suzuki household; a modern and fairly spacious two-storey house, nestled in the kind of suburb that aspires to look wealthy, but isn't quite there. Suzu's sister must be home, as her little white car is parked neatly in the gravel driveway."

    "Looks like they've done some painting since the last time I was here, with the white walls and brown beams painted cream and black respectively. That modern, minimalist look is getting common these days, but I can't say I like it."

    "We march through the gate and up the stairs to the entrance in single file, Hisao's gaze flitting around to take in the carefully cultivated greenery in front. Suzu just looks ahead, taking the lead of our merry band."

    show tsu_tooth_smile at right with charaenter

    "As she digs around in her handbag for her house keys, the door swings open. A familiar figure rests her arm on the doorframe, taking in the sight of the trio before her."

    tsu "Well, well. Look who we have here."

    "Suzu's sister has always been easy on the eyes. Overall, she's about my height and blessed with quite a pretty face, adorned with a set of thin glasses. That, and her smart ponytail, give her an air of maturity that contrasts heavily with Suzu's youthful nature."

    "Her plain and slightly tattered grey hoodie is an unmistakable sign that she hasn't ventured outside the house all day, probably being busy with some project or another. Her welcoming expression is undoubtedly sincere, though it's always felt like she's just a little too old to socialise with us beyond being polite."

    "I assume Suzu's notified her of the hastily invited additional guest, as she doesn't look surprised in the least."

    suz "Mom and dad out?"

    show tsu_annoyed at right with charachange
    hide tsu_tooth_smile at right

    tsu "That's not how you should greet your lovely sister..."

    show tsu_smile at right with charachange
    hide tsu_annoyed at right

    tsu "But yes, they're still at work. They should be back for dinner."

    "Suzu nods, expecting the answer. With that, the conversation turns to other matters."

    tsu "I see you've brought the troublemaker around."

    mk "That's not fair! Since when did I cause you any trouble?"

    show tsu_annoyed at right with charachange
    hide tsu_smile at right

    tsu "Since I had to format my computer after letting you use it for five bloody minutes?"

    "I don't have a comeback for that. The Internet is a scary place sometimes."

    show tsu_tongue at right with charachange
    hide tsu_annoyed at right

    tsu "I'm just being mean. How are you getting along these days?"

    mk "Same old, same old."

    show tsu_smile at right with charachange
    hide tsu_tongue at right

    tsu "I see you picked up a stray somewhere along the way. You must be Nakai?"

    show hisao_smile at center with charachange
    hide hisao_erm at center

    hi "Pleased to meet you, Miyu."

    "I hastily try to stop myself from snickering, but it's useless. She just smiles as she levers herself off the doorframe, by now wise to my antics."

    tsu "It's Tsubasa. Tsubasa Suzuki."

    show hisao_blush at center with charachange
    hide hisao_smile at center

    hi "Ah... sorry."

    show tsu_deadpan at right with charachange
    hide tsu_smile at right

    tsu "I have no idea why anyone hangs out with you, Miura."

    suz "I wonder that myself all the time."

    "I just grin, content that I've had my fun. Trying to hide his embarrassment, Hisao quickly offers the sweets to her."

    show tsu_ooh at right with charachange
    hide tsu_deadpan at right

    "Tsubasa's face lights up as she takes the box, quickly popping the top open to check on its contents. If there's one thing the Suzuki sisters share, it's a sweet tooth."

    show hisao_smile at center with charachange
    hide hisao_blush at center
    show tsu_smile at right with charachange
    hide tsu_ooh at right

    tsu "Approved. Welcome to the Suzuki household."

    scene bg city_houseint with locationskip
    show suzu_normal_d at center
    show hisao_erm at left
    show tsu_smile at right
    with charaenter

    "Tsubasa moves from the door, gesturing with her head for us to follow her inside. We dutifully take off our shoes at the entrance and file in behind."

    "Her living room lives up to the exterior of the house, being both spacious and tidy. The large entertainment unit, with its sizable television turned to some insipid soapie, takes up most of one wall, with the couch and a few chairs sitting behind a black coffee table covered in magazines."

    "The still half-asleep head of a small brown dog pokes above the arm of the couch to see who's entered, before excitedly leaping off and galloping towards us happily panting and wagging its tail. Suzu immediately crouches down and scoops up the fluffball into her arms, smiling widely as she comes to her feet."

    show miyu_happy at center with moveinbottom

    suz "There, there. I'm home, Miyu."

    show suzu_grin_d at center behind miyu_happy with charachange
    hide suzu_normal_d at center

    "Her grin redoubles as she gets a few well-deserved licks on the cheek. I briefly wonder if dogs can hyperventilate, because it sure looks like this one might."

    show hisao_hmpf at left with charachange
    hide hisao_erm at left

    hi "Miyu, huh?"

    "He looks at me with as displeased a face as he can muster. A difficult task, after seeing Suzu's reaction."

    show hisao_smile at left with charachange
    hide hisao_hmpf at left

    hi "What breed?"

    suz "She's an Affenpinscher crossed with... something."

    show tsu_question at right with charachange
    hide tsu_smile at right

    tsu "No allergies or anything?"

    hi "Me? Nah. Dogs are nice."

    "He reaches out for Miyu, but stops a few inches from her face. Only after she gives his hand a bit of a sniff does he slowly advance further to petting her head, smiling as he does so. I suppose his gentle nature is the type to get along with animals well."

    hide miyu_happy with moveoutbottom

    "Suzu puts Miyu back on the ground afterwards, the dog busily giving both me and her new friend a good inspection."

    tsu "I think you'll get along here just fine. Come with me and I'll show you the guest room. You can throw your bag down there."

    hi "Thanks. You two good?"

    mk "I'll just bunk with Suzu. Have fun with Tsubasa."

    mk "...You stud."

    show tsu_smile at right with charachange
    hide tsu_question at right
    hide tsu_smile with moveoutleft
    hide hisao_smile with moveoutleft

    "Tsubasa just smiles as she leads him into the hallway, the sound of her pointing out the directions to this and that to be heard after they leave. Miyu's interest seems to be piqued by the new arrival as she trots out after them."

    play sound sfx_pillow

    "I just let my bag drop on the floor, content to drag it up to Suzu's room some time later."

    show suzu_speak_d at center with charachange
    hide suzu_grin_d at center

    suz "Drink?"

    mk "Yeah. Just some juice, thanks."

    suz "Coming right up."

    stop music fadeout 2.0

    "As she turns to leave, I feel my heart twitch. Just a little."

    "Suzu looked so delicate and fragile when I agreed to go out with her. She'd finally opened up towards me, knowing full well how much she could have been hurt. Such a frail and unassuming girl appeared at that moment to be so much stronger than I ever was."

    "But now, she acts as if it never happened. Like it's just another day."

    show suzu_speak_close_d with charamove
    hide suzu_speak_d at center
    ##bring suzu in close

    play music music_suzu

    "I quickly start moving towards her, catching her attention as I do so. Just as she turns to see what I'm doing, I bring my arms around her small body and press her to my chest."

    "Hugging's never really come naturally to me. It's not that I dislike it, but more that it's never felt very special. Maybe I was just never hugged enough as a kid."

    "Holding her to me as I do now feels different, somehow. Not because I can feel her soft, warm body against mine, but because such a normally apprehensive girl would allow me to get so close at all. She trusts me."

    "For a moment it looks like she might not reciprocate, taken too off guard to return the gesture. Eventually, though, she picks her arms up and wraps them around my back, drawing me into a tight embrace. With her face turned to the side, I press my lips to the top of her head."

    show suzu_veryembarrassed_close_d with charamove ##up close
    hide suzu_speak_close_d

    suz "Sorry. I just..."

    mk "You don't need to hold back, Suzu. You always worry too much."

    suz "Only because you don't worry enough."

    show suzu_embarrassed_d at center with charamove
    hide suzu_veryembarrassed_close_d

    "I smile a little as I step back, rubbing her shoulder with my hand as a I do."

    mk "It's good to see you're holding up. You've been through a lot lately."

    suz "And that was who's responsibility?"

    mk "I was trying to avoid mentioning that..."

    hi "So this means you're back to your old selves again?"

    show hisao_smile at right with moveinright

    "Looking over Suzu reveals Hisao standing in the doorway, arms crossed and smiling. Suzu clamps her eyes shut to maintain her composure, but her rosy cheeks give her away."

    suz "How long have you been there?"

    hi "Only just now. She went to her room, so I came back down."

    hi "I was worried about the two of you as well, you know. It's good to see you've made up."

    mk "Yeah, thanks. Guess I've finally got my head screwed on right."

    "Suzu just nods at him, but both of us know she's thankful."

    stop music fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve
    ##5 character onscreen tsubasa - mom - dad - suzu - hisao
    scene bg city_houseint with shorttimeskip
    show suzu_father_normal at leftoff
    show mother_normal at twoleftsit
    show tsu_smile at centersit
    show suzu_concerned_d at tworightsit
    show hisao_erm at rightedgesit
    with charaenter

    play sound sfx_cutlery loop
    play music music_soothing

    "The clatter of knives and forks rings out as the Suzuki family, plus their two guests, dig in to a lavish dinner. Various bowls of different salads sit on the table, complimenting the still steaming pieces of roast chicken on our plates."

    "With Suzu, Hisao, and I seated on one side of the table, Suzu's sister, mother, and father sit on the other. Miyu hovers around the floor, making sure she's positioned to grab any scraps of food that might fall."

    "I've always found it difficult to work out the age of her mother, with her chic short-cropped hair and smart clothing making her look quite trendy. It's a nice style, though it would be improved by her smiling a little more. Perhaps a result of stress from her job, now that I think of it."

    "Her father... isn't like that. With a somewhat wiry body and thick spectacles perched on his round face, his greying hair noticeably beginning to thin, he's always felt like a much warmer and unassuming personality. Despite his position as a prefectural bureaucrat, he's always held a sense of pride that I've respected in him."

    mot "So how are things going at school, Suzu?"

    suz "Fine."

    mk "Exams are over, so things are a bit more relaxed now."

    mot "And how did you do on them?"

    mk "Well..."

    suz "I think I did fine. Maths aside."

    show mother_tight at twoleftsit with charachange
    hide mother_normal at twoleftsit

    "Her mother puts down her fork to think, her face disappointed. It must be hard to have parents who drive so hard for good marks, despite the fact that her narcolepsy works against her."

    mot "Hmm. Maybe we should get a tutor, then."

    show tsu_ooh at centersit with charachange
    hide tsu_smile at centersit

    tsu "There's a tutor right here."

    suz "I just need to study more. It'll be fine."

    show tsu_smile at centersit with charachange
    hide tsu_ooh at centersit

    "She doesn't appear to have convinced her mother, but she manages to have the topic dropped. For now."

    "I wonder what her parents think of my influence on her, given they'd be well aware of my pretty average grades. Hisao would be a much better fit for her, in personality as well as academics, than I would."

    dad "Nakai, wasn't it?"

    hi "Ah, y-yeah."

    "Speak of the devil. Content to let him speak for himself, I busy myself with the delicious food in front me."

    show suzu_father_happy at leftoff with charamove
    hide suzu_father_normal at leftoff

    dad "You've been terribly quiet; there's no need to be nervous."

    show mother_normal at twoleftsit with charachange
    hide mother_tight at twoleftsit

    mot "That's right. How do you think you've fared?"

    hi "Uh, well, I don't usually have much problem that with sort of thing."

    mk "Nerd."

    show suzu_speak_d at tworightsit with charachange
    hide suzu_concerned_d at tworightsit

    suz "Hisao's really good with science and maths. He's been helping me a bit with them."

    show hisao_frown at rightedgesit with charachange
    hide hisao_erm at rightedgesit

    hi "I'm not that good..."

    "That false humility makes me want to strangle him. From the focus he's receiving from her parents, I get the feeling he's at least making a good impression for them."

    show suzu_concerned_d at tworightsit with charachange
    hide suzu_speak_d at tworightsit
    show tsu_tongue at centersit with charachange
    hide tsu_smile at centersit

    tsu "And here I was thinking you'd come to your sister for help."

    show mother_soften at twoleftsit with charachange
    hide mother_normal at twoleftsit

    mot "Any intentions of what you might do in university?"

    show tsu_smile at centersit with charachange
    hide tsu_tongue at centersit
    show hisao_talk_small at rightedgesit with charachange
    hide hisao_frown at rightedgesit

    hi "I suppose just more of what I'm good at. I don't really know what kind of job I want to do."

    dad "The main thing is to have skills behind you and a good head on your shoulders. It sounds like you have both."

    mot "So what do you do with yourself outside of school? Any hobbies? Interests?"

    hi "Studying, mostly. Used to play sports, but I can't really do that anymore."

    "The brief lull in discussion says a lot. There's no doubt they've been briefed on Hisao's condition, but that's a far cry from knowing how to handle it best in conversation. If there's one thing that my time in Yamaku's taught me, it's that everyone's different in that regard."

    "Taking a bit of pity on her parents for inadvertently bringing up the subject, I give the conversation a little push."

    mk "And how much of your bag was taken up by books?"

    show hisao_erm at rightedgesit with charachange
    hide hisao_talk_small at rightedgesit

    hi "It wasn't that much."

    show suzu_normal_d at tworightsit with charachange
    hide suzu_concerned_d at tworightsit

    suz "You should just join the literature club, already. Why are you even in track and field?"

    show hisao_disappoint at rightedgesit with charachange
    hide hisao_erm at rightedgesit

    hi "You've asked me that before. Then again, it's a question I continually ask myself as well..."

    mk "He's ours, you can't have him!"

    suz "The others in the lit club would be happy with have him. He already knows Ikezawa, after all."

    show hisao_talk_small at rightedgesit with charachange
    hide hisao_disappoint at rightedgesit

    hi "Do I get a say in this?"

    show tsu_tongue at centersit with charachange
    hide tsu_smile at centersit

    tsu "Shouldn't a boy be happy he's in high demand?"

    show hisao_hmpf at rightedgesit with charachange
    hide hisao_talk_small at rightedgesit

    "He just grimaces at her. I do think he secretly enjoys being our chew toy, but he'd never admit it."

    mot "Maybe you should join her club. You do have similar interests after all."

    "That's... not subtle. Suzu cuts me off before I can make light of the situation, obviously bothered by her mother's interjection."

    show suzu_angry_d at tworightsit with charachange
    hide suzu_normal_d at tworightsit

    suz "We're just teasing him. It's up to Hisao which club he joins."

    mot "Such a shame. You're going to give up without a fight?"

    suz "We're just friends."

    mot "But he seems like a smart, handsome lad. Aren't too many like that around."

    show mother_smile at twoleftsit with charachange
    hide mother_soften at twoleftsit

    "She gives him a genuine smile, evidently pleased with her attempts to play matchmaker."

    show hisao_biggrin at rightedgesit with charachange
    hide hisao_hmpf at rightedgesit
    show tsu_erm at centersit with charachange
    hide tsu_tongue at centersit

    "He tries to reciprocate as best he can, but his terribly stilted smile betrays the fact that he knows as well as I that this conversation is like a car careening towards a cliff."

    show hisao_erm at rightedgesit with charachange
    hide hisao_biggrin at rightedgesit

    "Once more I try to jump in, but Suzu cuts me off. As much as I hate to say it, I'm at least learning something about her in this exchange; it's rare for her to be assertive towards others, but that may be more due to her shyness around unfamiliar people than true submissiveness."

    show suzu_veryangry_d at tworightsit with charachange
    hide suzu_angry_d at tworightsit

    suz "I said I'm not interested in him."

    show mother_normal at twoleftsit with charachange
    hide mother_smile at twoleftsit

    mot "But why?"

    show suzu_veryembarrassed_d at tworightsit with charachange
    hide suzu_veryangry_d at tworightsit

    suz "Because I like girls."

    "...And there's the cliff"

    stop music
    stop sound

    show suzu_father_normal at leftoff with charamove
    hide suzu_father_happy at leftoff
    show mother_tight at twoleftsit with charachange
    hide mother_normal at tworightsit
    show tsu_ooh at centersit with charachange
    hide tsu_erm at centersit

    "Where the table had been humming with the noise of chatting, chewing, and clinking of utensils, in a flash it turns to dead silence. Not one person speaks, nor moves an inch. Knives and forks hang above plates, mouths still, and eyes stuck."

    "Suzu stares straight into her mother's eyes, a look of exasperation written onto her face. It's unmistakable that she's taking full ownership of the words she's just said. For her part, her mother appears to have simply stopped functioning, unable to process the last few seconds of her life."

    suz "Miki's my girlfriend."

    "Oh wow. I'm torn between fear at what might unfold in the next few seconds, or total adoration of the sheer balls this girl has on her."

    "I'd be lying if I said this didn't make me like her more. I've never seen this side of Suzu before, her true strength of will on display with her back to the wall. I feel the muscles in my throat tense as if my body wanted me to say something, but I have no idea what to speak, or even if I should."

    "Suddenly realising that Suzu and her mother aren't the only people at the the table, my eyes dart from one person to another."

    "Suzu's father has the same reaction as her mother, simply looking at his daughter with a remarkably neutral expression. He tends to let her mother define the collective household opinion most of the time, but it's hard to say if that'll hold true of such a personal matter."

    "Tsubasa looks more interested than shocked, slowly beginning to chew the food in her mouth once more. I get the feeling she's waiting more for her mother's reaction than actually coming to terms with what Suzu's said."

    "As my glance falls to Hisao, his eyes meet mine. The look in his eyes makes me feel sorry for him; he's like an actor abruptly thrown onto the stage without a script, surrounded by other actors reciting entirely unknown lines. When his cue will come, and what he's supposed to do once it does, is a mystery to him."

    "But none of us have been given our lines. We're all actors without a script right now."

    play music music_shadow

    show mother_closed at twoleftsit with charachange
    hide mother_tight at twoleftsit
    show suzu_unhappy_d at tworightsit with charachange
    hide suzu_veryembarrassed_d at tworightsit

    "My heart sinks as Suzu's mother lowers her fork to the plate and slowly closes her eyes. Suzu's disposition changes as her shoulders slump and expression falls, knowing that her mother's judgement has been given without a word being spoken."

    "Everyone's lives changed in the last few seconds, and it wasn't for the better."

    mk "Um... I..."

    "I desperately try to choke some words out of my tightening throat, but I still don't know what it is I want to say. This is bigger than me. It's usually so easy to laugh my way out of awkward situations, but this is something I don't understand at all."

    "A movement out of the corner of my eye grabs my attention, Suzu's plate suddenly being pushed towards me."

    show suzu_asleep_d at tworightsitlow with charamove
    hide suzu_unhappy_d at tworightsit
    play sound sfx_impact

    "Hisao quickly withdraws his arm as Suzu's upper body falls forward, her face landing flat on the table where her plate has been. I feel even worse for having completely failed to account for her condition, Hisao's reflexes having just saved the day."

    "Everything about this feels absurd. It may be a sleep attack or cataplexy from the stress, or one leading to the other. In any case, this seems a reasonable excuse to extract her from the room and get things back under control."

    show suzu_father_unhappy at leftoff with charamove
    hide suzu_father_normal at leftoff
    show mother_angry at twoleftsit with charachange
    hide mother_closed at twoleftsit

    "Her mother puts her elbow on the table and buries her face in her hand out of frustration, her husband's hand reaching out and rubbing her back in concern."

    mk "Should I-{w=.25}{nw}"

    mot "Just take her."

    show hisao_frown at rightedgesit with charachange
    hide hisao_erm at rightedgesit

    "I can take that; I was prepared for her snapping. Hisao, on the other hand, looks to me with pained eyes as I collect Suzu's limp body. While he may be desperate for some instruction on how to deal with them, all I can do is look to the floor in defeat. He's on his own, and I hate that fact."

    hide suzu_asleep_d with moveoutbottom

    "With the girl sliding onto my back and still not making so much as a movement as we make to leave the room, it looks like she's slipped into sleeping after the attack."

    "As much as I hate to say it, that's probably for the best."

    stop music fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve
    scene bg city_housekitchen with shorttimeskip
    show tsu_hmm with dissolve

    play music music_caged_heart fadein 1.0

    "With the fracas of dinner over, things have settled down a little by late evening."

    "Suzu's mother has a bath as Tsubasa and I do the dishes, with Hisao and her father watching the day's news on the television. Looks like Hisao's a hit with Miyu, the small fluffy thing deciding to sleep on his lap."

    "Then again, I heard somewhere that dogs are good at sensing people's emotions. Given the tense feeling in the air, Miyu may just be happy to be with someone who's not freaking out."

    "At least there's some semblance of domestic normality now, even if the atmosphere could be cut with a knife."

    mk "Hell of a dinner, huh?"

    show tsu_sad with charachange
    hide tsu_hmm

    "She just sighs, pausing her washing of the plate in her hands as she looks back to the living room."

    tsu "I feel sorry for Nakai. What a welcome to the family."

    mk "He'll be fine. I know he looks like... that, but he's actually a pretty sturdy guy."

    mk "What about her father?"

    show tsu_erm with charachange
    hide tsu_sad

    "She pulls an uncomfortable face, wanting to give me one answer, but knowing that another would be the truth."

    tsu "Dad might not be as stubborn as our mother is... but he's also pretty old-fashioned. Who knows, he might come around."

    tsu "Maybe."

    "With that, she finishes sponging the plate in her hands and passes it along to me for drying while grabbing the next."

    "I move to take it from her, but with my mind on other matters and my hand wet, it slips straight out of my grasp."

    mk "Crap...!"

    "With my hand too far to possibly grab it before it hits the floor, I try to at least break its fall with my stump. All I accomplish is making it tumble some more before it smashes to the ground."

    play sound sfx_broken_plate
    with vpunch
    show tsu_ooh with charachange
    hide tsu_erm

    tsu "Sorry, I wasn't looking where-"

    "Tsubasa's frantic apology betrays her touchiness around my missing hand, immediately blaming herself for not taking it into account. It's not like she had anything to do with it, and while I might have caught the damn thing otherwise, my stump is the last of my worries right now."

    mk "It's fine, I just..."

    "I reflexively bend down to try and at least take some of the larger shards off the tiled floor, but something rushes to my face and threatens to overwhelm me as I do so."

    with blackflash

    mk "Ah, shit."

    scene black with shuteyefast

    "Snapping back upright and bring my back to the counter for support, I close my eyes and take the bridge of my nose in my fingers to try and compose myself."

    "As little as Tsubasa and I have in common, she's at least a kind soul. I feel her warm hand on my shoulder, silence hanging in the room as she lets me take my time."

    scene bg city_housekitchen with openeye
    show tsu_ooh

    mk "What about you?"

    show tsu_question with charachange
    hide tsu_ooh

    tsu "Sorry?"

    mk "You sure didn't seem too surprised by all this."

    show tsu_smile with charachange
    hide tsu_question

    tsu "Sister's intuition."

    "I raise an eyebrow at her cheeky smirk."

    tsu "...and maybe I saw an autocomplete entry or two when fixing her laptop. Plus a couple of interesting manga in her desk."

    mk "She wasn't that good at hiding it, was she?"

    tsu "Not at all."

    "I give a weak smile her Suzu's expense, but it soon drops as I catch sight of the shattered plate once more."

    "If it were anyone but me, I wonder how this would have gone. I have no ambition, poor grades, I'm crude and impolite, and share barely any interests with her. Next to me is, in their eyes, a charming wonder-boy who's on a straight ticket to university."

    "Suzu's mother probably had it all planned out for her. Following her sister into university, pushing past her narcolepsy to get a respectable career in some academic field or another, marrying into a reasonably well-to-do family. Grandchildren, too."

    "Then I came and messed it all up."

    show tsu_hmm with charachange
    hide tsu_smile

    tsu "Miki."

    mk "Yeah?"

    tsu "Don't beat yourself up, okay? None of this is your fault."

    "I wish she wasn't as sharp as she is."

    mk "Do you really think that?"

    show tsu_smile with charachange
    hide tsu_hmm

    tsu "It's up to Suzu who she's attracted to. That happened to be you. Shouldn't you be happy about that?"

    mk "I guess. I mean, I'm glad she likes me, and I like her."

    tsu "That's more like it. It's strange to see you not smiling."

    tsu "Go on, I'll clean this lot up and grab Nakai to help for the rest."

    mk "Thanks. I owe you."

    "I give her a nod and dry my hands off on a towel before taking my leave, though Tsubasa's voice from behind me catches my attention."

    tsu "Oh, there was one more thing."

    tsu "You're still a kid. You know that, right?"

    mk "Yeah, I know."

    show tsu_deadpan with charachange
    hide tsu_smile

    tsu "Who my sister likes is her business, but if I find out that you've hurt her... I will ruin your life in ways only an adult would know."

    "My heart freezes. I have absolutely no doubt that she means every word she says, delivered in that chilling voice."

    stop music fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve
    scene bg suzu_bedroom with dissolve
    show suzu_asleep_d with dissolve

    play music music_suzu fadein 1.5

    "Suzu's bedroom as the same as it's always been, bookshelves filled with a mix of girly manga, a few shelves holding various characters from shows she's watched, and a number of plush animals sitting around the largely white and light pink room."

    "A spoiled little princess, quietly slumbering away surrounded by her little luxuries. It's nice to see her sleeping so peacefully, her mind not worried by the day's events."

    play sound sfx_sitting
    scene bg 4399 with dissolve

    "Walking over to her bed, I carefully take a seat on the side where she's sleeping. Without thinking, I reach down and brush away a stray hair on her face, disturbing her just enough to make her eyelids flutter."

    "I try to keep my voice as low and gentle as possible, not wanting to bother her any more than I already have."

    scene bg suzu_bedroom with dissolve
    show suzu_sleepy_d with dissolve

    mk "Hey. You okay?"

    "She just looks at me through half-closed eyes before letting them mournfully drop to the side."

    "I feel stupid for not knowing how to comfort her. I came up here, after all, but now I'm suddenly left realising that I've never really tried emotionally supporting such a fragile person before. It's one thing to talk a guy through some day-to-day frustration or whatever, but quite another to be stuck together in the trenches like this."

    "I end up just stroking her head, completely at a loss for what else to do."

    show suzu_unhappy_d with charachange
    hide suzu_sleepy_d

    suz "What happened afterwards?"

    mk "Hmm... not much, really. Just a few bits of small talk before everyone went off to do their own thing."

    suz "They hate m-{w=.25}{nw}"

    mk "Don't be like that. They were just taken off guard, that's all."

    mk "Remember when you kissed me out of the blue? Even I was a bit shocked, and you know how I am."

    suz "Thick-headed?"

    "I give a snort in spite of myself. She's still the same old girl, that's for sure."

    mk "Yeah, I deserved that."

    "In the brief silence that follows, Suzu fidgets a bit and manages to sit up, albeit slightly groggily."

    scene bg bed with dissolve

    "As she looks at me, her eyes staring into mine, her intentions are plain to see. Without a word, both of us lean towards each other as she holds her blanket to her chest."

    scene bg suzu_bedroom with dissolve

    show suzu_smile_d with charachange
    hide suzu_unhappy_d
    show suzu_smile_close_d with charamove
    hide suzu_smile_d
    ##move upclose

    "Our lips meet each other. It's not much more than a peck, a momentary touch before we each sit back, but it's enough."

    show suzu_veryembarrassed_d with charamove
    hide suzu_smile_close_d

    "I feel a stupid grin sitting on my face, the feeling of our kiss still lingering. Suzu manages to hold her composure for a scant few moments before her cheeks fill with a bright scarlet, forced to look down in embarrassment as she clenches her hand to her chest."

    "I know it's irrational, that it makes absolutely no sense, but somehow I can't help but feel that everything will work out fine when I see her like this."

    "It's a terribly strange feeling. Not so much to love someone, but to be loved yourself. To know that to someone else, you're the most important person in their mind. Not by blood, but by choice."

    "Maybe that's why everything feels like it'll be alright. Because Suzu's there, and even after all I've done, she loves me. She accepts me."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_S5:

    scene black with dissolve

    window show
    scene bg city_houseint with dissolve
    play music music_daily

    "A tired Suzu follows my lead as we head down the stairs and into the hallway, a great yawn escaping as I make my way to the living room."

    play sound sfx_dooropen

    "Opening the door reveals that we're not the first to arrive. With her body hidden by the recliner's back, all that's to be seen are two grey-clad arms lazily hanging over the sides."

    show suzu_concerned_d at twoleft
    show tsu_dumps at right
    with charaenter

    mk "You okay?"

    tsu "Life is pain. Leave me to my fate."

    "Her dreary voice is nothing short of pathetic to behold."

    suz "What have you been told about all-nighters?"

    tsu "Internal compiler error: segmentation fault. Internal compiler error: segmentation fault. Internal compiler error..."

    mk "Okay, okay. We'll leave you to mope in peace."

    "She repeats herself a couple more times as we leave her aura of depression to get something for breakfast. I think this might be the first time I've seen her this frazzled."

    stop music fadeout 3.0

    scene bg city_housekitchen with dissolve
    show suzu_unhappy_d at left
    show mother_normal at right
    with charaenter
    play music music_tension

    "The moment we enter the kitchen, I freeze. The very last person I wanted to see stands before us, her cold eyes locked to mine as she lowers her cup of coffee to the counter."

    suz "Good morning."

    "Suzu's timid voice draws the attention of her mother, giving me a chance to breathe as her expression lightens ever so slightly."

    show mother_soften at right with charachange
    hide mother_normal at right

    mot "Good morning, Suzu. Have you had your morning tablets, yet?"

    suz "I'll have them with breakfast."

    mot "Good girl. Don't forget to wash them down with something; I know you keep dry-swallowing them."

    suz "Yes, mom."

    show mother_normal at right with charachange
    hide mother_soften at right

    mot "I'll be off to work then. You'll have Tsubasa to watch over you."

    suz "I'm not a child any more, you know. I don't need adult supervision."

    hide mother_normal with moveoutright

    "Her mother takes one last sip of coffee before depositing her cup and taking her keys from the counter, Suzu's protests falling on deaf ears. We both step aside to let her through, sharing sense of relief that what might have been a confrontation has turned out to be nothing."

    "Looks like we're doing the whole 'forget anything was ever said' routine, keeping up the appearance of normality. As much as I'm grateful for avoiding an argument, it's obvious that this is only a stay of execution."

    "Just as I'm about to get breakfast and do my best to forget the whole experience, her sharp voice calls out from behind."

    mot "Miura, would you come with me for a moment?"

    "I don't even bother hiding the slumping of my shoulders."

    stop music fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve

    scene bg city_houseext with dissolve
    show mother_angry
    with charaenter
    play music music_tragic

    "Her fancy grey car is right there, keys clutched in her hand as she stands with her arms crossed. If only I could will her to just get inside and drive off, leaving us in peace."

    "Instead, I feel like I'm on trial. Her ice cold stare is obviously intended to assert her dominance over me, and it's working. This feels more like an interrogation than any kind of cordial chat between she and her daughter's love interest."

    mot "Before this goes any further, I want to make something perfectly clear to you."

    mk "Yeah?"

    mot "Make the most of your time here. This is the last time you'll set foot in this house, after all."

    mk "But-!{w=.25}{nw}"

    mot "I'd suggest you don't talk back to me. You should be glad you're still here at all."

    "So that's how this is going to be played. It's disappointing, of course; I liked Suzu's family a lot, and now they've come to roundly reject even the sight of me. That said, the silver lining is that she's taking this out on me rather than Suzu."

    "At least, for now. Just the thought of me being the cause of her mother being angry at her makes me feel sick, so if this is what it takes, so be it."

    "She evidently takes my absentminded rubbing of my arm as submission to her demands, pressing the key fob to disable the car alarm and beginning to get inside."

    mk "This isn't fair..."

    "My thought freezes as I realise what I've mumbled. Why do I always have to have the last word? Why can't I just keep my mouth shut?"

    stop music
    play music music_tension

    show mother_yell with charachange
    hide mother_angry

    "My worst concerns are realised as her mother abruptly stops getting into the car and steps back out, rounding on me with a face of burning resentment."

    mot "Don't you dare talk to me about what's fair."

    "Shit, what do I do? I can't simply say sorry. I know damn well that I wouldn't be able to force the words out, an apology for this being against every instinct I have. If I take her up on her argument though, there's every chance I'll be thrown out and make things far worse for Suzu."

    "I've never had a problem with telling teachers or other authority figures to go stuff themselves if I felt they were being unfair, even back in elementary school. Maybe that was because I was a badly-behaved little brat, but that's beside the point."

    "But right now, all I can do is stand mortified, unable to stand up against this woman before me. Not out of concern for myself, but for another."

    "The sound of the front door opening behind us draws our attention, Tsubasa's figure coming into sight."

    show tsu_erm at rightedgetsu with moveinright

    tsu "Hey, mom...?"

    mot "Yes?"

    tsu "Could you pick up some milk on the way home? I'd text dad, but he'll just forget."

    "Her gaze shifts to me, the momentum from her previous anger having been abruptly brought to a halt."

    "The game being played is perfectly obvious, but it's clear that she wants to keep this directed at me right now given that she dragged me out here just before she left for work."

    show mother_closed with charachange
    hide mother_yell
    pause(1.0)
    show mother_murder with charachange
    hide mother_closed

    stop music

    "The way she closes her eyes and reopens then with an entirely different disposition should unsettle me, but right now I'm just relieved that it's all over."

    mot "Milk. Got it."

    hide mother_murder with moveoutleft
    play sound sfx_car_door

    "With that, she lowers herself into the car while doing her best not to acknowledge my presence."

    play sound sfx_car_drive_off

    "The relief of seeing her car back out of the driveway and disappear down the street is palpable. I waste no time in turning on the ball of my heel and heading straight back inside."

    mk "Thanks. I owe you one."

    show tsu_deadpan at rightedgetsu with charachange
    hide tsu_erm

    tsu "And don't you forget it."

    ##centered "~ Timeskip ~" with dissolve
    scene bg city_houseint with shorttimeskip
    show hisao_talk_small at tworightsit
    show suzu_neutral_d at twoleftsit
    with charaenter
    play music music_raindrops

    "With Tsubasa having retreated to her room and Hisao finally awake, the three of us settle in on the couch as the console slowly boots up. Miyu quietly lays on the recliner, content to sleep the day away."

    "Seated in the middle of us, with me to the right and Hisao to the left, it's Suzu who has command of the controller. With the game already chosen and inserted, it starts up in short measure."

    hi "Ah, this. So you're into RPGs, then?"

    "She gives a nod."

    suz "You?"

    hi "I mostly just played at the local arcades, like before."

    show suzu_normal_d at twoleftsit with charamove
    hide suzu_neutral_d at twoleftsit

    suz "It shows."

    hi "Well at least I'm good at something beyond schoolwork."

    hi "What about you, Miki?"

    mk "Eh, I kinda had a deprived childhood when it comes to this sort of thing. It still blows my mind how good they look these days."

    show hisao_smile_teeth at tworightsit with charachange
    hide hisao_talk_small

    hi "And you're the one calling me old-fashioned."

    mk "Hey, at least I wasn't born 50 years old."

    show suzu_grin_d at twoleftsit with charachange
    hide suzu_normal_d at twoleftsit

    suz "You just got stuck as a 10 year old, instead."

    "The smartass comment earns her a stuck-out tongue."

    show suzu_neutral_d at twoleftsit with charamove
    hide suzu_grin_d at twoleftsit
    show hisao_erm at tworightsit with charachange
    hide hisao_smile_teeth at tworightsit

    "She finally gets past the menus and starts running around the fictional school building once the game loads, picking up from where she left off with remarkable ease."

    "As she runs up to a girl in the game and starts some dialogue, I can't help but comment. I'm kinda curious what her type is when it comes to women, after all."

    mk "I like her."

    suz "Who?"

    mk "Her. The redhead chick. She's cool."

    suz "She's kind of bossy..."

    mk "Hisao, second opinion?"

    show hisao_heh at tworightsit with charachange
    hide hisao_erm

    hi "I'm with Miki on this one, for once."

    suz "Hmph."

    mk "So who's your favourite? Please not the hangdog mopey girl."

    show suzu_veryangry_d at twoleftsit with charamove
    hide suzu_neutral_d at twoleftsit
    show hisao_smile at tworightsit with charachange
    hide hisao_heh at tworightsit

    "Suzu glowers at me, but it isn't unexpected. I just chose the one who resembled her the most, after all."

    "Oh yeah, I meant to find out her type. I ended up indirectly teasing her, instead. Whoops."

    "Hisao just gives a smile, content to let us pick at each other."

    hi "So what's there to do around here, anyway? Seems like a pretty nice place."

    show suzu_speak_d at twoleftsit with charachange
    hide suzu_veryangry_d at twoleftsit

    suz "There's a ridiculous number of restaurants. A museum, as well."

    mk "Don't forget the beach."

    suz "That too. Did you pack swimwear?"

    hi "Yeah."

    mk "Only because I reminded him at the last minute."

    show suzu_concerned_d at twoleftsit with charachange
    hide suzu_speak_d at twoleftsit
    show hisao_erm at tworightsit with charachange
    hide hisao_smile at tworightsit

    hi "You didn't have to mention that..."

    "As we yak away on the couch, a very particular smell enters the room. The kind that irritates your nose and throat just enough to demand your attention. The slightly acrid edge it has makes it unmistakable."

    "Being the first to apparently catch it, I turn around to see the source. Sure enough, Suzu's sister enters with a cigarette perched in her mouth, shoving the packet and lighter into her hoodie pocket."

    "The attention of the others is finally drawn as she inhales sharply and takes the cigarette from her mouth, blowing a thin wisp of smoke past her lips. Her gaze is at nothing in particular, just happy to foul up the room as she lets off steam."

    show hisao_erm at rightsit with charamove
    show suzu_concerned_d at leftsit with charamove
    show tsu_deadpan at center with charaenter

    mk "Taking a break?"

    tsu "Finished. Thank God."

    show tsu_smile at center with charachange
    hide tsu_deadpan at center

    "Replacing the stick back in her mouth, she retrieves a a thumb-drive from her pocket and flicks into the air before snatching it with her hand, apparently quite pleased with herself."

    suz "Mom and dad will kill you if they find out."

    tsu "Snitches get stitches."

    suz "The smell. It'll hang around if you do that inside."

    show tsu_ooh at center with charachange
    hide tsu_smile at center

    "The warning gives Tsubasa pause, too flushed in her victory over her project to consider that fact."

    show tsu_deadpan at center with charachange
    hide tsu_ooh at center
    show suzu_neutral_d at leftsit with charamove
    hide suzu_concerned_d at leftsit

    "She stares at her sister for a moment before giving a displeased puff in her direction, with Suzu going back to her game in response."

    show hisao_talk_small at rightsit with charachange
    hide hisao_erm at rightsit

    hi "What's all this for, anyway?"

    tsu "Uni project. I know just enough programming to keep getting stuck with the job during group assignments and projects."

    hi "You're a student?"

    tsu "Yeah, mechanical engineering."

    show hisao_smile at rightsit with charachange
    hide hisao_talk_small at rightsit

    hi "That's cool."

    show tsu_smile at center with charachange
    hide tsu_deadpan at center

    "The statement fills her with pride, her smile making the cigarette between her lips angle sharply upwards."

    tsu "You hear that, Suzu? I'm cool."

    #show suzu_grin at leftsit with charamove
    #hide suzu_neutral at leftsit

    suz "At least someone thinks you are."

    "Suzu just keeps tapping away at the controller, launching some loud group attack on a boss character. She really is good at shutting out discussion she's not interested in."

    "Used to her sister's antics, Tsubasa instead turns to Hisao once more."

    show tsu_question at center with charachange
    hide tsu_smile at center

    tsu "Hmm... you'd be into robots and stuff, right? Tell you what, how about you come see what we're working on?"

    show hisao_talk_small at rightsit with charachange
    hide hisao_smile at rightsit

    hi "Seriously? That'd be okay?"

    tsu "It isn't exactly top-secret military stuff we're doing, you know. Either of you two up for it?"

    #show suzu_normal at leftsit with charamove
    #hide suzu_neutral at leftsit

    suz "I think I'll be fine."

    mk "Neeeeerds."

    show tsu_smile at center with charachange
    hide tsu_question at center

    tsu "Tough crowd. Get your stuff and we'll be off, Nakai. No point hanging around for these two."

    show hisao_smile at right with charamove
    hide hisao_talk_small at rightsit

    hi "Sure, I'll be right out."

    hide tsu_smile #with moveoutright
    hide tsu_deadpan
    with moveoutright
    hide hisao_smile with moveoutright
    show suzu_neutral_d at centersit with charamove
    #show suzu_concerned at centersit
    #hide suzu_neutral at centersit

    "Passing by the recliner on the way, she gives Miyu a much-appreciated rub on the head before leaving. For his part, Hisao jumps off the couch and goes to grab his phone and wallet from the guest room."

    "As he returns and heads towards outside, he briefly stops to give us a wave of goodbye. I pucker my lips and make kissing motions to tease him in response, earning an obscene gesture before he disappears out the door."

    "Come to think of it, he never used to do that before. Maybe I'm starting to rub off on him."

    mk "Those two sure are getting along."

    suz "She'd be a good influence on him. Smoking aside."

    "Can't say I'm a fan of the habit either. That sort of thing used to be popular back home, but then again, it's not like there was much else do out in the sticks."

    stop music fadeout 2.0

    "Suzu's attention is wholly focused on the television in front her, right now going through some dialogue section as two characters gossip between themselves. I kind wish she was playing a shooter, or anything else that was more exciting to watch. At least this has some cute girls, I suppose."

    play music music_suzu fadein 2.0

    show suzu_surprised_d at centersit with charachange
    hide suzu_neutral_d at centersit
    pause(1.0)
    show suzu_neutral_d at centersit with charachange
    hide suzu_surprised_d at centersit

    "In a move that's probably not all that subtle, I let my left arm drop from the couch and around Suzu's other shoulder. She pauses, albeit briefly, but continues on after a badly hidden glance towards me."

    show suzu_normal_d at centersit with charamove
    hide suzu_neutral_d at centersit

    "A little smile fights for its life on her face, eventually managing to eke out a fragile existence as I hold her to my side. It proves infectious, with my own grin soon widening."

    suz "Sorry."

    mk "What's wrong?"

    show suzu_concerned_d at centersit with charachange
    hide suzu_normal_d at centersit

    suz "You'd prefer me to be more affectionate, wouldn't you?"

    mk "I wouldn't exactly say no, but you are what you are. If you're not the touchy-feely type, that's fine."

    "She falls silent, the game's music as a battle starts being the only sound in the room."

    mk "We both know that's bullshit, don't we?"

    mk "He's fine with it, you know. Hisao, that is."

    suz "I know. I just..."

    "As she looks down, I become increasingly doubtful of my reasoning. I'm sure being... that way inclined plays a part, but even if she liked men, her distrust of others would still be there."

    "I don't like that fact at all. I know that if she doesn't deal with it at some point, it's going to take over her entire life. That's a large part of why I've tried to work it out of her, after all."

    "But even if it's incredibly selfish, I can't help but treasure, just a little, how she's opened up to me. She chose me as the only person she's willing to show herself to. Wouldn't anyone be thankful for that?"

    suz "What happened earlier?"

    mk "With your mother?"

    "She gives a nod. That's the very last topic I wanted to talk with her about, let alone now of all times. The more I think about it, the deeper the barbs go from what she told me, but I can't let Suzu bear that burden. It's not her fault."

    "Doing my best to gin up a lie on short notice, I shrug my shoulders."

    mk "Just going off at me about being a lout. Could've been worse."

    show suzu_neutral_d at centersit with charamove
    hide suzu_concerned_d at centersit

    "Suzu glances at me, but seems to take the statement at face value as she goes back to her game."

    "Whether to reassure myself or her, I bend down and give an affectionate peck on her cheek."

    stop music fadeout 2.0

    show suzu_embarrassed_d at centersit with charamove
    hide suzu_neutral_d at centersit

    play music music_aria

    "Her reaction isn't quite what I'd expected; with her fingers slipping off the buttons and joystick, she looks up to me with a hopeful, almost yearning expression. It takes some effort for her to maintain eye contact, forcing herself to look me in the eyes."

    scene black with shuteye

    "My heart skips a beat as I begin to lean in, my last sight being of her rosy cheeks and delicate lips before I close my eyes."

    play sound sfx_pillow

    "And so, I press my lips to those of Suzu, the controller falling to the floor with a thud."

    "As we kiss, my lust finally gets the better of me as I push my tongue forward, passing my own lips and pushing into Suzu's."

    "Suzu's body jerks as I make the move, but her hesitation soon melts as she responds in kind, her tongue moving around inside my mouth and pressing against my own tongue. She doesn't seem to really know what to do with it, her innocence only spurring me to excite her more and more."

    "As I press my mouth against hers, I can feel Suzu's breath tickling my face and her body heaving from the desire running through it. Her controller lies on the floor forgotten as her hands hold me, one on my side and the other to my cheek."

    "The two of us part with almost identical timing, our faces flushed and breathing heavy."

    "I can feel my heart tighten as I look at her face. The way her eyes look up at my own, loose hairs hanging as she pants in excitement through those slightly open lips, entirely too taken with the situation to bother trying to compose herself. It's surprising how little it takes to make her completely flustered, and all the more endearing."

    "I push myself on her once more, the two of us making out without a care for the outside world. I didn't think someone like her would find this sort of thing fun, but then again, it isn't the first time she's surprised me."

    "My hand on her waist slips downward, taking in the feeling of her leg as it slowly moves along her thigh. Attempting to sate my lust by rubbing up and down her thigh only makes me more excited, as does the weak whimper escaping from her mouth."

    "I want her. I want all of her. I want to take this girl for myself."

    "Not content with her cute leg, my hand slips from the top of her thigh to the inside, my heart beating faster and faster as my hand ever so slowly slides further upwards, my tongue chasing her own as she desperately attempts to escape for so much as a breath."

    "The tips of my fingers disappear under her dress, brushing against her thin underwear, the feeling of everything underneath clear to the touch."

    "A sharp inhalation gives me pause, suddenly breaking me out of my relentless advance on her. Sensing something's up, I pull back my adventurous hand and withdraw from my kiss."

    scene bg city_houseint with dissolve
    show suzu_veryembarrassed_d at centersit with charaenter

    "Suzu's body is completely frozen, one hand on the couch supporting her body, the other raised defensively in front of her as she leans back. Her eyes flit to mine and then away, unable to keep contact for more than a second."

    "I open my mouth to speak, but once again find myself unable to find words. All I can do is frantically stuff down my desire as I try to work out how to settle the panicked rabbit before me."

    mk "Sorry, I didn't..."

    "Didn't what? There are a lot of things I didn't do. While she was obviously content with making out, I let myself become consumed by my libido, pushing myself on her without a word. She's never done this before, and hell, tends to skirt the mere mention of anything remotely sexual in conversation."

    "I try to force a grin to lighten the mood, but as I do so, I notice the telltale signs that doing so will be entirely pointless."

    show suzu_asleep_d at centersitlow with charamove
    hide suzu_veryembarrassed_d at centersit

    "Sure enough, the muscles in Suzu's face relax and her eyelids close, her arm buckling soon after. Suddenly limp as a rag, she flops backward onto the couch like a lifeless doll, one arm over her stomach as the other haphazardly drops over the side."

    stop music fadeout 3.0

    "Well. That's that."

    "I let my head droop in defeat, looking at her unconscious body for a while before picking up the long-forgotten controller. As if to make the situation as awkward as possible, the dog decides now is the best time to start snoring loudly, reminding us of her presence."

    "Sitting the thing in my lap in practiced fashion, I use my stump to carefully move the left stick and operate the buttons with my hand, managing to, eventually, save the game. As it writes to the memory card, a movement from the corner of my eye draws my eyes from the television."

    show suzu_sleepy_d at centersit with charamove
    hide suzu_asleep_d at centersitlow

    "With her muscle control returned to her, Suzu brings her arm over her face, hiding her eyes underneath. She doesn't say a word, nor make any other movement."

    "Bereft of anything to say that could make the mood any better, I decide to just avoid the topic completely."

    mk "Mind if I choose the next game?"

    suz "Do as you want."

    ##centered "~ Timeskip ~" with dissolve
    scene bg suzu_bedroom with shorttimeskip
    show suzu_neutral_d with charaenter

    play music music_comfort

    "Having settled in for the night, Suzu lies at the end of the bed on her stomach watching TV. The small flatscreen, perched on a low dresser at the end of the room, is unsurprisingly tuned to some late-night animated series."

    "It's kind of cute how she gets so taken with whatever she's doing. From studying to games, she really does take everything in her life seriously."

    "As for me, I just lay on my back with my head propped up on the bed head, arms bent back providing a makeshift cushion for my head. The show's interesting enough to hold my attention, even if it is a bit artsy for my liking."

    mk "Aren't you tired? It's getting pretty late."

    suz "If you want to sleep, I can just record it."

    mk "That's not what I'm asking."

    suz "I'm fine."

    "Annoyed with her brushing off my concern for her, I read out with my foot and poke Suzu's butt with my big toe."

    hide suzu_neutral_d with moveoutbottom
    with vpunch
    play sound sfx_impact

    "Her reaction is both immediate and startling, a loud sound coming from her that'd be best described as a squeak as she suddenly lurches forwards and topples off the bed as she twists around and scrambles for a handhold."

    "The ordeal ends with a thud as she crashes onto the floor, the silence afterwards making me more than a little concerned."

    mk "Hey, Suzu? You okay down there?"

    show suzu_angry_d at centersitlow with easeinbottom

    "The top half of her head slowly rises from behind the end of the bed, her annoyed eyes just visible as she glares at me over the sheets. I just smile."

    mk "C'mon, don't be like that."

    show suzu_veryangry_d at centersitlow with charachange
    hide suzu_angry_d at centersitlow

    "My remark only serves to make Suzu furrow her brow even further. I guess she really is mad."

    "I doubt it's from my poking her, though. Her reaction was completely out of proportion, making me think that she had something else on her mind. Without her having told me what's bothering her, all I can do is take a wild stab at it."

    mk "Look, I'm sorry about what happened earlier. I didn't mean to come onto you that fast."

    show suzu_unhappy_d at centersitlow with charachange
    hide suzu_veryangry_d at centersitlow

    "The side of my mouth twitches as I hope I've latched onto the right problem, but her sighing shows that I've missed the mark."

    "Sitting her chin on the sheets and laying her arms out in front of her, she looks to me with a resigned expression, having given up on letting me finding the answer myself."

    stop music fadeout 3.0

    suz "Why do you insist on coddling me like a child? It's bad enough when my parents do it."

    mk "Huh?"

    suz "This morning. I heard what mom told you."

    mk "I was going to tell you."

    "Suzu looks at me with suspicion."

    mk "I mean it! It just didn't feel like the right time."

    suz "Why does everyone think I'm so fragile?"

    mk "Well, I mean... that's not totally without reason."

    "I should not have said that. I so should not have said that."

    show suzu_glare_d at center with charamove
    hide suzu_unhappy_d at centersitlow

    "As she stands up, looking at me with a dark face, I quickly sit up and try to think of something to cover my ass. It's true, though; someone like me has trouble accounting for her innocence, and her condition. It hurts a little to think how someone more laid back and thoughtful would've been such a better fit for her than I."

    scene black with dissolve

    play music music_to_become_one

    "Before I can mumble any sort of half-hearted apology, Suzu does the last thing I expected. Standing at the foot of the bed, she begins to undo the buttons of her pyjama top."

    "Taken completely off guard, and perhaps a little swayed by wanting her to continue, all I can do is watch as she slowly and silently undoes button after button."

    "Upon unfastening the last, she shrugs off her top and lets it drop to the ground, revealing her petite breasts. My heart is practically in my mouth, her stripping evidently not yet finished as she works off her pyjama bottoms with her panties."

    "With every inch of her bared before me, she stands simply with her arms hanging by her sides. Despite her blushing, she looks to me with an expression of sincere disapproval, is if to silently scold me."

    "This is the same girl who had a cataplexy attack when I tried to come onto her, right? I've seen her body before, in showers and changing rooms, but she has an essence of eroticism around her that she never had before."

    mk "Suzu..."

    suz "You want to do this with me, right?"

    "All I can do is gulp. Knowing the way she is, it's totally impossible that she's ever done this before. That in itself makes me admire her gumption in doing such a thing."

    "As the seconds tick by, I begin to notice the cracks in her facade. The way she fiddles with her fingers, her uneven breathing, the way her cheeks become ever more flushed. In spite of all that, she still forces herself to keep eye contact."

    mk "If you're not ready, I don't want to-{w=.40}{nw}"

    suz "I am ready. I want to do this with you, Miki."

    "Ah, that's what her face reminds me of. A petulant child, annoyed that her latest petty wish isn't being obeyed. A smile spreads across my face as I realise that she's acting just the way she always does."

    "Suzu's a spoiled child, after all. Always had been. That's not necessarily a bad thing, though; it's what's given her such a pigheaded nature, after all."

    "That's what makes me sure that Suzu isn't just offering herself up to me. She wouldn't push herself so hard if she didn't want to do this, and even if she may be more modest than I about her body, that doesn't mean she lacks her own desire for sex. It's surely played on her mind before."

    suz "What are you smiling about?"

    mk "You really need to lighten up, you know that?"

    "She flowers into a full blush as the facade falls, looking away to hide her embarrassment for taking this so seriously compared to me."

    "I take the opportunity to take my own clothes off, her interest piqued as my tank top comes off and gets thrown to the floor. She has trouble avoiding staring at my breasts as I work off my shorts, my panties following both onto the floor in short measure."

    "I can't help but imagine how I'd be run out of the house if her parents discovered us naked like this, indulging in the very last thing they'd want me doing with their precious daughter. Here we are, though, taking in the sight of each other's bodies."

    mk "You're beautiful, Suzu."

    "The words are as sincere as could be. Her smooth, lithe body is a harsh contrast to my own, her complexion pale compared to my tanned skin. She isn't especially curvaceous, nor mature looking by any definition, but she does have an unpretentious charm to her dainty figure."

    "Not that I'm ignorant of what Suzu sees in me. I suppose I should acknowledge the bonuses of puberty as well as the minuses, as having a body I like looking at myself is always a pleasure."

    "I reach out to the bashful girl bidding her to join me. She promptly does so, clambering onto the bed and pressing her lips to mine in the most brief of kisses."

    "It's not her kiss that sets me aflutter, though. Rather, the way she reaches out and brings her hand under my cheek, brushing it with her fingers. The love in her eyes is unmistakable, leaving me utterly speechless. I've never seen someone look at me like this before."

    "I must have a really dumb smile on my face. With a wonderful warmth flowing through me, all I can do is stroke her hair in response."

    suz "I love you, Miki."

    mk "I know."

    "I try to grin and play it off, but she's making it obvious that she wants me to say those words. Suzu's really got me wrapped around her little finger to make me the bashful one."

    mk "I love you too."

    "I follow up by pushing my chin forwards just little. Suzu takes the hint as she gingerly closes her eyes, my mouth pressing to hers in short measure."

    "An affectionate peck is followed by a much more adult kiss, our desire for each other being indulged. She moves to pull her face away, but I gently bite her lip before going on to press mine to hers once more."

    "Only when I've had my fill do I let her go, her face flushed and breathing heavily."

    suz "Miki..."

    "It's obvious that there's no going back now. As she looks to me with those dreamy eyes, I bring my hand to her side and guide her into my lap."

    "Content to follow my lead, nuzzles the side of her face against mine as I hold my arms around her. The smell of shampoo plays on my nose, the feeling of her soft skin against mine filling me with lust."

    "The girl just sighs as I bring my mouth to the base of her neck, meekly tilting her head to allow me. The television ahead blares away as I lick at her skin, still warm from her bath. As she starts moving about in my lap, I realise she's taking in the feeling of my breasts against her back."

    "I almost laugh, her awkward attempts to push past her prudishness making me hold her all the tighter."

    "Hoping that getting her more excited will help her loosen up, I move my hand over her breast, at first cupping it and feeling out its contours before gently kneading it. She whimpers a little, but the way she starts to settle down seems to show it's working."

    "Tweaking at her nipple starts to excite even me, a moan escaping her lips showing that she enjoys it just as much. Slowly but surely she begins to let herself go, letting me play with her supple body as I wish."

if persistent.adultmode:
    scene bg 4150 with dissolve

    "As she begins to fidget about, the sight of the area between Suzu's legs becomes inviting. I've never pleasured a girl before, only able to go by what I enjoy doing with myself. I have little choice but to learn, though, as my hand begins to inch down her stomach."

    "She goes quiet out of anxiety as my fingers slide downwards, gently brushing through her lower hair before reaching my goal."

    "Her breath catches and muscles tense as my fingers slide between her legs, the mere fact I'm touching her down there making my own heart skip a beat. I desperately want to avoid hurting Suzu, but my own lusts are starting to get the better of me."

    "I begin to delicately stroke her nub, being as delicate as I possibly can. Her excitement has already left my fingers faintly moist, evidently already taken by the experience."

    "Her quiet nature makes it terribly hard to gauge if she's enjoying this. Worried that it's a sign, I adjust my motions and begin pressing a little harder, eventually moving my fingers further afield to stimulate other parts as well."

    "A momentary quiver shooting through her body almost makes me stop in fear that I've hurt her, but it passes as soon as it came. Her hips begin to move and fidget, her ecstasy slowly escalating."

    mk "Is this right?"

    suz "Don't speak..."

    "I smile at her breathless words as she squirms in my lap."

    "Suzu's breaths becoming faster and moans more frequent, a slight sweat forming on her skin. I quickly pat her a few times  to excite her further before returning to rubbing, my motions settling on a speed and motion. With her body beginning to heave and tighten in my grasp, I can only guess she's nearing the end."

    suz "Miki... Nnnnnn..."

    "She can't close her mouth any more for her frantic breathing, her attention wholly focused on the welling ecstasy within her. Little by little she gets further to the edge, her moaning getting increasingly impossible to suppress."

    "As her thighs begin to quiver, it should only take a little more, and..."

    suz "Ah... Aaaaahn!"

    "Suzu's body tenses unmistakably as her breath catches, her voice going silent as she desperately clutches at the peaking climax, every sense overtaken by the rush of euphoria."

    "She clutches frantically at that wonderful feeling as it begins to wane, but inevitably and ever so slowly... it leaves her."

    scene black with dissolve

    "Suzu's body slumps in my arms as the excitement ebbs away, a little effort being needed to keep her upright in my arms. I give her an affectionate peck on the cheek, satisfied that she seems to have enjoyed herself."

    "It's so rare that I get to see her with her guard completely lowered, but today, at this moment, I can finally say she's given in. What I saw when it did could only be called one thing."

    "Interested to see what she has to say for herself, I tilt my head over her shoulder to try and catch a glimpse of her face. It earns me a sideways glance, her look one of both physical and emotional exhaustion."

    mk "Thank you, Suzu. I'm glad I got to do this with you."

    "She just nuzzles her head against mine, but I don't mind. That's all the answer I need, after all."

    "As the afterglow begins to wear off, she twists and kisses me once more, her hands taking weak hold of my shoulders."

    mk "Suzu...?"

    suz "You want to as well, don't you?"

    mk "You don't have to-"

    "What am I saying? Of course she isn't forcing herself. She wants to. I can only guess how long she's yearned for this moment."

    "Playing with her has left me excited, I can admit that much. Making the best of it, I reach out and bring my hand around Suzu's head, drawing her in for another kiss."

    "She she moves down to kiss my collar, I uncross my legs and let myself sit back while supporting myself with my hand and stump. Suzu can take this at her pace, her gaze already focused on my body rather than my eyes."

    "My chest is the next area of her exploration, one hand supporting her as the other feels out and kneads my left breast. She brings her mouth towards it, sucking and licking before playing at my nipple with her tongue. The sight of her combined with the pleasure of her teasing at it makes me giggle."

    suz "Is this... wrong?"

    mk "I was just thinking how curious you look."

    mk "It feels nice, Suzu. You shouldn't worry so much."

    "She hesitates, before pressing her lips to my breast as a parting goodbye. The feeling of her spit evaporating off is wonderful, the cool sensation a contrast to the warm summer air."

    "Next is my stomach, her face held so close that she might almost be touching it as she lays down."

    "She hesitates a moment before moving downward, not from nerves, but as if to engrave its feeling onto her mind as she runs her hand over it. It's not my most feminine feature, admittedly, but my toned body is one of the few things I've manage to keep from my days before Yamaku. That she seems to like it makes me a little glad."

    "Her hand brushes against my untidy hair, stopping before going any further. My only answer to her questioning eyes, as if she needed permission to advance any further, is to grin."

    "She takes a moment to get her bearings, before reluctantly moving her head forwards. Even the air from her nose brushing against my hair and crotch is enough to make me shudder, the area already covered in a heavy dew from our messing about."

    scene bg lewd with dissolve

    "Starting with a mere kiss before beginning in earnest, she begins to timidly and slowly lap between my legs, her hands resting on the inside of my thighs."

    "Her nervousness about whether she's doing everything correctly makes it hard to even look at her. I suppose I shouldn't complain, given that I was thinking just the same way."

    "I just give an indulgent smile as she goes, her eyes eventually closing as she becomes more comfortable. I don't think she really knows what she's doing, beyond what she might have seen in some lewd media or another, but it feels nice in any case. I'm not sure how much time passes as I let myself drift in this intoxicating sensation, nor do I care."

    "A suddenly piercing feeling draws me out of my trance, Suzu's fingers having become abruptly adventurous as she burrows two inside of me."

    suz "Sorry, is this...?"

    mk "Just keep going."

    "She doesn't look wholly convinced, but decides to go along with it. I can't decide whether the feeling is good or bad as her fingers haphazardly move inside of me, the occasional touched nerve giving me an involuntary giggle as she goes."

    "It might be in the most reluctant of ways, but the fact she's willing to try and experiment in making me feel as best she can makes me a little happy."

    "She pulls them out after her curiosity is sated, my back arching as a wave of pleasure suddenly overcomes me. Her tongue finds a damn good motion, and she thankfully manages to catch it."

    mk "Suzu... More..."

    "My entire body begins to move and shiver in anticipation, pleasure emanating from that one spot."

    "The look in Suzu's eyes, a mixture of embarrassment, passion, and curiosity only makes it all the harder to hold on. I can feel her tongue on my nub, her lips covering mine, hands pressing against my legs as they begin to shake. More... I just want to feel Suzu more..."

    "I'm close, I can feel it just dancing on the edge of my grasp. Just a little further.... Just a little..."

    mk "Aaah!"

    scene black with dissolve

    "As if having fallen into a deep ocean, the world drops away as a surge of pleasure washes over my entire body and overwhelms every sense. For a precious few seconds I bask in the bliss running through me, my muscles clenching as if to hold tight to that most wonderful feeling."

    "But as the seconds pass, so too does the rush of emotion. I desperately clutch at the last dregs of pleasure as they begin to leave me, savouring what little I can as normality begins to seep in."

    "The sweat against my skin begins to sting, the cold air around my bare legs being the next feeling to enter my consciousness. Every breath is a laboured effort, and with my muscles feeling unbearably weak, I let myself fall back onto the bed."

    "My view of the ceiling lasts only a moment, with Suzu's face taking up my sight as she clambers on top of me. Her face, as always, is that inscrutable stoic expression."

    "I just give a dumb smile as I reach up, brushing her dishevelled hair as a few hairs hang past her face. As much as I might try, I can't quite find the words I want to say."

    stop music fadeout 2.0

    "Well, whatever. Words were overrated anyway."

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

else:
    scene bg doggo with dissolve

    "As she begins to fidget about, the sight of the area between Suzu's legs becomes inviting. I've never pleasured a girl before, only able to go by what I enjoy doing with myself. I have little choice but to learn, though, as my hand begins to inch down her stomach."

    "She goes quiet out of anxiety as my fingers slide downwards, gently brushing through her lower hair before reaching my goal."

    "Her breath and muscles tense catches as my fingers slide between her legs, the mere fact I'm touching her down there making my own heart skip a beat. I desperately want to avoid hurting Suzu, but my own lusts are starting to get the better of me."

    "I begin to delicately stroke her nub, being as delicate as I possibly can. Her excitement has already left my fingers faintly moist, evidently already taken by the experience."

    "Her quiet nature makes it terribly hard to gauge if she's enjoying this. Worried that it's a sign, I adjust my motions and begin pressing a little harder, eventually moving my fingers further afield to stimulate other parts as well."

    "A momentary quiver shooting through her body almost makes me stop in fear that I've hurt her, but it passes as soon as it came. Her hips begin to move and fidget, her ecstasy slowly escalating."

    mk "Is this right?"

    suz "Don't speak..."

    "I smile at her breathless words as she squirms in my lap."

    "Suzu's breaths becoming faster and moans more frequent, a slight sweat forming on her skin. I quickly pat her a few times  to excite her further before returning to rubbing, my motions settling on a speed and motion. With her body beginning to heave and tighten in my grasp, I can only guess she's nearing the end."

    suz "Miki... Nnnnnn..."

    "She can't close her mouth any more for her frantic breathing, her attention wholly focused on the welling ecstasy within her. Little by little she gets further to the edge, her moaning getting increasingly impossible to suppress."

    "As her thighs begin to quiver, it should only take a little more, and..."

    suz "Ah... Aaaaahn!"

    "Suzu's body tenses unmistakably as her breath catches, her voice going silent as she desperately clutches at the peaking climax, every sense overtaken by the rush of euphoria."

    "She clutches frantically at that wonderful feeling as it begins to wane, but inevitably and ever so slowly... it leaves her."

    scene black with dissolve

    "Suzu's body slumps in my arms as the excitement ebbs away, a little effort being needed to keep her upright in my arms. I give her an affectionate peck on the cheek, satisfied that she seems to have enjoyed herself."

    "It's so rare that I get to see her with her guard completely lowered, but today, at this moment, I can finally say she's given in. What I saw when it did could only be called one thing."

    "Interested to see what she has to say for herself, I tilt my head over her shoulder to try and catch a glimpse of her face. It earns me a sideways glance, her look one of both physical and emotional exhaustion."

    mk "Thank you, Suzu. I'm glad I got to do this with you."

    "She just nuzzles her head against mine, but I don't mind. That's all the answer I need, after all."

    "As the afterglow begins to wear off, she twists and kisses me once more, her hands taking weak hold of my shoulders."

    mk "Suzu...?"

    suz "You want to as well, don't you?"

    mk "You don't have to-"

    "What am I saying? Of course she isn't forcing herself. She wants to. I can only guess how long she's yearned for this moment."

    "Playing with her has left me excited, I can admit that much. Making the best of it, I reach out and bring my hand around Suzu's head, drawing her in for another kiss."

    "She she moves down to kiss my collar, I uncross my legs and let myself sit back while supporting myself with my hand and stump. Suzu can take this at her pace, her gaze already focused on my body rather than my eyes."

    "My chest is the next area of her exploration, one hand supporting her as the other feels out and kneads my left breast. She brings her mouth towards it, sucking and licking before playing at my nipple with her tongue. The sight of her combined with the pleasure of her teasing at it makes me giggle."

    suz "Is this... wrong?"

    mk "I was just thinking how curious you look."

    mk "It feels nice, Suzu. You shouldn't worry so much."

    "She hesitates, before pressing her lips to my breast as a parting goodbye. The feeling of her spit evaporating off is wonderful, the cool sensation a contrast to the warm summer air."

    "Next is my stomach, her face held so close that she might almost be touching it as she lays down."

    "She hesitates a moment before moving downward, not from nerves, but as if to engrave its feeling onto her mind as she runs her hand over it. It's not my most feminine feature, admittedly, but my toned body is one of the few things I've manage to keep from my days before Yamaku. That she seems to like it makes me a little glad."

    "Her hand brushes against my untidy hair, stopping before going any further. My only answer to her questioning eyes, as if she needed permission to advance any further, is to grin."

    "She takes a moment to get her bearings, before reluctantly moving her head forwards. Even the air from her nose brushing against my hair and crotch is enough to make me shudder, the area already covered in a heavy dew from our messing about."

    "Starting with a mere kiss before beginning in earnest, she begins to timidly and slowly lap between my legs, her hands resting on the inside of my thighs."

    "Her nervousness about whether she's doing everything correctly makes it hard to even look at her. I suppose I shouldn't complain, given that I was thinking just the same way."

    "I just give an indulgent smile as she goes, her eyes eventually closing as she becomes more comfortable. I don't think she really knows what she's doing, beyond what she might have seen in some lewd media or another, but it feels nice in any case. I'm not sure how much time passes as I let myself drift in this intoxicating sensation, nor do I care."

    "A suddenly piercing feeling draws me out of my trance, Suzu's fingers having become abruptly adventurous as she burrows two inside of me."

    suz "Sorry, is this...?"

    mk "Just keep going."

    "She doesn't look wholly convinced, but decides to go along with it. I can't decide whether the feeling is good or bad as her fingers haphazardly move inside of me, the occasional touched nerve giving me an involuntary giggle as she goes."

    "It might be in the most reluctant of ways, but the fact she's willing to try and experiment in making me feel as best she can makes me a little happy."

    "She pulls them out after her curiosity is sated, my back arching as a wave of pleasure suddenly overcomes me. Her tongue finds a damn good motion, and she thankfully manages to catch it."

    mk "Suzu... More..."

    "My entire body begins to move and shiver in anticipation, pleasure emanating from that one spot."

    "The look in Suzu's eyes, a mixture of embarrassment, passion, and curiosity only makes it all the harder to hold on. I can feel her tongue on my nub, her lips covering mine, hands pressing against my legs as they begin to shake. More... I just want to feel Suzu more..."

    "I'm close, I can feel it just dancing on the edge of my grasp. Just a little further.... Just a little..."

    mk "Aaah!"

    "As if having fallen into a deep ocean, the world drops away as a surge of pleasure washes over my entire body and overwhelms every sense. For a precious few seconds I bask in the bliss running through me, my muscles clenching as if to hold tight to that most wonderful feeling."

    "But as the seconds pass, so too does the rush of emotion. I desperately clutch at the last dregs of pleasure as they begin to leave me, savouring what little I can as normality begins to seep in."

    "The sweat against my skin begins to sting, the cold air around my bare legs being the next feeling to enter my consciousness. Every breath is a laboured effort, and with my muscles feeling unbearably weak, I let myself fall back onto the bed."

    "My view of the ceiling lasts only a moment, with Suzu's face taking up my sight as she clambers on top of me. Her face, as always, is that inscrutable stoic expression."

    "I just give a dumb smile as I reach up, brushing her dishevelled hair as a few hairs hang past her face. As much as I might try, I can't quite find the words I want to say."

    stop music fadeout 2.0

    "Well, whatever. Words were overrated anyway."

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_S6:

    scene city_houseint with dissolve
    show suzu_neutral_d at twoleftsit
    show hisao_disappoint at tworightsit
    with charaenter

    play music music_tranquil

    "With Hisao, Suzu and I lazing about the living room while watching a movie, a pleasant sense of routine has come over the Suzuki household."

    "While things have improved slightly from the heavy stuff around my arrival, it'd be a lie to say everything's back to normality. Now that the dust has settled, it seems her parents are simply ignoring my existence before I'm out of their hair for good."

    "Questions such as whether I deserve that treatment or not are irrelevant now. I've never been one to ponder how the world isn't or how it should be, only how it is."

    "Hisao's interest in what's playing is about as low as it could be while still being polite, his attention more on patting the sleeping dog in his lap than anything else. Having no such worries, I loudly begin to snore."

    suz "Be quiet."

    "Her placid face holds, holding her knees to her chest as she watches the television ahead of us with total concentration."

    "I don't even see the appeal of this. Sure, she likes romantic shows and the usual sappy crap, but this is the most delightfully boring show she's inflicted on me yet. Set in Victorian England, it seems to be about some fancy estate this rich woman wants to keep."

    "I think, anyway. It's gone on so long that I've started to lose track."

    mk "Hisao, what's the appeal in this?"

    "He just shrugs, content to relax in the recliner with his new furry friend."

    hi "Don't ask me."

    mk "Suzu...?"

    suz "It's a nice setting. The houses and outfits are pretty, too."

    "Nerds are so weird."

    "As much as I'd like to complain further, I did get my choice of movie before this, so I guess she has to have her turn."

    "Accepting my fate and doing my best to avoid falling asleep before it ends, a familiar smell enters the room. 'Musty' would be the best word for it. Miyu's head perks up, practically trained to recognise the scent."

    show suzu_neutral_d at leftsit with charamove
    show hisao_disappoint at rightsit with charamove
    show tsu_deadpan at center with moveinright

    "Sure enough, Tsubasa strolls into the room with a cigarette perched in her mouth. She takes a hold of her shoulder before rolling her arm about in its socket to try and free up the joint."

    show hisao_smile_teeth at rightsit with charachange
    hide hisao_disappoint at rightsit

    hi "You're not old yet."

    tsu "I sure feel like it."

    "She grabs her neck next, tilting her head from side to side. University sure seem to take its toll on her."

    suz "You shouldn't do that inside. Mom and dad'll kill you if they find out."

    show tsu_annoyed at center with charachange
    hide tsu_deadpan at center

    tsu "Snitches get stitches."

    suz "I mean the smell. It sticks around."

    show tsu_ooh at center with charachange
    hide tsu_annoyed at center

    "Tsubasa looks a little surprised at her sister's looking out for her. She really should just kick the habit already."

    "She takes the cigarette from her lips and gives a haughty puff, her focus moving from her sister to the television as dramatic music suddenly plays. Perhaps the only interesting thing in the movie happens, with a bookcase falling on some guy."

    show tsu_deadpan at center with charachange
    hide tsu_ooh at center

    tsu "Ouch."

    tsu "Anyway, I'm taking the dog for a walk. You kiddoes want to come?"

    show miyu_happy with moveinbottom

    "Miyu catches the key word, excitedly leaping off Hisao and tearing up to Tsubasa with its tail flicking wildly."

    show tsu_question at center behind miyu_happy with charachange
    hide tsu_deadpan at center

    "With Suzu's attention remaining wholly on what's happening on the screen, she doesn't notice the pointed way her sister locks eyes with me. Wanting to escape the house and get some sun anyway, I shrug and accept."

    mk "Sure."

    show hisao_talk_small at rightsit with charachange
    hide hisao_smile_teeth at rightsit

    hi "It's over."

    mk "Huh?"

    "I turn around to see the television once more, the credits having finally begun to scroll."

    mk "Thank God. How bloody long was that thing?"

    show suzu_speak_d at leftsit with charamove
    hide suzu_neutral_d at leftsit

    suz "It was only two hours. Can you really not sit in one place that long?"

    hide miyu_happy with moveoutbottom
    show tsu_annoyed at center with charachange
    hide tsu_question at center

    tsu "Can you two stop picking on each other? I'm about to go."

    "Miyu's started running about the room in anticipation, her lead trailing behind her."

    mk "Coming!"

    show suzu_smile_d at leftsit with charachange
    hide suzu_speak_d at leftsit

    suz "I'll come too."

    "As Suzu looks at me, I find myself slightly pleased by her eagerness. She isn't the type to enjoy going outside and getting exercise for its own sake, after all."

    stop music fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve
    scene bg suburb_road with shorttimeskip
    show suzu_normal_d at twoleft
    show tsu_deadpan at tworighttsu
    show miyu_happy
    with charaenter

    play music music_normal

    "With Hisao deciding the allure of Suzu's game collection was greater than his want to take a walk with us, she, her sister, and I end up making a misshapen trio as we walk along the sun-baked street."

    "Suzu takes command of Miyu as the dog stops every so often to sniff at this or that, while her sister smokes away with her hands in her pockets. As for me, I continue my reading of a manga I scavenged from her room."

    mk "Hey, Suzu... why do you like this stuff?"

    show suzu_concerned_d at twoleft with charachange
    hide suzu_normal_d at twoleft

    suz "Do you have to insult my tastes all the time?"

    mk "I mean it, I seriously don't understand."

    mk "Like, take this one. A girl goes to a cafe, mopes a bit, gets a coffee refill from the waitress, then leaves after they tell each other their names."

    show suzu_happy_d at twoleft with charachange
    hide suzu_concerned_d at twoleft

    suz "Ah, that one. I like that chapter."

    "Her voice lilts a little, the mere thought of it enough to please her."

    mk "And that's it? There's no more chapters?"

    suz "It's a short story about hope and budding romance between passing strangers. There are no more chapters."

    mk "...They told each other their names."

    "Miyu stops to pee on a flower that apparently deserved a bit of watering. Tsubasa just lets her gaze wander around the houses lining the suburb street. It's almost maddeningly pedestrian."

    "It probably means nothing to Tsubasa, but after so long living within the school campus and nearby town, what passes for normality takes on a new significance. Maybe that's one of the reasons I wanted to come here beyond Suzu; a chance to live the normal middle-class life I've never had, at least for a time."

    show suzu_normal_d at twoleft with charachange
    hide suzu_happy_d at twoleft
    show suzu_normal_d at left with charamove
    show miyu_normal with charachange
    hide miyu_happy
    show miyu_normal at left with charamove

    "I turn out to be a lost cause for Suzu as she tugs at an obstinate Miyu, eventually managing to get her to walk once more."

    "Noticing Tsubasa walking a little slower than usual, I match her pace as we end up falling a few more yards behind the other two. Our voices are little more than a whisper."

    mk "So what's up?"

    tsu "It really should be dad following this up, but with things as they are..."

    "Oh, so it's about that. Arrangements regarding medication and other ways of dealing with her narcolepsy have generally fallen to her father to manage. It feels really dumb to need her sister to act as an intermediary, but that's the way things stand."

    show miyu_happy at left with charachange
    hide miyu_normal at left
    show miyu_happy at leftoffmiyu with charamove
    show suzu_speak_d at left with charachange
    hide suzu_normal_d at left

    "She starts telling Miyu off for struggling to reach a middle-aged man walking on the other side of the road, making it clear she's not listening in on us."

    mk "Shoot."

    tsu "How's she been?"

    mk "There's one thing I want to tell you, and another I should tell you."

    mk "It's hardly scientific, but she hasn't been great lately. She's been trying to hide it, too."

    show suzu_normal_d at left behind miyu_happy with charachange
    hide suzu_speak_d at left
    show miyu_happy at left with charamove
    show tsu_hmm at tworighttsu with charachange
    hide tsu_deadpan at tworighttsu

    "The cigarette in her mouth takes on a distinct downward slant."

    tsu "Guess I'll report that back to the mothership, then. Her doctor wanted to try a new regime, so I guess it's not working."

    tsu "What a pain..."

    mk "Sorry to be the bearer of bad news."

    tsu "What about you, anyway? You're chipper as always."

    mk "Can't keep me down for long."

    show tsu_tooth_smile at tworighttsu with charachange
    hide tsu_hmm at tworighttsu

    "My cheesy grin seems to lighten her mood. It's true that missing a hand causes a lot of day-to-day annoyances, but at least I don't have to take drugs to deal with it. Both of us came off better than Hisao, too."

    tsu "Thoughts gone to your other comrade?"

    mk "Yeah. Guy's a bit of a weird one like Suzu, I'm afraid."

    show tsu_smile at tworighttsu with charachange
    hide tsu_tooth_smile at tworighttsu

    tsu "Haha, he isn't so bad. Damned shame what happened to him, though."

    mk "You know about it?"

    show tsu_hmm at tworighttsu with charachange
    hide tsu_smile at tworighttsu

    tsu "He told me a while ago. Shitty thing to happen to such a sweet kid."

    mk "You really need to stop talking like some fifty year-old."

    show suzu_grin_d at left behind miyu_happy with charachange
    hide suzu_normal_d at left

    suz "She was born fifty years old."

    "Both of us briefly wonder how much of our conversation Suzu's caught, but she gives no indication of having heard anything untoward."

    show tsu_deadpan at tworighttsu with charachange
    hide tsu_hmm at tworighttsu

    tsu "Being mature is considered a positive thing, Suzu."

    suz "I am mature. Unlike some."

    mk "And there's the dig at me. Every bloody time."

    show tsu_smile at tworighttsu with charachange
    hide tsu_deadpan at tworighttsu
    show miyu_happy at right with charamove

    "Tsubasa just smiles at us as she takes Miyu's leash and skips on a couple of steps ahead, leaving Suzu and I to walk behind."

    "Suzu opens her handbag, allowing me to deposit the book and take her hand in mine. With that, our trio sets forth once more."

    "I really could get used to these quiet days."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_S7:
    scene bg road with dissolve
    $ renpy.music.set_volume(0.4, 0, channel="sound")

    play sound sfx_car_driving loop

    play music music_everyday_fantasy

    "With the last day at Suzu's house finally having arrived, there was little doubt at how to spend it."

    "Thankfully the trip to the beach is a short one from Suzu's house, with she and I squeezed into the back seat of her sister's car along with our stuff, and Hisao in the front. Tsubasa just taps away at the wheel as she drives, her homely hoodie thankfully shirked in favour of a light, airy shirt."

    tsu "Everyone got everything? I'm not turning back, you know."

    mk "Yes, mom."

    "I look to Suzu, her gaze directed out the car window. While she might put on her usual stoic act, it's obvious that the whole affair around her parents has taken its toll on Suzu. If nothing else, at least this trip might take her mind off things."

    hi "Not taking a swimsuit, Tsubasa?"

    "Come to think of it, Hisao's slipped into using her first name in the last few days. I barely even noticed the change."

    tsu "You sound disappointed."

    hi "Well..."

    mk "He's not the only one disappointed, you know."

    tsu "Not much for swimming, I'm afraid. Just here to cool off from uni for a bit."

    suz "All you ever think about is your university work."

    tsu "That's what uni's like, Suzu. Some day you're gonna have to go through all this, too."

    hi "Planning on following your sister into engineering?"

    suz "What? No."

    tsu "It's not that bad..."

    "I kind of want to jump into the conversation, but there's not much I can really say. Far as my mind goes, the end of Yamaku is a full stop. A period at the end of a sentence. I don't have the grades nor work ethic to make it very far."

    "Suzu just stays quiet, with Hisao and Tsubasa ending up talking between themselves. With Hisao proving a willing audience, Tsubasa tends to talk casually about this aspect of her work and that with him, occasionally wandering into other aspects of her life almost accidentally."

    "It's charming, for lack of a better term. Hard to tell if she's just using him as a scratching post or genuinely thinks fondly of him, but they seem to enjoy each other's company nevertheless."

    "It all makes me wonder how they, or any other watching us, would see the relationship between Suzu and I. The question plays on my mind for the rest of the journey."

    stop sound fadeout 0.5

    ##centered "~ Timeskip ~" with dissolve
    scene bg ishigaki_day with shorttimeskip #dissolve

    play sound sfx_beach loop ##get some waves and seagul sfx or something

    "It takes a bit of a scan to find where Tsubasa's set up the umbrella, towel, and bags, given the multitude of similar little areas set up around the beach's expanse. Looks like it's a pretty busy day, thanks to the good weather and summer holidays."

    "Parents try their best to lather their kids with sunscreen before they race off to build sandcastles and run about, a few guys have set up a beach volleyball area, and the teenage girls occupy themselves with working on their tans. I suppose I'm already covered, there."

    show hisao_beach_erm with charaenter

    "It's Hisao who helps me find the modest camp, having already changed as he stands by it and keeping a watch for us. Tsubasa becomes visible just past him as I walk up, laying back on the towel with her eyes closed as smoke wafts upwards from her cigarette."

    mk "So this is home base."

    "As Hisao nods, his gaze moves downwards from my head. I wouldn't mind if it settled on my bust given that he is a guy, especially given the black bikini showing them pretty well, but it's another part of me that he finds trouble with."

    mk "You don't need to stare, dude."

    hi "Sorry..."

    mk "Well, it's not I like don't know why. You haven't seen my stump without the bandages before, have you?"

    hi "Why do you wear them, though? I can't see any injuries."

    mk "Looks cool."

    hi "That's it?"

    mk "Isn't that a good enough reason? It's an improvement over a bare stump."

    "I shouldn't be too hard on him; assuming I'd done something to myself is reasonable enough. Even if he might still be unconvinced, I'm sure the bandaged look is definitely cooler."

    "As his eyes move off my stump and pass over the rest of my body, it's obvious he has more than a passing interest."

    mk "The stump might be new, but you have seen a girl before, right?"

    hi "I was just thinking how all that exercise sure pays off..."

    show hisao_beach_blush with charachange
    hide hisao_beach_erm

    "I give a grin and move my hips from side to side, but even as he tries to appear nonplussed, his cheeks come that little bit rosier. He can be a real prude sometimes."

    mk "You're not half bad yourself, you know."

    show hisao_beach_frown with charachange
    hide hisao_beach_blush

    hi "Aside from the scar."

    mk "C'mon, it's just a line. Nobody seriously cares about that."

    show hisao_beach_smile with charachange
    hide hisao_beach_frown

    "Something, or more likely someone, catches Hisao's attention as he leans sideways to look past me and waves."

    hi "Oh, hey Suzu."

    show suzu_beach_annoyed with moveinright
    hide suzu_beach_annoyed with moveoutleft

    "I turn to greet the girl, dressed in her usual blue and white striped two-piece, but she passes me as soon as I do so. Without so much as a word nor glance of the eyes, she walks straight past the both of us and heads for the water."

    mk "Hey, Suzu? Suzu!"

    "She doesn't respond to my voice or waving, putting me off more than a little."

    mk "I get the feeling she's not happy."

    show hisao_beach_erm with charachange
    hide hisao_beach_smile

    hi "Is that a rhetorical question? You obviously pissed her off."

    mk "Huh? How?"

    hi "It's not that hard to see why. You were being kinda flirty."

    mk "We were just talking..."

    tsu "He's right, you know."

    "Tsubasa doesn't even bother to open her eyes as she gives her input, content to expend as little energy today as possible."

    mk "Alright, fine, I'll go pick her up."

    ##centered "~ Timeskip ~" with dissolve
    scene bg 4337 with dissolve

    "I trudge back to camp with my mission accomplished, Suzu's body held under my right arm. She kicks and struggles a little, but more so out of obligation than any real attempt to work herself free. Not that she probably could, anyway."

    suz "Put me down, please!"

    mk "Later."

    suz "Now!"

    "As we reach the two waiting for us, Suzu's protestations give Tsubasa enough reason to finally open her eyes and stare at us. Hisao's expression betrays that he at least half-expected something like this."

    suz "I'm not a kid, I said put me down!"

    mk "Why are you being so aggressive all of a sudden? You don't usually complain when I manhandle you."

    suz "I'm going to have an attack if you keep this up."

    mk "Good, it'll make you easier to carry."

    "The smile on my face makes her finally give up, her head drooping in defeat."

    tsu "Just put her down. You're making a scene."

    "Oh yeah, we're on a public beach. Looking around affirms that fact, with a few people around us distracted by the goings on."

    scene bg ishigaki_day with dissolve
    show hisao_beach_erm at twoleft
    show suzu_beach_normal at tworight
    with charaenter

    "Content that I've had my fun, I do as she asks and set her back on her feet. I still don't think she was being that reasonable about me and Hisao, but at least this took her mind off it."

    "Or at least, I think so. She still refuses to smile, holding on to that placid face as always. It seems Hisao has caught on to the same thing, but comes to a different conclusion."

    hi "I guess this would be a bit old hat for you, given you grew up here."

    suz "What do you mean? I like the beach."

    hi "You certainly don't look it..."

    show suzu_beach_angry at tworight with charamove
    hide suzu_beach_normal at tworight

    "Hoping to help Suzu convey her emotions a little better, I bring my finger around her cheek from behind and poke it into the side of her mouth, dragging the corner upwards."

    mk "Can't you see? She's smiling. A nice big, happy grin."

    show hisao_beach_disappoint at twoleft with charachange
    hide hisao_beach_erm at twoleft

    "Hisao just looks at her with an expression of pity."

    hi "Are you sure you don't have Stockholm Syndrome?"

    show suzu_beach_small_em at tworight with charachange
    hide suzu_beach_angry at tworight

    suz "I have wondered."

    "Assuming whatever that is isn't a positive thing, I give her mouth a couple of tugs to try and make her smile on her own from amusement. Unsurprisingly, she doesn't."

    "I give up on the idea and let her go, taking a glance around the beach. A good few people have decided to come out and enjoy the sun while it lasts, the place dotted with umbrellas, towels and fold-up chairs of all colours."

    "Given there's increasingly little room to run about on land, the water seems as good a place as any to start."

    mk "I'm goin' for a swim. See you losers later."

    scene bg ishigaki_sea_run with dissolve

    "Sprinting off before they can mount any opposition, I head straight towards the blue expanse."

    $ renpy.music.set_volume(0.8, 0, channel="audio")
    play audio sfx_splash

    "The water's delightfully warm as I run in, and the surface is relatively calm as well. It's only after getting near waist-high depth that I stop to turn around, urging the others in."

    scene bg ishigaki_sea with dissolve
    show suzu_beach_normal at tworight
    show hisao_beach_erm at twoleft
    with charaenter

    "The two take their time, strolling up to the water's edge at a leisurely pace. Suzu skips further in as Hisao, ever the cautious one, stops to carefully gauge the water's temperature with his foot before joining us."

    suz "You can swim, right?"

    hi "A bit. It's not like I'm going to drown."

    suz "Good. Probably should've asked you that before."

    hi "What about you?"

    hide suzu_beach_normal with moveoutright
    play audio sfx_splash

    "Suzu's response is to twist around and take a running dive into the warm, blue water. All we can do is watch as she disappears for a couple of seconds, before floating to the surface a good few meters away with her arms out and head looking back to us."

    show suzu_beach_smile at tworight with moveinbottom

    suz "I'll be fine."

    mk "I'll be fine', she says."

    hide suzu_beach_smile at tworight with moveoutbottom

    "With that, she goes back to swimming about as the two of us observe."

    show hisao_beach_erm at center with charamove
    show hisao_beach_talk with charachange
    hide hisao_beach_erm at center

    hi "She's not half bad."

    mk "You said it yourself earlier; she did grow up here."

    hi "What about you?"

    mk "I'm no slouch, even without a hand. There was something else I wanted to mention, though."

    show hisao_beach_erm with charachange
    hide hisao_beach_talk

    "He leans in as my voice grows quieter, surely out of Suzu's hearing range as she once again dives below the surface with practiced ease."

    mk "Keep an eye on her, alright?"

    hi "Sure, but why?"

    mk "If she has a cataplexy attack and ends up face-down..."

    show hisao_beach_frown with charachange
    hide hisao_beach_erm

    "His face drops instantaneously, horribly disturbed by the image. One thing I like about the guy is that he knows when to take things seriously."

    mk "Yeah."

    hi "I'll keep an eye on her, then. Don't worry."

    mk "'Atta boy."

    #hide hisao_beach_frown with dissolve
    show suzu_beach_smile at right with moveinbottom

    "I clap him on the shoulder a couple of times as the two of us watch Suzu resurface once more."

    stop music fadeout 3.0

    "It's nice to see her like this, devoting herself to having fun instead of angsting about others. It's rare that she acts so free, barely even noticing us as she freely flits about in the water."

    "I'm reminded of how I used to be, before the accident. Just having fun without a care in the world, life's worries being the furthest thing from my mind as I took to the field."

    "And then life kicked me in the balls."

    hide suzu_beach_smile at right with dissolve
    with vpunch
    play audio sfx_splash
    show hisao_beach_grin with charachange
    hide hisao_beach_frown

    play music music_pearly

    "The cool feeling of water suddenly splashing against my body makes me reflexively brace, the culprit grinning as he brings his cupped hands under the surface of the water and throws another lot of water at me."

    mk "Son of a bitch...!"

    show hisao_beach_declare with vpunch
    play audio sfx_splash
    hide hisao_beach_grin

    $ renpy.music.set_volume(1.0, 0, channel="audio") # restoring audio volume

    "I counterattack with a sweep along the water's surface, flicking a spray of water into his face and sending him reeling backwards."

    suz "Miki, what are you doing?"

    mk "Just messin' around."

    show hisao_beach_smile with charachange
    hide hisao_beach_declare

    mk "Hey, wanna race? That swimming dock out there'd make a good goal."

    "I point to the fairly large platform floating a good distance out from where we are now. With nobody between it and us, it should be a clear run."

    show hisao_beach_smile at twoleft with charamove
    show suzu_beach_small_em at tworight with moveinright

    "Evidently agreeing after taking a look, she swims towards us and wades up the final few feet. Suzu's body might not have the same kind of athletic build as mine, but she isn't half bad looking as she confidently emerges from the water and brushes her sopping hair back."

    suz "What?"

    mk "Nothin'. You coming too, boy?"

    show hisao_beach_erm at twoleft with charachange
    hide hisao_beach_smile at twoleft

    hi "It's probably for the best if I don't."

    "He makes an awkward face, with his thumb pointing to his chest. I probably should've remembered that."

    suz "So out to the platform and back to Hisao?"

    stop music fadeout 3.0

    mk "Sure. Give us a countdown, will you?"

    show hisao_beach_smile at twoleft with charachange
    hide hisao_beach_erm at twoleft

    hi "Alright. Get ready..."

    hide hisao_beach_smile at twoleft
    hide suzu_beach_small_em at tworight
    with dissolve

    "The two of us turn and orient ourselves towards the objective. I think I have an okay chance at this, given how she lazes around at school."

    play music music_running fadein 0.3

    hi "And... go!"

    scene bg ishigaki_sea_run with dissolve

    "We spring forwards simultaneously, each of us off to a good start as the water washes over my body."

    "Suzu might have the advantage in technique, but I have brute force. Pushing myself onward with my somewhat hobbled freestyle, my arms pulling me forwards with every stroke, I can feel the yards rapidly disappearing."

    "Comfortable with my pace, I take a moment to slip underwater and see Suzu's efforts. The sight I see is just as I'd hoped for."

    "Her body slides through the water as if she were a native to the sea rather than land. Her hands remain together, pointing the way ahead as her feet flick up and down and body undulates. One could only compare her movement to a dolphin's."

    "I find myself captivated by the sight, her lithe body gliding through the deep blue expanse. If only I could see this side of her every day."

    "As she passes, I stop my gawking and begin racing again in earnest. I can feel every muscle in my body working away as I punch through the water, reefing myself towards the platform with every ounce of strength I have."

    "I close my eyes and hammer forwards, throwing myself the last few yards towards the goal."

    "Feeling the wooden barrier brush against my fingertips, I throw my head up out of the water to get my bearings and take numerous deep gasps of air. My muscles feel like they're on fire despite being drenched, desperately needing a moment's rest before going on."

    "It turns out Suzu has the same idea as she floats with an arm over the side, a couple of seconds being needed to even notice her for my panting. She might've been there even before I arrived."

    mk "We goin' back?"

    scene bg 4361 with dissolve

    "She suddenly closes her eyes and pushes her face forwards, pressing her lips to mine with some force. My heart freezes for a moment in shock, not only at the kiss itself, but also her initiative."

    "It's a jarring sensation, with the water on both our lips intermingling and leaving a salty taste on the mouth. I can't even move, my mind left completely addled by her affection."

    scene bg ishigaki_sea with dissolve

    n "Her lips withdraw all too soon, leaving me to recall the sensation fondly. A dumb grin finds its way onto my face, a warm sensation flooding my body."

    n "Perhaps that sensation is what reminds me of the water lapping at my shoulders, my eyes suddenly darting left and right to collect myself and take in my surroundings once more."

    n "Suzu, that little brat, has fled. There's no mistaking it; she's used her feminine wiles to distract me and taken off at full speed."

    n "Torn between despising her for playing such a horrible trick and delight at her deviousness, I bring my feet to the side of the platform and launch myself back towards the beach in hopes of catching her."

    n "The effort needed to reach parity with her speed has worked against me, leaving my body tired from the first leg. Doing my best to ignore the pain, I surge onwards."

    n "It isn't long before she's in sight, and knowing what I have to do, I make one last push to reach her."

    n "I reach out once, but only grab at the water and lose speed. With only one chance left, I make one last lunge and push my hand out once more."

    n "Success comes as I feel the back of her shin in my grasp, one solid tug jerking her body back towards mine and sending her arms flailing."

    n "What follows is a chaotic mess of arms and legs as we struggle in the water. Suzu fights to get her head up and work out what's happening, while I struggle to get a grip on her slippery torso to throw her back, a task made all the harder with only one hand."

    n "I quickly begin to run out of air as we sink further down with our thrashing, my instincts taking command of my body and forcing me away from Suzu towards the surface. Much-needed air fills my lungs as I take a great breath the moment I breach the waterline."

    n "Satisfied that I can still hear her moving about in the water rather than silently drowning, I kick onwards to the shallower waters."

    stop music fadeout 2.0
    nvl hide dissolve

    nvl clear


    show hisao_beach_erm with dissolve

    "With that, the ordeal is over. With a heave I bring myself to my feet and begin to wade out, dragging my sore legs out and on to the dry land where I belong. Water pours off my back, hair, and shoulders as I lurch forwards like some shambling swamp monster."

    mk "I... win..."

    "Hisao doesn't comment as I drop to my knees, my upper body soon following as I flop to the ground in exhaustion. Sand pressed against my cheek and lips, but I don't care. I'm on sweet, sweet land, and that's all that matters."

    "I hear the splash of Suzu coming up out of the water behind me. I want to gloat, but I'm too tired to do anything right now."

    hi "You okay, Suzu?"

    "I wait for Suzu's answer, with none forthcoming as I hear her footsteps slowly coming closer."

    with vpunch
    play audio sfx_impact

    mk "Urk!"

    "Suzu gives a surprisingly firm stomp to my back, sending me into a choking fit as she huffs and continues on to where her sister's sitting. It's Hisao's footsteps that I now hear come beside me, but thankfully, no abuse from him is forthcoming."

    hi "Was it worth it?"

    mk "Yeah... totally."

    "I do my best to sound convincing, but I don't quite think I manage it."

    $ renpy.music.set_volume(1.0, 0, channel="sound") # restoring sfx volume


    ##centered "~ Timeskip ~" with dissolve
    scene bg ishigaki_day with shorttimeskip

    $ renpy.music.set_volume(0.4, 0, channel="sound")

    play sound sfx_beach loop

    "With Suzu and I too pooped to mess around much more, Hisao's gone to explore around the edge of the beach while I grab a few drinks from the nearby vending machines. With my left arm holding the small juice boxes, the walk back to home camp begins."

    "There's something cathartic about heavy exercise, and doubly so when you do it with a friend. With my energy worked out of me and a pleasant atmosphere in the air as the others on the beach fool around, I can say it's been a pretty good day."

    "I stop momentarily to avoid bumping into a young boy running across my path, giving a reflexive smile as I do so."

    show tsu_beach_deadpan at tworightsit
    show suzu_beach_normal at twoleftsit
    with charaenter

    play music music_lullaby

    "Looking back up, I see Suzu and Tsubasa ahead sitting and talking to one another, Tsubasa seated casually with her hands on the ground behind her as Suzu holds her knees to her chest. I almost start moving towards them again, but stop as I faintly overhear the topic of conversation."

    suz "They put you up to this, didn't they?"

    tsu "Up to what?"

    show suzu_beach_angry at twoleftsit with charamove
    hide suzu_beach_normal at twoleftsit

    suz "Don't play stupid. Chaperoning us, to keep an eye on me and Miki."

    "The thought hadn't even entered my mind, but it does make sense. Tsubasa's reluctant pause in answering all but confirms the idea."

    show tsu_beach_erm at tworightsit with charachange
    hide tsu_beach_deadpan at tworightsit

    tsu "Well, it's not like I didn't want to come anyway. I did need a break, just as I said."

    show suzu_beach_sad at twoleftsit with charamove
    hide suzu_beach_angry at twoleftsit

    "Suzu's shoulders slump in disappointment."

    tsu "Don't worry about mom and dad. I'll sort them out."

    suz "But they-{w=.25}{nw}"

    show tsu_beach_closed at tworightsit with charachange
    hide tsu_beach_erm at tworightsit

    tsu "I'll sort it out."

    "Her tone is as authoritative as it is final, bringing an end to the line of discussion. I want to jump in and lighten things up, but the mood is terribly dour."

    "Tsubasa thankfully relents, rubbing Suzu's shoulder a little."

    show tsu_beach_tooth_smile at tworightsit with charachange
    hide tsu_beach_closed at tworightsit

    tsu "Don't be like that. You're having fun, aren't you?"

    "She nods, which gives me at least a little relief."

    tsu "You got to see Miyu again, and your dear sister. Just in the last few months you got a romantic partner too, and another friend."

    tsu "Far as I can see, things are working out pretty well for you."

    "She looks to Suzu to see how her assurances have gone down."

    suz "Hey, Tsubasa..."

    tsu "Hmm?"

    suz "...Thank you."

    show suzu_beach_sad at centersit with charamove

    "The two look at each other for a while, with Tsubasa eventually bringing her arm around Suzu to bring her to her side."

    "It's a sweet sight, with the sisters sharing a moment between themselves despite all that's gone on. The two don't see each other that often thanks to school, after all, and occupy vastly different social worlds."

    "But today, perhaps just for a moment, they see eye to eye."

    scene bg ishigaki_day_run
    show suzu_beach_sad at centersit
    show tsu_beach_tooth_smile at tworightsit

    "My weight shifts as I begin to run towards them, unceremoniously dropping the drinks in my now cold arm on the towel."

    "Neither can get a word out before I grab Suzu's forearm, my body continuing forwards and dragging her up from where she was sitting with barely any resistance."

    show suzu_beach_surprised at centersit with charamove
    hide suzu_beach_sad at centersit
    show suzu_beach_surprised at center with charamove

    suz "Wait, hold on!"

    hide tsu_beach_tooth_smile at tworightsit with dissolve

    suz "I'm still recovering from what you already did to me! Miki...!"

    "I look back to her sister as I drag Suzu towards the water line, Tsubasa just smiling as she watches the two of us leave."

    stop music fadeout 1.0

    $ renpy.music.set_volume(1.0, 0, channel="sound") # restoring sfx volume

    ##centered "~ Timeskip ~" with dissolve
    scene bg ishigaki_evening with shorttimeskip
    show suzu_neutral_d with dissolve
    play sound sfx_beach loop

    play music music_night

    "With the both of us drained from the day's activities, Suzu and I slowly walk along the beach as Hisao and Tsubasa pack the car. With the both of us changed back into our normal clothes and the sun setting, it feels like an appropriate way to send off a nice day."

    "Suzu's hand feels warm as she holds onto mine, her soft skin and delicate grasp a harsh contrast to my own."

    suz "So that's summer holidays over with."

    mk "Yup. Couldn't have asked for a better end, even if the rest didn't exactly go to plan."

    show suzu_unhappy_d with charamove
    hide suzu_neutral_d

    "With this, her footsteps stop. Her hand trembles in mine, her grip becoming tight as she tries to steady herself."

    suz "I'm sorry, Miki."

    mk "What's there to be sorry about?"

    suz "It wasn't supposed to be like this. You chose to spend your last summer holidays with me, and this is what you got."

    suz "I wanted this to be fun for you..."

    mk "You're bein' dumb again, girl."

    mk "Is this the face of someone who didn't enjoy herself? Your house is as lively as ever! That's what I like so much about it!"

    mk "My home's in the middle of nowhere, there's jack-all to do, and the local wildlife doesn't exactly make for good pets. You've got Tsubasa, Miyu, your parents... even if they're not exactly fans of me right now... and we had Hisao around, too."

    mk "I got to be around all of them, around the people who've raised you and shaped you. That's all I wanted, and I got all of that."

    suz "What do you see in me to keep trying so hard?"

    "Now there's a curveball. Now that I think about it, I never really gave much consideration to how I thought of Suzu. I just went along with things, and did what felt right at the time."

    "I love her, I know that much. She's a genuinely good person, once the veil of cynicism and misanthropy is lifted. How I fit into that... I have honestly no idea."

    "In frustration, I end up tapping my head with my stump to try and make something drop out."

    "To my surprise, I turn back to her mirroring the action as if to mock me. I can't help but burst into a laugh, given how dumb it looks."

    show suzu_smile_d with charachange
    hide suzu_unhappy_d

    "While she might not do the same, it earns me an amused smile. It only makes me laugh harder in happiness, all the more glad that I've lifted her spirits."

    "With the two of us basking in each other's joy in the setting sun, I know that I'll ever forget this holiday with Suzu."

    stop sound fadeout 1.0
    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_S8:

    scene bg school_scienceroom with dissolve

    window show
    show suzu_neutral at leftsit
    with charaenter

    play music music_miki

    "With the holidays finally over, the mundane routine of school begins all over again."

    "Mutou fiddles with the teaching material on his desk, occasionally stopping to scrawl this note or that on the blackboard in preparation for the lesson ahead. While he might hope for a refreshed and eager class of students thanks to our chance to recharge, like every teacher would, I'm afraid he's going to be disappointed."

    "A few look genuinely ready to go, but most appear either tired from seeing off the holidays with fanfare, or reluctant to even walk in the door as they face months of drudgery after the fun they've just had."

    "After yesterday's late night trip back to Yamaku, and given my unfortunate allergy to schoolwork, I can safely say both apply equally to me. Bereft of anything else to do, I rock back and forth in my chair while looking to my side."

    "Suzu sits with her hand in her chin as always, silently turning another page of the manga magazine on her desk. They never provoke much of a visible reaction from her, but she reads so many that she must like them."

    "While piecing together my uniform from around my dorm room, I'd found the old crumpled-up blouse of the girl's summer outfit. Seeing her in her uniform once again reminds me of it."

    mk "Hey, Suzu?"

    "She continues to read the manga with the same bored expression."

    suz "Yes?"

    mk "Would you prefer it if I wore the normal girl's uniform?"

    show suzu_surprised at leftsit with charachange
    hide suzu_neutral at leftsit

    "I take the fact that she suddenly stops her reading, a page left in the middle of being turned, as a sign that the question's not as banal for her as I thought it might be."

    "It was only a month or two before I gave up on it after coming to Yamaku, so she's probably never seen me wear it. The arms and bust felt too constricted and uncomfortable, while the men's shirt was much more loose and airy. Then there's that dumb bow."

    "Suzu turns to me, trying to imagine how it'd look. The fact that her forehead is gathering creases shows it to be a hard task."

    show suzu_speak at leftsit with charamove
    hide suzu_surprised at leftsit

    suz "That would look weird."

    har "Damn right it would."

    show haru_smile at center with moveinright

    "The voice behind me turns out to be Haru, waltzing in with his bag held over his shoulder. He looks pleased with himself. Far too pleased."

    mk "What's with that face? You hook up or something?"

    har "The only thing better. Workin' at the family bakery over the holidays got me some fat stacks. I'm rich, baby."

    mk "Awesome, you can pay for dinner!"

    show suzu_neutral at leftsit with charamove
    hide suzu_speak at leftsit

    suz "Can't you buy your own dinner for once?"

    mk "I can't help it if my allowance is shit."

    mk "C'mon Haru, we're buddies, right?"

    show hisao_smile_u at right with moveinright

    "Hisao decides to pick now to enter the classroom, showing some interest in our impromptu little gathering as he comes through the door. Pleased with the development, Haru clears his throat to make an announcement."

    har "Worry not, children; dinner is on me! Everyone in the track club's welcome!"

    show suzu_normal at leftsit with charamove
    hide suzu_neutral at leftsit

    hi "Today's sure off to a good start."

    har "You can come as well, Suzuki. If you wanna."

    mk "Don't worry, we'll both be there. Got a restaurant in mind?"

    har "I know this fantastic place. Best food ever."

    mk "If it's a bakery, I will hit you."

    har "Just a quiet little traditional place. Nothin' fancy, just real solid food."

    stop music fadeout 1.0

    scene black ##with shorttimeskip

    #centered "~ Timeskip ~" with dissolve
    scene bg izakaya with shorttimeskip
    $ renpy.music.set_volume(0.6, 0, channel="sound")

    play sound sfx_crowd_indoors loop

    play music music_raindrops

    ##pay attention to the film sound later. Maybe need to use audio channel instead if we're keeping crowd during? Film sound plays -Niji 01/01/2018

    "Looking around the numerous low tables and cushions at their sides, Haru's definition of 'little' might be questionable. That might be for the best, though, given the number of track club members that showed up."

    "The waitress who guided us to where everyone's set up bows out, leaving us to take in the scene before us. Compared to the fracas of the post-track meet celebrations, the mood is much more sedate. I'm glad, not so much for myself so much as Suzu."

    "Looks like word got out, especially amongst the first-years, as the turnout's a good sixteen or so. The gathering ends up strewn across two tables, having outgrown the one, with the first-years having the numbers to claim their own."

    "Given the usual amount of sausages at these things, perhaps the biggest surprise is how many of the fairer sex showed up. A good five by my count, which is five more than usual. Even Emi's here, yakking away to the track captain seated next to her."

    "Perhaps the sheer number is why the teacher in charge of the club showed up, the old warhorse sitting quietly at the end of our table as he sips his carefully guarded beer. Between him, Emi and the captain, Yukio, Hisao, and Haru, our table will be full with the addition of Suzu and I."

    show haru_yo at centersit
    with charaenter
    show suzu_neutral_d at left with moveinleft
    show suzu_neutral_d at leftsit with charamove

    "With everyone jammed tightly around the table, the only place left for Suzu and I to take a seat is at the end. I take my place next to Haru, with Suzu unsurprisingly ending up on the fringe."

    har "Hey, you finally showed up."

    mk "Sorry 'bout that. Someone was busy studying."

    suz "Sorry."

    har "Don't worry about it, it's fine! We haven't started eating yet, anyway."

    "After glancing over our table and noticing a lack of drinks before Suzu and I, a waitress quickly shuffles over to take our orders. With a fairly sparse non-alcoholic menu, both of us take green tea. As she bows and leaves, I take a passing note of her uniform."

    "Yes, Yuuko's outfit is definitely better."

    "As she passes by the table of first-year students, it's they who next enter my thoughts. I've seen the others out of their uniforms plenty of times, but this lot are new to me. Despite only being a couple of years younger, their styles as a whole are all subtly different to ours."

    mk "What's with all the brats?"

    show haru_basic at centersit with charamove
    hide haru_yo at centersit

    har "You know how things are when Yukio gets involved. A first year girl heard about it from him, she told her friends, and..."

    show junko_question at right with moveinright

    "One of the first-year students from the other table suddenly slips between Haru and I, both of us leaning to the sides to make room for her. The bright purple highlight in her carefully styled black hair is the most striking thing about her, followed by her dark punk-inspired clothing. She's an ostentatious one, if nothing else."

    "She quickly flips around a small notepad so he can see it, to which he quickly shakes his hand."

    har "It's fine, the more the merrier."

    show junko_question at rightsitlow with charamove

    mk "Hmm? What is it?"

    "The girl looks to me and dutifully turns her notepad around."

    yam "[[What was that about me and Hasegawa?]"

    mk "Oh, right. Wait, uh..."

    "My brief look of confusion at whether she's deaf, and if so, whether she could read my lips, is quickly answered as she points to her mouth and makes a shaking motion with a balled fist. At least being mute wouldn't be as troublesome as being deaf."

    "The waitress returns with the tea for Suzu and I, gently placing it down before each of us before bowing and taking her leave. Suzu blows on hers to try and cool it down, while I just leave mine for later."

    "Evidently wanting to continue the conversation further, Junko quickly takes out her blue pen and scrawls on the notepad with both astonishing speed and immaculate handwriting. I guess this must be what Shizune's like when she's separated from her bright, bubbly shadow."

    show junko_smile at rightsitlow with charachange
    hide junko_question at rightsitlow

    yam "[[Junko Yamada. You must be Miura, right?]"

    mk "Guess I'm easy to pick out. I like the hair, by the way."

    show junko_frown at rightsitlow with charachange

    yam "[[My parents gave me no end of grief for that. It was pretty lame.]"

    mk "Parents are important. You shouldn't be flippant about them."

    show junko_question at rightsitlow with charachange
    hide junko_smile at rightsitlow

    "The response seems to greatly surprise her. Maybe it's from the way I was brought up, but I've never taken kindly to people who take their parents for granted."

    "She taps at her pad a few times to try and work out what to say, eventually coming to a satisfactory new topic as she starts writing once more."

    yam "[[Who's the girl next to you? I haven't seen her at the track before.]"

    "She pokes her head out a little to see Suzu, moving the pad into her field of vision."

    show suzu_surprised_d at leftsit with charachange
    hide suzu_neutral_d at leftsit

    "Suzu's reaction is to look at me with a slight edge to her expression. Come to think of it, I haven't told anybody about us dating yet, and there's no way she would have. How Suzu wants to play it soon becomes obvious."

    suz "Suzu Suzuki. We're friends."

    "I know why she says it, but that doesn't make it feel any better. Am I supposed to keep that lie going to everyone I know for the rest of my time here? Is it even okay for her to make that judgement for the both us?"

    "Unsatisfied and perhaps a little jilted, I quickly take the pad and pen from Junko before she writes a response, adding my own addendum to what Suzu said before handing them back."

    show junko_grin at rightsitlow with charachange
    hide junko_question at rightsitlow
    show suzu_veryangry_d at leftsit with charamove
    hide suzu_surprised_d at leftsit

    "As hoped, she gives an amused snort. Suzu's reaction is markedly less charitable, a silent frustration written to her face. There's no doubt I'm going to pay for this later."

    mk "Damn..."

    har "What's wrong?"

    mk "I got her pissed at me again."

    "He takes a moment to look at Suzu, but doesn't appear any the wiser for doing so."

    show haru_serious at centersit with charamove
    hide haru_basic at centersit

    har "You can tell?"

    "I hadn't really thought I could read her better than anyone else in particular, but maybe it's true. We've been around each other for a year, after all."

    "Another scrawled note is held to my side by Junko."

    show junko_smile at rightsitlow with charachange
    hide junko_grin at rightsitlow

    yam "[[You're different to what I imagined.]"

    mk "How so?"

    show junko_frown at rightsitlow with charachange
    hide junko_smile at rightsitlow

    stop music fadeout 3.0

    "The way her face instantly drops makes it obvious she's heard the rumours. She immediately regrets what she's said, but it's far too late to take it back."

    yam "[[I heard that you got into a lot of fights.]"

    "The temptation to grab Junko and force her to say who told her such things rushes to my mind, but I quickly smother the thought given the number of people around. There's no reason for the newer students to know."

    show junko_embarrassed at rightsitlow with charachange
    hide junko_frown at rightsitlow
    show suzu_neutral_d at leftsit with charamove
    hide suzu_veryangry_d at leftsit

    "Looking bashful as she taps at her pad trying to work out what to say in apology for getting me riled up, I decide to take pity on her."

    mk "Well... let's just say people change."

    "I glance to Suzu to acknowledge her, but she's already back to her tea. I know that she changed me, but despite my best efforts, I'm not sure I've helped her much in return."

    "It's a shame the conversation got awkward so quickly, but respite comes in the form of two waitresss bring in massive platters of assorted food. Sushi, nigiri, tempura, and various other little delicacies abound. The collective anticipation in the room can be heard from everyone."

    show junko_embarrassed at right with charamove
    hide junko_embarrassed with moveoutright
    show haru_basic at centersit with charamove

    "Junko gives a nod before retreating to her own table. While she seems a nice enough person, I can't say the conversation left me in higher spirits."

    "Haru just gives a weak smile to try and cheer me up. I do my best to return the gesture. It's people like he, Suzu, Shizune, and Misha who I owe everything to, after all."

    $ renpy.music.set_volume(1.0, 0, channel="sound") # restoring sfx volume

    ##centered "~ Timeskip ~" with dissolve
    scene black with shorttimeskip
    scene bg izakaya with dissolve
    show suzu_concerned_d at centersit
    with charaenter

    play music music_night

    mk "I'm dead."

    "I let myself fall forwards onto the table, my near-bursting gut held in with my hand."

    "The room is reduced to a quiet background hum after everyone's finished pigging out, simply too full to do much beyond trying to hold the food down. Each table's gigantic platter was followed by another, and this being the track club, that was seen more as a challenge than an offer."

    "While a scant few sushi rolls are left, salmon by the looks of them, I'd say we did a pretty damn good job. Not helped much by Suzu who, as always, ate like a sparrow."

    "Determined to make her eat more, I take one of the few remaining pieces and hold it in front of her mouth as she finishes sipping yet another cup of tea."

    mk "Vroooom, here comes the airplane~"

    scene bg sushi with dissolve

    "She looks at me with a despising frown before taking the sushi in her hand and thrusting it towards me. Before I know it, she's got it half into my mouth."

    mk "Bib I piff you moff?"

    scene bg izakaya with dissolve
    show suzu_speak_d at centersit
    with charaenter

    suz "I feel like the only one with any constraint here."

    "Giving in to my fate, I push the roll into my mouth with my thumb and force it down. It takes some effort."

    mk "Probably."

    suz "You shouldn't feel bad about it."

    "She answers my questioning look by throwing her head back to where Junko's sitting."

    mk "It's not like she's wrong. I did some pretty bad things back-{w=0.80}{nw}"

    show suzu_veryembarrassed_d at centersit with charachange
    hide suzu_speak_d at centersit

    suz "That's exactly why. You did bad things, but that's different to being a bad person."

    "And again we come to this discussion. On the one hand, I want to just agree with her and wash my hands of everything I've done in the past, taking the weight of guilt off my shoulders. On the other, I don't feel like I have the right to do that. Not when I'm the one who did it in the first place."

    "It's a lot easier to forgive, than to forget."

    show haru_basic at right with moveinright
    show haru_basic at rightsit with charamove
    show suzu_neutral_d at centersit with charamove
    hide suzu_veryembarrassed_d at centersit

    har "You two enjoy yourselves?"

    mk "You picked a good place, man."

    show haru_smile at rightsit with charamove
    hide haru_basic at rightsit

    har "Was there any doubt?"

    show suzu_smile_d at centersit with charamove
    hide suzu_neutral_d at centersit

    suz "It was nice though, thank you."

    yuk "It sure was."

    show yukio_smile at left with moveinleft
    show yukio_smile at leftsit with charamove

    "Yukio pokes his head between Suzu and I, having scooted around to chat."

    show haru_sad at rightsit with charamove
    hide haru_smile at rightsit

    har "Shame we're not gonna be able to do this kind of thing anymore, though."

    yuk "I'm sure we can scrape something together to send us off with closer to graduation."

    har "It's not really gonna be the same."

    "It's weird to see the eternally optimistic Haru looking so down. That, and that damned word 'graduation', makes the gravity of the coming months weigh down on all of us."

    "The first years will be fine; they've got a good couple of years more to enjoy. Everyone at this table will go their separate ways, into different universities, colleges, and jobs. Then there's the matter of Suzu and I..."

    yuk "It'll all work out. Haru's got his bakery, Emi and the captain are easily good enough to get scholarships, I've got a political science course at a fine university lined up, and I'm sure Hisao will get into a good uni, too."

    yuk "You've got a good brain up there, don't you Suzuki? I'm sure you could do whatever you wanted."

    show suzu_neutral_d at centersit with charamove
    hide suzu_smile_d at centersit

    "Suzu just shrugs, not really invested in the conversation as she sips at her tea once more. His judgement of her seems a bit generous, given her relatively average marks in class."

    show yukio_notimpressed at leftsit with charachange
    hide yukio_smile at leftsit

    yuk "Don't be so humble. Least you're doing better than that lout."

    mk "Don't start."

    har "What are your plans anyway, Suzuki?"

    suz "University, I guess."

    "Silence reigns as everyone waits for her to say what she intends studying, how good a university she'll try for, what area it'd be in, or anything further in general. All that's to be heard is the chatter from the table behind us."

    show yukio_huh at leftsit with charachange
    hide yukio_notimpressed at leftsit

    yuk "...Well, I mean, it's good to keep your options open. Something will take your interest if you keep working at it."

    "Smooth. I'm pretty sure I've heard that exact line from at least a half dozen teachers before, giving their usual generic pep-talks on life after Yamaku."

    mk "Sounds like you've got it all figured out."

    show yukio_notimpressed at leftsit with charachange
    hide yukio_huh at leftsit

    yuk "Me? Pretty much. There's still a couple of things I want to wrap up before graduation, though."

    hide yukio_notimpressed at leftsit
    hide suzu_neutral_d at centersit
    hide haru_sad at rightsit

    n "The track captain calls out to Haru, holding a camera as he does so. Shouldn't have thought we'd get out of this without a group photo."

    n "With Haru nodding in assent and calling over the first-year students, the captain calls over a passing waitress to take our picture."

    n "Suzu doesn't look thrilled by the idea, but closes her eyes as she realises she's not going to get out of this. No further prompting's needed as I bring my arm around her neck, tugging her closer."

    n "With Yukio reluctantly returning to his seat amidst the chaotic movements and orders being given, we end up with a haphazard arrangement of third-years and the teacher sitting in the front and first-years standing over us."

    n "I can't help but give a wide grin as the waitress's finger comes down on the camera's trigger."

    n "Suzu's body is held tight to mine as everyone crushes together to fit into the shot, and the new generation of the track club stands behind, ready to take our places once we leave."

    nvl hide dissolve

    nvl clear

    with flash
    play sound sfx_photo

    scene bg track_team_photo with dissolve

    #fix this paragraph so there's a space or insert a photo scene

    "For a brief moment as the camera flash blinds us, it feels like everything really will work out."

    #nvl hide dissolve

    #nvl clear

    window hide

    scene black
    with dissolve

    #centered "~ Timeskip ~" with dissolve

    scene bg city_street3_ni with shorttimeskip

    "With the event over and time marching on, I idly stand around on the dark street outside the restaurant, a slumbering girl held to my back. Only Haru and the teacher are still around, the rest of the students having left by bus."

    "Our teacher busies himself with moving things from the back seat to the trunk, so that Suzu and I can hitch a ride to Yamaku with him. Haru, on the other hand, slowly reads the long receipt with a remarkably dour face, prompting me to peek over his shoulder at it."

    show haru_sad with dissolve

    har "Man..."

    mk "Geez. That's pretty much the lot, isn't it?"

    har "The teacher said he'd help with the cost a bit, but still..."

    mk "Easy come, easy go."

    "He just hangs his head. If nothing else, at least he's going to finish his time at Yamaku being venerated as a benevolent god of free food. There are worse fates."

    "I adjust my hold on Suzu a bit, hitching her up a little further. She's gone a fair while without a nap, so it isn't a surprise it'd catch up with her eventually. I'm just glad she managed to last through most of the dinner."

    show haru_serious with charamove
    hide haru_sad

    har "Think you'll be alright with Suzu?"

    mk "I've done this plenty of times before, dude."

    har "That's not what I'm talking about."

    show haru_smile with charamove
    hide haru_serious

    "Haru just smiles. After being around each other since entering Yamaku, for good or ill, it isn't a surprise he'd have a pretty good read on me."

    mk "Everything'll be fine. Somehow."

    har "I never thought I'd get to hear you say that, after all these years."

    mk "You gettin' sentimental, boy?"

    har "No, no."

    show haru_basic with charamove
    hide haru_smile

    har "...A bit."

    mk "Well cut it out. It's weird."

    "He gives a grin and a salute as the teacher calls out for us to get in. Knowing him, we'd better get a move on."

    stop music fadeout 1.0

    #centered "~ Timeskip ~" with dissolve

    scene bg school_dormext_full_ni with shorttimeskip

    "After giving thanks to the teacher for the lift back to Yamaku, and letting Haru go on ahead to the male dorms, I slowly continue the journey to the female dormitories."

    play music music_innocence

    "The school building looks different of a night, barely lit by the lamps in the grounds out the front. Without teenagers running about and the rooms busy with staff and students, it's little more than an empty shell. It's not creepy at all, but more... lonely. A world without people in it."

    "But that's how Suzu's world largely was, before meeting me. How someone could live so long without others, whether they liked you or not, is a mystery to me. Maybe that's the reason for her distorted personality; spending so long in her own mind without the company of other people."

    "As if she'd heard my thoughts, she chooses now to stir. I obediently let her down as she starts to fidget, waiting a little for her as she reorients herself."

    show suzu_sleepy_d with charaenter

    suz "What did I miss?"

    mk "Nothin' much. It was winding up when you went to sleep, and the club teacher gave us and Haru a ride back."

    "We start walking back to the dorm, her hand slipping into mine as we do so. She does her best to look like it's an ordinary thing, but I can tell she's a little brighter than usual."

    show suzu_unhappy_d with charachange
    hide suzu_sleepy_d

    suz "I'm sorry about before."

    mk "What's there to apologise for?"

    suz "Calling you a friend."

    mk "...Yeah, that did kinda hurt."

    mk "They'll be fine with it, you know. I'm pretty sure a few think I lean that way already."

    suz "I assumed you were straight."

    mk "So guys think I'm into girls, and girls think I'm into guys. I'm wounded."

    mk "If that's true though, why'd you confess to me?"

    show suzu_veryembarrassed_d with charachange
    hide suzu_unhappy_d

    suz "When you said you refused your father's offer in order to stay with my family, I felt..."

    "She stops herself, too embarrassed to continue as her grip on my hand tightens. Too curious to let her wiggle out of this, I patiently wait for her to continue on."

    suz "I felt hope. I'd never felt that before, so I ended up clutching desperately at it."

    mk "You make that sound like a bad thing. When I was thinking about what happened afterwards, that courage you showed made me like you even more."

    suz "That's..."

    show suzu_embarrassed_d with charachange
    hide suzu_veryembarrassed_d

    "Maybe I was coming on too strong, the girl falling silent as we come to the front of the dormitory building and make our way inside."

    scene bg school_dormhallground with locationchange

    "Both of us squint as we enter the brightly-lit first floor. The common room lies empty as we pass, everyone most likely sleeping by now in preparation for the day ahead."

    scene bg school_girlsdormhall with locationchange
    show suzu_embarrassed_d with charaenter

    "Coming up the stairs and down the hall to the door of my room, I move to take my hand from Suzu's in order to grab my keys. It proves futile, with her hand refusing to let go of my own."

    mk "Suzu...?"

    suz "I don't want to let go."

    mk "I can't get in if you don't."

    show suzu_veryembarrassed_d with charachange
    hide suzu_embarrassed_d

    suz "Then sleep in my room."

    "It seems Suzu still can't speak about such things in a straightforward way, but even coming that close is a surprise. Her eyes betray her nervousness, as if she might be making a terrible faux pas in asking in such a way. It's probably one of our biggest differences, as I don't really get why she gets so keyed up about it."

    "With no offense or refusal forthcoming, she gingerly leads on down the hallway."

    #scene black with shorttimeskip

    play sound sfx_dooropen

    scene dormsuzu with locationchange

    queue sound [ sfx_void, sfx_void, sfx_doorclose ]

    #centered "~ Timeskip ~" with dissolve

    "I open the door with my copy of her key, and the moment Suzu closes the door behind us, I pull her into a tight embrace and press my mouth to hers with all the force I dare use."

    stop music fadeout 1.0

    scene black with dissolve

    play music music_heart fadein 1.0

    "Her surprise melts away almost instantly, defensively raised arms dropping loosely by her side as she lets herself be swept up in the lustful rush."

    "For a flicker of time, it feels like we're both in unison with our emotions. A desperation to affirm our feelings for each other, and to continue what had come to flourish during the holidays. After spending the day suddenly surrounded by so many people now that we're back in Yamaku, this is a time for us, and us alone."

    "Things are different now. We can't go back. We don't want to go back."

    "Our kissing deepens as our want for each other redoubles, the feel of her breath brushing against my face as her body remains near-limp, all but surrendered to my desires."

    "I pull away with reluctance, as much to gasp for air as take in the sight of her. Suzu's face is dreamy as she looks back into my eyes, breathing heavily as her lips remain just slightly open, as if hoping they were met again."

    "My shirt and undershirt find themselves dropped to the floor, my temptation getting the better of me after I shirk my jeans as I dive at her neck and collar, licking them to take in her taste. She merely lifts her chin to allow my indulgence, saying not a word."

    "My lips meet the skin between her breasts soon after, my knees bending as I work my way down. A peck to her left breast is followed by another to her navel, my hand taking hold of her leg and working its way up her supple thigh underneath her dress."

    "Her shyness makes her hesitate, but I need not ask as she timidly brings her forearms underneath her dress, holding up its front. Her reward is a kiss to her pink underwear, her breath catching in response."

    "I begin to lap between her legs, teasing her with my tongue through the thin fabric. Her whimpers only drive me on, my want to see her in raptures making he grip her leg all the harder."

    "As her underwear discolours from her excitement and moans begin to heighten, I tug downward at her panties. Her dainty legs lift one after the other to allow them off, my lapping at the delicate nub between her legs resumed."

    suz "Miki..."

    "I move faster and faster, my motions progressively less thought out as my sense of restraint all but leaves me. I want to ravage this body, to make it mine. To see her squirm and moan at my control. I want her."

    "Suzu's grip on her dress tightens as she desperately tries to control her growing ecstasy, quivering legs and pained expression giving away the growing difficulty. My lips cover her most private area, sucking as I flick her with the tip of my tongue."

    suz "Aah... Aaaaahn!"

    "She teeters on the edge of euphoria, but I don't care. I can't stop until I've had my fill of her. Her muscles tighten as she clings on, but as her breathing accelerates, it becomes all but impossible."

    suz "Ah...!"

    "Her moan of joy is suddenly silenced, all control of her body lost as her knees buckle from underneath her. I quickly jerk my head back as Suzu's crumples to the ground before me, her upper body thrown forwards with what little energy she has left."

    "Exhausted, her head lies on my shoulder with hair dishevelled, arms slung around me in a loose embrace as she pants. The sweat on her cheek is cold, gently pressed against my own in her near-lifeless state."

    "But it's not enough. I want more of her. I want every inch of her, my hand taking a hold of her shoulder and pushing her back onto the floor with a thud."

    "I throw myself on her without a moment's notice, taking hold of her dress and jerking it up. Once, twice, three times I try to reef it off, my reward for succeeding being the beautiful skin of her heaving chest. Her chemise follows without as much of a struggle, leaving her body bare."

    "With the floor too uncomfortable, I scoop her small body up in my arms, her arms coming up to hide what she can of her breasts."

    suz "Please, Miki...!"

    play sound sfx_impact

    "Her voice more startled than panicked, I step over to her bed and dump her body onto the sheets. She bounces up and down as she lands on the thick mattress back-first, my bra and panties thrown off before I throw myself on top of her."

    "Suzu's body squirms and wriggles under mine as I force my mouth to hers once more, tongues intermingling as her back arches and feet kick about."

    "Hair falls past my face as I grope her breast, taking in its softness as the smell of her sweat from the exertion begins to enter the air."

if persistent.adultmode:
    scene bg 4237 with dissolve

    "Satisfied, I break off and turn on all fours to orient my head between her legs. Suzu seizes the brief moment of freedom as she turns on her side and begins to shuffle towards the head of the bed, but her strength leaves her after I fall onto my shoulder and kiss her below the tuft of hair."

    "Clutching her butt with my hand and bringing my stump over her other side, she surrenders and brings her lips to me. The pleasure as she does so surges through my body like lightening, driving me to pleasure her even further."

    "Again and again I lap at her, my advances less delicate than those of Suzu. It's wonderful, absolutely wonderful. I can feel my body filling as she holds me, taking in my taste as I do hers."

    "It isn't long before I feel the pleasure from that spot welling up inside of me, my grip tightening as I begin to lose myself."

    "Just a little more, just a little further..."

    "I'm forced to break my mouth from Suzu as the muscles in my neck tighten, a groan coming from deep in my chest as I desperately fight to control the feeling threatening to overwhelm me."

    "It's no use. I can't hold back, I can't...!"

    mk "Aaaaaah!"

    stop music fadeout 1.0

    scene black with shorttimeskip #dissolve

    scene bg misc_ceiling_ni
    with openeye

    "The cool night air sticks to my skin, the first sensation to return as my eyes blearily flicker open. The plain white ceiling hangs over me, a faint light from the front of the room just barely illuminating it."

    "I reach out with my hand to feel out Suzu, but I only end up patting at the bed. A brief glance confirms the fact."

    scene bg dormsuzu with dissolve

    play sound sfx_sitting

    "Disappointed that I couldn't wake next to her, I sit up and rub my eyes in an attempt to see where she is. Despite still being out of focus, the silhouetted figure staring at her laptop's screen is unmistakable."

    mk "Suzu...?"

    show suzu_concerned with charaenter

    play music music_moonlight

    "She glances around to see me, her pyjamas back on and a blanket draped loosely over her shoulders and back for warmth."

    suz "Sorry. Did I wake you?"

    mk "Nah, it's fine."

    "She did, but I manage to mumble out a half-truth that seems to satisfy her enough to turn back to what she was doing."

    "Curious, mildly frustrated, and already awake, I have little reason to stay in bed. After looking at Suzu with a disgruntled face as if I might will her back, I give up and throw my legs over the side, staggering up behind her."

    "On the screen is an unfinished history assignment. My first instinct is to scold her for being overeager, but if her narcolepsy is messing up her sleep patterns again, it's not like there's much else to do in the dark."

    "Her finger repeatedly taps lightly on a key, only stopping as I drape my arms over her shoulders and bring my head beside hers. I get the feeling she's frustrated, given how she still keeps her focus on the screen instead of me, despite her usual timidity about physical contact."

    mk "Sorry about being so forceful before. I just kinda let myself go, and..."

    suz "Hmm? I don't really mind."

    "The way she says it makes me think she actually rather enjoyed it. So she's that kind of person."

    "Relieved that I haven't actually annoyed her, the question of what the problem is remains unsolved. Maybe it really is as simple as what's before my eyes."

    mk "If you're having trouble, just leave it for later."

    show suzu_unhappy with charachange
    hide suzu_concerned

    suz "But I know this. It's what I was trying to get done before we left."

    "I read what she's done already to see if I can be of any help. An essay on the Meiji Era, by the looks of it. The four paragraphs she's done so far look fine, if a little padded in the usual 'meeting a teacher's arbitrary word count' way. As for the rest... I haven't even started it myself, so I don't really know."

    "I remain quiet for fear of disrupting her thought process, though it looks like she's struggling to get out of neutral either way."

    "The brick wall refuses to move as she wracks her brain, the frustration boiling over as she brings her forehead down to her open palm and grinds against it in annoyance. I can't help but feel sorry for Suzu as her face scrunches up, silently beating against the immovable block in her mind."

    show suzu_veryangry with charachange
    hide suzu_unhappy

    suz "I know this... I know this...!"

    "I quickly come to realise that there's little I can do for her, even if I did know more about what she was writing on. The problem isn't merely academic, after all."

    "If Hisao had his physical prowess torn from him thanks to his heart attack, it's Suzu's intelligence and work ethic that were torn from her by this troublesome condition. No matter how smart she may be, or how stubbornly she may stick to a task, she still hits the wall created by her permanent state of sleep deprivation."

    "I think over the talk I had with her sister earlier. Perhaps, thanks to that, she might get a new medicine regime that'll work better. It's not like the current one seems to be doing her much good."

    "She saved me, I have absolutely no doubt of that, yet I can't help her. My heart sinks as I wrap her in a hug, able to do little else."

    mk "Just come back to bed, Suzu. A fresh set of eyes'll help."

    show suzu_unhappy with charachange
    hide suzu_veryangry

    suz "But I-{w=.25}{nw}"

    "I clamp my hand over her mouth, having expected her to protest. I feel terrible as her face goes from frustration, to displeasure, and finally, to defeat."

    "My hand is removed from her mouth. She closes the laptop with a solemn click. Hope for working tonight leaves her."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

else:
    scene bg doggo with dissolve

    "Satisfied, I break off and turn on all fours to orient my head between her legs. Suzu seizes the brief moment of freedom as she turns on her side and begins to shuffle towards the head of the bed, but her strength leaves her after I fall onto my shoulder and kiss her below the tuft of hair."

    "Clutching her butt with my hand and bringing my stump over her other side, she surrenders and brings her lips to me. The pleasure as she does so surges through my body like lightening, driving me to pleasure her even further."

    "Again and again I lap at her, my advances less delicate than those of Suzu. It's wonderful, absolutely wonderful. I can feel my body filling as she holds me, taking in my taste as I do hers."

    "It isn't long before I feel the pleasure from that spot welling up inside of me, my grip tightening as I begin to lose myself."

    "Just a little more, just a little further..."

    "I'm forced to break my mouth from Suzu as the muscles in my neck tighten, a groan coming from deep in my chest as I desperately fight to control the feeling threatening to overwhelm me."

    "It's no use. I can't hold back, I can't...!"

    mk "Aaaaaah!"

    stop music fadeout 1.0

    scene black with shorttimeskip

    ##centered "~ Timeskip ~" with dissolve #Here's probably a timeskip in imachine needed if we ever get bgs for Suzu's room [AHA]

    #scene black with dissolve

    scene bg misc_ceiling_ni
    with openeye

    "The cool night air sticks to my skin, the first sensation to return as my eyes blearily flicker open. The plain white ceiling hangs over me, a faint light from the front of the room just barely illuminating it."

    "I reach out with my hand to feel out Suzu, but I only end up patting at the bed. A brief glance confirms the fact."

    scene bg dormsuzu with dissolve

    play sound sfx_sitting

    "Disappointed that I couldn't wake next to her, I sit up and rub my eyes in an attempt to see where she is. Despite still being out of focus, the silhouetted figure staring at her laptop's screen is unmistakable."

    mk "Suzu...?"

    show suzu_concerned with charaenter

    play music music_moonlight

    "She glances around to see me, her pyjamas back on and a blanket draped loosely over her shoulders and back for warmth."

    suz "Sorry. Did I wake you?"

    mk "Nah, it's fine."

    "She did, but I manage to mumble out a half-truth that seems to satisfy her enough to turn back to what she was doing."

    "Curious, mildly frustrated, and already awake, I have little reason to stay in bed. After looking at Suzu with a disgruntled face as if I might will her back, I give up and throw my legs over the side, staggering up behind her."

    "On the screen is an unfinished history assignment. My first instinct is to scold her for being overeager, but if her narcolepsy is messing up her sleep patterns again, it's not like there's much else to do in the dark."

    "Her finger repeatedly taps lightly on a key, only stopping as I drape my arms over her shoulders and bring my head beside hers. I get the feeling she's frustrated, given how she still keeps her focus on the screen instead of me, despite her usual timidity about physical contact."

    mk "Sorry about being so forceful before. I just kinda let myself go, and..."

    suz "Hmm? I don't really mind."

    "The way she says it makes me think she actually rather enjoyed it. So she's that kind of person."

    "Relieved that I haven't actually annoyed her, the question of what the problem is remains unsolved. Maybe it really is as simple as what's before my eyes."

    mk "If you're having trouble, just leave it for later."

    show suzu_unhappy with charachange
    hide suzu_concerned

    suz "But I know this. It's what I was trying to get done before we left."

    "I read what she's done already to see if I can be of any help. An essay on the Meiji Era, by the looks of it. The four paragraphs she's done so far look fine, if a little padded in the usual 'meeting a teacher's arbitrary word count' way. As for the rest... I haven't even started it myself, so I don't really know."

    "I remain quiet for fear of disrupting her thought process, though it looks like she's struggling to get out of neutral either way."

    "The brick wall refuses to move as she wracks her brain, the frustration boiling over as she brings her forehead down to her open palm and grinds against it in annoyance. I can't help but feel sorry for Suzu as her face scrunches up, silently beating against the immovable block in her mind."

    show suzu_veryangry with charachange
    hide suzu_unhappy

    suz "I know this... I know this...!"

    "I quickly come to realise that there's little I can do for her, even if I did know more about what she was writing on. The problem isn't merely academic, after all."

    "If Hisao had his physical prowess torn from him thanks to his heart attack, it's Suzu's intelligence and work ethic that were torn from her by this troublesome condition. No matter how smart she may be, or how stubbornly she may stick to a task, she still hits the wall created by her permanent state of sleep deprivation."

    "I think over the talk I had with her sister earlier. Perhaps, thanks to that, she might get a new medicine regime that'll work better. It's not like the current one seems to be doing her much good."

    "She saved me, I have absolutely no doubt of that, yet I can't help her. My heart sinks as I wrap her in a hug, able to do little else."

    mk "Just come back to bed, Suzu. A fresh set of eyes'll help."

    show suzu_unhappy with charachange
    hide suzu_veryangry

    suz "But I-{w=.25}{nw}"

    "I clamp my hand over her mouth, having expected her to protest. I feel terrible as her face goes from frustration, to displeasure, and finally, to defeat."

    "My hand is removed from her mouth. She closes the laptop with a solemn click. Hope for working tonight leaves her."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_S9:

    scene bg school_scienceroom with dissolve

    window show

    play music music_caged_heart

    "I always feel antsy when Suzu doesn't show up to class, and today is no different."

    "With lunch nearing and no Suzu in sight, I make up my mind to pass by her dorm room once the break starts. Until then, I have to put up with yet another drawn-out science lesson. While a few others manage to keep at least some attention focused on the blackboard as Mutou scrawls down another chemical reaction, most are beginning to watch the clock instead."

    "Hisao should be paying full attention and jotting down notes like the good little student he normally is, but he seems just as distracted as I am. Over and over he taps his pen against the page, his gaze unfocused as he stares blankly ahead."

    "Having caught my rather overt gawking, Misha gives a smile. I quickly turn my head back to the front, lest she become curious about what's going on."

    play sound sfx_normalbell

    "Eventually, thankfully, the school bell heralds the beginning of lunch. The relaxation of everyone in class is plainly obvious, even if it isn't spoken. It's no surprise that Mutou gives up on any prospect of keeping the lesson going, bidding us to have a good lunch as he collects up his teaching material."

    scene bg school_hallway3 with locationchange

    "As the class begins to file out into the hallway, Hisao does the same. Curious if he knows aything, I follow him out."

    mk "Hey."

    show hisao_frown_u with dissolve

    hi "Oh, hey."

    mk "You don't look happy to see me."

    hi "Just a lot going on right now. I'll tell you later."

    "He tries to leave, but I quickly turn behind him and throw my left arm around his neck without warning. With his neck caught in the crook of my elbow as I hold it tight with my right hand, he's completely immobilised."

    with hpunch
    show hisao_wtf_u with charachange
    hide hisao_frown_u

    hi "Miki... What are you...?"

    mk "You didn't think you were gonna get out of it that easily, did ya?"

    "He uselessly bats at me and grabs at my arm."

    hi "Let go... I can't..."

    mk "You gonna tell me what's up, then?"

    show hisao_talk_big_u with charachange
    hide hisao_wtf_u

    hi "Fine, fine! Just let me go...!"

    "I release my gip on Hisao, letting him recuperate for a few moments as he catches his breath and rubs his neck."

    show hisao_hmpf_u with charachange
    hide hisao_talk_big_u

    hi "I swear being around you is going to take years off my life..."

    mk "So, what's the story? I'm guessing this is about Suzu."

    show hisao_declare_u with charachange
    hide hisao_hmpf_u

    hi "Yukio... confessed to Suzu."

    stop music fadeout 3.0

    "Oh boy."

    show hisao_frown_u with charachange
    hide hisao_declare_u

    hi "Suzu rejected him, of course. The problem is that he didn't take it very well."

    play music music_tension

    mk "This is about me, isn't it?"

    "Hisao reluctantly nods."

    hi "Apparently he's been angry with you for a while, and now that all this happened, he let it all out on her. It was a complete mess."

    "I feel a familiar sensation beginning to run through me. Images of Yukio berating Suzu over my failures as a person come to mind, lashing out at her after bottling up his feelings."

    mk "Were you there?"

    hi "If I had been, I might've been able to do something. All I can do now is try and smooth things over."

    mk "With Suzu?"

    hi "Yukio. He was still pretty pissed, so I was going to try and calm him down first."

    "So he hasn't had enough. Fair enough; if he wants to settle the score with me, then that's just what I'll let him do."

    "I walk past Hisao and start down the hallway, knowing full well where the ass would likely be. My blood is already boiling in anticipation."

    mk "You go talk to Suzu. I'll deal with Yukio."

    show hisao_talk_big_u with charachange
    hide hisao_frown_u

    hi "Wait, Miki...!"

    stop music fadeout 1.0

    scene bg school_track with shorttimeskip

    #Timeskip

    play music music_tension

    "Striding past the line of trees separating the track from the school gardens, it doesn't take long to pick out Yukio given the few people milling about."

    scene bg school_track_on with locationchange

    show yukio_angry with charaenter

    "He looks downcast as he stands around, venting at someone with his arms crossed. So occupied is he, that he doesn't notice me walking up until I'm on the track and facing him."

    yuk "What are you doing here?"

    "The way he addresses me, in both his angered expression and acidic tone of voice, only makes me even more pissed off with him. This is all his fault, what the Hell reason does he have for looking at me with such disdain."

    "The guy he was talking to backs away. He'd have been around long enough to know how this will probably turn out."

    mk "Giving you a chance to notice me so this doesn't count as an ambush."

    show yukio_notimpressed with charachange
    hide yukio_angry

    "The corner of his mouth tugs upwards. Yukio seriously thinks he can win this? He almost looks like he's looking forward to it."

    yuk "So you've come to put me in my place, huh? Work off some stress?"

    mk "You know what you did."

    yuk "Me? I only told Suzu what I thought of her getting hitched to-{w=.75}{nw}"

    stop music

    $ renpy.music.set_volume(0.5, 0.0, channel="sound")

    play sound sfx_impact
    with vpunch
    show yukio_eeh with charachange
    hide yukio_notimpressed

    "His annoying nasally voice is cut short as my fist meets the front of his face square-on. It's little more than a quick jab to make him shut his mouth, but it's enough to send him staggering backwards."

    "Shock is written to his eyes as he stares back, his fingers brushing underneath his nose upon feeling blood trickling down. What did he think was going to happen if he talked to me like that?"

    "Several people who'd been doing club activities walk over, the flurry of activity having piqued their curiosity. One reaches out in an attempt to help him, but gets batted away as Yukio notices the red stain on his fingers."

    play music music_shadow

    show yukio_angry with charachange
    hide yukio_eeh

    yuk "You...!"

    "He suddenly moves forward with surprising speed, letting fly as he raises his fist."

    "Caught unawares by the speed he's apparently capable of,{w=.25}{nw}"

    $ renpy.music.set_volume(1.0, 0.0, channel="sound")

    play sound sfx_impact
    with vpunch
    with vpunch

    "Caught unawares by the speed he's apparently capable of,{fast} his swing at my face lands with a fair amount of force, sending my head jerking to the right."

    "But I know what to do. No, my body knows what to do. Still dazed by the blow, I reflexively raise my arms in front of my face as a shield. Even without a hand, my left arm is more than capable of this much,{w=.25}{nw}"

    $ renpy.music.set_volume(0.5, 0.0, channel="sound")

    play sound sfx_impact
    with vpunch

    "But I know what to do. No, my body knows what to do. Still dazed by the blow, I reflexively raise my arms in front of my face as a shield. Even without a hand, my left arm is more than capable of this much,{fast} the forearm absorbing his next punch."

    "It's obvious from his face that he has no idea what he's doing, simply flailing about in a violent rage. With my senses returned and Yukio on the back foot as he shakes his sore hand, now's the time to counterattack."

    "I drop my right knee as he starts another wild swing, his balled fist sailing over my shoulder as I drive my own into his undefended stomach."

    $ renpy.music.set_volume(1.0, 0.0, channel="sound")

    play sound sfx_impact
    with vpunch
    with vpunch
    show yukio_eeh with charachange
    hide yukio_angry

    "He hadn't braced at all as it drives deep into his torso, forcefully pushing the air from his lungs. Spit and a pathetic groan escape from his mouth, his stunned face frozen as his body tries to comprehend what's just happened to it."

    "There's no doubt he can't possibly fight back, confused and disoriented as he stumbles, arms tightly crossed around his pained stomach as he reflexively doubles over."

    "The boy lurches towards me for whatever reason as he begins to right himself,{w=.25}{nw}"

    $ renpy.music.set_volume(0.85, 0.0, channel="sound")

    play sound sfx_impact
    with vpunch

    "The boy lurches towards me for whatever reason as he begins to right himself,{fast} earning a powerful swing at his head in hopes of dropping him. It has the intended effect, his body sent{w=.25}{nw}"

    $ renpy.music.set_volume(1.0, 0.0, channel="sound")

    play sound sfx_sitting

    "The boy lurches towards me for whatever reason as he begins to right himself, earning a powerful swing at his head in hopes of dropping him. It has the intended effect, his body sent{fast} sprawling to the ground as my knuckles smash into his cheek."

    "This isn't enough. He won't learn from this. I have to make this final and irrefutable in his idiotic head."

    scene bg school_track_running with locationchange
    show yukio_eeh

    play sound sfx_sitting

    "I drop to my knees, following him to the ground and straddling his chest. The look of absolute fear in his eyes as he realises the situation only drives me on. This is what I want. This is the emotion I want him to feel, to remember long after this ends."

    "He raises an arm over his bloodied head, but it's in vain. I twist my entire upper body as I ready the blow, my fist flying downward at him with all the force I can muster."

    $ renpy.music.set_volume(0.8, 0.0, channel="sound")
    play sound sfx_impact
    with vpunch

    "The feeling of impact ripples up my arm and floods my entire body. All prospect of defense deserting him as the strength leaves his arm, but it isn't enough. He deserves this. This repugnant being deserves this. Why shouldn't I enjoy teaching bad people like him a lesson?"

    "I pull back my arm,{w=.25}{nw}"

    play sound sfx_impact
    with vpunch

    "I pull back my arm,{fast} slamming it into him once more. I can feel my face distorted by the wild grin my mouth has twisted into. This is fun. He'll remember me for this. He always will. He'll never forget how it was his fault this happened."

    "He'll never forget how powerful I am compared to him. That's what truly matters. He's a bug. That's all he is, an ugly little bug under my foot. And now, he'll never forget it"

    "I pull my fist back, my knuckles covered in a mix of his blood and dirt from the ground. This bug can't even defend itself now. It's at my mercy. I can stomp on it as much as I want!"

    play sound sfx_impact
    with vpunch

    "Again my knuckles slam into the broken face below me, eyes rolling about with each catastrophic blow. The blood running into its throat giving a slight gurgle with each ragged breath taken. So what if I'm stupid? So what if I lost everything? I'm stronger than this bug. Nothing could be better than this feeling."

    "But as my arm flies down at the bug beneath me for another hit, it suddenly stops."

    with vpunch

    "I try to pull back and punch once more simply due to the adrenaline coursing through me, but only afterwards do I realise that someone's firmly grabbed my arm."

    mk "Let go-!"

    "Rage begins to fill my mind as another hand comes around my right armpit, followed by another set of hands taking a firm grasp of my left arm. I jerk my body{w=.25}{nw}"

    with vpunch

    "Rage begins to fill my mind as another hand comes around my right armpit, followed by another set of hands taking a firm grasp of my left arm. I jerk my body{fast} with all my might, but the groaning body beneath me slowly becomes smaller and smaller as I'm dragged off it."

    mk "Let go! Let go of me!"

    "Try as I might, I can't escape their grasp. Flicking my head around as I desperately try to work myself free reveals my captors to be Haru and Hisao, likely the only two track club members who'd ever dare approaching me in a fight."

    scene bg school_track_on with locationchange

    "They manage to pull me a few yards away with some difficulty, holding me fast as help finally comes to Yukio. It pisses me off to see him still awake, dribbling blood as slowly staggers to his feet with the help of another guy who was hanging around."

    show yukio_punched with moveinbottom

    "He very barely manages to stay on two feet, practically held up by the one who aided him, but that doesn't stop him staring me down through half-closed eyelids."

    yuk "Happy now? You... really put me in... my place..."

    mk "Don't you feel sorry, you asshole!? How can you do that to someone you pretend to like!"

    yuk "And let her go... to some violent bitch... like you?"

    mk "I'm not like that anymore! That was years ago!"

    show yukio_punched_defiant with charachange
    hide yukio_punched

    "Somehow, to the surprise of damn near everybody, he breaks out into laughter. A warped, pitiable laughter. Tears begin to stream down his bruised cheeks, face twisted in impotent rage."

    yuk "Look at you! Look at you!"

    yuk "How can you say you've changed!?"

    "I feel my arms drop to my sides, Hisao and Haru having let go. I only notice now that I haven't been struggling for a while, but try as I might, I can't find the will to move at him."

    "This... is what I wanted, right? I did what I set out to do, after all. He made Suzu sad by ranting at her. He deserved this. I can't let myself be distracted from that."

    mk "I...!"

    show yukio_punched_angry with charachange
    hide yukio_punched_defiant

    yuk "I, I, I, that's all you ever thought about, isn't it?"

    yuk "I did everything right! You only ever hurt everyone around you! Now you waltz around like you're a different person?"

    yuk "You never changed! You think everyone can forget what you did!? Fuck you!"

    show yukio_punched with charachange
    hide yukio_punched_angry

    "With his fury seemingly spent, he simply hangs his head and shakes it from side to side. He's mentally and physically defeated, reduced to weeping pathetically in front of everyone who's gathered for the spectacle."

    yuk "It's not fair... It's not fair..."

    "All he can do is repeat the sorry mantra. Snot and blood drip onto the ground from his nose, his shoulders occasionally jerking as he tries to hold it back. Nobody says a word."

    show yukio_punched_angry with charachange
    hide yukio_punched

    "His fists tighten as he speaks, his knuckles becoming white. Just as I realise what it means, his shuddering body lurches forward, slipping from the grasp of the guy next to him."

    yuk "Someone like you doesn't deserve happiness!"

    "He screams the words as he surges towards me, the intense pain that must be wracking his body all but forgotten in his blind fury."

    "Yukio's arm rears back over his shoulder as he prepares for as hard a blow as he can manage. I should probably raise my arms to defend myself right about now. Maybe evade to the side and dodge the blow."

    "But I don't care anymore. All I can do is stand there and watch his fist moving through the air as his words reverberate in my mind."

    "Someone like me really doesn't deserve happiness."

    "With that,{w=.25}{nw}"

    stop music

    play sound sfx_impact
    with vpunch

    scene black with dissolve

    "With that,{fast} my world goes black."

    $ renpy.music.set_volume(1.0, 0.0, channel="sound") #restoring volume to default

    ##centered "~ Timeskip ~" with dissolve
    with shorttimeskip

    play music music_moonlight

    "I've always hated the nurse's office. The smell of bleach and strong cleaning agents, the pure white light flooding the room, the way everything is so immaculately clean and perfect... it's unnatural."

    scene bg misc_ceiling_ss with openeye

    "A familiar metallic taste plays on my tongue as I wake from my rest. Tapping at the small gauze patch placed over where it's split shows that it isn't doing a great job of stemming the bleeding. Passing my hand over my aching cheek, it seems that's started swelling up, too. Never would've expected that asshole to throw a decent punch."

    scene bg school_nurseoffice_ss with locationchange

    "While I might be content to stew in my discontent, it seems some people have other ideas. As my head lazily lulls over to the side to see the office, I find a pair of legs in front of my vision, one knee smartly brought over the other as two hands sit atop them."

    show shizu_basic_normal2 with charaenter

    "Shizune looks down at me past her glasses, her stare more analytical than judgemental. Glancing around, it looks like she and I are the only ones here right now."

    mk "Of all the people to greet me, it had to be the one I can't even communicate with..."

    "She produces a notepad and pen from her lap, placing them both on my chest before resuming her previous posture."

    "Ah, I see. By giving me these without telling me what to write, she wants to see how I'll explain myself."

    "Given that I can't see any way of talking my way out this,{w=.25}{nw}"

    play sound sfx_sitting

    "Given that I can't see any way of talking my way out this,{fast} I sit up with a pained grunt and set the pad in my lap. Knowing my voice to be useless here, I silently scrawl away in my usual horrid handwriting, giving the items back to her afterwards."

    mk "[[I fucked up.]"

    show shizu_behind_blank with charamove
    hide shizu_basic_normal2

    "She quickly writes her short reply, our method of communication settled as she hands the notepad and pen back."

    shi "[[It would seem so.]"

    "So she wants to be my scratching post. While I can't say her presence thrills me, at least she's not going to give me a lecture."

    "Writing like this to talk between each other forces you to think before you say anything. It's not natural for me, so I end up keeping my side of the conversation brief."

    mk "[[Mutou put you up to checking on me?]"

    shi "[[Your cynicism is duly noted, but I came of my own accord.]"

    mk "[[How much do you know?]"

    show shizu_basic_angry with charamove
    hide shizu_behind_blank

    "She just looks at me disapprovingly before handing the notepad straight back. Right, stupid question."

    mk "[[Am I done for?]"

    shi "[[That hasn't been decided yet. Suffice to say, you are not a popular person right now.]"

    "That's fair enough; expelling a student is hardly a quick process. The idea fills me with dread, but after having been so graciously given a second chance when the entire staff were so set against me, I don't feel that I have any right to argue against it."

    mk "[[I guess your little project went pretty bad, huh?]"

    show shizu_cross_angry with charamove
    hide shizu_basic_angry

    "Woah, she's actually pretty scary when she's pissed. I shrink back into my bed as she furiously scribbles, gingerly taking the notepad and pen as she thrusts them at me. It seems to have been somewhat cathartic, as she settles down a bit after huffing in displeasure."

    shi "[[I didn't defend you back then out of mercy or some desire to play student counsellor. I felt the attitude of the teachers towards you was unjust. Which students were involved doesn't matter.]"

    "So I'm nothing special to her, but just another person who happened to be unfairly treated. In a way, that actually makes me like her a little more."

    "Evidently sick of waiting for me to make a response, Shizune takes back her notepad once more."

    shi "[[You should stop thinking about yourself.]"

    "Shit, Suzu! There's no way word about all this wouldn't have reached her by now. There's also the fact that probably damn near half the school knows about the two of us being together as well thanks to Yukio's big mouth, despite her wanting to keep it on the down-low."

    "Noticing my regret, Shizune quickly adds more text."

    show shizu_basic_angry with charamove
    hide shizu_cross_angry

    shi "[[Suzuki also came to check on how you were. I don't think I need to explain her reaction.]"

    mk "I really did fuck up..."

    "Of all the people I never wanted to hurt, she was at the top, but I couldn't even manage that. She offers me the notepad, but there's little point in taking it."

    shi "[[If there's nothing else, I'll leave you in peace.]"

    mk "[[Thanks for bothering to come, and give Misha my regards.]"

    "I manage, somehow, to eke out a smile. Satisfied, she picks herself up and begins to leave with a curt bow, though holds up one final note after a brief moment of thought."

    show shizu_basic_normal2 with charachange
    hide shizu_basic_angry

    shi "[[If you wish, I'll tell Suzu you're okay. I have no intention of meddling in your relationship any further, mind.]"

    "I know it's the easy way out, but I swallow my pride and give her a nod. I can't even think of what I'd tell her, after all."

    "As Shizune closes the door behind her,{w=.25}{nw}"

    play sound sfx_pillow

    scene bg misc_ceiling_ss with dissolve

    "As Shizune closes the door behind her,{fast} I let myself fall back into my bed."

    "I guess this means Suzu's seen with her own eyes how wrong she was."

    "So what if I made myself useful to her or not? I spent so long trying to distract myself from the crap I'd done, that I pushed aside all those I'd caused pain to. What right do I have to ask for forgiveness, when I was the one who inflicted all of this in the first place."

    "'There's no such thing as good people or bad people.' What a load of idealistic rubbish."

    "In the end, I was right. I really am a horrible person."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_S10:

    $ renpy.music.set_volume(0.2, 0.0, channel="ambient") #may need to be more silent depending on music or maybe louder -Niji

    play ambient sfx_rain fadein 2.0

    play music music_raindrops

    scene bg mp3 with dissolve

    "Today, the weather turned bad."

    "The sound of rain hitting the window mixes with the tinny pop music in my left ear, the girl in my lap having the other earbud. It's not a terrible way to spend a lazy evening, to be honest."

    "The MP3 player lays on the tatty upturned box in my room as it blares away, Suzu tapping away on her phone while sitting in my lap. She'd never have let me watch her browsing her internet sites before, so I count it as a small success in gaining her trust."

    "Discussing some show on a message board doesn't seem all that exciting, but at least it means she's socialising more than it appears within school."

    mk "You sure spend a lot of time on the Internet. You always talking to people like this, or what?"

    suz "Some of the time. Most of my friends are online, after all."

    mk "Ah, so you're still in contact with your friends from when you were younger. That's pretty nice."

    suz "I mean I know them online. I've never met them in person."

    mk "That's kinda different to real friends, you know."

    suz "They are real friends. Why does it matter if I don't see them?"

    mk "Well... I mean..."

    "What she said is so foreign to me that I struggle to actually come up with a counterargument. How can you have a meaningful relationship with someone you've never met?"

    mk "It just doesn't seem the same."

    suz "You're really old-fashioned sometimes."

    "Like so many of our conversations, this one peters out just the same with little satisfactory conclusion. As much as I might try to build bridges between our different lives, they never quite seem to meet in the middle."

    "But then again, it's always been like that. Maybe I was hoping that going out with her might change things, but Suzu still feels as impenetrable as ever. After such a long time staying so intensely private, the door to let others inside has become jammed."

    "Then again, given recent events, maybe this is a bad time to reflect on her social skills."

    "While I may have avoided the wrath of my teachers beyond a long period of detention, ostracization was much harder to escape. In the minds of those who knew me, every idea they had about my real nature was validated. To those who didn't, I was simply deemed trouble that was best avoided."

    "Suzu's a solitary person to begin with, but I can't imagine she's oblivious to the weird atmosphere around us now. Any idea of peacefully coasting along to graduation has been ruined, all thanks to Yukio and I."

    "If I hadn't fought him, if he hadn't goaded me onward, if he hadn't confessed, if I'd mentioned our relationship, the amount of 'if's that came before where we are now is endless."

    play sound sfx_doorknock
    scene bg school_dormmiki with dissolve

    "The sound of a hand rapping on my door breaks me from my thoughts. I'm almost thankful."

    mk "It's unlocked!"

    play sound sfx_dooropen
    show hisao_smile_u at rightedge with moveinright
    show haru_yo at center with moveinright

    "Two pairs of feet shuffle into the room, their owners revealed to be Haru and Hisao. The former waves, while the latter holds up the pack of cards he's carrying."

    har "'Evening."

    suz "Hi."

    mk "Hey. Looks like you two came prepared."

    show haru_basic at center with charamove
    hide haru_yo at center

    har "Not like there's much we can do outside. Up for a game of poker?"

    mk "Sure. Suzu?"

    "She just nods. With something to do having finally arrived, I take out the earbud and loosen my grip around Suzu's waist."

    show suzu_neutral at leftoff with moveinleft
    show suzu_neutral at leftoffsit with charamove
    show haru_basic at centersit with charamove
    show hisao_smile_u at rightedgesit with charamove

    "She takes her cue to wrap up the earphone cable around the MP3 player, put away her phone, and shuffle around to the side of the box as Hisao and Haru take their places around it."

    "Waiting on Hisao to finish clumsily shuffling the deck, I can't help but feel that what Haru says is little more than a pretext to check up on us, but that isn't necessarily a bad thing."

    mk "Oh, right. We bettin' anything?"

    show suzu_speak at leftoffsit with charamove
    hide suzu_neutral at leftoffsit

    suz "I don't have any money on me."

    show hisao_wtf_u at rightedgesit with charachange
    hide hisao_smile_u at rightedgesit

    hi "We're not betting real money. Good grief."

    "How boring. Being such a stickler for rules is one of his worse traits."

    show hisao_erm_u at rightedgesit with charachange
    hide hisao_wtf_u at rightedgesit
    show suzu_neutral at leftoffsit with charamove
    hide suzu_speak at leftoffsit

    "It's eventually agreed that we'll bet using small scraps of torn-up paper as tokens, an old unused worksheet being sacrificed for the task. Hisao ends up the dealer by virtue of already having the pack, doling out a set of cards to each of us."

    "Receiving my cards, I take a look. Three of a kind, but low. Not the worst hand, I guess."

    show haru_sad at centersit with charamove
    hide haru_basic at centersit

    har "Guess the dry spell was just the weather preparing to dump it all in one go."

    mk "It's sure comin' down hard."

    "Looking to Hisao to try and get a read on his cards, I find him already glancing at us."

    mk "What's with you?"

    hi "I was just thinking how you two are all over each other these days."

    "It's natural, isn't it? With everything feeling like it's slipping out of my control, I want to stay close as I can to what I still hold dear. Given her unusual comfort with being physically close, I've little doubt she thinks the same way. Even as I hold her, it feels like she might slip from my grasp at any moment."

    show suzu_unhappy at leftoffsit with charamove
    hide suzu_neutral at leftoffsit

    suz "Is that bad?"

    mk "You need to quit assuming the worst of what people say."

    "Suzu accepts the scolding without word, making me feel a little bad. Whether to comfort her or myself, I give her head a little rub. She seems to like it when I do so, at least as far as I can tell."

    "As the game continues on, the elephant in the room is finally addressed. It was going to be either Suzu or I who brought it up, and it turns out to be her."

    show suzu_concerned at leftoffsit with charachange
    hide suzu_unhappy at leftoffsit

    suz "What happened to Hasegawa?"

    "Suzu's gaze is focused on her cards, my own looking to the other two with us. It's strange to see Haru so uncomfortable, Hisao ending up having to give the news."

    hi "Just keeping to himself, really. Ended up leaving the club."

    "He says the second part with all the gravity of the first, as if such a thing hardly mattered."

    "Yukio never did have that much attachment to the club compared to most of the others, but it's still an unwelcome surprise. While his face may eventually mend, his pride would be another matter."

    "Perhaps Yukio's departure is what makes breaking my own news somewhat easier."

    mk "To be honest.. I've been thinking of quitting the club as well."

    show suzu_surprised at leftoffsit with charamove
    hide suzu_concerned at leftoffsit
    show haru_serious at centersit with charamove
    hide haru_sad at centersit
    show hisao_talk_big_u at rightedgesit with charachange
    hide hisao_erm_u at rightedgesit

    suz "What?"

    "Three pairs of eyes round on me in shock."

    hi "Did the teachers tell you to, or...?"

    mk "No, nothing like that. It's just, after everything that happened..."

    mk "Besides, I can spend more time with Suzu this way."

    "I feel like I'm spluttering out excuses, but I've no reason to considering who I'm with."

    "There's no point in continuing to push myself. I've done enough damage already, and it's clear that I'll never fit in with the others any more. It's one thing to get in a scrap or two, but another to make past events return to people's minds."

    show suzu_neutral at leftoffsit with charachange
    hide suzu_surprised at leftoffsit

    "I look to Suzu expecting a smile in return for my thinking of her, but she just calls out that she wants to fold instead. As impenetrable as ever."

    har "Geez. I mean, it is up to you, but isn't that kinda overdoing it? The club ain't gonna be the same without you around."

    suz "If you're doing this for me, then don't."

    show hisao_talk_small_u at rightedgesit with charachange
    hide hisao_talk_big_u at rightedgesit

    hi "Seriously. There isn't that much time left, so why not stick around until graduation?"

    mk "I appreciate you tryin' to keep me, but it's seriously fine."

    mk "I'm folding, by the way."

    show hisao_erm_u at rightedgesit with charachange
    hide hisao_talk_small_u at rightedgesit

    "There's a moment of confusion before everyone realises that we were actually playing poker. With everyone folding but Hisao, he nets himself a nice little haul of tokens."

    mk "You sure you don't want to put money on this, Hisao? You're actually pretty good at it."

    "He shrugs simply."

    hi "Card games are just probability puzzles."

    har "Easy for you to say..."

    with shorttimeskip

    "Looks like Haru's down to his last couple of tokens, and it's the same for me. Suzu's managing to hold her own, but it's clear who's dominating the game."

    show hisao_frown_u at rightedgesit with charachange
    hide hisao_erm_u at rightedgesit

    "Hisao checks his watch, frowning at the result. I suspect that we have our winners and losers decided for the night."

    hi "We'd better wrap this up. It's getting late."

    show haru_sad at centersit with charamove
    hide haru_serious at centersit
    show haru_sad at center with charamove

    "Haru looks reluctant, but after glancing at his own watch, he comes to his feet."

    har "Man, I was so close..."

    har "Well, whatever. See you guys tomorrow, 'kay?"

    suz "Good night."

    mk "See ya. If you see Yukio..."

    "Then what? Say sorry for me? I still feel like he was in the wrong. Even saying hi to him would feel weird, though."

    mk "Just make sure he's okay, will you?"

    show haru_serious at center with charamove
    hide haru_sad at center
    show hisao_smile_u at rightedgesit with charachange
    hide hisao_frown_u at rightedgesit

    "A nod from Haru is the response, the last of the playing cards being shovelled into the packet after Hisao and Suzu finish collecting them off the box."

    show hisao_smile_u at rightedge with charamove
    hide hisao_smile_u with moveoutright
    hide haru_serious with moveoutright

    queue sound [ sfx_dooropen, sfx_void, sfx_void, sfx_void, sfx_doorclose ]

    "The two take their leave, Hisao giving a friendly wave goodbye as he does. If they did come to check on how we were doing, I wonder if they were happy with what they found."

    hide suzu_neutral with moveoutbottom
    play sound sfx_pillow

    "Suzu lets herself fall back and closes her eyes, chest heaving from her tired sigh. Being around people sure takes a lot out of her."

    mk "You awake?"

    suz "Yes."

    mk "I'm sorry. About Yukio, that is."

    suz "It's not your fault."

    mk "It is my fault; I started that fight."

    suz "There's no point crying over spilled milk. It was going to happen eventually."

    mk "What do you mean by that?"

    suz "Nothing. Go and take a shower."

    mk "C'mon, why are you being like that?"

    suz "Because you stink. We can talk afterwards."

    "I raise an arm and take a sniff. I guess I have been more anxious than usual during the day, given all that's happened."

    "Giving up without an argument, I stand and begin to fossick around my room for wherever my pyjamas gave gotten to."

    mk "You should probably head back to your own room sometime, too."

    "With no reply forthcoming, I pause and look back to her. Eyes still closed, a few seconds pass as I wait for any kind of response."

    suz "I want to stay with you tonight."

    "I guess that's that, then."

    stop ambient fadeout 1.0
    stop music fadeout 1.0

    #centered "~ Timeskip ~" with dissolve

    scene bg school_dormbathroom with shorttimeskip

    $ renpy.music.set_volume(0.85, 0.0, channel="ambient") #restoring volume to default

    play ambient sfx_shower fadein 0.3

    show steam with dissolve

    "The warm water of the shower brings to mind the hot baths I used to enjoy back home. It's exactly the kind of relaxation I needed."

    "So much so that I can't help but yawn. Suzu's sleep schedule might be messed up, but for those of us with a normal sense of time, this is getting pretty late. I end up just standing around more than actually washing, enjoying the peaceful solitude."

    "What Shizune said, or wrote, stuck in my mind. Maybe I am selfish; I have tended to think about what I enjoy over what others might think of me or want they to do. I've tried to fix that, though. I've tried to make everyone happy, and especially so for Suzu."

    "But have I managed that? It seems that things are worse than ever since Suzu and I became an item. We may still not see eye to eye on when we should've come out, not that it matters now, but aside from that it's hard to find fault with her."

    "Shizune may have told me not to think so much about myself, but it's hard not to when it feels like I'm the root of so many people's problems."

    queue sound [ sfx_dooropen, sfx_void, sfx_void, sfx_void, sfx_doorclose ]

    "Past the sound of the running shower, the sound of someone opening the door and closing it behind them can be heard. Unusual for anyone to be taking a shower this late, so much so that I open the stall door and poke my head out to see if it's who I think it is."

    "The girl's body isn't hard to make out past the light fog, her arms awkwardly positioned as she fights against her embarrassment."

    play music music_to_become_one

    "My first thought is that Suzu's just going to take a shower as well, but I find myself stepping backward in sheer startlement as she advances. With every step I take being matched, the two of us end up packed into the one stall with the door left hanging open."

    "Suzu's initiative is charming, but try as I might to play it off with some witty comment, I feel so uncomfortable that the words don't come. The way she just looks ahead, not reacting at all to the shower's water now pouring over her, is off-putting. She's also said before that she hates how hot I run my water."

    mk "Suzu... what's going on?"

    "The words seem to stir her into action, arms wrapping around my back as her lips come to mine. It doesn't take long for me to reciprocate, my resistance melting away as our tongues intermingle."

    "Her wet body feels wonderful, my hands running over the nape of her neck, her impossibly smooth back, her petite butt, every inch of her that I can get my hand over. I can't get enough of this feeling, out bodies pressed against one another and simply taking in each other's forms."

    "Suzu really is beautiful, in a way that I could never be. Even when I was young I never looked as cute as she, her silky, near unblemished skin telling of a pampered life so unlike my own."

    "But that in itself makes me think back to what I'd been ruminating over. Suzu is gentle, unlike my brutish nature. She doesn't see the world as I do, nor has she experienced the hardships I have. What worth do I have, in her eyes?"

    "I break from our kissing, but before I can say a word, her head lowers. A peck to the collar, before working her way down to my right breast. She plays at it with her mouth, sucking at it, kissing the nipple, teasing and caressing it with her tongue."

    "A moan escapes my lips, hurriedly stifled in the case someone outside may hear. I don't want to think about anything other than Suzu. Just now, just for this moment, I want to think only of her. I desperately try to turn off my mind and let myself drift along with the pleasure she's trying so earnestly to give me."

if persistent.adultmode:
    scene bg 4255 with dissolve

    "Her lips move downward, her hands on my sides slipping downward with her. She holds her face so close to me that it might almost be touching, as if observing every detail as closely as possible. A kiss to my toned stomach follows, then to my bellybutton, then to my lower hair, and finally..."

    mk "Ah..."

    "She kisses my nub before beginning to tease it with her tongue, her movements less careful around the area than when we've done this before. My advice for her to be less gentle seems to have taken as she pleases me, lapping up both my moisture and the water flowing over me as she goes."

    "I just stroke her hair, basking in her adoration as she looks up at me expectantly. Perhaps it's the excitement of her coming onto me, or of us doing this in the showers, but either way I can't get enough of her."

    mk "Like that... just keep going..."

    "She obeys me without complaint, now keeping her motions even as she sucks and flicks at me with the very tip of her tongue. The tide of euphoria starts rising without receding, my muscles relaxing as I let myself get carried away."

    "Almost by surprise, a sharp spike in pleasure floods through me. I desperately hold on to the thread as it so nearly slips my grasp, my breathing accelerating as I feel the end so quickly approaching."

    mk "Suzu... Suzu...!"

    mk "Aaahn!"

    "My mind blanks as the bliss of climax washes over me, every sense forgotten as I focus on that most wonderful feeling."

    "But all too soon, it leaves me. The water running over my body, Suzu's hands holding my thighs and butt, those beautiful eyes of hers with their mix of happiness and timidity; it all returns, with each as comforting as the last."

    scene bg school_dormbathroom with dissolve
    show steam

    "Suzu stands back up, holding me tightly. It's far from unappreciated, as even now the feeling of her against me feels somehow more vivid than ever. My hand sinks tightly into her skin, pressing us together as tightly as I can."

    "Taking a hold of her shoulder, I pull back to twist her body around, pulling her back against me and holding her once more. She doesn't protest as I kiss her shoulder, nor as I grope her breast while holding my stump across her stomach."

    "My hand ventures downward until sliding between her legs, Suzu's breath catching as I begin to massage her."

    "Her body relaxes in my arms as I do so, her flustered face visible in the mirror ahead as I circle and stroke with my finger. I don't think she realises I can see her reflection, the expression on her cute face twisting and turning as I fiddle with her."

    "Wanting to push her excitement further, I take my hand from her and reach behind me for the still-running showerhead, twisting it from its holder."

    suz "Miki, what are you doing?"

    mk "Quiet..."

    "My words do little to settle Suzu, but her curiosity and my grip on her provide a persuasive enough counterargument as she falls silent."

    scene bg 4258 with dissolve

    "I lower the showerhead slowly, allowing her time to prepare herself before, finally, it reaches her most tender spot."

    suz "Aah..."

    "She sounds more pained than anything as the water hits her, the initial stimulation proving to be too much."

    "Without another hand to adjust the strength of the flow, I simply hold her close and move the spray in a stroking motion over her groin, hoping to ease her into it."

    "The moans escaping her lips tell of the pleasure starting to overcome Suzu, the showerhead now held steady. I can't help but smile as she begins to lose herself, succumbing to the joy I'm giving her."

    "With one hand on my thigh and the other holding my own, she throws her head back. With her mouth so close to my ear, I find myself getting carried away by the sound of her desperate whimpering."

    suz "Miki, I... Aahn!"

    "Her body freezes as she reaches the end, eyes shut tightly as she lets herself drown in the sensation."

    scene bg school_dormbathroom with dissolve
    show steam

    "All too soon, it passes. I let the showerhead drop to the floor and clutch her tightly, lest she fall in her relaxed state. The glow of climax lingering, with a long, satisfied breath passing her lips."

    "My hand digs into her skin as my mind starts to dwell. This isn't enough; I want to push her further."

    "I lift her just enough to allow myself to walk forwards, stepping forward as best I can."

    $ renpy.music.set_volume(0.65, 3.0, channel="ambient")

    suz "Miki... what are you...?"

    "Reaching the counter ahead, I let Suzu drop and thrust her forward. She has no opportunity stop herself before her legs hit the side, sending her top half sprawling forwards."

    "As Suzu's body flops over the counter with a wet thud, her arms splaying out and hands gripping at the slippery surface, she manages to pick herself up and look behind her in surprise. The expression on my face is no doubt telling of what's about to happen."

    "I wordlessly push her back down with my stump, Suzu's chest pressing against the counter once more as she looks back down in submission. A shiver of excitement runs through me as she does so, knowing that she's surrendered her body to my wishes."

    "By now, only the lightest brush is needed to make her groan as I scoop my right hand between her legs, her whimpers full of renewed lust as my fingers begin to move back and forth, around and around."

    "As I stand behind her, I toy freely with Suzu's body as I bask in the sight of her consumed by desire at my hand. Suzu has rather nice legs, now that I can see them from this angle, and the arch of her back is a wonderful sight."

    "Driven onward by the sight, I bring two fingers together and end my playing with her nub. Her body jerks forwards in response to my penetrating her, her barely-constrained whimpers peaking sharply in volume and pitch in surprise."

    "I'm slowly coming to understand what she enjoys, my moistened fingers drumming against those areas she gives the most reaction to. "

    suz "Aah... Miki, please..."

    "Her voice takes on an almost alarmed edge, my movements going faster to unsettle her further. At this moment, her body is mine. Even now she'd be approaching the end, her fingertips pressing at the counter with ever more force to try and restrain herself."

    suz "Aaah..."

    suz "Miki, I can't... please... I'm going..."

    "The reason for the strange lilt to her voice is lost on me for a scant couple of seconds, before it becomes all too obvious."

    "All control of her muscles leaves Suzu, her arms that had been clutching at the counter going limp, and head dropping. I barely have time to step back as her knees buckle and collapse from beneath her, sending her body slipping off and falling towards the ground."

    "Caught completely by surprise, I barely manage to catch her wet body. Her slipperiness makes it impossible to stop her falling, the only thing I can do being to hold her to me and letting myself drop with her."

    stop music

    play sound sfx_impact
    with vpunch

    "The two of us end up sprawled on the floor, Suzu's limp figure awkwardly perched in my arms as I sit on the tiled floor. My butt hurts, but that's the least of my worries."

    "She doesn't seem to be hurt, thank goodness. Bringing my arm around her back and slowly lifting her up into a more sensible position, I hold her limp body against me as delicately as I can manage. If it's a cataplexy attack as I imagine it is, she'd still be well aware of what's going on."

    mk "I'm sorry, Suzu. I got carried away. I'm really, really sorry."

    suz "It's okay..."

    "She manages to mumble the words despite her muscles still being weak, barely even able to lift her eyelids. It only makes me hold her all the tighter."

    stop ambient fadeout 0.3

    hide steam with dissolve

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

else:
    scene bg doggo with dissolve

    "Her lips move downward, her hands on my sides slipping downward with her. She holds her face so close to me that it might almost be touching, as if observing every detail as closely as possible. A kiss to my toned stomach follows, then to my bellybutton, then to my lower hair, and finally..."

    mk "Ah..."

    "She kisses my nub before beginning to tease it with her tongue, her movements less careful around the area than when we've done this before. My advice for her to be less gentle seems to have taken as she pleases me, lapping up both my moisture and the water flowing over me as she goes."

    "I just stroke her hair, basking in her adoration as she looks up at me expectantly. Perhaps it's the excitement of her coming onto me, or of us doing this in the showers, but either way I can't get enough of her."

    mk "Like that... just keep going..."

    "She obeys me without complaint, now keeping her motions even as she sucks and flicks at me with the very tip of her tongue. The tide of euphoria starts rising without receding, my muscles relaxing as I let myself get carried away."

    "Almost by surprise, a sharp spike in pleasure floods through me. I desperately hold on to the thread as it so nearly slips my grasp, my breathing accelerating as I feel the end so quickly approaching."

    mk "Suzu... Suzu...!"

    mk "Aaahn!"

    "My mind blanks as the bliss of climax washes over me, every sense forgotten as I focus on that most wonderful feeling."

    "But all too soon, it leaves me. The water running over my body, Suzu's hands holding my thighs and butt, those beautiful eyes of hers with their mix of happiness and timidity; it all returns, with each as comforting as the last."

    scene bg school_dormbathroom with dissolve
    show steam

    "Suzu stands back up, holding me tightly. It's far from unappreciated, as even now the feeling of her against me feels somehow more vivid than ever. My hand sinks tightly into her skin, pressing us together as tightly as I can."

    "Taking a hold of her shoulder, I pull back to twist her body around, pulling her back against me and holding her once more. She doesn't protest as I kiss her shoulder, nor as I grope her breast while holding my stump across her stomach."

    "My hand ventures downward until sliding between her legs, Suzu's breath catching as I begin to massage her."

    "Her body relaxes in my arms as I do so, her flustered face visible in the mirror ahead as I circle and stroke with my finger. I don't think she realises I can see her reflection, the expression on her cute face twisting and turning as I fiddle with her."

    "Wanting to push her excitement further, I take my hand from her and reach behind me for the still-running showerhead, twisting it from its holder."

    suz "Miki, what are you doing?"

    mk "Quiet..."

    "My words do little to settle Suzu, but her curiosity and my grip on her provide a persuasive enough counterargument as she falls silent."

    scene bg doggo with dissolve

    "I lower the showerhead slowly, allowing her time to prepare herself before, finally, it reaches her most tender spot."

    suz "Aah..."

    "She sounds more pained than anything as the water hits her, the initial stimulation proving to be too much."

    "Without another hand to adjust the strength of the flow, I simply hold her close and move the spray in a stroking motion over her groin, hoping to ease her into it."

    "The moans escaping her lips tell of the pleasure starting to overcome Suzu, the showerhead now held steady. I can't help but smile as she begins to lose herself, succumbing to the joy I'm giving her."

    "With one hand on my thigh and the other holding my own, she throws her head back. With her mouth so close to my ear, I find myself getting carried away by the sound of her desperate whimpering."

    suz "Miki, I... Aahn!"

    "Her body freezes as she reaches the end, eyes shut tightly as she lets herself drown in the sensation."

    "All too soon, it passes. I let the showerhead drop to the floor and clutch her tightly, lest she fall in her relaxed state. The glow of climax lingering, with a long, satisfied breath passing her lips."

    "My hand digs into her skin as my mind starts to dwell. This isn't enough; I want to push her further."

    "I lift her just enough to allow myself to walk forwards, stepping forward as best I can."

    $ renpy.music.set_volume(0.65, 3.0, channel="ambient")

    suz "Miki... what are you...?"

    "Reaching the counter ahead, I let Suzu drop and thrust her forward. She has no opportunity stop herself before her legs hit the side, sending her top half sprawling forwards."

    "As Suzu's body flops over the counter with a wet thud, her arms splaying out and hands gripping at the slippery surface, she manages to pick herself up and look behind her in surprise. The expression on my face is no doubt telling of what's about to happen."

    "I wordlessly push her back down with my stump, Suzu's chest pressing against the counter once more as she looks back down in submission. A shiver of excitement runs through me as she does so, knowing that she's surrendered her body to my wishes."

    "By now, only the lightest brush is needed to make her groan as I scoop my right hand between her legs, her whimpers full of renewed lust as my fingers begin to move back and forth, around and around."

    "As I stand behind her, I toy freely with Suzu's body as I bask in the sight of her consumed by desire at my hand. Suzu has rather nice legs, now that I can see them from this angle, and the arch of her back is a wonderful sight."

    "Driven onward by the sight, I bring two fingers together and end my playing with her nub. Her body jerks forwards in response to my penetrating her, her barely-constrained whimpers peaking sharply in volume and pitch in surprise."

    "I'm slowly coming to understand what she enjoys, my moistened fingers drumming against those areas she gives the most reaction to. "

    suz "Aah... Miki, please..."

    "Her voice takes on an almost alarmed edge, my movements going faster to unsettle her further. At this moment, her body is mine. Even now she'd be approaching the end, her fingertips pressing at the counter with ever more force to try and restrain herself."

    suz "Aaah..."

    suz "Miki, I can't... please... I'm going..."

    scene bg school_dormbathroom with dissolve
    show steam

    "The reason for the strange lilt to her voice is lost on me for a scant couple of seconds, before it becomes all too obvious."

    "All control of her muscles leaves Suzu, her arms that had been clutching at the counter going limp, and head dropping. I barely have time to step back as her knees buckle and collapse from beneath her, sending her body slipping off and falling towards the ground."

    "Caught completely by surprise, I barely manage to catch her wet body. Her slipperiness makes it impossible to stop her falling, the only thing I can do being to hold her to me and letting myself drop with her."

    stop music

    play sound sfx_impact
    with vpunch

    "The two of us end up sprawled on the floor, Suzu's limp figure awkwardly perched in my arms as I sit on the tiled floor. My butt hurts, but that's the least of my worries."

    "She doesn't seem to be hurt, thank goodness. Bringing my arm around her back and slowly lifting her up into a more sensible position, I hold her limp body against me as delicately as I can manage. If it's a cataplexy attack as I imagine it is, she'd still be well aware of what's going on."

    mk "I'm sorry, Suzu. I got carried away. I'm really, really sorry."

    suz "It's okay..."

    "She manages to mumble the words despite her muscles still being weak, barely even able to lift her eyelids. It only makes me hold her all the tighter."

    stop ambient fadeout 0.3

    hide steam with dissolve

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_S11:

    $ renpy.music.set_volume(1.0, 0.0, channel="ambient") #restoring volume to default

    play ambient sfx_alarmclock

    "Tapping at the clock a couple of times before I find the button to stop the alarm,{w=.25}{nw}"

    play sound sfx_switch

    stop ambient fadeout 0.05

    "Tapping at the clock a couple of times before I find the button to stop the alarm,{fast} I blearily{w=.25}{nw}"

    play sound sfx_sitting

    "Tapping at the clock a couple of times before I find the button to stop the alarm, I blearily{fast} sit myself up in bed and rub my tired eyes."

    scene bg school_dormmiki with openeye

    "Bright summer sunshine already pours through the thin blinds, casting a dull light over the already warming room. Giving up on the prospect of going back to sleep, I pull off the sheets and swing my legs over the side of the bed."

    "My school clothes are... somewhere. All I can do is scratch my head and yawn as I glance around, the most complex matter my brain can handle at the moment being whether to get dressed or go to the toilet first."

    $ renpy.music.set_volume(0.6, 0.0, channel="sound")

    play sound sfx_hammer

    "The normal morning routine finds itself interrupted by a noise at the door. The question of whether it's someone knocking for me or just someone bumping against it is answered as another set of knocks comes soon after."

    play sound sfx_hammer

    "Staggering over while asking whoever it is to wait, I feel something soft underfoot. At least I know where my uniform shirt is, now."

    $ renpy.music.set_volume(1.0, 0.0, channel="sound")

    play sound sfx_dooropen

    show suzu_normal_d with charaenter

    play music music_suzu

    "Opening the door reveals a most unexpected sight. Suzu stands silently before me, dressed in her usual light summer dress."

    "This is a weekday... right? I was sure today was Monday, but unless the Yamaku uniform's significantly changed, the girl before me sure isn't dressed for the day ahead. It hardly helps that I'm more inclined to trust her than myself on such a matter."

    mk "I'm so confused."

    suz "Good morning to you, too."

    mk "Yeah, 'morning."

    mk "Why are you even here so early? And what's with the clothes?"

    show suzu_speak_d with charachange
    hide suzu_normal_d

    suz "I want to go out with you."

    mk "Out... you mean on a date? Don't we have classes?"

    show suzu_grin_d with charachange
    hide suzu_speak_d

    suz "It's unlike you to worry about skipping a day."

    "She's not wrong, per se, but that also misses the point. Suzu's always taken school so seriously that her choosing to skip is almost unthinkable."

    "Then again, I suppose these aren't normal times. A day where we can just forget all the crap going on and spend time together might well be just what we need."

    "The fact that Suzu showed up at my door already dressed for a day out is less than subtle; she knew that'd be my mindset, and how likely it'd be that I'd accept. It makes me briefly wonder if I'm really the one leading everything between us."

    "Resigned to my fate, I give a weary smile."

    mk "I'll get dressed now. Wait outside the gate so the teachers don't see you."

    stop music fadeout 1.0

    #centered "~ Timeskip ~" with dissolve

    scene bg city_street1 with shorttimeskip
    show suzu_normal_d with charaenter

    play music music_soothing

    "Walking through the shopping centre hand in hand with Suzu, I can't help but notice how few people are milling about. Aside from a few housewives and old people, the place isn't exactly doing a brisk trade. Maybe I shouldn't be surprised, given that most adults are going to be at their workplaces around this time, and teenagers would be in school."

    "I doubt Suzu is paying attention to the number of people around us, though, with her cheeks slightly rosy as she walks briskly to keep up with me. I might be doing my best to play it off, but this is the first real date I've had as well."

    suz "What do you want to do first?"

    "That's a good question. It's probably worth saving my appetite for lunch, and despite clothing store after clothing store, shopping at one doesn't feel like date material. Where's the manual on dating, anyway? I never did get my copy."

    "As we walk onward, a fancy sign standing next to a bench catches my attention."

    suz "You want to check out the movie?"

    mk "I was just thinking how that sign is pretty neat."

    show suzu_surprised_d with charamove
    hide suzu_normal_d

    suz "The sign...?"

    mk "C'mon, just look at it."

    "We both do. It seems to be some fancy electronic sign, faintly glowing as it displays some samurai movie advertisement. Not that the movie looks bad, but the way the sign is animated is what gets me, with the text occasionally disappearing and being re-written by fake sword slashes, plus the subtle smoke movements in the background moving around."

    show suzu_normal_d with charamove
    hide suzu_surprised_d

    suz "You sure do like ordinary things."

    suz "Then again, maybe it is amazing in its own way. Thousands of years of technological development, just to make people buy a product."

    mk "I was thinking more that you don't see these in the country. We just have plain old posters stuck on train stations."

    show suzu_embarrassed_d with charachange
    hide suzu_normal_d

    "She looks a little bashful for her flimsy attempt at guessing my mindset. The fact she wants to move the topic on isn't a surprise."

    suz "So, do you want to check out the movie?"

    stop music fadeout 1.0

    #centered "~ Timeskip ~" with dissolve

    scene bg cinema with shorttimeskip

    play music music_miki

    "This is awesome. Nothing beats a good samurai movie."

    "As we sit in the darkened theatre and watch the big screen, I grin as another fight scene finishes up, the blood flicked off the main character's blade before it's returned to its scabbard. We timed this well; I haven't seen this one before, and there are no annoying kids talking through the movie."

    "Leaning back and taking a swig of my gigantic drink, I cast a glance to my companion."

    show suzu_neutral_d at centersit with charaenter

    "It makes me think that maybe taking Suzu to see such a violent movie wasn't such a great idea. Her passive expression might be holding, but only because she's nervously clutching the popcorn bucket to her chest to steady herself."

    "I really should've picked a chick flick, or at least something a little less violent. Searching for a silver lining, at least this means I have ownership of both the adjacent armrests."

    "Taking the opportunity as an overly-long pan of some boring scenery starts, I reach beside me to take some popcorn for myself. The only result is my hand grabbing at the air."

    "She leaned away as I went to take some, the devious little rat."

    mk "Hey, Suzu?"

    suz "Yes?"

    show suzu_surprised_d at centersit with charachange
    hide suzu_concerned_d

    "I lunge over and take a large handful while she's distracted, stuffing the lot into my mouth at once. My chipmunk-like cheeks don't win any favours."

    #centered "~ Timeskip ~" with dissolve

    scene bg city_street1 with shorttimeskip

    "Both of us end up squinting a little as we emerge back into the bright late-morning light of the shopping centre."

    mk "Man that was great."

    show suzu_speak_d with charaenter

    suz "It sure was... a movie."

    suz "So you like samurai flicks?"

    mk "They're the best! You've got the action, you got cool dudes with honour and some great lines, the underdog coming out on top, the valiant sacrifice for the greater good. What's not to like?"

    suz "Do they have to be so violent?"

    mk "How can you have a samurai movie without violence? That'd be, like, a historical drama or something."

    show suzu_embarrassed_d with charachange
    hide suzu_speak_d

    suz "I did like the love interest."

    mk "Hmm? Oh, right, that cute girl. She was nice."

    mk "The main dude though was so cool. First you think he's some aimless middle-aged guy, then he becomes someone else completely once he finds his purpose in life."

    show suzu_concerned_d with charachange
    hide suzu_embarrassed_d

    suz "You're not cute at all, are you?"

    mk "Nope!"

    "She just looks at me. Did she mean to imply that I should be more feminine? She does like cute things, after all."

    suz "Want to grab something to eat?"

    show suzu_sleepy_d with charachange
    hide suzu_concerned_d

    "I initially move to check my watch, but the real reason why she wants to retreat somewhere becomes obvious given the slightly unsteady way she's managing to hold her head up. Was she pushing herself to stay awake during the movie so I wouldn't feel offended?"

    "Guessing she doesn't want it brought up, I make a show of checking the time in order to feign ignorance."

    mk "Sure. How about the cafe around there?"

    "A nod is all the response I need, the two of us setting off."

    #centered "~ Timeskip ~" with dissolve

    scene bg city_street2 with shorttimeskip
    show suzu_normal_d with charaenter

    "With lunch eaten and a nap had, we end up aimlessly wandering around for something to do."

    "As the day's worn on, more and more people have started to show up around the place, including hawkers for tissue packs and flyers. "

    "My feet stop as we almost pass a sports good store, my attention taken by a particular item sitting on a mannequin in the window. Nothing all that unusual for a store to carry, but something that I can't help but notice."

    stop music

    scene bg uniform with dissolve

    play music music_painful

    "The world feels to drop away as I simply stare. The faceless white mannequin is dressed in full uniform, with boots, socks, pants, undershirt, and jersey. It's even got my number, good ol' forty-five."

    "It takes me back. I really do miss those days."

    suz "Miki, come on."

    mk "Ah, sure."

    "I look up one last time to the mannequin, something in me hesitating despite knowing I should just put it out of my mind. What have I achieved since then? Has the year I've been with Suzu just been a temporary peak, like my time playing baseball?"

    "No matter how I think about it, our relationship can't last. We're two so very different people, and once we graduate, we'll end up living such different lives. Just when I thought I had a chance of getting everything together once more, the light at the end of the tunnel starts darkening so quickly."

    "I'm broken from my thoughts by a girl uselessly tugging at my left arm. It's almost amusing how little she achieves despite pulling with both her hands."

    scene bg city_street1 with dissolve
    show suzu_speak_d with charachange
    hide suzu_normal_d

    suz "We're not here for you to mope around. Come on!"

    "She tries to walk away with me in tow, doesn't get far."

    "So that's what this whole thing was about. Suzu was just trying her best to cheer me up after all the fracas we've been through lately, though she'd dare not say it to my face."

    "I smile a little in spite of myself. Maybe this won't last, maybe it will. What I do know, is that this girl cares for me. That's enough. At least right now, that's all I need to keep going on."

    stop music fadeout 1.0

    #centered "~ Timeskip ~" with dissolve

    scene bg ital_res with shorttimeskip
    show suzu_normal_d at centersit with charaenter

    $ renpy.music.set_volume(0.4, 0.0, channel="ambient")

    play ambient sfx_crowd_indoors fadein 2.0

    play music music_jazz fadein 2.0

    "After hitting up about half the stores, mostly just breezing in and out, the two of us settle in for dinner."

    "While not exactly high-end, given that neither of us could afford such a place, the restaurant's distinctly Italian, or at least pseudo-Italian, styling makes it something a bit different to the norm. At least, that's what it's designed to do."

    mk "I didn't know you liked pasta."

    show suzu_surprised_d at centersit with charamove
    hide suzu_normal_d at centersit

    suz "How can anyone not like pasta?"

    mk "I don't mind the stuff, but you sure wanted to come here when you saw the sign."

    show suzu_neutral_d at centersit with charachange
    hide suzu_surprised_d at centersit

    "Suzu just shrugs as she goes back to reading the menu. She's never been good at feigning disinterest."

    "My mind starts to wander as I look over the food on offer, the multitude of Italian names meaning little to me. I know spaghetti and lasagne, but the rest are rather lost on me."

    "By now, the restaurant's at least three-quarters full, the waiters manoeuvring from table to table with practiced speed. Being the kind of place where tables have two seats and no more, the amount of affectionate chatter and loving glances is almost sickening."

    "Suzu does her best not to show it, but I can tell she's noticing the lovey-dovey atmosphere just as I am. It annoys me a little that she isn't showing me any affection despite that, so I decided to take matters into my own hands."

    mk "Hey, Suzu?"

    show suzu_surprised_d at centersit with charachange
    hide suzu_neutral_d at centersit

    "I quickly lean over the table as she looks up from her menu, pressing my lips to hers just as she's about to speak. I linger for just a moment, taking in those cute, small lips, before withdrawing back to my seat and smiling widely."

    show suzu_veryembarrassed_d at centersit with charamove
    hide suzu_surprised_d at centersit

    "Suzu looks ahead of her, mouth just slightly open. She might as well be frozen in stone for all she moves, her face slowly becoming more and more flushed until she's become a bright scarlet. I might have taken things too far, as she looks totally dazed."

    "The girl's senses finally return to her as she buries her face into her hands, desperately hiding from the outside world."

    mk "That's what you get for ignoring me."

    suz "Can't you see we're in public?"

    mk "So?"

    "She just keeps her face buried, my eyes beginning to wander to see the public she's so worried about."

    hide suzu_veryembarrassed_d at centersit with dissolve

    "I'm used to the occasional sidelong glance from others, but I have a feeling that the looks we're getting from a couple of the others aren't because of my missing hand."

    "I decide to mess with a woman chancing a badly-hidden peek from under her thick bangs by looking her dead in the eyes. The way she sheepishly turns her head away makes me grin. The question of whether she's looking because she found us cute, curious, or simply off-putting comes to mind, but it makes little difference to me."

    suz "Miki!"

    show suzu_speak_d at centersit
    show waiter_neutral at left
    with charaenter

    "Turning about, it seems my own curiosity has come at the expense of having time to properly select my meal. A waiter, dressed in a rather dapper black and burgundy outfit, stands beside our table while patiently holding his pad and pen ready, Suzu likely already having ordered."

    mk "Oh, uh, what she's having?"

    hide waiter_neutral at left with moveoutleft

    "The waiter gives a curt nod before scrawling the order down without question and heading back towards the kitchen."

    mk "So... what did I just order?"

    suz "Twit."

    mk "I have no idea what any of this stuff is anyway. Maybe I should've just ordered spaghetti after all."

    show suzu_normal_d at centersit with charachange
    hide suzu_speak_d at centersit

    suz "Well you're in luck, because that's what I asked for."

    mk "Really?"

    show suzu_grin_d at centersit with charachange
    hide suzu_normal_d at centersit

    suz "No. You'll see when we get it."

    "I stick out my tongue in response."

    show suzu_concerned_d at centersit with charachange
    hide suzu_grin_d at centersit

    suz "You could limit your teasing to those you know."

    mk "I'm just messing around. It's not like I can exactly help that we're the only two girls sharing a table."

    mk "Maybe if I put my stump up on top, everyone can stare at that instead."

    show suzu_unhappy_d at centersit with charachange
    hide suzu_concerned_d at centersit

    suz "I just don't like sticking out."

    mk "At least you have a choice."

    mk "Sorry. I guess that came out wrong."

    suz "This doesn't feel very romantic, does it?"

    mk "Not at all. Guess I'm not really good with this sort of thing."

    mk "What about you? It's hard to believe I'm your first partner."

    suz "I've never had many friends. Offline, at least. What am I going to do, go to a bar and hit on women?"

    "The image of Suzu trying that is hilarious, sitting on a stool trying to chat up some hot girl next to her in some seedy joint while half-drunk. It doesn't seem to be the reaction she intended for me to have."

    "More seriously, she does have a point. Introverts sure have it hard, regardless of the fact she's only interested in girls."

    mk "At least you've got me."

    suz "For good or ill."

    show suzu_concerned_d at centersit with charachange
    hide suzu_unhappy_d at centersit

    suz "Have you... mentioned this? To your father, I mean."

    mk "Not yet. To be honest, though, I think he'd be more surprised if I came out as straight."

    show suzu_smile_d at centersit with charachange
    hide suzu_concerned_d at centersit

    "She manages to eke out a smile, which I count as a small victory. What I say is true though; I often had guys visit my house as friends without any romantic undertones, and got along with them as any other guy would. Not that I didn't like the odd peek at their bodies."

    "Our conversation enters a lull as we notice the waiter coming up with what we presume to be our dishes, only for him to walk past and serve them to a different table."

    show suzu_concerned_d at centersit with charachange
    hide suzu_smile_d at centersit

    suz "It's annoying when that happens."

    mk "I know, right? You get all excited about being able to dig in, only for the chance to fly right by."

    mk "Thanks for paying for this, by the way."

    suz "You paid for the movie, so it's only fair."

    "Unsaid is that the movie cost a lot less than what this meal will. I kind of appreciate Suzu not bringing that up, though."

    show waiter_happy at left with moveinleft

    "Once again a waiter begins to walk towards our table, the two of us hoping against hope that this is our food. Our wishes turn out to be true, with the waiter politely setting down our plates and drinks before bidding us to have a good meal."

    hide waiter_happy with moveoutleft

    "The pasta sure looks nice, whatever it's called. Shaped like little bow-ties, it's covered in a thick layer of steaming sauce and parmesan cheese. I'm salivating just from looking at it."

    suz "It's farfalle, if you're wondering."

    mk "Delicious is what it is. Less talk, more eat."

    scene bg food with dissolve

    "I quickly dig in, fork in hand. Managing to burn my tongue with my eagerness, I end up taking a swig of my drink to try and soothe the pain before carefully blowing on the next mouthful."

    "It really is nice. The sauce is delightfully rich, and the pasta's well-cooked. Not too dry, but not too soggy. The smell makes the taste all the better, making me savour the somewhat small portion as best I can."

    "Seated across from me, Suzu carefully nibbles at her own meal. She looks a bit like a chipmunk, almost seeming to graze given how little she puts into her mouth each time. At least she'll make the food last as long as it possibly could, I suppose."

    mk "Good?"

    suz "Yeah."

    "A girl of few words, and even fewer when eating."

    scene bg ital_res with dissolve
    show suzu_sleepy_d at centersit with dissolve

    "I move to speak, but pause as I realise that her usual quiet nature and slow eating aren't what's at play. All of her movements are terribly slow, and what I'd taken as her simply looking at her food now appears to be an attempt to hide the effort she's putting in to do even that much."

    "It's been a long day for the both of us, and now that I think of it, a single short nap at lunch probably wouldn't be enough for her. We've been at this since the very beginning of the day, after all."

    "I don't want to remind her of it, but it's a little painful to see her barely even chewing her food from tiredness. The sheer concentration she's using to accomplish even the most mundane tasks would be using up even more of what little energy she has left."

    mk "Suzu. Suzu...!"

    show suzu_sleepy_d at flinch

    "Failing to get her attention, I put my fork down and give her shoulder a mild shake."

    "Suzu's face could only be described as one of defeat. She knows she lost this fight without a word needing to be said."

    mk "It's okay."

    show suzu_asleep_d at centersit
    hide suzu_sleepy_d at centersit
    show suzu_asleep_d at centersitlow with charamove

    "The last of her resistance breaks, head falling down and twisting sideways onto her arm. Her mostly-eaten meal sits beside her."

    "Resting my chin on my hand, I idly look at her sleeping face. It really does seem like these are the only times I ever get to see Suzu with her guard down."

    stop ambient fadeout 3.0

    "Time wears on as one couple leaves, and then another. We've outlasted everyone who was here before us by now, and after absentmindedly sipping at my drink for want of something to do, my third glass is almost empty."

    "Try as I might, it's getting hard to deny that she's going to be out for a good while. I don't seem to have much of a choice, here."

    "Suzu's probably been pushing herself to stay awake as long as she probably could, and now she's paying the price. I doubt she'll be happy with me cutting things short for her sake, but for all I know, she could be out for hours."

    stop music fadeout 3.0

    "Accepting my fate and considering the day's fun over, I motion to a passing waiter and ask for the bill."

    #centered "~ Timeskip ~" with dissolve

    scene bg school_road_ni with shorttimeskip

    play music music_night

    "I wonder how many times I've made my way up this hill with a slumbering girl on my back."

    "Not that I mind doing so. Being useful to someone is something I've always needed, and it's good exercise in any case. Then there's the view."

    "Shining through the darkness of the night, the street lamps and residents's lit windows shine up from the town below. People, hundreds of them, reduced to so many pinpricks of light in the black expanse. All those lives, reduced to little more than lonely splotches."

    "It's made all the more poetic by the total lack of life around the two of us. All that's to be heard is the occasional rustle of gravel underfoot at the side of the road."

    mk "It's pretty, isn't it, Suzu?"

    "No answer. I can't say it's a surprise."

    "The air is nice and cool compared to the day's heat. It's calming."

    "My enjoyment of the night's stroll is disrupted as I become aware of my shoulder becoming wet. She's started to drool on me now? Not cool."

    "The resigned smile on my face soon drops, however, as a quiet whimper comes from Suzu. The dead silence around us makes the sound impossible to mistake."

    "I try to think of a time when Suzu's teared up before, but it's hard. Aside from the time I first met her, and once or twice when she's hurt herself, she's never been much for crying."

    "There's nothing I could say to help the situation, so I end up keeping my mouth shut. It would suck to try so hard to make this a great day, only to have it stolen from you at the last moment."

    suz "I'm sorry. It's always like this."

    mk "Come on, that's my line."

    mk "I had fun today, Suzu. It's been the best day in a damn long while, actually."

    "Suzu's sobbing stops, but only because she's pushed her face into my shoulder to try and steady herself."

    mk "I should be the one apologising. I've always been a brute, after all. I'm selfish, a total simpleton, stupid, and I manage to make a total mess of everything all the time."

    mk "Compared to me, you come out pretty good."

    "Silence returns as I continue to trudge up the hill. I come so very close to asking the one question I want an answer to, but also the one that would likely mean the end of us being together if I asked it."

    "I wish I could say that I'm trying to keep us together for the sake of Suzu's happiness, but I know I'd be lying to myself. I need her. I needed her ever since that fateful day those years go, and if I lost her, I don't know what I'd do."

    "It's Suzu who breaks the silence, giving four whispered words."

    suz "Thank you. For everything."

    mk "You're welcome."

    stop music fadeout 1.0

    $ renpy.music.set_volume(1.0, 0.0, channel="ambient") #restoring volume to default

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_S12:

    scene bg school_scienceroom with locationchange

    play music music_normal

    "Walking into class, it seems like it'll be another ordinary day."

    "Suzu sits bored at her desk as she looks out the window, having joined the other early arrivals to class. With Hisao talking to Misha and Shizune, and Haru not yet here, I stride up to her."

    show suzu_neutral at centersit with charaenter

    mk "Good morning, Suzu. You look very... happy?"

    "She just stares at me with that bored face of hers. Assuming I was wrong, I take another try."

    mk "...Depressed?"

    mk "...Annoyed?"

    mk "I give up. I don't even know why I bother trying."

    "I hop up on the side of my desk to talk to her, for lack of anything else to do."

    mk "Ready for the test after lunch?"

    suz "Test?"

    mk "Yeah. Mutou mentioned it a few days ago."

    "She just shrugs. It's unlike Suzu to forget something like that, let alone not care about it. I guess her mind's still on other matters, not that I'm completely innocent of that either."

    suz "Are you still going to quit the track club?"

    mk "Hmm... probably. Just a matter of telling the teacher in charge, really."

    show suzu_speak at centersit with charamove
    hide suzu_neutral at centersit

    suz "Don't. Do anything else you want, but don't do that."

    mk "Unlike you to feel so strongly about that kind of thing."

    suz "Only because you don't feel strongly enough. You've been in that club for years, don't quit on my behalf."

    mk "It's not all for you, you know. I thought you'd like seeing me a bit more."

    show suzu_concerned at centersit with charachange
    hide suzu_speak at centersit

    "Suzu just stares at me. I don't know whether to appreciate her unusual strength of will on the issue, or be somewhat hurt by her rejecting having more time together. The more I stay like I am, the less I feel as if we really belong with each other, but now she acts like this when I try to bridge that gap."

    mk "Alright, I'll hold off. I guess we can talk about it later."

    "She nods simply, apparently pleased with the compromise."

    mk "Come on, Suzu. What's up? You're in a weird mood today."

    suz "I'm fine. You should just cherish your friends more."

    "I can't say I'm totally placated by the response, but she has a fair point. Maybe someone like her, who's rarely had many, is the best kind of person to listen to on such matters."

    "With Haru skipping into the room moments before the first teacher of the day walks in, the both of them very nearly late, I hop off my desk and take a seat. Suzu really does seem out of sorts today, but that wall between her and I is strong as ever."

    stop music fadeout 1.0

    #centered "~ Timeskip ~" with dissolve

    scene bg school_scienceroom with shorttimeskip

    play music music_caged_heart fadein 3.0

    "With the class having returned from lunch, Mutou begins his lecturing on what today's test will cover. Little more than a retread of what we've been taught on the current topic, with a few harder questions thrown in to check what we've retained over the holidays."

    "I might pass, though it'll be close if I do. In any case, that's less of a concern to me right now than the empty desk to my left."

    "The other students just walked by as if nothing were amiss, perhaps throwing a casual glance at Suzu's empty seat before writing it off as yet another episode of her narcolepsy. It'd be easy to think that way myself if not for recent events."

    "But I'm not the only one who knows what's happened in the past. Rumours regarding me, and by extension her, aren't hard to catch on the wind. Does everyone really think this is normal, or are they just giving themselves an excuse not to get involved?"

    "It is most likely just another nap, but I can't concentrate at all. Knowing that I have no other option, I raise my hand."

    show muto_normal with dissolve

    mu "Yes, Miura?"

    mk "I feel sick. Can I go to the nurse's office?"

    show muto_irritated with charachange

    "'I'll bet', his face says. He wouldn't be wrong."

    "Mutou sighs, but we both know that he has little option but to let me go. It'll be a pain for him to rerun the test for my sake, but he'd have needed to for Suzu, anyway."

    mu "Hakamichi, escort Miura down there, please."

    "Shizune nods, with Misha getting up to follow her."

    mu "Not you, Mikado. I think you know why."

    "The sting is palpable as she sits herself back down, Hisao doing his best to silently console her."

    show shizu_basic_normal2 at left with moveinleft

    "Shizune walks over and motions for me to follow her out, Mutou wasting no time in getting back to his pre-test briefing."

    scene bg school_hallway3 with locationchange
    show shizu_basic_normal2 with dissolve

    "The two of us quietly walk down the abandoned hallway, the sound of one teacher following another as we walk past the filled classrooms. My body feels unbearably tense, which I'd hoped would stop once I gained my freedom from class."

    "I notice that Shizune's pulled her notepad as she walks in front of me, scrawling something down. At least nobody can accuse us of making a noise in the corridors like this."

    shi "[[What's the story?]"

    "I really need to work on my lying. Knowing that Shizune would get to the truth eventually, I decide to give up without a fight as I take the notepad and pen."

    mk "[[I want to check on Suzu. I promise I'll come straight back if it turns out to be nothing.]"

    show shizu_behind_frown with charamove
    hide shizu_basic_normal2

    "Handing the items back, it takes her a moment to decipher my hasty chicken scratch. It's clear she isn't pleased with the proposal, but her answer after handing them back is a surprise."

    shi "[[Go.]"

    "With my mind occupied with my new goal, I verbally thank her before realising the mistake, taking off without checking her reaction."

    stop music fadeout 1.0

    play music music_drama fadein 1.0

    scene bg school_staircase2 with locationchange

    scene bg school_lobby with locationchange

    "I move as fast as I dare down the stairs and onto the lower floor, lest a teacher pull me aside to scold me for running in the hallways. I don't bother looking to this class or that any more, only the path ahead."

    scene bg school_gardens_running with locationchange
    play sound sfx_running loop

    "Emerging from the main entrance into the empty school gardens, the fresh air hitting my face spurs me into a flat run. There's little point to walking now that I'm outside, and the distance from here to the dormitories isn't great."

    "There aren't many places someone like Suzu would be, after all. If she were in the library, it's likely one of the staff there would at least try to wake her, leaving the dormitory as the most likely place she'd retreat."

    scene bg school_dormext_full with locationchange
    stop sound fadeout 0.3

    "It doesn't take long to reach the building, taking a moment to have a breath before opening the door and heading inside."

    scene bg school_dormhallground with locationchange

    "Those horrid artificial lights above the entrance blare away, their slightly too perfect white glare sharply contrasting with the sunlight outside. Wasting little time, I stride through to the stairwell."

    scene bg school_girlsdormhall with locationchange

    "The quiet of the dormitory building entrance is just as present in the wing housing her room. I know it's unlikely I'd hear her if she was indeed sleeping, but I can't help but wonder if I guessed the wrong location nevertheless."

    "With her door shut as expected, and knowing that knocking would be pointless given that she wouldn't hear it if she were asleep, I fish out her key from my pocket and insert it into the lock. The door gives a satisfying click as it unlocks, a slight push sending it swinging open."

    play sound sfx_dooropen

    scene bg dormsuzu with locationchange

    stop music fadeout 1.0

    "I have to squint a little in response to the sunlight pouring into her room from the small window, my gaze shifting to the figure seated on the side of her bed. A glint of light catches my eye as I do so."

    play music music_tragic

    n "My heart stops."

    n "The girl's eyes look downward with a distant stare."

    n "Her left arm rests on her leg, the palm upturned and sleeve pulled up."

    n "The point of a small utensil rests against the wrist, held by her right hand."

    n "A kitchen knife. Suzu is holding a kitchen knife against her forearm."

    n "My centre of gravity shifts forwards, my body immediately taking over where my mind has failed."

    n "I'm already almost upon her by the time Suzu notices my presence, adrenaline almost feeling to pour from my eyes, such is the amount coursing through my body."

    n "Every motion is born of pure reflex as I come over her, my mind lagging terribly behind in comprehending the situation."

    n "Time feels to slow as I fall on top of her, my left stump pushing her right hand outward as my bent right forearm is shoved against her neck. Her dazes expression tells of her not having any idea what's just happened in the last two seconds as we tumble downward."

    play sound sfx_impact

    n "Crashing to the bed, we find ourselves tangled. With my hand still pressed to Suzu's neck holding her down, her right arm held against the bed with my left forearm, all I'm left to do is stare down at her with our faces barely inches from each other."

    n "Despite unambiguously being the one in physical control of the situation, I have no idea what I'm supposed to do. What comes after something like that?"

    n "It's Suzu's eyes that give the first indication of what's happened, bulging wide as tears begin to well up. Her breath catches as she desperately attempts to keep some control over herself."

    n "Her face twists and distorts as she tries to keep a flood of emotions in, but it's utterly hopeless. Her tears overflow and begin to fall over her cheeks, first as a trickle, before becoming a river."

    n "I want to say something to help her, anything at all, but I'm powerless. Even as hold myself inches over Suzu's frail body, the girl I love so much just... breaks."

    n "All semblance of composure shatters as the dam breaks, her whimpers breaking out into wild bawling. My heart breaks as I watch her body seize and convulse beneath mine, her wailing face overflowing with tears."

    n "Everything is messed up. It wasn't supposed to be like this. It wasn't supposed to be anything like this."

    n "I'm so sorry, Suzu..."

    stop music fadeout 2.0

    nvl hide dissolve

    nvl clear

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_S13:

    scene bg school_track with locationchange

    play music music_drama

    "The soft breeze is cool as I sit watching the gaggle of guys fooling around on the track. Seated in the shade of the trees lining the edge of the track area, I simply lack the energy to get up and join in."

    "It's been a week since that terrible day. Might as well have been yesterday, as far as my memory is concerned. The image of her sitting there, knife in hand, solemnly contemplating the end of her existence with those distant eyes still makes me feel physically sick. I'll never forget that scene, no matter how long I live."

    "Suzu hasn't been at school since then, with her parents having collected her. A cover story of unspecified family issues was given as the reasoning for her temporary disappearance, which seems to have stuck. Like all good rumours, it had just enough truth to be believable, and few dared ask questions of the girl who'd just flattened a guy over her."

    play sound sfx_rustling

    "A piece of bread in its plastic wrapper suddenly dangles in front of my face. Despite not having an appetite at all, I take the packet just to get him off my back."

    show hisao_disappoint_u with charaenter
    show hisao_disappoint_u at centersit with charamove
    play sound sfx_sitting

    "As expected, it's Hisao who takes a seat beside me. He and Haru are the only others who know the truth, beyond the teachers and staff. As for Suzu and her family, I haven't heard a peep since that fateful day."

    mk "I'm not hungry."

    show hisao_declare_u at centersit with charachange

    hi "I don't care."

    "His tone is harsher than I'm used to, and with little fight left in me, I obediently rip open the thin packaging."

    "Even if I'm loathe to admit it, the smell of fresh bread playing on my nose does incite a small hunger. The two of us end up eating our lunches side by side, the distant sounds of playing and shouting drifting in the air."

    "As we munch away, I can't help but say what's on my mind."

    mk "It feels weird, doesn't it? Everyone else playing around, completely oblivious to what happened."

    show hisao_erm_u at centersit with charachange
    hide hisao_declare_u at centersit

    hi "Yeah, I know what you mean. It's like everything diverged from that moment, with the rest of the world in a different timeline to the one we're in. Nobody treats us any differently, but in a way, that's the problem."

    "As always, Hisao's the one to find words where I struggle for them."

    hi "I know you lied about the relationship between you and Suzu, back when I asked."

    mk "Sorry. I just... I wanted a clean slate, you know? Someone who I could deal with as if none of that crap had ever happened."

    mk "I guess that's kind of impossible now, huh?"

    stop music fadeout 4.0

    "Hisao just looks to me expectantly. I can't keep this from him any longer, and after all the support he's given me, he deserves to know."

    "I take a long breath, thinking back to those days. It isn't something I enjoy doing."

    play music music_painful fadein 4.0

    mk "I suppose you've gathered by now that I used to be an unpleasant kind of person."

    show hisao_heh_u at centersit with charachange
    hide hisao_erm_u at centersit

    hi "Yeah, something like that."

    mk "Most of the kids who enter Yamaku are pretty well-adjusted, normal folk. Just your usual kids who happened to have some shit luck. I wasn't like that."

    mk "After I lost my hand, I guess you could say I went off the rails. I got off on beating people, to put it bluntly. Pretty much anyone who I didn't like the look of, but mainly those who looked down on me. I'd always been built pretty damn well, by the standards of a girl or a guy. That strength was damn near all I had left, so I used it."

    show hisao_erm_u at centersit with charachange
    hide hisao_heh_u at centersit

    hi "A real delinquent, huh?"

    mk "Nothing so romantic. I was just a shithead bully. Nothing more."

    mk "Over the years, I got a reputation. One I deserved, mind you. People didn't stand up to me, and I could see the humility people had if they felt they'd gotten in my way. I'm not gonna lie; it felt good. I felt powerful again. It gave me a twisted sense of accomplishment and status."

    mk "But one day, I met someone who didn't know about that reputation."

    hi "The day you met Suzu."

    "I give a nod."

    mk "I don't remember everything about that day, but I do remember the way Suzu looked."

    mk "She was sitting on the ground near the storage shed. Could barely see her between the legs of the three girls and some guy who were standing around insulting at her. Something about the situation annoyed me, so I walked up to them and challenged the girl who seemed to be leading the little charade."

    show hisao_smile_u at centersit with charachange
    hide hisao_erm_u at centersit

    hi "That's pretty admirable. Standing up for her when you didn't need to, that is."

    mk "Yeah, that would be admirable. I still don't know if I genuinely wanted help her, or if I just had a chip on my shoulder that day."

    mk "In any case, the girls backed off after recognising me, but the guy made the mistake of picking an argument. I think he was the boyfriend of one of them, or something. He started going off about Suzu, and how she'd screwed up something or other. I honestly didn't care much."

    mk "But then he made the mistake of insulting me. I can't recall what he said, but something inside of me tripped."

    show hisao_erm_u at centersit with charachange
    hide hisao_smile_u at centersit

    hi "What happened then?"

    mk "I broke him."

    show hisao_frown_u at centersit with charachange
    hide hisao_erm_u at centersit

    "Silence washes over us, Hisao leaning back as I realise the dark face I must be making right now as I remember the event. The ambient noise of people playing around ahead feels slightly surreal, given the atmosphere."

    hi "You didn't kill him, did you?"

    mk "I wasn't far off. I just... I went absolutely berserk on him. I don't even know if I got hurt or not; every part of my mind was purely dedicated to destroying his body."

    mk "If a couple of teachers hadn't found us and dragged me off the guy, I really don't know what might have happened."

    "I take a breath to pull myself out of the moment. Hisao just looks on, understandably speechless as macabre images fill his thoughts."

    "This is the first time I've told anybody this stuff myself, come to think of it. Such things tend to get around quickly though, so everyone in school at the time largely knew, as rumours if not in detail." #Suriko had written “in vagueries if not in detail” here. I get what he was trying to say but vagueries #is not a word so I substituted as rumours instead. Of course, it would be that Miki the character #doesn’t know she’s using a word that doesn’t exist. Still though, aside from using the occasional #Australianism she hasn’t used any made up words, so I feel somewhat justified in substituting.

    hi "And Suzu?"

    mk "I remember seeing her face as the teachers pulled me away."

    mk "No, not her face. Her fear. I'd never seen someone so terrified in my life."

    mk "I think that was the first moment I realised what a detestable being I'd become. That someone could look at me, and see something that gave them that much fear."

    hi "For what it's worth, I'd never have guessed it. You've always seemed like a pretty laid-back kind of person to me."

    hi "Now that I think of it, what happened afterwards? Surely you didn't get out of that without punishment."

    mk "I was pretty much set for expulsion. By that point the staff were looking for an excuse to throw me out, and it's not like I had any friends willing to come in and bat for me."

    mk "But then, one day... it was never mentioned again."

    show hisao_erm_u at centersit with charachange
    hide hisao_frown_u at centersit

    hi "They dropped the matter?"

    mk "Yeah. It was the strangest thing."

    mk "It was so bizarre that my curiosity got the better of me. The staff weren't going to tell me anything, so I ended up fingering the student council for information."

    mk "Turned out that they'd taken up my cause and argued that I had my reasons. That Suzu was being bullied, and I was defending myself after trying to argue them away from her."

    show hisao_talk_small_u at centersit with charachange
    hide hisao_erm_u at centersit

    hi "Why would they do that, though?"

    mk "Because a particular girl told them that's what happened."

    show hisao_disappoint_u at centersit with charachange
    hide hisao_talk_small_u at centersit

    "Seizing on the lull in conversation, I set about finishing the bread in my hand. Hisao just looks out to the field ahead, thinking on what I've said."

    hi "So you felt a debt to her?"

    mk "I'm not the kind of person to worry about that sort of thing."

    show hisao_smile_u at centersit with charachange
    hide hisao_disappoint_u at centersit

    hi "Yeah... I noticed."

    mk "Asshole."

    mk "Rather than a debt, it's more... I felt useful to someone."

    show hisao_erm_u at centersit with charachange
    hide hisao_smile_u at centersit

    mk "That's why we ended up hanging around each other. Suzu had no friends, so when I was around, she wouldn't get bullied, and had someone to help if she had a cataplexy attack or suddenly felt sleepy."

    mk "As for me, it was mere curiosity at first. Working out why she'd done such a thing. After a while, though, I realised that I had a purpose again. I could live for Suzu's sake."

    mk "That girl saved me."

    stop music fadeout 5.0

    hi "You shouldn't forget that you saved her. It's a miracle you got to her in time."

    mk "Saved her? I did no such thing. It's my fault she even fell that far to begin with."

    mk "I thought I could change. That I could somehow redeem myself. In the end, it was all a fantasy."

    hi "Suzu told me something once. I didn't understand why she felt about it so strongly then, but now it makes sense."

    mk "Yeah?"

    show hisao_smile_u at centersit with charachange
    hide hisao_erm_u at centersit

    hi "She said that she didn't believe in the concept of 'good people' or 'bad people'. Just people, who do good or bad things."

    "It's the kind of hopelessly naive thing she'd believe. She's lived a sheltered life, after all. That's not a bad thing in itself, but her innocence because of it makes her attempts to form a worldview look childish."

    "From the way Hisao's smiling, she managed to get at least one believer. It would be nice to think that I'm somehow a different person to who I was those years ago, but I imagine those I hurt would have very different opinions."

    "A buzzing sound suddenly comes from Hisao's pocket, his hand quickly diving in to retrieve his phone. He looks to me with an expression of surprise after glancing at the display."

    show hisao_talk_small_u at centersit with charachange
    hide hisao_smile_u at centersit

    hi "It's Tsubasa..."

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_S14:

    scene bg suburb_park with shorttimeskip
    show hisao_erm with charaenter
    play music music_moonlight fadein 1.5

    $ renpy.music.set_volume(0.5, 0.0, channel="ambient")

    play ambient sfx_park fadein 2.0

    "I can practically hear my heart thumping away as I walk through the park. While I do my best to appear casual, I don't think Hisao buys it."

    "An offer to talk to Suzu once more finally came, perhaps unsurprisingly from her sister rather than her parents. It's the first contact I've had with her since that day, and I really have no idea what to expect."

    "While I may have hoped that the time that's passed would have dulled my memories, they're still as fresh as ever. Moreover, if it's bad for me, it could only be worse for her."

    show hisao_disappoint with charachange
    hide hisao_erm

    hi "You okay?"

    mk "Almost pissing myself, actually. Thanks for coming with me."

    "Hisao claps me on the shoulder a couple of times. He needn't have come, but I must've made a pitiable impression on him when I implied I wouldn't be comfortable doing this alone."

    "As we clear the trees, a lonely wooden park bench comes into view, with a lonely girl seated on it. Only the top of the back of her head is visible, but there's no mistaking her."

    "I stop in my tracks. Now that I can see her, I'm forced to admit that it feels wrong to bring Hisao into this. It's not his fault any of this happened, and I'm the one with the most time spent with Suzu."

    "My mind begins to fill with all the events that lead to this situation, what might have been in her head as she stared into the abyss of nonexistence, what I did to make her hurt so badly, and what I could've done to stop it. What I saw, what I didn't see, what I did, and what I didn't."

    hi "Miki?"

    "I take a sigh to steady myself. It makes me feel a little sheepish, but I have to admit the obvious."

    mk "Sorry, Hisao, but..."

    show hisao_smile with charachange
    hide hisao_disappoint

    "He just smiles. It's always bugged me how easy it is to make him wear a smile, but how hard to is to make him genuinely do so. This, at least, is the latter."

    hi "I understand. Good luck."

    mk "Thanks. I owe you one."

    "He turns on the ball of his heel and begins to stroll off, hand held in the air."

    hide hisao_smile with moveoutright

    hi "I'll hold you to that."

    "With that, he disappears into the trickle of people walking along the concrete path out of the park. It's just me and Suzu, now."

    show suzu_concerned_d at centersit with charaenter

    "With my heart in my mouth, I walk up to the bench and park myself beside her. My first mistake is waiting for her to greet me before doing the same, with an awkward silence lingering after she fails to say a word."

    "Indeed, her only reaction to my presence is a quick sideways glance before looking straight ahead once more. The only silver lining is that I feel a little less conspicuous as I examine her as best I can."

    "The most immediate observation is that she looks small. I do my best to try and work out why, but come to the conclusion that it isn't physical, beyond her slumped shoulders. She gives the aura of someone wholly defeated, the spark of life within her glowing terribly dim."

    "It doesn't look as if she's been crying recently, at least. A little thinner for the experience, perhaps, but she's always been a problematic eater."

    "Content that I'm not going to work out anything further from looking at the girl, I take a breath and try to work out what I'll say."

    "...Which is impossible. Do I address her casually, like today's just another day? We both know that wouldn't be the case. How do I even begin to approach what happened, though? Is she mad at me for stopping her? Thankful? Does she want to break up with me, or stay together?"

    "Giving up on making conversation, I simply reach out to rub Suzu's hair."

    "A strange feeling comes over me the moment I place my hand on her head and begin to stroke her. A sense of calm, in sharp contrast to the previous anxiety of facing her again."

    "She's just Suzu, after all. The same girl I've known for all this time. Maybe she feels something similar to what I am, as her cheeks have become distinctly rosy."

    "Time goes by as I gently stroke her head, but try as we might, we can't ignore what's happened. Suzu's eyes begin to moisten, her mouth trembling as she tries desperately to hold in her emotions."

    show suzu_cry_d at centersit with charachange
    hide suzu_concerned_d at centersit

    "Slowly but surely, tears begin to form, overflowing and gently rolling down her cheeks. My heart drops as I watch her, the girl weeping in sorrowful silence."

    "I wrap my arms around Suzu and bring her head to my chest, holding her shuddering body to mine in a warm embrace. It's from her that the first words come."

    stop music fadeout 4.0

    suz "I'm sorry."

    mk "Come on now, none of this is your fault. I'm the one who messed everything up, but it feels like you're the one taking the fall."

    suz "Stop saying that."

    mk "Isn't it true though?"

    "She picks herself off of me, wiping her eyes with the back of her wrist. She's managed to pull herself together a little, but barely."

    play music music_innocence fadein 4.0
    show suzu_cry_smile_d at centersit with charachange
    hide suzu_cry_d at centersit

    suz "You're not terrible person, Miki. You're beautiful, outgoing, kind..."

    show suzu_cry_d at centersit with charachange
    hide suzu_cry_smile_d at centersit

    suz "Unlike me. All I ever do is constantly cause others problems. No matter how hard I try, I've always been useless..."

    mk "You had the courage to confess. That takes some guts, especially to another girl."

    suz "I panicked. That's all that happened."

    suz "For so long I stood on the sidelines and tried to help you improve yourself, and saw your circle of friends getting greater and greater. When I saw you with Hisao, I realised that you'd finally become someone who might have a bright future ahead of them."

    suz "But then, when you mentioned you that chose to come to my house..."

    suz "To put it in your terms, I guess it was like instinctively reaching for something thrown towards you."

    suz "I'd always thought you were straight, but even if you weren't, I was a useless person to begin with. I didn't have the right to be with someone like you."

    suz "But when I heard that, when I saw the first ray of hope I'd seen for so long... I grabbed at it without thinking."

    mk "You should be proud of that. I know I made things worse, but I was trying to change for you..."

    show suzu_despair_d at centersit with charachange
    hide suzu_cry_d at centersit

    "I trail off as her expression falls to one of abject despair."

    suz "Yes, that's right, isn't it."

    suz "Everyone has to change because of me. Everyone has to make allowances, and act differently."

    mk "Suzu..."

    suz "I love you, Miki! You're strong-willed, you're brave, you look out for others. You have such a strong spark of life, more than anyone I've ever known."

    suz "I don't care if you think you're stupid or rough, or what you've done in the past."

    suz "Miki, I didn't fall for you because of what I wanted you to be. I fell for you because of what you are. When I saw how I messed up, hurting the one I loved the very most..."

    "I feel a big lump in my throat as I stare at Suzu, her declaration of her feelings hammering home. I'm not gonna cry. I told myself that I damn well wasn't gonna cry."

    mk "Damn it, Suzu. You had me scared, you know? More scared than I've ever been in my life."

    scene bg bench with dissolve

    "I reach for Suzu and grab her tightly, pressing her into my chest with all the strength I can muster."

    ##show suzu_cry

    suz "Miki, you're holding me too tight..."

    mk "Too bad, because I'm not letting you go. I don't want to lose you, Suzu. Not again."

    mk "I won't change. I promise."

    ##show suzu_cry_smile

    "As I hold her body tightly, her arms find their way around my back."

    "For the first time, I feel like we truly understand each other. There are no walls any more. All there is, is me and her."

    "I lost everything, all those years ago. But now, I realise I've found someone truly worth the pain I've felt since then."

    "My precious Suzu, who I so nearly lost."

    window hide

    stop ambient fadeout 2.0

    stop music fadeout 2.0

    scene black
    with Fade(2.0, 0.5, 0)

    play sound sfx_whiteout

    play music music_credits fadein 2.0

    call credits from _call_credits

    return

label HisaoRoute:
    # Agree to go

    window show
    "After thinking about it, I finally come to a decision."

    mk "Alright, I'll come. I'll be bringing two of my friends, though."

    jun "That's what I like to hear! Couple of your running friends, or what?"

    mk "Just Suzuki and Nakai, if they agree."

    jun "Nakai... Nakai..."

    "Oh, right. I haven't mentioned Hisao to him yet."

    mk "He's a friend from class. Pretty mild-mannered dude, shouldn't be trouble."

    jun "Bah! Your friends have always been trouble. Good thing I'm used to it by now."

    jun "It'll be good to see you again. Take care of yourself until you get here, alright?"

    mk "I will. Thanks."

    "With that, we say our goodbyes."

    hide phone

    "I guess I have some explaining to do with Suzu... but it should be an interesting holiday, provided they come."

    "After all these years, I'll finally be returning home."

    # Continue to Hisao branch
    window hide

































label en_H1:

    ##start with Hisao route chapter card
    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(sfx_tcard)
    show neutral with fade
    show act2hisao with passingacthisao
    $renpy.pause(10.0)
    $renpy.music.stop(fadeout=2.0)

    scene school_dormmiki
    with dissolve

    window show

    play music music_raindrops

    "With the last class of the semester having ended a few hours ago, I find myself straddling a chair backwards to watch the two interlopers in my room. Aside from the occasional rustle of paper and the squeaking of my hand gripper as I exercise the hand I still have, there's little to be heard."

    show hisao_erm_u at tworightsit
    show suzu_neutral at twoleftsit
    with charaenter

    "Hisao and Suzu work quietly as they sit on the floor, each on opposite sides of my upturned box table. On it sits one science textbook and one notebook each, equations and notes from the former carefully being written to the latter."

    mk "I have a question."

    suz "Yes?"

    mk "Have you two noticed that exams are over, right? You can stop studying now."

    show hisao_declare_u at tworightsit with charachange
    hide hisao_erm_u at tworightsit

    hi "That's exactly why we're studying; to go over what we felt we didn't do well with during the exams."

    mk "Uh huh. And this is happening in my dorm room because...?"

    show suzu_speak at twoleftsit with charamove
    hide suzu_neutral at twoleftsit

    suz "Because someone had the silly idea that you might actually join us."

    show hisao_disappoint_u at tworightsit with charachange
    hide hisao_declare_u at tworightsit

    "Hisao looks displeased with the assessment of his plan. To be fair, there was no way it'd work; I'm already firmly in holiday mode, and couldn't be paid enough to study."

    "That does remind me of something, though."

    mk "Ah right, I probably should've mentioned this earlier. There might be a problem with going to Suzu's place during the holidays."

    show suzu_surprised at twoleftsit with charamove
    hide suzu_speak at twoleftsit
    show hisao_erm_u at tworightsit with charachange
    hide hisao_disappoint_u at tworightsit

    "Both of them look to me with interest. I guess holiday plans being threatened is enough to break them from their oh so important schoolwork."

    mk "My dad called. I ended up agreeing to go home for the break."

    suz "So you're not spending the time with us?"

    mk "Well, that's the next thing. Our house has room if you two want to come, and I'm sure dad would be fine with it."

    show suzu_angry at twoleftsit with charamove
    hide suzu_surprised at twoleftsit
    show hisao_heh_u at tworightsit with charachange
    hide hisao_erm_u at tworightsit

    suz "Why do I get the feeling you've made our holiday decisions for us?"

    mk "I have no idea what you mean."

    "I pull a silly face to try and amuse her, but it doesn't work. Then again, I doubt Suzu's actually annoyed; she'd make it clear if she was."

    "Hisao, for his part, looks more contemplative than anything. I get the feeling he has a greater sense of curiosity than the norm, so a trip like this should be quite an adventure for him. Either way, his reaction doesn't escape Suzu."

    show suzu_speak at twoleftsit with charachange
    hide suzu_angry at twoleftsit

    suz "I guess I'll call my parents to let them know."

    mk "You won't regret it, I promise."

    suz "You're not going to leave me alone with her, are you?"

    show hisao_smile_u at tworightsit with charachange
    hide hisao_heh_u at tworightsit

    hi "Don't worry, I'll come. Seeing where someone like Miki grew up would be interesting."

    mk "You make me sound like some kind of weirdo."

    show suzu_grin at twoleftsit with charachange
    hide suzu_speak at twoleftsit

    suz "You don't say."

    show suzu_sleepy at twoleftsit with charachange
    hide suzu_grin at twoleftsit

    "As I'm about to protest, Suzu rubs her tired eyes wearily. It is getting pretty late, looking at the clock beside my bed."

    show hisao_talk_small_u at tworightsit with charachange
    hide hisao_smile_u at tworightsit

    hi "If you want to get some rest, go ahead."

    suz "I still need to finish this..."

    hi "There's no point going on if you're tired; none of it'll stick. We can pick this up again tomorrow."

    suz "Fine."

    mk "Say 'thank you' to the teacher, Suzu."

    "To my surprise, she does, but manages to stick a barb in there."

    suz "Thanks. Now you can try teaching her."

    show hisao_smile_teeth_u at tworightsit
    hide hisao_talk_small_u at tworightsit

    hi "I'm not a miracle worker."

    show suzu_sleepy at twoleft with charamove
    hide suzu_sleepy with moveoutright
    show hisao_erm_u at tworightsit with charachange
    hide hisao_smile_teeth_u at tworightsit
    show hisao_erm_u at centersit with charamove
    queue sound [ sfx_dooropen, sfx_void, sfx_void, sfx_void, sfx_doorclose ]

    "Reaching for her school bag and sliding her books into it, Suzu comes to her feet and yawns as she groggily leaves the room. Both of us say our goodbyes as she does, the old door creaking shut behind her."

    "Hisao might go back to reading over his work, but my attention is elsewhere. Leaving the hand gripper on the desk, I get off my chair and sit down where Suzu previously was, picking up the notebook she's left behind."

    "Her handwriting is an odd form of scrawl, with tiny characters and no flairs at all. It's fast to write and fits a lot of text onto each page, sure, but it's also damn near impossible to read."

    mk "Guess I'll give this to her tomorrow."

    "Expecting Hisao to mention something, his silence draws my attention. Sure enough, he still sits there fiddling with some equation or another, pen tapping at his mouth thoughtfully."

    mk "I don't get it. How did a nerd like you ever get a girlfriend?"

    hi "It's not as if I was always like this. Just wasn't a lot else to do in hospital."

    mk "Really? You're pretty smart, though. I mean, Mutou praises you all the time."

    hi "I never really applied myself much before then. Messing around with friends and playing soccer was more fun."

    "He looks back down to his books, but gives up on the prospect of studying further as he sits back."

    show hisao_talk_small_u at centersit with charachange
    hide hisao_erm_u at centersit

    hi "What about you, anyway? Ever had a boyfriend?"

    show hisao_erm_u at centersit with charachange
    hide hisao_talk_small_u at centersit

    hi "Or girlfriend, for that matter. I won't judge."

    "I give a brief laugh at his timid indecision over which way I lean."

    mk "I'd be cool with either, but I've never really felt like getting romantic with anyone. I think friendship is underrated."

    "He nods, apparently pleased with the answer."

    hi "Hmm, it's later than I thought."

    mk "You can stay overnight if you want, I don't care. It'll be like an old-fashioned slumber party."

    hi "Sure, but... with a girl?"

    mk "It's not that weird is it?"

    show hisao_disappoint_u at centersit with charachange
    hide hisao_erm_u at centersit

    hi "A teenage girl and a teenage guy, both alone in a bedroom? I think you're the one being weird."

    mk "It's a genuine offer, you know. Not my fault you're preoccupied with sex."

    show hisao_talk_big_u at centersit with charachange
    hide hisao_disappoint_u at centersit

    hi "I am not."

    mk "You're a teenage guy, you know. You're allowed to think about that stuff; all teenagers do. Except for maybe Suzu. I'm still not sure she isn't a robot."

    mk "I guess you're lucky that you had a girlfriend, at least. Dipping your toe in while you're still young is good."

    show hisao_frown_u at centersit with charachange
    hide hisao_talk_big_u at centersit

    hi "Well..."

    mk "Wait, you did get lucky with her, didn't you?"

    hi "That's none of your business."

    mk "Heh, that confirms it. If there's one thing I’ve learned about guys, it's that they can't resist bragging about their experience."

    show hisao_declare_u at centersit with charachange
    hide hisao_frown_u at centersit

    hi "Leaving that aside, if you're fine with me staying overnight, I will. Not much to do in my own room, after all."

    stop music fadeout 1.0

    show hisao_wtf_close_u with charamove
    hide hisao_declare_u at centersit
    ##maybe show hisao_wtf en close up like with kimono_happy_close

    play music music_fripperies fadein 1.0

    "He attempts to play it cool, but I'm not willing to let him go that easily. Grabbing his tie and pulling him in, I give an impish grin."

    mk "You know, we could give it a try if you want. Sex is pretty fun, you know."

    mk "You're a pretty cute guy, after all. Seem pretty trustworthy, too. I wouldn't mind one bit."

    show hisao_erm_close_u with charachange
    hide hisao_wtf_close_u

    hi "That's an awfully strange way to start a relationship with someone."

    mk "'Relationship' is such a strong word. It's not like there's a law saying you have to be lovers to have sex, you know."

    "I do my best to get a read on him, but it's hard to say if he's really willing. He seems to be giving it sincere thought at least, which is heartening."

    "As moments pass, I slowly become aware that this could probably be called sexual harassment. I wouldn't want something like this to sour our friendship, and things would just be awkward if he wasn't really into it."

    show hisao_erm_u at centersit with charamove
    hide hisao_erm_close_u

    "Accepting that this is Hisao's decision rather than mine, I let go of his tie and sit back."

    mk "You need to loosen up, man."

    mk "If you want to save yourself for someone special, that's fine. You can stay overnight to just study or talk if you want. I'm just saying that if you want to screw as well, I'd be up for it."

    show hisao_talk_small_u at centersit with charachange
    hide hisao_erm_u at centersit

    hi "How can you always be so carefree? I'm kind of envious."

    mk "Well?"

    show hisao_declare_u at centersit with charachange
    hide hisao_talk_small_u at centersit

    "His decision appears to be made, his staring at me ending with a great sigh."

    hi "I guess just messing about with a friend would take some anxiety out of the first time."

    mk "Right?"

    show hisao_blush_u at centersit with charachange
    hide hisao_declare_u at centersit

    "A silence falls as Hisao's face drops."

    mk "Something wrong?"

    hi "So... do we kiss, or...?"

    "I break out into laughter. Probably the worst thing to do in this situation, but I don't care at all. How is this guy so bloody innocent?"

    mk "You're makin' me feel guilty about this!"

    hi "Yeah, yeah. Laugh it up."

    stop music fadeout 2.0

    "After having a good chuckle, I manage to slowly get myself back together. His innocence is charming, but I suppose innocence itself can be fun to corrupt."

    play music music_to_become_one

    "Knowing that Hisao taking the initiative is unlikely to happen, and would be awkward at best if he did, I decide to lead him as best I can. The box between us is easily shoved aside, leaving me to shuffle myself in front of him."

    "Reaching out and starting to pop his shirt buttons one by one, I can feel my eagerness starting to get the better of me. For Hisao's part, he takes his cue and dutifully undoes his tie."

    hi "You're pretty good at that. Undoing buttons, that is."

    mk "You learn this stuff pretty quick when you need to."

    hide hisao_blush_u at centersit with dissolve
    show hisao_topless with dissolve

    "Coming to the bottom button of his shirt and undoing it with practiced ease, I quickly pull it off and admire the sight in front of me. I can't help but give a long, wistful breath at the sight of his bare chest."

    "He does his best not to notice, but I can tell he likes the reaction. While not exactly chiselled, it's clear he's in better shape than the average dude. Rather than being the result of some careful weights regime, his body tells of someone who, like a certain other in the club, has kept himself quite fit."

    "His heart attack was all the more unfortunate, in that light. He must've been an active and outdoorsy kind of person before that happened, and now he's stuck studying long into the night just for something to do. The scar running up his torso makes that clearer than words ever could."

    "Without thinking, I reach out and start feeling up his chest."

    mk "You're pretty nice looking, you know."

    hi "Scar aside."

    mk "It's just a line. Besides, at least you can hide it."

    mk "This might be a bit late, but are you sure it's okay to do this with your heart thing?"

    hi "Arrhythmia. I'll be okay, I just have to take it easy."

    "As I continue running my hand over him, I notice Hisao's eyes peering down into my top. He takes my smile as permission, his hand gingerly reaching forwards."

    ##return

# H-scene separator for those who disabled adult scenes in main menu. [str]
label en_H1h:

    scene black with dissolve

    "He seems mildly surprised at how my breast feels as he begins to gently grope my left one, feeling out its shape and seeing how it reacts when lightly kneaded."

    "My heat skips a beat as his hand chases underneath my tank top, playing with it directly before moving to my nipple. The look on his face of lust mixed with sheer curiosity turns me on more than his haphazard groping could."

    "My hand slowly moves down from his chest to his stomach, before coming over the now tight crotch of his trousers. His breath catches as I move it up and down a little, the thickening shaft inside obvious to the touch."

    "Hisao and I look to each other for a moment, the both of us knowing that there's no going back after this. Our eyes couldn't be more different, mine asking for this to continue as his show caution."

    "He manages to settle himself with a gulp, accepting the idea of stripping in front of me. Off comes his belt, soon followed by his socks. He manages to tug off his trousers with some effort, before the reluctant strip show ends with his underwear being done away with."

    "And there Hisao is, entirely naked as he sits on the floor of my room before me. I can't help but pause a little to appreciate the lovely sight."

    "Looks like my assessment of him having a nice body was spot on, his legs also being suitably toned with a light covering of hair. Then there's his crotch, entirely exposed with its rod standing proudly erect in anticipation. I kind of want to jump his bones right now, though think better of it."

    hi "You look pleased with yourself."

    mk "Shouldn't you take pride in turning a girl on?"

    "He blushes at the praise, words stolen from his mouth as I slowly begin to lower myself down and brush back my hair."

    "I wonder if I'll ever get used to seeing a man's junk this closely. It might be more simple than a girl's, but it just looks so odd. Thankfully there's barely any smell, with only a faint musk left thanks to him having had a bath before coming."

    "Unable to help myself, I reach forward and delicately run my finger down the stiff organ from the pink head to its fleshy base, the thing twitching in response. It amuses me how they have such a life of their own, with so many involuntary motions and reactions."

    "My cheeky grin up to him is met with a grimace as he blushes heavily. My staring so closely and poking at him probably isn't helping his embarrassment, nor that I'm fully dressed while he's in the buff."

    "As much as he might enjoy this, I have to psyche myself up a little as I work up some spittle. Using my mouth to do this still doesn't feel natural, regardless of how recently he may have washed."

if persistent.adultmode:
    scene bg 4561 with dissolve

    "A gasp comes from Hisao as my pursed lips slide over the head, slowly moving down over his shaft. Peeking up to see his reaction shows a flustered face, his eyes trying their best to engrave what he's seeing to memory."

    "My close up view of his crotch as I do this isn't exactly great, but the hold I have over his emotions is kind of nice. It's obvious he's enjoying this, and as I begin to slowly move my head up and down, he begins to let himself go with what his body is telling him."

    "The feeling of his swollen rod pressing against my tongue spurs me to move it around a bit, as much for my own comfort as his. I must be doing something right, as restrained moans start coming from Hisao's lips."

    "I pull my mouth from him, taking the now wet shaft in my hand and using it to continue his pleasure. Given that this is the first time he's done this, I go as lightly as I can. He's already breathing heavily, his solid chest heaving as he tries to control himself."

    mk "So, what do you think?"

    hi "You know the answer to that..."

    "How unfortunate; he's getting too good at knowing when I'm fishing for praise. I just smirk."

    "Taking him into my mouth once more, I return to my motions. He seems to enjoy what I'm doing so far, so I just stick with what I've been doing."

    "Hisao must be getting close, as his breathing is beginning to get more ragged and the muscles in his groin begin to tighten. His concentration on controlling his urges is written to his face."

    scene black

    mk "Miki... Ahn!"

    "My eyes open wide as thick liquid suddenly shoots into my mouth, forcefully hitting the back of my throat. Hisao's body jerks and spasms uncontrollably as he climaxes, the muscles of his shaft pumping away. All I can do is shudder as I desperately try to deal with the fluid suddenly filling my mouth."

    "The event is over, at least for Hisao, as his orgasm runs its course. With his rod slowly beginning to shrink, still twitching from its earlier vigour, I pull myself off of it and quickly bring a hand over my mouth."

    "I've never tasted this stuff before, and if I thought its texture was off-putting in normal circumstances, it's ten times more so inside my mouth. I gingerly try to swallow, but the viscous white goop sticks to the inside of my throat."

    "My gag reflex suddenly triggering, I frantically come to my feet and run over to my desk and grab for a tissue. The disgusting mucus-like mess takes some effort to get out, my body heaving as I forcefully spit and huck."

    "I manage to get the vast majority out with some work, crumpling up the tissue and throwing it at the bin before taking a few much-needed breaths of air."

    mk "Men are so gross..."

    hi "Are you okay?"

    "I wipe my mouth with the back of my hand as I drearily look to him. He still sits there naked, same as before save for his face of concern and much smaller member."

    mk "You could warn me, asshole."

    hi "Does it really taste that bad?"

    mk "Imagine taking a mouthful of thick mucus. Maybe I should feed you some back one day."

    "The face he pulls says all that need be said, the boy rising to his feet with a grunt before walking over."

    "He asks for a tissue which I helpfully provide, setting about cleaning his junk as I stand next to him. I can't help but look down and watch, a little pleased that he's at least acting a bit less uptight about this stuff now."

    hi "Thanks, anyway. That felt really good."

    mk "You're talking like this is over."

    hi "But I've already..."

    mk "You're not the only one here, dude. We're not stopping at third base."

    "He looks unsure, but I guess it's understandable; it's hard to say when he'll be ready for round two. I'm still ready and rearing to go, though, so he's at least going to learn how to pleasure me before this is over."

    scene bg topless with dissolve

    "I take a hold of my top and begin to lift, his eyes widening as I let it fall to the floor. My bust isn't the only thing he's going to see, with my shorts and panties following in short measure. I just stand back and put my hand on my hip, letting him admire the first naked girl he's likely seen outside of porn."

    "His hormones get the better of him, his eyes moving up and down as he takes in my figure. It's obvious that he likes what he sees."

    hi "Geez..."

    mk "I'll take that as a compliment."

    "He hesitates, but takes a step forwards towards me. I answer his hand running up my side by wrapping my arms around him to draw him into a hug, pulling us together."

    "Our hands begin to explore each other as we savour the feeling of each other's bodies, Hisao's hands pressing lustfully into my back and pressing my breasts to his chest as mine slides down his back and grips onto his hard butt."

    mk "Hisao..."

    "I can hear his lustful breathing next to my ear, his head tilting down to take a lick at the base of my neck. My mind is filled with desire, desperately wanting to ravage him."

    "Tiring of being gentle, I break from our embrace and step back towards the bed, drawing him along with me as I hold his wrist. He's starting to recharge by now, so it shouldn't take much more stimulation to get him going."

    scene black
    play sound sfx_pillow

    "He steps ahead of me and slides onto the bed, with me crawling on after him. He takes the hint as I push on his shoulders a little, flopping down on his back as I shuffle about on all fours over him."

    "Throwing a leg over his head, I position myself with my head over his crotch and his head beneath mine."

    hi "So this is what it looks like..."

    mk "Hey, I had to get close to your junk before. You know how to do this?"

    hi "I'm not an idiot, you know."

    mk "I sure hope not."

    "Content with my teasing, I lower my head and lap a little at the base, trying my best not to get hairs in my mouth. I can feel Hisao's hands running up my thighs and gripping my butt as I do, taking in how it feels."

    "I let out a long sigh of pleasure as he kisses my already rather moist nub, my desire for his body finally sated. As he begins to kiss and lick at the various parts between my legs, I dutifully do my bit for him."

    "He isn't quite hitting the motions I most enjoy, but I leave him to explore my regions as he likes. As his member slowly becomes more erect from all the fooling around, it seems like he's liking this as much as I am."

    "I pick my head up, lick my lips, and slide my mouth over his shaft once more. He stops his playing with me for a moment to let out a moan of pleasure, before lapping away at me with renewed vigour."

    "The sweat on my body and his is starting to form, the scent of our excitement starting to pick up on the air. Even as I'm moving my head, I can't help a moan escaping as pleasure starts to overwhelm me."

    hi "Hey, Miki?"

    "Stopping the moment I hear his voice for fear of repeat of earlier, I pick my head up and look around to his flustered face."

    hi "Do you want to..."

    mk "Sure. Stay there a moment."

    "I pick myself off him and get off the bed, my movements a little stilted thanks to how turned on I am."

    "Reach my desk and pulling out the drawer, I grab a small foil square and chuck it at him. He looks a little puzzled for a moment as it lands on his chest."

    hi "Oh, right. That was lucky."

    mk "Guessing you didn't want to run to the convenience store right now, eh?"

    "Hisao quickly sits himself up and sets about ripping the wrapper and applying the condom, sliding it over his shaft without too much trouble. As I come back to the bed, it looks like he's finally lost his reluctance about popping his cherry."

    "We end up fooling around a bit after I get back on the bed, eventually ending up with me on my back and Hisao sitting up at my waist. I suppose there's nothing wrong with him taking the lead."

    "He gives me a cautious look before taking a deep breath, eyes passing over my body. I reach down and take the base of his rod in my hand, having a little fun in rubbing it over my wetted lower lips before pressing the head against my entrance."

    "With one slow thrust, Hisao gently pushes his hips forward and inserts himself into me as far as he can go. A long, pleasureful breath passes my lips, that wonderful feeling of fullness engulfing my mind."

    mk "Ooh..."

    hi "Miki..."

    "I look up at him, his body seeming all the lager as he sits upright, hands on the bed beside my waist. I really like this view of him."

    mk "You've done good, boy. Now stop sitting there."

    "He responds by starting to move his hips, ever so slowly thrusting away as he takes in the feeling inside of me. I just let myself relax, content to sit back and let myself drift in the experience as I grip at the sheets beneath me."

    "Thankfully he needs no prompting to stop being so gentle, his timidity slowly dropping as he realises he's not going to hurt me by being a little more rough. As he keeps at it, he eventually hits a pretty nice rhythm as the sounds of our lustful breathing and bodies hitting each other begin to fill the air."

    "As much as I try to let myself just go with the flow, I can't help but smile at the expression of concentration he's making. He's really trying to do this right, and to engrave everything he's doing to memory. It's a funny contrast to how relaxed I feel as he thrusts into me."

    hi "Why are... you smiling like that?"

    mk "You just look funny, man. Relax a bit."

    "He makes an honest attempt at it, and to his credit, sort of manages to do so. As feelings of euphoria start to cloud my mind, my hand moves to start pleasuring myself, circling my nub with my finger as he goes."

    "This is so wonderful. I can't get enough of Hisao, his beautiful broad chest heaving away as he grunts and groans. His inexperience is cute, the way his mind takes in the wholly new smells, sounds, and sensations shown plainly on his face."

    "Wanting to feel that body for myself, I reach up with my arms for him."

    mk "Come here."

    "Hisao follows my directions, shifting his body down with his elbows on the bed either side of me. I wrap my arms around his back, holding his body to mine as he starts thrusting into me once more."

    "I think we're both getting close to our limits now, the sound of his breathing next to my ear turning me on further, as does the feeling of his sweat-covered back and butt as I move my hand over them."

    hi "Miki... Miki..."

    "The first flicker of extreme pleasure pulses through me as I feel myself reaching the end, clutching at Hisao's hard body as if I were trying to grab hold of that fleeting feeling."

    "My hand digs into his back as my pleasure begins to rise rapidly, my desperate attempts to catch on to each flash of ecstasy making them last longer and longer. Don't you dare finish on me now, Hisao. I'm so close... so close..."

    hi "Miki, I can't...!"

    "I squeeze him tightly to try and make him hold on just that little bit longer. I'm almost there, just... a little... more...!"

    mk "Ahn!"

    "I stuff my face into his shoulder as the feeling of climax rips through my entire body, every muscle clenching as hard as it can. Hisao's body, the scent of his sweat, the sound of his frantic breathing, it all fills my mind as I feel myself drowning in desire."

    "An unmistakable grunt comes from Hisao, his body jerking as the twitching and spasming around his shaft pulls him into climax as well. Once, twice, three times he gives powerful, rough thrusts into me, only serving to make my orgasm all the better."

    "But slowly, sadly, it begins to fade. I try to hold on to the threads of pleasure, but one by one they slip from my grasp, my muscles slowly relaxing as that crescendo of joy falls silent."

    "With the high of sex has to come the low, I suppose. The both of us are left a mess as our business comes to an end, our bodies both sweaty and limp, save the odd involuntary twitch."

    "I'm glad Hisao didn't roll off me after we finished; it's nice to feel his body as the warmth lingers. There's little point in asking him if it was good, as the answer to that is painfully obvious."

    "All I can do as we recover ourselves, is tiredly pet his dishevelled hair."

    stop music fadeout 1.0

else:
    scene bg doggo with dissolve

    "A gasp comes from Hisao as my pursed lips slide over the head, slowly moving down over his shaft. Peeking up to see his reaction shows a flustered face, his eyes trying their best to engrave what he's seeing to memory."

    "My close up view of his crotch as I do this isn't exactly great, but the hold I have over his emotions is kind of nice. It's obvious he's enjoying this, and as I begin to slowly move my head up and down, he begins to let himself go with what his body is telling him."

    "The feeling of his swollen rod pressing against my tongue spurs me to move it around a bit, as much for my own comfort as his. I must be doing something right, as restrained moans start coming from Hisao's lips."

    "I pull my mouth from him, taking the now wet shaft in my hand and using it to continue his pleasure. Given that this is the first time he's done this, I go as lightly as I can. He's already breathing heavily, his solid chest heaving as he tries to control himself."

    mk "So, what do you think?"

    hi "You know the answer to that..."

    "How unfortunate; he's getting too good at knowing when I'm fishing for praise. I just smirk."

    "Taking him into my mouth once more, I return to my motions. He seems to enjoy what I'm doing so far, so I just stick with that I've been doing."

    "Hisao must be getting close, as his breathing is beginning to get more ragged and the muscles in his groin begin to tighten. His concentration on controlling his urges is written to his face."

    scene black

    mk "Miki... Ahn!"

    "My eyes open wide as thick liquid suddenly shoots into my mouth, forcefully hitting the back of my throat. Hisao's body jerks and spasms uncontrollably as he climaxes, the muscles of his shaft pumping away. All I can do is shudder as I desperately try to deal with the fluid suddenly filling my mouth."

    "The event is over, at least for Hisao, as his orgasm runs its course. With his rod slowly beginning to shrink, still twitching from its earlier vigour, I pull myself off of it and quickly bring a hand over my mouth."

    "I've never tasted this stuff before, and if I thought its texture was off-putting in normal circumstances, it's ten times more so inside my mouth. I gingerly try to swallow, but the viscous white goop sticks to the inside of my throat."

    "My gag reflex suddenly triggering, I frantically come to my feet and run over to my desk and grab for a tissue. The disgusting mucus-like mess takes some effort to get out, my body heaving as I forcefully spit and huck."

    "I manage to get the vast majority out with some work, crumpling up the tissue and throwing it at the bin before taking a few much-needed breaths of air."

    mk "Men are so gross..."

    hi "Are you okay?"

    "I wipe my mouth with the back of my hand as I drearily look to him. He still sits there naked, same as before save for his face of concern and much smaller member."

    mk "You could warn me, asshole."

    hi "Does it really taste that bad?"

    mk "Imagine taking a mouthful of thick mucus. Maybe I should feed you some back one day."

    "The face he pulls says all that need be said, the boy rising to his feet with a grunt before walking over."

    "He asks for a tissue which I helpfully provide, setting about cleaning his junk as I stand next to him. I can't help but look down and watch, a little pleased that he's at least acting a bit less uptight about this stuff now."

    hi "Thanks, anyway. That felt really good."

    mk "You're talking like this is over."

    hi "But I've already..."

    mk "You're not the only one here, dude. We're not stopping at third base."

    "He looks unsure, but I guess it's understandable; it's hard to say when he'll be ready for round two. I'm still ready and rearing to go, though, so he's at least going to learn how to pleasure me before this is over."

    scene bg doggo with dissolve

    "I take a hold of my top and begin to lift, his eyes widening as I let it fall to the floor. My bust isn't the only thing he's going to see, with my shorts and panties following in short measure. I just stand back and put my hand on my hip, letting him admire the first naked girl he's likely seen outside of porn."

    "His hormones get the better of him, his eyes moving up and down as he takes in my figure. It's obvious that he likes what he sees."

    hi "Geez..."

    mk "I'll take that as a compliment."

    "He hesitates, but takes a step forwards towards me. I answer his hand running up my side by wrapping my arms around him to draw him into a hug, pulling us together."

    "Our hands begin to explore each other as we savour the feeling of each other's bodies, Hisao's hands pressing lustfully into my back and pressing my breasts to his chest as mine slides down his back and grips onto his hard butt."

    mk "Hisao..."

    "I can hear his lustful breathing next to my ear, his head tilting down to take a lick at the base of my neck. My mind is filled with desire, desperately wanting to ravage him."

    "Tiring of being gentle, I break from our embrace and step back towards the bed, drawing him along with me as I hold his wrist. He's starting to recharge by now, so it shouldn't take much more stimulation to get him going."

    scene black
    play sound sfx_pillow

    "He steps ahead of me and slides onto the bed, with me crawling on after him. He takes the hint as I push on his shoulders a little, flopping down on his back as I shuffle about on all fours over him."

    "Throwing a leg over his head, I position myself with my head over his crotch and his head beneath mine."

    hi "So this is what it looks like..."

    mk "Hey, I had to get close to your junk before. You know how to do this?"

    hi "I'm not an idiot, you know."

    mk "I sure hope not."

    "Content with my teasing, I lower my head and lap a little at the base, trying my best not to get hairs in my mouth. I can feel Hisao's hands running up my thighs and gripping my butt as I do, taking in how it feels."

    "I let out a long sigh of pleasure as he kisses my already rather moist nub, my desire for his body finally sated. As he begins to kiss and lick at the various parts between my legs, I dutifully do my bit for him."

    "He isn't quite hitting the motions I most enjoy, but I leave him to explore my regions as he likes. As his member slowly becomes more erect from all the fooling around, it seems like he's liking this as much as I am."

    "I pick my head up, lick my lips, and slide my mouth over his shaft once more. He stops his playing with me for a moment to let out a moan of pleasure, before lapping away at me with renewed vigour."

    "The sweat on my body and his is starting to form, the scent of our excitement starting to pick up on the air. Even as I'm moving my head, I can't help a moan escaping as pleasure starts to overwhelm me."

    hi "Hey, Miki?"

    "Stopping the moment I hear his voice for fear of repeat of earlier, I pick my head up and look around to his flustered face."

    hi "Do you want to..."

    mk "Sure. Stay there a moment."

    "I pick myself off him and get off the bed, my movements a little stilted thanks to how turned on I am."

    "Reach my desk and pulling out the drawer, I grab a small foil square and chuck it at him. He looks a little puzzled for a moment as it lands on his chest."

    hi "Oh, right. That was lucky."

    mk "Guessing you didn't want to run to the convenience store right now, eh?"

    "Hisao quickly sits himself up and sets about ripping the wrapper and applying the condom, sliding it over his shaft without too much trouble. As I come back to the bed, it looks like he's finally lost his reluctance about popping his cherry."

    "We end up fooling around a bit after I get back on the bed, eventually ending up with me on my back and Hisao sitting up at my waist. I suppose there's nothing wrong with him taking the lead."

    "He gives me a cautious look before taking a deep breath, eyes passing over my body. I reach down and take the base of his rod in my hand, having a little fun in rubbing it over my wetted lower lips before pressing the head against my entrance."

    "With one slow thrust, Hisao gently pushes his hips forward and inserts himself into me as far as he can go. A long, pleasureful breath passes my lips, that wonderful feeling of fullness engulfing my mind."

    mk "Ooh..."

    hi "Miki..."

    "I look up at him, his body seeming all the lager as he sits upright, hands on the bed beside my waist. I really like this view of him."

    mk "You've done good, boy. Now stop sitting there."

    "He responds by starting to move his hips, ever so slowly thrusting away as he takes in the feeling inside of me. I just let myself relax, content to sit back and let myself drift in the experience as I grip at the sheets beneath me."

    "Thankfully he needs no prompting to stop being so gentle, his timidity slowly dropping as he realises he's not going to hurt me by being a little more rough. As he keeps at it, he eventually hits a pretty nice rhythm as the sounds of our lustful breathing and bodies hitting each other begin to fill the air."

    "As much as I try to let myself just go with the flow, I can't help but smile at the expression of concentration he's making. He's really trying to do this right, and to engrave everything he's doing to memory. It's a funny contrast to how relaxed I feel as he thrusts into me."

    hi "Why are... you smiling like that?"

    mk "You just look funny, man. Relax a bit."

    "He makes an honest attempt at it, and to his credit, sort of manages to do so. As feelings of euphoria start to cloud my mind, my hand moves to start pleasuring myself, circling my nub with my finger as he goes."

    "This is so wonderful. I can't get enough of Hisao, his beautiful broad chest heaving away as he grunts and groans. His inexperience is cute, the way his mind takes in the wholly new smells, sounds, and sensations shown plainly on his face."

    "Wanting to feel that body for myself, I reach up with my arms for him."

    mk "Come here."

    "Hisao follows my directions, shifting his body down with his elbows on the bed either side of me. I wrap my arms around his back, holding his body to mine as he starts thrusting into me once more."

    "I think we're both getting close to our limits now, the sound of his breathing next to my ear turning me on further, as does the feeling of his sweat-covered back and butt as I move my hand over them."

    hi "Miki... Miki..."

    "The first flicker of extreme pleasure pulses through me as I feel myself reaching the end, clutching at Hisao's hard body as if I were trying to grab hold of that fleeting feeling."

    "My hand digs into his back as my pleasure begins to rise rapidly, my desperate attempts to catch on to each flash of ecstasy making them last longer and longer. Don't you dare finish on me now, Hisao. I'm so close... so close..."

    hi "Miki, I can't...!"

    "I squeeze him tightly to try and make him hold on just that little bit longer. I'm almost there, just... a little... more...!"

    mk "Ahn!"

    "I stuff my face into his shoulder as the feeling of climax rips through my entire body, every muscle clenching as hard as it can. Hisao's body, the scent of his sweat, the sound of his frantic breathing, it all fills my mind as I feel myself drowning in desire."

    "An unmistakable grunt comes from Hisao, his body jerking as the twitching and spasming around his shaft pulls him into climax as well. Once, twice, three times he gives powerful, rough thrusts into me, only serving to make my orgasm all the better."

    "But slowly, sadly, it begins to fade. I try to hold on to the threads of pleasure, but one by one they slip from my grasp, my muscles slowly relaxing as that crescendo of joy falls silent."

    "With the high of sex has to come the low, I suppose. The both of us are left a mess as our business comes to an end, our bodies both sweaty and limp, save the odd involuntary twitch."

    "I'm glad Hisao didn't roll off me after we finished; it's nice to feel his body as the warmth lingers. There's little point in asking him if it was good, as the answer to that is painfully obvious."

    "All I can do as we recover ourselves, is tiredly pet his dishevelled hair."

    stop music fadeout 1.0

    ##return

# H-scene end. [str]
label en_H1x:

    scene bg school_dormmiki with shorttimeskip

    show hisao_smile_u with dissolve

    #centered "~ Timeskip ~" with dissolve

    "With the both of us cleaned up and clothed once more, we lie beneath the sheets next to each other as we try to go to sleep. Not that we try very hard, admittedly."

    hi "Thanks for tonight, Miki."

    mk "Hey, it was nice for me too. Aside from you-{w=.85}{nw}"

    show hisao_blush_u with charachange
    hide hisao_smile_u

    hi "Alright, you don't need to go on about that. It just kinda snuck up on me."

    mk "I'll bet."

    hi "So we're off on our little adventure tomorrow. What's your home like, anyway?"

    mk "You'll see. I reckon you'll like it."

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_H2:

    play ambient sfx_traffic

    window show
    scene bg busstop

    "With the last of our luggage off the bus and piled onto the chair of the shelter, the old thing slowly pulls away with a friendly wave from the driver. It's a small wonder that it's still around after all these years."

    stop ambient fadeout 3.5

    "As the rumble of the tired old engine fades away, it's replaced by nothing but silence. A comfortable, nostalgic silence."

    "Looking out from the wooden bus stop, topped by a rusted sheet of iron that only barely keeps the sun out, a bright green expanse greets us."

    scene bg countryside with dissolve

    play music music_daily

    "The lonely cracked road cuts a straight line between the multitude of farms and rice paddies that cover the valley. A multitude of perfect rectangles, the muddy fields rimmed by embankments of thick grass, and going on as far as the eye can see."

    "All that breaks up the view are the wooden poles carrying sagging power lines, trees, and the occasional traditional-style house for the tirelessly working farmers who live here."

    "Then finally, the hills of the valley. Rising sharply on either side of the town, they frame the entire village with their lush woods."

    "I'd say memories come back of hiking and messing around in those woods, but that's true of everywhere here. Not one thing in sight doesn't have a memory attached to it. I lived here, from my birth to just three years ago. Now, I'm finally back."

    "I've come home."

    hi "What's up?"

    show hisao_talk_small at tworight
    show suzu_surprised_d at twoleft
    with dissolve

    "I turn to my two companions on this trip. In my unexpected nostalgia for the place, I'd forgotten that it was their reactions that I was looking forward to, not my own."

    "Suzu couldn't give less of a damn about me, simply standing wide-eyed at the sight before her. You'd be forgiven for thinking she'd just seen the landscape from one of her computer games become real."

    "Even Hisao, despite his attention being on me, obviously has his mind in two places at once."

    mk "What do ya mean?"

    hi "You don't have an excuse to look distracted like we do."

    "He's not wrong. If I'd left on different terms, or even just taken the chance to visit once or twice, perhaps I'd be totally ambivalent about being back here."

    "They see a bunch of farms and woodland, but I see memories of a fate I'd given up on. That I'd wanted, desperately, to give up on. If only life worked like that."

    mk "Come on, it's not that weird a place, is it?"

    "I give a disarming smile to Hisao, but he doesn't seem to buy the misdirection. It's only now that I realise I've been absentmindedly rubbing the stump of my left arm."

    show suzu_concerned_d at twoleft with charamove
    hide suzu_surprised_d at twoleft

    suz "It pretty much is, yeah."

    show hisao_erm at tworight with charachange
    hide hisao_talk_small at tworight

    hi "I remember seeing places like this in the news, but that's different to actually being here."

    hi "There's just... nothing."

    mk "C'mon, there's plenty of stuff."

    suz "Like?"

    mk "Farms, the mountains."

    hi "And?"

    mk "...Farms, the mountains."

    "Their faces fall flat. Using hyperbole really doesn't work when they already believe it."

    mk "I'm joking! That's a joke!"

    mk "C'mon, if there are people who live here, that means a bunch of stuff has to be around to support them, right?"

    hi "I guess that's true."

    "He doesn't look convinced. Suzu looks like she didn't even hear me, given that she's begun to wander around and take in the sights from outside the little shelter. It doesn't take long for her to pick up on something from down the road."

    show suzu_speak_d at twoleft with charachange
    hide suzu_concerned_d at twoleft

    suz "Ah, there's a truck coming."

    mk "Probably dad. Told you he wouldn't be long."

    play sound sfx_kei_arrive fadein 2.0

    "She skips back off the road to where we're standing, picking up her duffel bag from the chair. As the old white Kei truck slows down and comes to a stop, the unmistakable figure of my father can be seen taking off his seatbelt and swinging open the door."

    show suzu_speak_d at left with charamove
    show suzu_neutral_d at left with charamove
    hide suzu_speak_d at left
    show hisao_erm at rightedge with charamove
    show dad_smile at center with dissolve

    "He's a well built man, by any definition. That, in combination with his stubble and his distinct tan from labouring in the fields, would make him an intimidating figure if not for his wide smile. His cheerful expression is always the first thing people notice about him, and for good reason."

    "That said, he's not all that well kept, admittedly. His hair is cut badly from doing it himself, his stubble is shaved irregularly, and his fingernails are always blackened from dried mud underneath."

    "But that's the kind of person he always was. He loves his work, and he loves people. We might have different personalities, but I always felt a grudging respect for his outlook."

    mk "Hey, dad. It's been a while."

    show dad_smile_close at center with charamove
    hide dad_smile at center
    with hpunch

    "He suddenly lunges forward and wraps his arms around me, much to my admittedly half-hearted protest. I try to shout him down for doing it in front of my friends, but he only lets go after giving me a good shake."

    show dad_smile at center with charamove
    hide dad_smile_close at center

    jun "Good to see you, girl. It's amazin' how much you've grown since I saw you."

    "I kinda want to joke with him, but I'm having trouble finding the words. It never really hit me how long three years was until now, face to face with my dad after so long. I can feel a really dumb grin on my face."

    "After taking a breath to settle myself, I clear my throat and gesture to Suzu."

    mk "Suzu, this is my dad. Dad, this is Suzu Suzuki. She's the friend I've talked to you about."

    show suzu_asleep_d at left with charamove ##with yuuko bow animation?
    hide suzu_neutral_d at left
    show suzu_asleep_d at leftsitlow with charamove
    show suzu_asleep_d at left with charamove
    show suzu_concerned_d at left with charachange
    hide suzu_asleep_d at left
    show dad_smile at centersit with charamove
    show dad_smile at center with charamove

    "She bows deeply to him, to which he responds in kind. I wonder if she's trying to mask her shyness about meeting someone new through excessive manners."

    suz "Pleased to meet you, Mr. Miura."

    show dad_smirk at center with charachange
    hide dad_smile at center

    jun "You don't need to be so polite. Thanks for putting up with her for so long; I know how much of a handful she can be."

    suz "I try my best."

    mk "Very funny. Anyway..."

    mk "This is Hisao Nakai. He's the other friend from class I mentioned."

    show hisao_declare at rightedge ##hisao bowing
    hide hisao_erm at rightedge
    show hisao_declare at rightedgesit with charamove
    show hisao_declare at rightedge with charamove
    show dad_smirk at centersit with charamove
    show dad_smirk at center with charamove

    "Hisao gives a smaller bow as the two greet each other. I hadn't specifically mentioned much about what Hisao was like to dad, but if he's put off by him coming, he isn't showing it."

    show dad_smile at center with charachange
    hide dad_smirk at center

    jun "I have to say... by the looks of you, I didn't exactly expect you two to be the kind of company Miki'd keep."

    show hisao_erm at rightedge with charachange
    hide hisao_declare at rightedge

    hi "Is that a bad thing?"

    show dad_laugh at center with charachange
    hide dad_smile at center

    jun "Hahaha! Believe me, she could do a lot worse, boy."

    show dad_talk at center with charachange
    hide dad_laugh at center

    jun "Anyway, the name's Junichi. You can call me Jun or Junichi, I don't care which. 'Mr. Miura' is too damn stuffy."

    play sound sfx_clap

    "Suzu's sly look towards me tells me one thing; Like father, like son. A loud clap from dad refocuses our attention."

    ##add sfx handclap

    show dad_laugh at center with charachange
    hide dad_talk at center

    jun "Now then, who's in the back tray? We can only fit one person in the front beside me."

    mk "Me! Me! I'm in back!"

    show hisao_frown at rightedge
    hide hisao_erm at rightedge

    "Hisao reluctantly raises his hand, resigned to his fate. He's a guy, he should be looking forward to this sort of adventurous thing he couldn't normally do."

    "Suzu just shrugs and chooses the front without a fight. To be honest, I didn't expect one."

    stop music fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve
    scene bg countryroad with shorttimeskip
    $ renpy.music.set_volume(0.7, 0, channel="sound")


    play sound sfx_car_driving loop

    play music music_pearly

    "It's nice to travel like this. The wind freely blowing past you, the occasional pothole and hump in the road bumping you up and down, and no windows to get between you and the outside world. It's far less boring than being bundled up in a little metal box."

    "Hisao, however, looks a little less sure of himself. His right hand grips the side of the tray tightly, with his back pressed hard against the cabin. Our luggage, sitting between us, bumps around loudly as we cruise down the road."

    mk "Guess it's your first time travelling on the back of a truck, huh?"

    hi "I seem to be having a lot of first times with you..."

    "He might be grumbling, but I think he's enjoying it. Just a little."

    scene bg boar_sign with dissolve

    "As we continue down the road, Hisao's head perks up as we pass something that's caught his interest."

    hi "Wait, was that a pig on that sign?"

    mk "Probably a boar. We get those around here."

    hi "Oh, those things. They look pretty cute, right?"

    mk "The piglets? Sure. Gotta be careful, though; boars can be evil little assholes if you piss 'em off."

    play audio sfx_pothole #fadein 1.0
    with vpunch

    "A pothole in the road gives us both a good jolt, abruptly ending the discussion. My companion looks a little put off."

    mk "Worried?"

    hi "Nah."

    "As time goes on he gets more used to the experience. By the time we turn off the main road and onto the side streets, it almost looks like he's genuinely enjoying himself."

    stop sound fadeout 1.0

    stop music fadeout 1.0

    $ renpy.music.set_volume(1.0, 0, channel="sound") # restoring sfx volume

    ##centered "~ Timeskip ~" with dissolve
    scene bg farm with shorttimeskip
    play sound "<from 2 to 13>kei_arrive.ogg" fadeout 2.0
    play music music_tranquil fadein 2.0

    "With the familiar rumble of braking wheels on rough dirt, the truck pulls to a stop a few feet from the house. Without further ado, Hisao and I hop off as the doors around the front can be heard opening."

    "It's like I'd never left. The grey-tiled roof still remains pockmarked by the odd leaf and stray broke branch that's settled on it, and the aged wood of the walls serves as a stark contrast to Yamaku's carefully tended-to exterior."

    "Glancing through the windows, I suspect dad's been putting a bit of extra effort in to make the place presentable before we arrived. Given that I usually made most of the mess around the house before I left, I doubt it's for my sake."

    "The only major difference I can really see is the vines on one corner of the house having grown some more. Given that I've been gone since entering Yamaku, it's like stepping back in time."

    show dad_smile at leftoff with dissolve
    show hisao_smile at center with dissolve
    show suzu_neutral_d at right with dissolve

    jun "So, what do ya think?"

    hi "It's nice. I haven't stayed at a traditional style house in a long time."

    suz "Likewise."

    jun "Well, I'm sure you'll get used to it. Feel free to wander around as much as you like, just be careful 'round the farm equipment."

    "He quickly walks around the back and dutifully grabs our bags, leaving me to show our guests into the house."

    scene bg farm_interior2 with dissolve

    play sound sfx_sliding_door

    "A good pull sees the door reluctantly slide away with a loud clatter, revealing the entrance foyer inside. With the interior doors having been opened to allow air to circulate through the house, most of the rooms are visible at a glance."

    "A lot of friends have said they felt like Yamaku was home after a few months, but I always felt more like a tourist in a foreign country when I was hanging around the dormitories. A school is a school, no matter where it is, but where you sleep and eat is a very different matter."

    "It could be just because I'm a country bumpkin at heart. Maybe it was because of the circumstances I was in when I first entered Yamaku, or just a matter of being in the female dormitories and cooped up with other girls every evening. Either way, for the first time in years, I finally feel like I'm home."

    "I quickly take my shoes off to distract myself from my meandering thoughts, with the busily gawking Hisao and Suzu doing the same. They hurriedly walk past me and into the main room after depositing their shoes, leaving me to follow behind them afterwards."

    show hisao_talk_small at center with charaenter

    hi "I had no idea your place was like this. You should've mentioned it before."

    "I just shrug."

    show suzu_concerned_d at left with charaenter

    "I look to Suzu to gauge her reaction, only to see her concerned face staring at her phone."

    show suzu_concerned_d at rightedge with charamove
    show hisao_erm at center with charachange
    hide hisao_talk_small at center

    "Before I can ask her what's up, she starts wandering around the room haphazardly, barely managing to step around the low table and other various obstacles. All Hisao and I can do is look at each other with puzzled expressions."

    hi "Uh... Suzu?"

    show suzu_concerned_d at oneleft with charamove

    "She continues on as if she's never heard him, walking around some more before slowly making her way towards the rice paper door leading outside, the sun streaming through. Without a moment's hesitation, she slides it open with her right hand, still holding her phone to her face with her left."

    show suzu_concerned_d at leftoff with charamove

    "As she steps from the tatami floor onto the sunlit wooden porch, she abruptly stops and holds her phone a little higher than before."

    show suzu_grin_d at leftoff with charachange
    hide suzu_concerned_d at left

    suz "I have a bar."

    mk "Huh?"

    show hisao_wtf at center with charachange
    hide hisao_talk_small at center

    "Hisao just hides his face in his hand. It takes me a moment to connect the dots about what she's actually been doing."

    "Never change, Suzu."

    show hisao_smile at center with charachange
    hide hisao_wtf at center

    "As I shake my head at her antics, I can't help but notice Hisao smiling. It's not that he does so rarely; all things considered, he manages to put on a weary smile surprisingly often. This time, though, it feels different."

    "It's going to be an interesting time here, between being home after so long, and sharing the experience with these two misfits."

    "But somehow... I think it's going to be good. The three of us together, enjoying summer in the country."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_H3:

    window show
    scene bg farm_mikiroom with dissolve

    play music music_generic_happy

    "A mighty yawn heralds the beginning of a new day."

    play sound sfx_rustling

    "The sun beaming through the rice paper screen gives the room a pleasant level of light as I prop myself up, rubbing my tired eyes as I look beside me. Looks like Suzu's already awake, going by her empty but impeccably tidy futon."

    "With my mind still half-asleep, I simply sit for a while and hazily look around the room. The walls look kinda bare without the collection of baseball posters and flags I had up when I was a kid, now that I think of it. All that's left is a single tatty poster for the local team."

    play sound sfx_sliding_door
    pause (1.0)
    play sound "<from 0 to 4>running.ogg" fadeout 2.0

    "As each of my senses fire up, the faint sound of chopsticks clattering reaches my ears. My reaction is immediate, taking to my feet, throwing open the bedroom door, and jogging down the hallway to the main room."

    play sound sfx_sliding_door
    pause (1.5)
    play sound sfx_cutlery loop
    scene bg farm_interior2 with dissolve
    show dad_smirk at centersit
    show suzu_neutral_d at leftsit
    show hisao_closed at rightsit
    with charaenter

    "Sure enough, I see three people greedily tucking into breakfast after sliding the screen open, the day's morning news blaring from the small television to the side."

    mk "That's cold."

    "Dad hurriedly gulps down the food in his mouth before looking to me, his face hardly apologetic."

    jun "Thought you might want to sleep in. You looked pretty tired."

    "He says, sitting next to a narcoleptic."

    "My breakfast waits untouched next to Hisao, who gulps down his miso soup without a care in the world. Suzu and dad sit on the other side of the table, the former grazing on some rice as dad gets back to wolfing down pieces of mackerel."

    play audio sfx_sitting

    "Huffing in displeasure, I walk over and take my place, setting myself down with a thud. Neither of the others pay me much heed, beyond glancing over to the loud distraction stomping about the room."

    "As I start eating, I feel myself quickly settling down. Dad's food is good as always, and it's hard to stay annoyed while having a nice warm bowl of miso."

    show dad_laugh at centersit with charachange
    hide dad_smirk at centersit

    jun "You hungry or something, boy?"

    "I look over to Hisao, his bowl of soup emptied and his rice quickly whittling down."

    show hisao_smile_teeth at rightsit with charachange
    hide hisao_closed at rightsit

    hi "This is the best breakfast I've had in a long time. I could get used to this."

    jun "I'll take that as a compliment."

    show dad_smile at centersit with charachange
    hide dad_laugh at centersit

    "As we continue our eating, I notice that dad seems to be in an unusually bright mood. Maybe it's just my imagination - he has always been the upbeat type, after all - but something feels different about him today."

    "Maybe the chance to simply share a meal is enough to lift his spirits. Since I've been at Yamaku, I doubt he's often had the chance."

    jun "So, any plans for the day?"

    show hisao_talk_small at rightsit with charachange
    hide hisao_smile_teeth at rightsit

    hi "Guess we're largely up to Miki's mercy."

    show suzu_grin_d at leftsit with charamove
    hide suzu_neutral_d at leftsit

    suz "Saying that sort of thing might get us killed."

    mk "You can relax. I was just thinking of riding up into town and taking it from there."

    hi "On bikes? Do you have enough to cover us?"

    jun "You can use mine, if you want."

    mk "That old thing? Does it even still work?"

    show dad_grump at centersit with charachange
    hide dad_smile at centersit

    "I find a pair of chopsticks jabbed at the air in front of me."

    jun "You watch your mouth. I use that old girl nearly every day. Might be getting on by now, but she's done me good."

    mk "Sounds like it's settled, then."

    stop music fadeout 1.0

    stop sound fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve

    scene bg fields with shorttimeskip

    $ renpy.music.set_volume(0.7, 0, channel="music")

    play music music_fripperies

    play sound sfx_cycling loop

    #tweak the sfx or music volume here maybe?

    "It didn't take long for us to escape the house after breakfast, the urge to explore the area on everyone's minds as dad went to feed the chickens."

    "With Hisao on dad's bike and Suzu sitting on the back of mine, we set a good pace as we breeze along the otherwise empty road. The odd hill or house is all that breaks up the flat expanse of rice paddies on either side of us."

    mk "Yo, Hisao. You keepin' up okay?"

    show hisao_talk_small with charaenter

    hi "Don't worry, this much should be fine."

    hi "I'm guessing you get a lot of use from these things out here."

    mk "Sure do, it's pretty much the perfect place for 'em. Flat, straight, not much traffic. Nice and easy to just shoot along the roads."

    suz "You do know where we're going, right?"

    mk "I remember this place like the back of my hand. I wanna drop by somewhere before we reach town, though."

    hi "Where?"

    "As we start approaching an intersection, I jerk my head to the left."

    mk "Follow me and I'll show you."

    hide hisao_talk_small with dissolve

    "Suzu clutches me tightly as I stop pedalling and let the bike tilt around the corner. This feeling of speed as the air flows past us is great, and going by Hisao's expression as he follows us around the corner, he's enjoying this just as much as I am."

    "As we right ourselves and end up roughly side by side once more, I notice the thin bead of sweat running down his face."

    mk "Heat not getting to you?"

    show hisao_talk_big with charaenter

    hi "I'm good."

    mk "Glad to hear it. Lots of people complain it's too hot 'round here."

    hi "You know, you don't need to worry so much about me."

    mk "But..."

    stop music fadeout 1.0

    hide hisao_talk_big with dissolve

    play music music_running fadein 1.0

    "Whether in response or just from a sense of competitiveness, Hisao pushes down on the pedals and brings himself out of his seat as he surges forwards, the bike tilting left and right as he pushes past us with great effort. It's impossible to take that kind of challenge lying down."

    mk "Hang on, Suzu!"

    scene bg fields_fast

    suz "Miki, don’t...!"

    "Ignoring Suzu's protests, I do my best to catch up with the boy. She clutches tightly to my waist, but doesn't seem to be panicking."

    "It feels refreshing to breeze along the roads like this, with the fresh air flowing past us and bright sun overhead. It's just like when I was younger, even including when my friends and I would race our bikes."

    show hisao_biggrin with charaenter

    "With some effort, I manage to pull alongside Hisao. His face, or rather his smile, takes me by surprise. He barely even notices me as he powers on, his mouth in a wide, childish grin."

    "Hisao really does look better when he's like this, finally freed from his inhibitions as he lets himself enjoy the moment."

    stop music fadeout 1.0

    stop sound fadeout 0.3

    $ renpy.music.set_volume(1.0, 0, channel="music") # restoring music volume

    ##centered "~ Timeskip ~" with dissolve
    scene bg school with shorttimeskip
    show hisao_erm at tworight
    show suzu_concerned_d at twoleft
    with charaenter

    play music music_soothing

    "Having arrived at our destination, Hisao and I prop our bikes up against a large tree as Suzu dusts herself off, and perhaps tries to collect herself a little."

    "The old school building stands ahead of me, just as it had all those years ago. Mostly wooden, like everything around here, it seems to have had a few more bushes planted around it in order to not look quite so bare."

    "Slightly puzzled, I absentmindedly tilt my head."

    hi "What's up?"

    mk "I could swear it looked bigger."

    show hisao_talk_small at tworight with charachange
    hide hisao_erm at tworight

    hi "That's normal, isn't it? You'd have been a kid when you were last here. Now you're taller and can see it for its real size."

    mk "I guess. Didn't think I was that much smaller back then, though."

    show suzu_surprised_d at twoleft with charamove
    hide suzu_concerned_d at twoleft

    suz "It sure is..."

    suz "...homely?"

    mk "It looks a bit run-down, I know. This place isn't like Yamaku; We got lunch change compared to their budget."

    show hisao_erm at tworight with charachange
    hide hisao_talk_small at tworight

    hi "I wonder if we could get in."

    show suzu_concerned_d at twoleft with charamove
    hide suzu_surprised_d at twoleft

    suz "I'm not sure that's allowed..."

    mk "Pretty sure the place'd be unlocked."

    show suzu_speak_d at twoleft with charachange
    hide suzu_concerned_d at twoleft

    suz "Not you too. What if somebody sees us?"

    mk "Relax, it's not like anybody's around. The teachers would remember me, anyway."

    hide hisao_erm at right with dissolve

    "The explanation doesn't seem to settle her, but Hisao's already on his way. It's nice to see my assumptions about his nature proven, his sense of adventure kindled."

    hide suzu_speak_d at left with dissolve

    play sound sfx_creaking_door

    "Knowing she's lost, Suzu and I follow him up to the door, dirt crunching underfoot as we cross the school grounds. He stands aside to let me have the honour, the old oak door reluctantly giving way with a bit of a heave."

    scene bg countryschool_hallway with locationskip

    "Hisao and Suzu file in as I automatically tug off my shoes. Only now do I remember that a teacher won't scold me any more for failing to carefully remove my shoes and slip them into the shoe locker beside the door. Smiling, I slip them in anyway."

    play sound sfx_wood_floor

    "The floorboards creak as we pass over them, our trio slowly making our way through the hallway as our heads swivel about."

    "Memories of running through these halls echo through my mind. It's only when I almost bump into Hisao that my distraction ends."

    show hisao_disappoint at tworight with charaenter

    mk "What's up?"

    hi "Just nearly tripped over this thing. Why would someone put a bookshelf here of all places?"

    "He looks down at the conspicuously placed waist-high bookshelf, placed firmly against the wall. Suspecting something, I walk around to the other side and place my hand under the bottom shelf, using my stump to help as best it can."

    mk "Help me shift this thing."

    show suzu_concerned_d at twoleft with charaenter

    "He and Suzu look to each other with uncertainty. She just sighs, knowing that protesting would go nowhere."

    "He takes the same position I do on the other side of the furniture, the both of us giving a grunt as we lift it up and set it down a few inches away."

    scene bg hole with dissolve

    "Sure enough, there's a hole in the wall about the diameter of a soccer or basket ball, beige plaster giving way to a dark abyss. It doesn't even look like there's been so much as an attempt to patch the area up"

    mk "Oh man, that's lame. They just shoved this over the hole instead of fixing it."

    "Hisao leans around the side to see, with Suzu grabbing at the bookshelf's top and levering herself over it a little."

    show hisao_talk_small at tworight with charachange
    hide hisao_disappoint at tworight

    hi "Huh. Know what happened?"

    show suzu_speak_d at twoleft with charachange
    hide suzu_concerned_d at twoleft

    suz "Was it you?"

    mk "Hey, not everything is my fault. All I did was hit a ball through a window once."

    show suzu_concerned_d at twoleft with charachange
    hide suzu_speak_d at twoleft

    "She stares at me, understandably dubious."

    mk "...twice."

    stop music fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve

    scene bg countryside_classroom with shorttimeskip

    play music music_night

    "After wanting to have a look inside my old classroom, Hisao suggested he and Suzu wander the school grounds outside. I guess they're getting bored by now, as admittedly the place is pretty bare. To them, anyway."

    "As I sit in the chair I used to sit in, feet up on the desk to relax a little, fragments of a life I once lived surround me."

    "The pot plant sitting on the windowsill, always looking like it was on its last legs, but never quite wilting entirely. An old clock on the wall ticking away. A cheerful message still scrawled on the blackboard for everyone to have a wonderful holiday."

    "Even now I can hear the sounds of chatter around me, the teacher trying to quieten us down for the lesson ahead. The smell from that kid who fell into a rice paddy on the way to school. Glitter getting everywhere as we made a card for a boy who broke his arm. A girl crying after pricking her finger as we tried to sew plush toys."

    "Then there was the baseball team. Nearly all of them were my classmates, after all. The best friends anyone could've hoped for."

    "And then... there's me. One day, chuckling away at another terrible joke from the boy sitting to my side. Another, making a paper plane and hitting the board next to the teacher. Man that lit her up. Not to mention that frantic rush out the door every break, tearing outside to mess around be it sun or snow."

    "And now I'm sitting alone in a classroom, surrounded by silent and empty chairs."

    "Every life has its peaks and valleys. I know that. Times are sometimes good, and sometimes they're a little rough."

    "I don't think I'm sad to relive those days, but it frustrates me how I can't put words to what I do feel."

    play sound sfx_footsteps_hard

    "Hearing footsteps approaching, I look to the door. Hisao stands smiling, arms crossed as he leans against the doorframe."

    show hisao_smile with charaenter

    hi "Finished?"

    mk "Yeah. Let's go."

    stop music fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve
    scene black with shorttimeskip

    "With Suzu's endurance beginning to flag, the decision was made to save the trip to town for another day. With Hisao and I slowly walking our bikes along the road with Suzu in tow, we make our way towards one of my other favourite corners of the town."

    scene bg apple with dissolve

    play music music_miki

    "An apple tree a small distance from the road catches Hisao's eye as we make our way along, his gaze lingering as we walk."

    show hisao_erm at tworight with charaenter

    hi "We should've brought some food; those look pretty damn nice right now."

    mk "Why don't we grab some?"

    show suzu_concerned_d at twoleft with charaenter

    suz "You think they'll allow strangers to just pilfer their fruit?"

    mk "That's how things work around here. We don't really worry about money much."

    "I give the dubious Hisao and Suzu a salute before quickly ducking away, leaving Suzu to quickly grab my falling bike."

    ##centered "~ Timeskip ~" with dissolve
    scene bg apple with shorttimeskip

    "Walking back up to the two of them, I motion for them to follow me up to the tree."

    "Reaching its base and propping our bikes against it, the three of us look up. It's taller than it looked from the road, with the lowest branches far from reach to anyone on the ground."

    show hisao_erm at tworight
    show suzu_concerned_d at twoleft
    with charaenter

    hi "So you're sure we can take a couple?"

    mk "Many as we want, they said. Better us having a feed than letting the birds get to 'em."

    suz "That doesn't help if we can't reach them in the first place..."

    hi "Guess somebody's just going to have to go up."

    show hisao_smile_teeth at tworight
    show suzu_grin_d at twoleft
    with charachange
    hide suzu_concerned_d at twoleft
    hide hisao_erm at tworight

    "They both look to me in unison. This... isn't good."

    mk "What?"

    show suzu_speak_d at twoleft with charachange
    hide suzu_grin_d at twoleft

    suz "What do you mean 'what'? I'm surprised you didn't offer to begin with."

    mk "Well, uh, I mean... there aren't many footholds. Maybe you forgot that I also only have one hand."

    show suzu_concerned_d at twoleft with charachange
    hide suzu_speak_d at twoleft

    suz "Since when did you suddenly start using your stump as an excuse?"

    play sound sfx_clap

    "Hisao's balled hand suddenly comes down on his palm."

    show hisao_talk_big at tworight with charachange
    hide hisao_smile_teeth at tworight

    hi "You're afraid of heights!"

    show suzu_surprised_d at twoleft with charamove
    hide suzu_concerned_d at twoleft

    "Suzu looks to me in shock, but all I can do is cover my face with my hand. Of course he'd be the one to figure it out."

    mk "Shut up, shut up, shut up!"

    suz "You learn something new every day. I had no idea."

    show hisao_disappoint at tworight with charachange
    hide hisao_talk_big at tworight

    "Looking up from underneath my hand, Hisao's stepped up to the foot of the tree and now looks intently at it. With me out for the count and Suzu unlikely to have the stomach for it, it looks like he's taking one for the team and plotting his approach."

    hide hisao_disappoint at tworight with charaexit

    "With a hop he starts on his way, plastering himself to the trunk with ease. He nimbly manages to hoist himself further and further upwards, usually with his feet, but sometimes resorting to reefing himself up with his hands where he can't find a foothold."

    "It doesn't take long for Hisao's to follow his plotted course, swinging a leg up over the lowest solid branch to straddle it, and scooting himself forwards to where the apples are hanging from."

    "Suzu and I just stare in surprise, both of us suitably impressed at his skill. With the sun shining through the leaves of the tree around him as he smiles down at us, quite pleased with himself at our response, I can't help but think Hisao looks a little cool. It's not often I think that about him."

    mk "So were you a monkey in a previous life, or what?"

    show suzu_speak_d at twoleft with charamove
    hide suzu_surprised_d at twoleft

    suz "He could be a ninja."

    mk "That's a good point."

    show suzu_neutral_d at twoleft with charamove
    hide suzu_speak_d at twoleft

    hi "You're not the only one who got up to mischief as a kid, you know."

    "Maybe I underestimated him. I had made a lot of assumptions given that he said he lived in the city, after all."

    hi "So how are we doing this? Catching them by hand might be a bit hard."

    show suzu_concerned_d at twoleft with charamove
    hide suzu_neutral_d at twoleft

    "Suzu and I look to each other. I guess I hadn't thought that far ahead."

    show suzu_asleep_d at twoleft with charachange
    pause(1.0)
    hide suzu_concerned_d at twoleft
    show suzu_concerned_d at twoleft with charachange
    hide suzu_asleep_d at twoleft
    show suzu_concerned_d at center with move

    "Evidently coming to a conclusion she rather wishes she hadn't, Suzu sighs and she steps underneath where Hisao sits. Taking the bottom of her dress in her hands, she holds it out a little, forming a net to catch them with. If it works, it ain't stupid."

    "Apparently happy with the idea, Hisao calls out before dropping the first apple. Successfully caught without any problems, he starts twisting off one after another, sending them falling to Suzu."

    "With none of us having discussed exactly how many we'd take, he ends up stopping once Suzu's skirt is reasonably full. Overcome with temptation, I pluck one out and take a bite to see how they are."

    "The answer turns out to be 'pretty damn good'. I stand there and munch away as Hisao lets his body roll off the branch, hanging by a hand for a moment to gauge the fall before dropping to the ground on his feet."

    show hisao_smile at tworight with charaenter
    play sound sfx_impact
    show suzu_happy_d at center with charachange
    hide suzu_concerned_d at center

    suz "Here."

    "Suzu offers the seven apples in her skirt, with Hisao collecting them in his arms after dusting himself off."

    "With that, the three of us set off for the creek once more, satisfied with our haul."

    stop music fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve
    scene bg creek with shorttimeskip
    show hisao_smile at centersit with dissolve
    #try and show him close until getting up?
    play sound sfx_brook loop

    play music music_lullaby

    "I've always enjoyed coming here as a kid, and even now I can appreciate it. Water quietly trickles along the small creek, a small bird or two crying out occasionally from the trees above. The place was just large enough to run around with a few friends in as a kid, and the ponds had enough water to float various makeshift boats."

    "Hisao and I lazily sit with our feet in the water, the boy munching away at the last of our food haul while I stroke Suzu's hair, her head on my thighs as she sleeps. It's nice to have a chance to rest and cool down, the cool water flowing past my shins a pleasant sensation."

    show hisao_talk_small at centersit with charachange
    hide hisao_smile at centersit

    hi "You know..."

    "He busily attempts to swallow the bit of food he's eating before continuing."

    hi "I'm surprised you can ride a bike that well. I mean, without..."

    mk "It's not so hard. It's like when I was undoing your buttons; you pick that stuff up pretty quickly when you have the need."

    show hisao_erm at centersit with charachange
    hide hisao_talk_small at centersit

    hi "I guess walking around an area this vast would be pretty gruelling."

    hi "What about prosthetics? I noticed some guy with a prosthetic arm in another class."

    mk "Eh... those fancy computer ones with the moving fingers are crazy expensive. Tried one of those hook ones, though."

    hi "No good?"

    mk "I made a great pirate impression, but I never got the hang of actually using the thing. Never felt comfortable, either."

    mk "Everyone's different, I guess. Just ended up being more of a pain than a help for me."

    "Much to the annoyance of my father and the therapist trying to work with me. The whole fuss is probably part of why dad thought sending me to Yamaku might be for the best. I still don't know whether he was right."

    "As he finishes the last of his apple, Hisao shakes his fingers in the water to clean them before looking to the slumbering Suzu."

    show hisao_smile at centersit with charachange
    hide hisao_erm at centersit

    mk "Peaceful, isn't she?"

    hi "Yeah. Then again, this whole town is like that."

    hi "I still don't get how someone like you could come from such a quiet place."

    mk "When you're surrounded by nothing, you've gotta make your own fun."

    show hisao_erm at centersit with charachange
    hide hisao_smile at centersit

    hi "Guess I had it easy, with the theatres, shopping malls, bookstores, and all that around. Used to hit up the arcades pretty often."

    mk "Yeah, I noticed."

    mk "Did you see those event things often? Like companies putting on street stuff for people passing by?"

    hi "You have no idea. People everywhere handing out flyers and packets, bands doing performances, little exhibitions run near the train stations, festivals..."

    show hisao_smile at centersit with charachange
    hide hisao_erm at centersit

    hi "When you have that many people so tightly packed together, you get a lot of spontaneous stuff happening. You can just wander around and find something to do, really."

    mk "Man, that sounds cool."

    hi "Yeah, it was. After the heart attack, though..."

    show hisao_disappoint at centersit with charachange
    hide hisao_smile at centersit

    hi "I guess there's not much point to that sort of thing when you're alone."

    mk "Didn't you have friends? You seem a pretty well-adjusted guy."

    show hisao_frown at centersit with charachange
    hide hisao_disappoint at centersit

    hi "Used to."

    "I really hate those two words. I recognise that tone all too well, too."

    "With Suzu beginning to stir, Hisao picks himself up and takes to his feet, shins and feet still wet from the creek's water."

    show hisao_frown at center with charamove
    show hisao_wtf at center with charachange
    hide hisao_frown at center

    "I get a little worried as he staggers a little, his face telling of a sharp pain. It passes in no time, but I remember seeing it once before."

    mk "You okay?"

    show hisao_blush at center with charachange
    hide hisao_wtf at center

    hi "I'm fine. Let's go."

    stop music fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve
    scene black with shorttimeskip
    play sound sfx_crickets loop

    "The house is always so quiet at night. Aside from the chirping of crickets outside and my footsteps on the floorboards, there isn't really anything around to make much noise."

    "It's not that Yamaku is loud. Quite the opposite, given that the teachers tend to be pretty strict about discipline in the dorms. There's still the occasional bit of music from the rooms around mine, though, or the chatter of some girls gossiping away a bit too noisily. Pretty sure I heard some suspicious moaning that one time, too."

    "I got used to the background noise quickly enough, but it makes the near-silence of home a bit jarring."

    "Somehow, despite my eyes only being open by a very generous interpretation of the word, I manage to notice a faint shadow against the rice paper door leading to the outside porch."

    "I wander towards the figure out of curiosity. If it's a burglar, I could probably take 'em anyway."

    scene bg farm_porch with dissolve
    play audio sfx_sliding_door
    play music music_night

    "Sliding the door open offers little surprise. Hisao sits on the edge of the porch looking up at the night sky, thinking to himself silently."

    play audio sfx_sitting

    "Turns out he's thinking so hard that he hasn't noticed me at all. It's not until I've plopped myself down beside him that he turns to see me."

    show hisao_talk_small at centersit with charaenter

    hi "Oh. Hey."

    mk "Here I was thinking I was gonna be a hero takin' down a burglar, and it turns out to be just some dork sitting outside."

    show hisao_smile at centersit with charachange
    hide hisao_talk_small at centersit

    hi "Sorry to disappoint."

    mk "Guess I'll just have to save the day some other time."

    hi "So what are you doing up so late?"

    mk "Midnight snack. Walking around all day makes you hungry."

    mk "What about you, sitting out here all by yourself?"

    show hisao_erm at centersit with charachange
    hide hisao_smile at centersit

    hi "Thinking."

    mk "You don't say."

    hi "It's just that you don't get a good view of the stars in the city. All the lights make them hard to see."

    hi "It's crazy how clear they are out here..."

    scene bg countryside_night_sky
    with dissolve

    "The stars, huh? I look up at them as he does, trying to get what about them interests him. All I see are the same stars I've always seen. Pinpricks of light in the night sky. They're pretty, I suppose, but I don't think that's what draws Hisao."

    "I get the feeling this is one of the main differences between us, besides the different ways we grew up. I only see what's in front of my eyes. The world as it is. Hisao's eyes seem to see so much more than mine do, and as we sit here looking up at the same night sky, even now I can see that childlike wonder on his face."

    hi "It's so quiet out here."

    mk "Yeah, I was just thinking that. Guessing the city would be different?"

    hi "Out in the suburbs it's fairly quiet. The nightlife around some places though is a culture all its own."

    mk "Is it all seedy and stuff like in the movies?"

    hi "If you go looking for those kinds of places, yeah, they're around. When you get that many people in one place, you start seeing some weird stuff beneath the surface."

    hi "Don't let your imagination get too wild; I walked pretty damn quickly if I ever found myself in those areas. Mainly just stayed downtown, with all the shoppers and gaming places. Lights and advertisements everywhere, crowds buzzing, music on the air from nightclubs and karaoke parlours, it's just so different to the dead of the night around here."

    mk "That sounds so cool. We should totally travel into the city over a weekend some time. Bet Yukio and Haru would have a blast."

    hi "Yeah, that'd be fun. Lots of those merchandise and manga stores for Suzu, too."

    mk "Getting nostalgic, are we?"

    hi "More... wistful, I guess."

    play audio sfx_snap

    "I click my fingers, finally realising the word I'd been searching for all day."

    mk "That's it! Wistful!"

    hi "Huh?"

    mk "When I was in my old school, I was trying to work out how I felt. You finally put words to it."

    hi "You're welcome, I guess."

    hi "That said, I feel the opposite right now. Actually, it's been like that ever since coming to Yamaku."

    hi "Every day's been full of new things. It's weird how quickly you get used to being in a school full of disabled students, but everything else feels so new. New friends and teachers, different surroundings, living alone for the first time, and all that."

    hi "And you've shown me a lot of that new stuff, as well. Roping me into the track club, dragging me out here, and yeah, I guess what sex is like as well."

    hi "Even this night sky is totally new to me, and it's thanks to you that I can be here to see it."

    scene bg farm_porch with dissolve
    show hisao_smile at centersit with dissolve

    "He turns to me with a really sweet smile. It's nice when he lets himself do that."

    hi "Thanks, Miki."

    "I reach over and scruff his hair a little. He really should get that cut a bit."

    show hisao_disappoint at centersit with charachange
    hide hisao_smile at centersit

    "Making my case for me, he tries to straighten out his hair after I remove my hand, only for that familiar misbehaving tuft to flick back up. He really is a dork."

    show hisao_erm at centersit with charachange
    hide hisao_disappoint at centersit

    "His eyes linger on me a little longer than usual, making me curious."

    mk "What's up?"

    hi "Well, about something I mentioned..."

    "I keep waiting for him to continue, but his awkwardness gets the better of him. A smile slowly spreads on my face as I begin to realise why."

    mk "Come on boy, say it."

    hi "Fine. If you don't want to do it again I'll just drop it, but..."

    mk "But..."

    show hisao_smile_teeth at centersit with charachange
    hide hisao_erm at centersit

    hi "Could you grab me something from the fridge if you're getting a snack?"

    with vpunch
    show hisao_wtf at centersit with charachange
    play audio sfx_impact

    "That son of a bitch. I lunge sideways and bring my stump around Hisao's neck, grabbing it and pulling back to lock him in a chokehold. He struggles for breath and clutches at my arm, but it's futile."

    hi "Can't... breathe... let...!"

    mk "Huh? What was that? You want a snack?"

    with hpunch
    play audio sfx_impact

    hi "Give... give..."

    mk "Give? Give me what? Come on boy, I can't hear you."

    "As Hisao's face starts to change colour, I decide I've had my fun and let go. He gasps for air as he rubs his sore throat, but it looks like I haven't done any real damage to him."

    show hisao_erm at centersit with charachange
    hide hisao_wtf at centersit

    hi "You're such a brute."

    mk "What was that, perv?"

    show hisao_smile_teeth at centersit with charachange
    hide hisao_erm at centersit

    hi "See? You already know what this is about."

    mk "Sorry, I'm just messing around. You get so keyed up about this stuff that I can't miss the opportunity to tease you, you know?"

    show hisao_disappoint at centersit with charachange
    hide hisao_smile_teeth at centersit

    "He snorts with displeasure, still rubbing his sore throat."

    mk "So, you got a rubber?"

    stop music fadeout 3.0

    show hisao_frown at centersit with charachange
    hide hisao_disappoint at centersit

    "The answer becomes obvious as his face becomes a frown. Guess it was too much to ask that he slipped one into his wallet or something. Then again, there are solutions to that problem."

    hi "Damn it..."

    mk "Since we're like this, maybe there's something you could do for me."

    hi "And that is?"

    play music music_heart

    mk "Masturbate."

    show hisao_blush at centersit with charachange
    hide hisao_frown at centersit

    "Even in the moonlit night, the red of Hisao's cheeks isn't hard to notice."

    hi "I shouldn't have asked..."

    mk "Oh come on, I've already seen your body."

    hi "That's completely different. Can't you just watch porn if you want to see a guy do it himself?"

    mk "You know porn's completely different from reality. I wanna see how a dude really does it."

    mk "Fine, how about I do myself as well? Does that sound good?"

    stop sound fadeout 2.0

    scene black

    "He moves to protest, but the words don't come out. It's a little amusing to see him to visibly ponder the question now that the scales have been tipped."

    "Eventually, he takes a long, shaky breath. It looks more like an admission of defeat than a teenager getting the chance to fool around with a girl."

    "Hisao pulls himself back off the side of the porch, both of us turning to face each other as we sit. I guess I got the advantage, with my back pressed against the wall for a backrest."

    "It's only now that I realise what I've gotten myself into. Getting another person off is one thing; you're focused on making them feel good, after all. This, however, is the sort of thing I've only ever thought of as being done in private. Of course, it'd be just the same for him."

    "For a brief moment, I try to think of this as simply watching 3D porn. It doesn't work at all."

    "With great hesitation, Hisao begins to work off his pants, followed by his underwear. With the two sitting by his side, his stick is sitting there plain to see, the tuft of hair behind it not quite hidden. His eyes move up and down, trying to look at me, but finding himself too embarrassed."

    "It'd be a lie to say that doesn't turn me on a bit. Being able to watch him do this for my benefit."

    hi "Could you not stare?"

    mk "That's kinda the point, dude."

    "He tilts his head in resigned acceptance as his hand haltingly makes its way onto his shaft."

    "With the other hand on the ground for support, he begins to move it up and down. The first thing I notice is that he doesn't bring it over the head, but only along the lower part. It also looks like a pretty firm grip he has on the thing, whereas I'd always thought it'd be way looser."

    "It's an odd atmosphere as he strokes himself, my elbow resting on my knee as I watch intently. His gaze begins to wander over my body as he goes, mentally trying to undress me as he gets more and more aroused."

    "As time goes on, the first bits of liquid start to seep out onto the head, flowing down and mixing with the motions of his hand. A slight pain from the side of my thumb makes me realise I've begun absentmindedly rubbing at it with the fingernail of my other finger."

    "Man... this really is turning me on. That mixture of arousal and shyness, the way he tries to imagine me as he pleasures himself."

    "Having had enough of enjoying this purely as an observer, I work off my shorts and underwear, spreading my legs a little to allow him a small reward."

    "I slide my hand down past my own lower hair and onto my own organs, already moistened from being able to watch him. If nothing else, at least it's been a damn enjoyable show to watch."

    "After bringing my fingers inside myself to wet them further, and enjoying the sensation enough to make a few motions before pulling them back out, I begin to work at my nub. Circling, petting, stroking this way and that with my fingertips."

    "Watching the precum continue to form on Hisao's shaft as he plays with himself, a pleasant sigh escapes my lips. Maybe it's because I was able to get off on watching him beforehand, but this isn't as weird as I thought it'd be."

    hi "Enjoying yourself?"

    mk "Sure as hell. You're really trying not to shoot too early, aren't you?"

    hi "This still feels weird to do in front of someone..."

    mk "Just go with it. Besides, you're getting to see me too."

    "I feel my muscles shiver as a small spike of pleasure runs through me. My toes curl as I keep going, the cold wood on my butt and cool breeze on the outdoor air doing little to temper my excitement."

    "As exciting as this might be, though, it isn't quite what I want. My fingers move faster and faster over the areas I most like being touched, and under normal circumstances that would be enough, but it's the thing before me that I want right now."

    "Hisao pauses as I reluctantly stop my playing and pull myself to my feet."

    hi "Hey, what are you...?"

    mk "Sssh."

    "I bring a finger to my lips, before covering my bared area with my hand and scuttling inside, closing the door behind me lest somebody see the half-naked boy. This would be a terrible time for someone else to be walking about the house."

    "Finding the room empty, much to my relief, I skitter over to my own wallet sitting on an end table near the door. Opening it with some difficulty, I only barely manage to make out what's inside of it, retrieving what I want before coming back."

    "Opening and quietly shutting the door behind me once more, I give the bewildered Hisao only a passing glance as I take a seat right before him. He looks on wordlessly, his shaft having regrettably shortened as he awkwardly cups it from modesty."

    hi "You had one? Seriously?"

    "As much as I'd like to make some quip at him, my mouth is full with the foil square gripped in my teeth. Managing to get a good tear, the top of the package obediently flicks off, letting me grab the translucent white condom inside before spitting it out."

    "My heart racing as my sense of temptation starts to get the better of me, I give him a gentle push. He gives no resistance as I move to roll the condom on his quickly expanding rod before he can protest any further, managing to do so with a couple of abortive attempts."

    "Straddling his body, I lose any sense of hesitation and I move to rip off his top."

    hi "Miki, please...!"

    "He might be offering to do it himself, or wanting to scuttle the whole thing for fear of somebody hearing us, but I'm past caring. Yanking at his clothing, it finally comes off after some force is applied to the problem. His beautiful bare chest is my reward, the line from his surgery doing little to slow my rushing hormones."

if persistent.adultmode:
    scene bg 4211 with dissolve

    "Pressing my hands against his lower stomach, I raise my knees for leverage and start to lower myself onto his rod, stopping a couple of times as I feel it bumping either side of the critical hole."

    "A long, deep sigh of euphoria rings out from the both of us as I feel it finally slide in, his thick shaft pressing against the moist, warm walls inside of me. Even through the condom the parts of his penis can be felt out, from the top of its head to its very base."

    "I really do like this position. Looking down at him shows a flustered face, sweaty and dazed as he looks up at me and my body. I have total control over him now, and over my own pleasure."

    "Without further ado, I begin to move my hips up and down, the feeling of penetration made all the better thanks to my knees being the air. My breasts move about as I do, the tank top providing little support for them."

    "We both do out best to keep the noise down, given our situation. I manage pretty well, I think, keeping my wits about me despite the usual huffs and puffs of being the one doing the work."

    "Hisao, as seems to usually be the case, is somewhat less controlled. It gives me a chance to get back at him."

    mk "You look like you're enjoying this."

    hi "I don't think... I can't..."

    mk "Settle down, boy. You just need... to go with it."

    "The words do little to calm him as my hips continue thrusting up and down, his crotch no doubt a mess from our combined fluids. I can feel my muscles starting to tighten slightly as I try to control my feelings as best I can, but as this goes on, that becomes increasingly difficult."

    "He really is quite a looker with his clothes off. That heaving chest of his, a thin sheen of sweat now covering it, looks nicer than ever."

    mk "Nnnnn... Hisao..."

    hi "Please, I can't..."

    "From the tone of his voice, this isn't going to last much longer. I keep moving regardless, the euphoria running through every inch of my body telling me to drive onward."

    "The look on his face as he clenches his teeth, holding on for dear life to try and keep this going just a few moments longer makes me even more excited. Harder and harder he tries, teetering on the edge as he desperately attempts to hold on."

    "More... I want more of him. Hold on boy, I just want that little bit more..."

    hi "Ahn...!"

    "His mouth opens wide as the rush of climax surges through him like a lightning bolt, his pelvis hitting so hard against my own that it almost hurts."

    "Once, twice, three times his hips jerk upward as intense muscles spasms grip him, eyes open wide as he orgasms. His entire body shakes and shivers as it grasps every little bit of the intense pleasure running through him."

    "And then... it's over. His hips sink back down to the wooden boards for the last time, rod still twitching away as his mouth hangs open and gasps for air. His eyes look dreamy and unfocused, the rush of hormones still leaving their mark."

    scene black

    "Knowing that I've had my fun for tonight, I slip myself off his slowly dwindling rod. The experience has take its toll on me just as much as it has on him, leaving me flat on my back and gasping for air too."

    "The two of us must look like dying fish right now, both lying on the porch with heaving bodies, our open mouths gulping for air."

    hi "You're crazy."

    mk "I was just... turned on..."

    hi "I can't believe... you hid that you had one..."

    mk "You never... asked..."

    "He raises his hand, probably to try and make an obscene gesture at me or something, but lets it flop back to the ground as he finds himself unable to muster the energy."

    scene bg countryside_night_sky
    with dissolve

    "With my senses returning to me, I let my head roll to the side. The stars that Hisao had been so wrapped in sit above us, twinkling away."

    #show hisao_erm with dissolve

    "Realising that I've stopped panting, Hisao looks to me, and then to the same stars that I watch."

    mk "You know..."

    hi "Yeah?"

    mk "They're just stars, man."

    scene bg farm_porch with dissolve

    show hisao_topless_smile with dissolve

    "Despite my expecting some joke or teasing remark, Hisao just smiles."

    hi "I know."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

else:
    scene bg doggo with dissolve

    "Pressing my hands against his lower stomach, I raise my knees for leverage and start to lower myself onto his rod, stopping a couple of times as I feel it bumping either side of the critical hole."

    "A long, deep sigh of euphoria rings out from the both of us as I feel it finally slide in, his thick shaft pressing against the moist, warm walls inside of me. Even through the condom the parts of his penis can be felt out, from the top of its head to its very base."

    "I really do like this position. Looking down at him shows a flustered face, sweaty and dazed as he looks up at me and my body. I have total control over him now, and over my own pleasure."

    "Without further ado, I begin to move my hips up and down, the feeling of penetration made all the better thanks to my knees being the air. My breasts move about as I do, the tank top providing little support for them."

    "We both do out best to keep the noise down, given our situation. I manage pretty well, I think, keeping my wits about me despite the usual huffs and puffs of being the one doing the work."

    "Hisao, as seems to usually be the case, is somewhat less controlled. It gives me a chance to get back at him."

    mk "You look like you're enjoying this."

    hi "I don't think... I can't..."

    mk "Settle down, boy. You just need... to go with it."

    "The words do little to calm him as my hips continue thrusting up and down, his crotch no doubt a mess from our combined fluids. I can feel my muscles starting to tighten slightly as I try to control my feelings as best I can, but as this goes on, that becomes increasingly difficult."

    "He really is quite a looker with his clothes off. That heaving chest of his, a thin sheen of sweat now covering it, looks nicer than ever."

    mk "Nnnnn... Hisao..."

    hi "Please, I can't..."

    "From the tone of his voice, this isn't going to last much longer. I keep moving regardless, the euphoria running through every inch of my body telling me to drive onward."

    "The look on his face as he clenches his teeth, holding on for dear life to try and keep this going just a few moments longer makes me even more excited. Harder and harder he tries, teetering on the edge as he desperately attempts to hold on."

    "More... I want more of him. Hold on boy, I just want that little bit more..."

    hi "Ahn...!"

    "His mouth opens wide as the rush of climax surges through him like a lightning bolt, his pelvis hitting so hard against my own that it almost hurts."

    "Once, twice, three times his hips jerk upward as intense muscles spasms grip him, eyes open wide as he orgasms. His entire body shakes and shivers as it grasps every little bit of the intense pleasure running through him."

    "And then... it's over. His hips sink back down to the wooden boards for the last time, rod still twitching away as his mouth hangs open and gasps for air. His eyes look dreamy and unfocused, the rush of hormones still leaving their mark."

    scene black

    "Knowing that I've had my fun for tonight, I slip myself off his slowly dwindling rod. The experience has take its toll on me just as much as it has on him, leaving me flat on my back and gasping for air too."

    "The two of us must look like dying fish right now, both lying on the porch with heaving bodies, our open mouths gulping for air."

    hi "You're crazy."

    mk "I was just... turned on..."

    hi "I can't believe... you hid that you had one..."

    mk "You never... asked..."

    "He raises his hand, probably to try and make an obscene gesture at me or something, but lets it flop back to the ground as he finds himself unable to muster the energy."

    scene bg countryside_night_sky
    with dissolve

    "With my senses returning to me, I let my head roll to the side. The stars that Hisao had been so wrapped in sit above us, twinkling away."

    #show hisao_erm with dissolve

    "Realising that I've stopped panting, Hisao looks to me, and then to the same stars that I watch."

    mk "You know..."

    hi "Yeah?"

    mk "They're just stars, man."

    scene bg farm_porch with dissolve

    show hisao_topless_smile with dissolve

    "Despite my expecting some joke or teasing remark, Hisao just smiles."

    hi "I know."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_H4:

    window show
    scene bg rice with dissolve

    play music music_tranquil

    "Wiping the sweat from my brow, I look down at my handiwork for the morning. A long line of freshly-planted rice seedlings, their bright green stalks poking just above the muddy brown of the water. A muddy brown that's also covered my hand, and the well-worn overalls I'm wearing."

    "Hisao and Suzu work on their own columns, smartly planting their seedlings, taking a couple of steps back, and putting in the next. They seem to be slowly getting the hang of it by now, and Suzu's finally stopped complaining about the heat."

    "To be honest, this is a bit old. While they might be enjoying an activity they've never done before, helping out on the farm has always been a drag for me. I don't have a problem with the effort required; such mindless fatiguing work isn't that much different to a good run around the track, after all. It's more that I'm not being paid to work my ass off."

    scene bg farm_porch_day with dissolve

    "Deciding it's time for a breather, I start trudging back to the house. I can feel dad's eyes on me from the porch as I do. Sure would be nice to be some people, sitting on a chair with a beer and watching his kid and her friends do all the work."

    show dad_smirk at centersit with dissolve

    jun "Had enough already?"

    mk "Just grabbin' a drink."

    play sound sfx_can

    "He dutifully reaches back into the cooler beside him, pulling out one of the several soft drink cans inside and opening it before handing it to me. I have to admit, I wouldn't have hated him accidentally handing me one of the beer cans."

    play sound sfx_sitting

    "I sit on the side of the porch and start on my nice cool drink, but a sip reveals it to be lukewarm already. Beggars can't be choosers, I suppose."

    mk "So when's the paycheck?"

    show dad_grump at centersit with charachange
    hide dad_smirk at centersit

    jun "The paycheck is me feeding you. Doesn't grow on trees, you know."

    mk "It kinda does."

    jun "The money, not the food. Don't get smart with me, girl."

    mk "Somehow, you scolding me doesn't sound so bad these days."

    show dad_smile at centersit with charachange
    hide dad_grump at centersit

    jun "It's good to be scolding you again, too."

    jun "Sounds like you've had quite a time at Yamaku."

    "He answers my puzzled expression quickly."

    show dad_talk at centersit with charachange
    hide dad_smile at centersit

    jun "That Suzu's quite a talkative type once you get to know her."

    mk "You didn't need to interrogate her for information."

    show dad_smirk at centersit with charachange
    hide dad_talk at centersit

    jun "Well, I think we both know there's a lot you haven't told me."

    "A feel a bit sheepish at the quip. It's perfectly true, and now I'm completely up to the judgement of my dad."

    show dad_normal at centersit with charachange
    hide dad_smirk at centersit

    jun "Well, there's not much point dwelling on it. Seems you've lived quite a life since you left."

    jun "One of the things I've learned over the years, is that keeping a tight leash on someone like you would never work out. If you need me, I'm here, but I know you want to work through these things yourself."

    "That's probably the best reaction I could've hoped for. While I wouldn't say our relationship's ever been bad, I've never been the best behaved kid. He surely knows, at least in vague terms, how much of an asshole I was in Yamaku, but resisted the urge to force me back home, or threaten to do so."

    "It might've take the intervention of Suzu, but I finally managed to get myself mostly sorted out. I doubt that would've happened if he'd gone through with it."

    "Maybe life would've been a lot easier if I were more respecting of authority. It can't be helped."

    "As the both of us go quiet from thought, I bring up something I'd been meaning to ask."

    mk "I see you took down the shed."

    show dad_frown at centersit with charachange
    hide dad_normal at centersit

    jun "Didn't have much use for it after selling the tools. Too many memories, anyway."

    "He's always been more touchy about that time than I've been, and now is no different. My exact memories of the day I lost my hand have always been weirdly foggy, but I'd take that over the sense of guilt dad still has."

    "I wonder how different my life would've been if not for that ill-fated time I used his power tools. I don't blame him at all for what happened, despite what he may say."

    "Seizing on a chance to take our minds off the subject, dad nods to the two ahead of us still working away."

    show dad_talk at centersit with charachange
    hide dad_frown at centersit

    jun "Geez, they're really going for it."

    mk "Or at least trying to."

    show dad_smile at centersit with charachange
    hide dad_talk at centersit

    "The both of us give a weak smile at Suzu's valiant attempts, but her stamina really isn't up to the work. Some of her seedlings have already come out of the ground and started floating on the water, too."

    "In contrast, Hisao's practically a machine. He's thrown himself at the task with gusto, trying his best as a man in the prime of his life to live up to dad's expectations. He seems to have figured this all out pretty intuitively."

    mk "So what do you make of 'em?"

    jun "They're a good couple of kids, even if they are a bit dainty."

    show dad_smirk at centersit with charachange
    hide dad_smile at centersit

    jun "Still the last kind o' people I'd imagine you to end up with, though."

    mk "Yeah, life can be funny sometimes."

    mk "Sorry for not sticking around on the farm. And for being a pain in the ass in general."

    mk "Guess I'm not really the son you wanted, huh?"

    show dad_laugh at centersit with charachange
    hide dad_smirk at centersit

    jun "Bah, what're you sayin'?"

    jun "You got nothin' to be sorry for, girl. I know it took me too long, but I know you've got your own life to live."

    "I feel his hand come down on the top of my head, giving my hair a good rub. It feels weird, after so long without having physical affection. Trying to complain ends up useless, the words catching in my throat."

    "There's little point in denying he'd like me to follow in his footsteps, and I still do think he'd have preferred to have son to a daughter. That said, the fact he accepts that I'm moving along my own path relieves me. I'd harboured that seed of doubt in the back of my head for so long, and now I can finally let it go."

    stop music fadeout 1.0

    show dad_frown at centersit with charachange
    hide dad_laugh at centersit

    jun "Hmm?"

    play music music_tragic

    "Pulled from my thoughts, I follow dad's gaze out into the fields. Suzu still keeps planting away, but Hisao stands slightly hunched over."

    show dad_frown at center with charamove
    #hide dad_frown at centersit

    "Whether there's a problem or if he's just tired out is answered as he staggers forwards a couple of steps, both dad and I standing up to get a better view of what's going on. My heart stops as a leg falls out from under him, his body collapsing sideways into the paddy."

    play sound sfx_running
    with Pause(0.0)

    stop sound fadeout 4.0

    ##dad disappears instead of moving off the screen. Check & correct.

    hide dad_frown with moveoutright
    scene black with dissolve

    "Dad quickly takes off towards him, little care given to suiting up in overalls as he tramples the planted rice along the way. He can move damn fast when he wants to, my role in the affair being reduced to a mere spectator as Suzu also tries to lumber through the thick mud to the fallen boy."

    "Helped up by dad, Hisao brings an arm over his shoulder for support. The two slowly struggle back towards the house, a deeply concerned Suzu in tow."

    "I feel terrible for not thinking of this. He was obviously pushing himself hard, and the sun's been beating down on us the entire time. As much as he may not want to admit it, Hisao can't exert himself as much as someone else might."

    jun "Miki, get the phone. The ambulance'll be faster than the truck."

    hi "It's fine, please..."

    mk "You don't look fine."

    hi "It's happened before. I just... need some rest."

    "Dad and I look to each other, unsure of whether to trust him. Given that Hisao's the one with the condition, I just give a shrug."

    jun "Alright. Let's just get you inside for now."

    stop music fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve
    scene bg farm_interior2 with shorttimeskip
    show suzu_unhappy_d at centersit with dissolve

    play music music_caged_heart

    "The fracas of earlier is finally over, with Hisao's pain having passed. An air of uncertainty still lingers though, as I'm pretty sure nobody is really convinced by Hisao's assurances that everything is fine now."

    "With noon approaching and nobody having the stomach for returning to the fields, Suzu and I sit at the low table in preparation for lunch. Given what's on the menu, the reason for Suzu's fidgeting is obvious."

    "Fresh chicken, and actually fresh unlike the crap in the supermarkets. I've seen it all before, but while I didn't expect Suzu to have the stomach to observe, I'm rather impressed that Hisao went with dad to see the process. I do wonder how much of that was trying to regain his manly pride, though."

    mk "You okay?"

    suz "I can't stop thinking about that poor chicken."

    mk "What do you think happens to all the chickens you've eaten before now? Least they're happier on a little farm like this."

    suz "While they're alive."

    mk "Just don't go vegetarian on me."

    play sound sfx_sliding_door

    "My efforts to help her seem to be going nowhere, making me almost thankful for the sound of the door sliding open."

    show hisao_pale at right with moveinright

    "Turning to see who's come through, my smile instantly turns upside down. Hisao's eyes are sunken back, his expression morbid and complexion a ghostly pale. You could be forgiven for thinking he'd just witnessed a murder."

    show hisao_pale at rightsit with charamove

    hi "I should not have watched that."

    "The monotone statement is all that need be said, the boy coming to our table and sitting more like a robot than a human. I feel a little sorry for him."

    "All I can do is scratch my head as I try to work out what to say. It's not that I don't understand how they feel - it's natural to become insulated from the reality of slaughter when the word 'meat' means a shrink-wrapped package from a deli. I've yet to meet a farmer who enjoys the process, either."

    "I guess it's at least a reality check for them. Life on a farm isn't all frolicking about in the wilderness."

    show dad_normal at leftoff with moveinleft

    "After some time, dad eventually arrives with a large plate in his hands. Hisao and Suzu couldn't look less excised to eat, with the thought of one of them hurling at the sight of chicken passing my mind."

    stop music fadeout 1.0

    play sound sfx_tray_rattling
    show suzu_happy_d at centersit
    hide suzu_unhappy_d at centersit
    show hisao_smile at rightsit
    hide hisao_pale at rightsit
    with charachange

    play music music_ease fadein 3.0

    "As he lowers the plate onto the table, the relief that washes over all of us is palpable. Rice bowls, assorted vegetables, and some fish. Practically a repeat of breakfast, but he's likely scrounged it up in a hurry."

    mk "You're just gonna waste that meat?"

    show dad_talk at leftoff with charachange
    hide dad_normal at leftoff

    jun "It'll keep. We can have it sometime later."

    show suzu_concerned_d at centersit with charachange
    hide suzu_happy_d at centersit

    suz "Sorry to make you go through all this trouble."

    jun "Bah, it's nothing."

    show dad_talk at leftsit with charamove

    "He quickly waves off Suzu's concern as he takes a seat, grabbing his set of food from the platter."

    jun "Go on, eat. Kids your age need all the food you can get."

    "Hisao manages to force a bite down after taking his food, followed by more in quick succession as his appetite returns. I have no such reluctance, taking my chopsticks in hand and starting on my fish without any reluctance."

    "I guess you can take a city boy out of the city, but you can't make him into a country boy so quickly."

    jun "By the way, there was one other thing."

    show hisao_erm at rightsit with charachange
    hide hisao_smile at rightsit

    "Suzu and Hisao look to each other with concern."

    show dad_smile at leftsit with charachange
    hide dad_talk at leftsit

    jun "After all the work you did in the fields, I thought that maybe we could hit the baths."

    mk "Awesome!"

    show hisao_smile at rightsit with charachange
    hide hisao_erm at rightsit

    "Suzu seems nonplussed by the offer, but Hisao looks mightily interested. Today's looking up after all."

    stop music fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve
    scene bg onsen with shorttimeskip
    show steam

    play music music_comfort

    mk "Aaah... This is heaven."

    "I lean back against the wooden skirting with my elbows resting behind me, taking in the warmth of the water. Every pore of my body soaks in the heat of the bath and steam in the air. It's been way too long since I had the opportunity to do this."

    "Water flows in via a wooden pipe mounted just a little above the water line, giving a nice ambient sound. That, and the open doors revealing a faintly moonlit sky outside, make for a relaxing atmosphere."

    show suzu_beach_annoyed at centersit with charaenter

    "The girl sitting next to me doesn't seem so pleased, her eyes closed as she sits next to me. Suzu always acts awkwardly in changing rooms and such, so I guess she's got a thing about being naked. Don't know why; she has a perfectly cute body down there, and the petite look's pretty in these days."

    "I gently poke her cheek with my stump to make sure she hasn't fallen asleep on me."

    show suzu_beach_normal at centersit with charamove
    hide suzu_beach_annoyed at centersit

    suz "I'm awake."

    "And there's my answer. She might open her eyes, but she still stares at the ceiling instead of looking at me."

    mk "You know, I never asked what you think of all this."

    suz "About the town?"

    mk "Yeah. Hisao's enjoying himself, but I can't get a read on you."

    suz "It's a living."

    mk "Guess as long as you have an internet connection you're fine, right?"

    suz "You catch on quickly."

    suz "Hisao sure seems to be enjoying himself. Health aside."

    mk "He's more adaptable than he looks. Sure was a surprise when he shot up that tree, eh?"

    suz "At least you didn't bring along the others from the track club."

    mk "Hey, they're not that bad."

    show suzu_beach_small_em at centersit with charamove
    hide suzu_beach_normal at centersit

    suz "And yet, the only one you brought along was Hisao."

    mk "And?"

    show suzu_beach_angry at centersit with charachange
    hide suzu_beach_small_em at centersit

    suz "You can be so stupid sometimes."

    suz "I'll say it straight: you're interested in him, aren't you?"

    "The question leaves me momentarily speechless, my body sinking into the bath a bit as I try to pin down my feelings."

    "If she puts things that way, it does look pretty suspicious. Hisao's a cool guy to hang out with, and his personality has become more interesting since I first met him. It's a little nice to look back and see that."

    "But going out with him? I've never felt romantically attracted to anyone in the past, so I'm not sure how I'm supposed to work out if I'm falling for the guy or not. Relationships seem so constricting that I'm not sure I want to be in one in the first place. This untethered life has its advantages."

    "I wonder if that's how he sees things, though. Now that I think about it, I never took his feelings into account."

    mk "That sure is a gnarly question..."

    show suzu_beach_surprised at centersit with charamove
    hide suzu_beach_angry at centersit

    "Suzu looks genuinely surprised that I'm mulling it over. She probably got some idea that I'd fallen for him in her head, and been running with it for a while now. It's only now that I realise she may have an ulterior motive in asking."

    mk "Wait, are you?"

    show suzu_beach_annoyed at centersit with charachange
    hide suzu_beach_surprised at centersit

    suz "He's a friend. Nothing more."

    "She gets points for making herself clear, at least. It's too bad; I would have thought him to be just her type."

    mk "I just brought him here because I thought he might enjoy it. When he said he didn't have any friends back home to spend the time with, I guess I could..."

    mk "Damn it, what's the word...?"

    show suzu_beach_small_em at centersit with charamove
    hide suzu_beach_annoyed at centersit

    suz "Empathise with him?"

    mk "Yeah, that's it! I could understand how that'd feel, so I let him hang with us."

    suz "So that's why most of this trip we've been on a tour of your childhood."

    "So now we finally get to the heart of the topic. She thinks I've been showing Hisao my past out of affection."

    "I guess I have been somewhat selfish in how I've been dragging them around with me wherever I wanted to go."

    show suzu_beach_normal at centersit with charamove
    hide suzu_beach_small_em at centersit

    suz "Don't worry about me or Hisao. If you have past debts to settle, go ahead and deal with them."

    mk "You make it sound like I have baggage."

    suz "Not a person alive who doesn't."

    "I guess that makes one person in the world who knows the carefree life I live in Yamaku isn't completely truthful. Even I thought I had my shit together, but it turns out life isn't always so simple."

    mk "Thanks. Suzu. I probably don't say this enough, but I'm glad to have you around."

    "I wait for a reply, but the only sound to be heard is water trickling in."

    "I give Suzu another bump on the cheek with my stump, but this time, no reaction is forthcoming."

    "Well, I guess staying in for a few more minutes wouldn't hurt."

    stop music fadeout 1.0

    hide steam with dissolve

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_H5:

    scene bg pitch with dissolve

    window show

    play sound sfx_cicadas loop

    play music music_painful

    ##maybe just have cicada sounds here and no music?

    "A gentle breeze flows through my hair as I stand where I'd spent so much of my childhood."

    "It's a sorry excuse for a baseball pitch, I suppose. Not much more than a disused field near the school, covered in dirt and tan gravel. The only sign of what it was ever used for are the barely visible white lines on the ground, and a couple of benches to the side."

    "The batting stance is still second nature after all these years, a reasonably straight branch serving as a makeshift bat as I prepare for the pitch. The beat-up pitching machine before me stands silent, ready to spit a ball at me at any second."

    "A heavy clunk sends the entire machine shuddering on its legs, the ball sent flying towards me at a relatively easy speed."

    play audio sfx_bat_hit
    with vpunch

    "The familiar feeling of impact flows through my arm, my entire body twisting as I give a good, solid hit."

    "The ball flies up, arcing into the sky..."

    "...Before giving up, pathetically dropping back down near second base. It gives a soft thud as it hits the ground, all energy lost as it barely even rolls before coming to a halt."

    "Worthless. Utterly shit. I knew I shouldn't have tried."

    play audio sfx_twig_snap

    "Infuriated, I slam the stick against the ground, breaking it in half without even trying. The spike of adrenaline in my system spurs me into flinging the half still in my hand into the air in a rage, sending it flying far further than the ball ever got."

    play audio sfx_kick_machine

    "Far from satisfied, I walk over to the pitching machine and give it a strong kick. the old thing falls to the ground with a loud clatter, but I'm sure it still works just fine. It's managed to survive so damn long that I probably couldn't kill it no matter how much I abused the thing."

    "The destruction at least lets me vent off a bit of steam, leaving me standing around frustrated and empty-handed."

    play audio sfx_impact

    "For lack of anything else to do, I give up and let myself fall back onto the ground with a thud. It hurts a bit to land on the gravel, but I don't care."

    scene bg misc_sky
    with dissolve

    "This is why being left to myself is always trouble; my mind wanders into troublesome places. Looking at the impossibly vast blue sky above, I'm left to wonder what I really expected from coming out here."

    "Baseball's supposed to be played with both hands still attached to their wrists, after all. It's pathetic - I can't even get a clean hit past the bases, let alone aim in any meaningful way. It's obvious time wouldn't change that, but something in my head kept whispering to me. Urging me to try just once, for old time's sake."

    "I guess that part of my head can shut up, now."

    "As I stare up at the sky, a face cast in shadow looms over me."

    show hisao_smile with dissolve

    hi "Hey."

    mk "'Sup. What're you doing here?"

    hi "Just wanted to see what you were up to, after how you disappeared."

    mk "Suzu with you?"

    hi "Nah, she's napping. At least, she was when I left."

    "I wonder how much he saw. Then again, it doesn't really matter. Being at a baseball field is plenty enough to understand, much less the pitching machine lying near me."

    "Hisao briefly looks up to see what I was staring at."

    show hisao_erm with charachange
    hide hisao_smile

    hi "That sure is a sky."

    mk "Smartass."

    mk "...Did you take dad's bike up here?"

    show hisao_talk_small with charachange
    hide hisao_erm

    hi "Yeah. Why?"

    mk "You sure you're okay to bike this far? After yesterday and all."

    show hisao_disappoint with charachange
    hide hisao_talk_small

    hi "I'm fine, don't worry about it."

    "Hisao steps back, the tone of his voice telling me that I've hit a landmine. He really doesn't like talking about his heart condition."

    scene bg pitch with dissolve
    show hisao_disappoint with dissolve

    play audio sfx_rustling

    "I pull myself to my feet in response, dusting off my hair and the back of my shirt afterwards."

    mk "You don't need to be like that. Everyone's got their share of problems to deal with, you know."

    play audio sfx_rumble

    "My stomach chooses now of all times to growl loudly. Farting around at midday may have been a mistake. Hisao just grimaces."

    show hisao_hmpf with charachange
    hide hisao_disappoint

    hi "You don't say."

    stop sound fadeout 0.3

    stop music fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve
    scene bg sobarestaurant with shorttimeskip
    show hisao_erm at centersit with charaenter

    play music music_raindrops

    "While some things might be the same, there are a few oddities that have popped up since I left. This place is one of them."

    "It's the kind of eatery that wants to be a restaurant, but can't help feeling more like a cafe. While the owner seems to be making a genuine effort at making their dream come true in owning their own little restaurant, their budget - and likely their customer base - is lacking."

    "But the food is what counts, and as the owner places a bowl of tempura soba before each of us, the smell is enough to know this is going to be good."

    "I split my chopsticks and grab at the tempura, taking a good chunk out of it as the noodles steam away. Hisao, on the other hand, simply blows on his bowl with the tempura still in it."

    mk "C'mon man, what're you doing?"

    hi "What do you mean?"

    mk "You're just gonna let it get all soggy?"

    show hisao_declare at centersit with charachange
    hide hisao_erm at centersit

    hi "It's called 'letting it soak in the broth'. It tastes better."

    mk "'Making a soggy mess in your noodles', more like."

    show hisao_erm at centersit with charachange
    hide hisao_declare at centersit

    "He just shrugs before idly looking about while his meal cools."

    hi "You know, there is something I've noticed about this town."

    mk "Yeah?"

    "I lean in, interested to hear his views on it."

    show hisao_smile_teeth at centersit with charachange
    hide hisao_erm at centersit

    hi "I think saying it's a town is being too generous. It's definitely a village."

    mk "Come on, really?"

    show hisao_talk_small at centersit with charachange
    hide hisao_smile_teeth at centersit

    hi "The 'town centre' you wanted to show us before is one street!"

    mk "So?"

    show hisao_talk_big at centersit with charachange
    hide hisao_talk_small at centersit

    hi "A small street! I can count the number of shops on one hand!"

    mk "Alright, fine, geez. We can't all come from the big smoke."

    mk "Still a town."

    show hisao_heh at centersit with charachange
    hide hisao_talk_big at centersit

    "He just snorts as I mumble a last rebuke."

    show hisao_erm at centersit with charachange
    hide hisao_heh at centersit

    hi "So why were you playing Godzilla in the baseball field, anyway?"

    "And there it is. I guess I should've paid more attention to my surroundings before losing my temper."

    "The two of us are briefly distracted by an impromptu visitor, with a dishevelled stray cat strolling past us as if it owned the place. It eventually hops up onto the sill of an open window, flicking its tail for a few moments before hopping down."

    show hisao_smile at centersit with charachange
    hide hisao_erm at centersit

    "Hisao just smiles, which at least lightens my own mood a little."

    mk "I guess I just couldn't admit that it was over."

    hi "I had no idea you were so into baseball. Were you good?"

    mk "Boy, I was the cleanup hitter. Slammed that thing harder than any of 'em could."

    hi "You must've been pretty talented."

    mk "'Talent' is how lazy people justify being bad at something."

    mk "I worked my god damn ass off to get that good. I lived and breathed baseball. Followed the leagues, had my favourite players, watched it on the little television even when the reception was shit. I put blood, sweat, and tears into it, all to run for the base just a second or so quicker, and hit the ball just that few more yards."

    mk "It was my thing, you know? I had purpose. I could always aim to be that little bit better every day. I never felt lost in life, because I could see the path ahead so clearly. I was going to devote myself to becoming the best there was, whether I was a boy or a girl."

    mk "And then... the accident happened."

    show hisao_frown at centersit with charachange
    hide hisao_smile at centersit

    hi "That must've been hard."

    show hisao_erm at centersit with charachange
    hide hisao_frown at centersit

    "I just shrug, making him lift a brow."

    mk "It's kind of weird. Losing my hand in itself was a pain the ass, of course. Found the physical therapy easier than most do, but that isn't really saying much."

    mk "But the hardest thing to accept, was that I'd reached my peak. I'd reached the top of my personal Everest, and could only ever see lower mountains before me. My life would be all downhill from there."

    mk "What do you do after you've reached the top, Hisao? In all these years, I've never found an answer."

    mk "Sorry. I'm using you as a scratching post, aren't I?"

    show hisao_disappoint at centersit with charachange
    hide hisao_erm at centersit

    hi "If I had an answer for that, I'd tell you. I'd sure like to know that myself."

    mk "...Hisao?"

    show hisao_disappoint at center with charamove

    "He gets up from his chair, his meal finished save for some broth left sitting in the bowl."

    hi "Let's go. I'm sure the others are waiting for us to get back."

    stop music fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve
    scene bg farm_interior2 with shorttimeskip

    play music music_fripperies

    "As soon as we walk in the door, bikes left propped against the wall, I can hear the voices of Suzu and dad from the living room. Wondering what they'd have to talk about, Hisao and I head towards the source."

    show dad_smile at leftsit
    show suzu_normal_d at centersit
    with dissolve

    "I groan the moment he slides open the door. The two sit at the table with an old leather-bound album opened in its centre, Suzu peering over to see this photo and that."

    mk "Do you have to show them that...?"

    jun "I don't get to do this often, you know."

    show hisao_erm at right with moveinright
    show hisao_erm at rightsit with charamove

    "Resigned to my fate, I follow Hisao to the table. Everyone crowds around to get the best view as dad sits to the side."

    "Having progressed past the baby photos and elementary school, it sits at the years I was in junior high. A school photo takes up most of the page, with a few elementary students sitting on chairs as about fourteen junior high schoolers - me included - stand behind them in our summer uniforms."

    suz "I like the outfit."

    "She points to the back row, the girls clad in our black-trimmed white sailor tops and long black skirts, and the boys in their smart white shirts. I don't mind the look, though they tended to get dirty pretty fast."

    show suzu_speak_d at centersit with charachange
    hide suzu_normal_d at centersit

    suz "Was this seriously the whole school?"

    show dad_normal at leftsit with charachange
    hide dad_smile at leftsit

    jun "Sure was. One class for elementary students, another for junior high. The teachers were good folks, despite whatever Miki's said."

    show suzu_neutral_d at centersit with charamove
    hide suzu_speak_d at centersit
    show hisao_smile at rightsit with charachange
    hide hisao_erm at rightsit

    hi "That's you, isn't it?"

    "He points to a girl in the back row, grinning away happily."

    mk "How'd you know?"

    show dad_unhappy at leftsit with charachange
    hide dad_normal at leftsit

    "Dad chuckles as he turns the page, but the corner of his mouth tugs downwards upon catching sight of the next photo."

    "Ten boys and a girl, all of us dressed in identical pinstripe baseball outfits. A lot less formal than the classroom photo, some have arms around those next to them, while others pull faces. One of my better friends at the time grabs me in close around my neck as I hold my trusty bat over my shoulder. Our ponytailed coach simply stands by us, smiling with pride at the team he worked so hard to raise."

    "Every one of us was a friend to each other. We had fights of course, as friends sometimes do. As we got older, those fights sometimes ended up with real injuries, too. Given a focus for our youthful energy, we all poured ourselves into the sport, trying to be the best junior team there was."

    "The last few months of my life here saw that wonderful life crumble before my eyes."

    show hisao_disappoint at rightsit with charachange
    hide hisao_smile at rightsit

    "I notice Hisao looking sidelong at me. Without knowing quite how to react, I just look away."

    suz "So this is the baseball club you were in."

    show suzu_speak_d at centersit with charamove
    hide suzu_neutral_d at centersit

    suz "Wait, you were the only girl?"

    mk "Yeah. Why?"

    suz "A lot of things about you suddenly made a lot of sense..."

    show hisao_erm at rightsit with charachange
    hide hisao_disappoint at rightsit

    hi "It's kind of hard to even recognise you, given you're all wearing the same stuff."

    mk "Puberty sure took a whack at me didn't it?"

    "Hisao's constant attempts to be tactful make it all too tempting to tease him."

    show suzu_concerned_d at centersit with charachange
    hide suzu_speak_d at centersit

    suz "What happened to them? Are they still around?"

    show dad_talk at leftsit with charachange
    hide dad_unhappy at leftsit

    jun "They left for the city. Happens a lot, these days."

    hi "I heard about that. Lots of rural places having problems with the younger generations moving out, without people replacing them."

    jun "That's exactly it. The way I see it, there's not much of a future in places like this."

    suz "That must be frustrating."

    jun "Frustrating? Nah. Some of the older folks 'round here have Opinions when it comes to today's kids, but I don't hold it against 'em."

    jun "You two would know better than most how inviting city life must be. 'Convenient' was the word they used when they described it after leaving."

    suz "But still, this is your home."

    jun "It might be a home, but it's also a business. Gotta make money to live, after all."

    jun "When you're up against those gigantic agriculture corporations, little family farms like this one don't stand much of a chance. It's the same story for all the farms here, whether the old coots admit it or not."

    jun "While it used to be a vibrant, lively place, I can't help but feel the town's not much more than a museum piece these days. Don't know if it'll take years or decades, but eventually this way of life just isn't going to exist anymore."

    show suzu_unhappy_d at centersit with charachange
    hide suzu_concerned_d at centersit

    suz "I'm sorry for bringing it up."

    jun "Don't be. Change happens, I know that. Ain't a good thing or a bad one. It's just the way things go."

    stop music fadeout 8.0

    show dad_unhappy at leftsit
    hide dad_talk at leftsit

    jun "But even so... I guess it does feel a little bit sad."

    "Hisao and Suzu appear to take him at his word, but I know something else lies behind those tired eyes. A wound that never truly healed."

    "With that, he solemnly closes the album."

    ##centered "~ Timeskip ~" with dissolve
    scene bg farm_porch with shorttimeskip

    play music music_comfort

    "Once again, I find myself sitting on the porch in the cool night time air. I suppose it's natural to want some time alone when surrounded by people the entire day, even if it does mean getting less sleep."

    "I look down at the photo held in my lap once more. Eleven happy kids, beaming at the camera. A girl with a bat, and a toothy smile."

    hi "You're up late."

    show hisao_smile with dissolve
    show hisao_smile at centersit with charamove

    play sound sfx_sitting

    "He takes a seat beside me, plopping himself down with a grunt. My first instinct is to hide the photo, but the question of where I possibly could puts a stop to that."

    mk "Become a bit of a nightly rendezvous, huh?"

    hi "Purely by accident, I swear."

    mk "You're not just feeling randy again?"

    show hisao_closed at centersit with charachange
    hide hisao_smile at centersit

    hi "So this is what I get for being worried about you. That's harsh."

    "We both chuckle, though it ends as Hisao looks down at the picture in my hand. I doubt he picked up on dad's feelings, but my moaning beforehand probably stuck with him."

    show hisao_erm at centersit with charachange
    hide hisao_closed at centersit

    hi "It's a nice photo."

    hi "You know, I was surprised not to see more baseball stuff around your house when I arrived."

    mk "Not much reason to keep that stuff. It only ever reminded me of what I lost, so I threw it all away."

    "I hold the photo up a little."

    mk "You know... I tried to get rid of this, too. I scavenged a cigarette lighter, and had the photo right there."

    mk "I just hated it. It was the last record of everything that was taken away from me; my friends, my hobby, my dreams."

    mk "I wanted to get rid of it so much, but..."

    show hisao_smile at centersit with charachange
    hide hisao_erm at centersit

    hi "...it's hard to truly let go."

    "With the words stolen from my mouth, I silently look to the boy sitting next to me. He looks like an old man, the weary smile on his face making my heart sting a little."

    mk "You..."

    show hisao_erm at centersit with charachange
    hide hisao_smile at centersit

    hi "The letter you saw, from Iwanako?"

    hi "I couldn't bring myself to throw it out. Scrunched it up and threw it into the bin, but I ended up just digging it back out."

    mk "But she broke up with you. What's the point in keeping something like that?"

    hi "Because it proves those times existed. Just because she broke up with me, it doesn't mean the times we had before that went away."

    hi "It's not just her, either. Ever since I saw the nostalgia on your face, I guess I felt sort of the same thing as I thought back to my childhood."

    hi "I know it's not the same as baseball was to you, but I never appreciated how much soccer practice meant to me until I lost it. Just getting together with friends every week to kick a ball around. It sounds so trivial, doesn't it?"

    show hisao_closed at centersit with charachange
    hide hisao_erm at centersit

    "He leans back and closes his eyes, his mind obviously in another place."

    hi "Messing around at arcades with friends. Gazing at cute girls. Sneaking peeks at dirty magazines in convenience stores. Riding bikes around the city. Covertly exchanging notes with friends during class. Hoping for a good mark as each new test rolled around."

    show hisao_frown at centersit with charachange
    hide hisao_closed at centersit

    hi "And then sitting alone in a hospital bed, smelling bleach and staring at four sterile white walls."

    mk "What happened to them? Your friends, that is."

    show hisao_talk_small at centersit with charachange
    hide hisao_frown at centersit

    hi "They visited damn near every day at first, All of us chatting away as they kept me up to date on what was happening at school and at soccer."

    hi "Then it became once every few days. Then once a week. As time went on, we stopped talking so much. None of us outright said it, but it was pretty obvious I was moving further and further from my circle of friends. They were living lives full of new experiences every day, while I just saw the occasional new patient wheeled into the room every so often."

    hi "Then finally, one day... they stopped coming at all."

    hi "I guess they got bored of me."

    mk "How can you say that so easily?"

    show hisao_erm at centersit with charachange
    hide hisao_talk_small at centersit

    hi "Hmm... probably because I knew it was coming. It was the same for Iwanako, as well. A long, slow fade to nothing, rather than any kind of dramatic breakup."

    hi "I suppose that's why I couldn't throw out that letter. It'd be easy to say my life got reset when I started at Yamaku, but that'd be a lie."

    hi "I lived. It was a good life, too. Even if I can't return to those times any more, I think I want to remember them."

    mk "And that's what you wanted to say to me before."

    show hisao_smile at centersit with charachange
    hide hisao_erm at centersit

    hi "Pretty much. I just wanted to let you know that you're not alone. I kinda get what you're going through."

    "I did come here to show Hisao and Suzu what country life was like, but in the process, I got completely distracted by the relics of my old life. Here I was thinking about myself, while Hisao was there going through all the same shit."

    "Only now do I realise what made me notice him in the first place after he transferred in. That feeling of connection, of sharing something, that was always in the background."

    "'You're not alone'. Those three words are enough to make a lump form in my throat. I take a deep breath to try and steady myself."

    mk "Man... what the hell?"

    mk "I thought I had all my shit together, and then you go and drop that on me."

    "I just sigh and smile at him, clearing my thoughts as I do."

    mk "Thanks. That means a lot."

    scene bg countryside_night_sky
    with dissolve

    "He just smiles, the two of us looking up into the night sky."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_H6:

    window show
    scene bg trail with dissolve

    play sound sfx_forest loop

    play audio sfx_twig_snap

    play music music_miki fadein 5.0

    "A stick loudly snaps as I move through the undergrowth, roots and fallen branches beneath my feet, and the forest's green summertime leaves hanging overhead."

    "No less noisy as we carry ourselves up past the foothills is Hisao, walking a couple of yards behind to let me navigate the barely visible path. Each of us uses a hastily-found stick as a trekking pole, which has helped us make pretty good progress up the hill so far."

    "I'm reasonably confident that said progress has been in the right direction. Nothing more than a trail of worn ground from previous travellers, the path we follow has very nearly faded back into the bushes and leaves thanks to nobody coming through here for so long."

    "Our movement disturbs a bird who'd been resting in a low branch, annoyed chirping ringing out with a slight echo as it flutters past us."

    hi "You sure it's alright not to ask Suzu to come along?"

    mk "She's probably going to sleep for ages, and besides, can you really imagine her wanting to do this?"

    hi "...Good point."

    "The two of us continue walking, looking at this and that as we move. It doesn't look like this pace is too hard for Hisao, as he isn't showing any signs of slowing."

    "This reminds me a lot of jogging around the track at Yamaku, come to think of it. Pushing myself onwards, with a feeling of accomplishment coming from the fatigue. The humidity is also pretty nice, with the moisture in the air trapped beneath the canopy."

    mk "Say, have you ever done this before? Hiking, camping, seeing the great outdoors?"

    hi "Sure. Not really my thing, but I've done it."

    mk "Wait, really? I thought you were some super urban kind of kid."

    hi "There are these things called cars, and trains for that matter. They can take you out of the city."

    hi "Let's see... I've been around Hakone a couple of times on family trips. Nice place for relaxing in a hot spring after a day of hiking, actually. Had a flight down to Okinawa once, as well."

    mk "You've flown? That's awesome!"

    hi "It's not that unusual these days."

    mk "What's it like? C'mon, tell me."

    "Taken off guard by my enthusiasm, he struggles a little to get his words together."

    hi "That's actually kinda hard to answer."

    hi "There's a lot of waiting around, for one. Waiting in lines, waiting at the terminal, waiting at the gate, waiting for takeoff."

    hi "Then once you're in the air, you're really just sitting in a metal tube for a few hours. Your ears go all funny from the changing pressure, and your eyes dry out from the recirculated air. The food's pretty miserable, too."

    hi "And don't get me started on crying kids, or being stuck next to some chatty person for ages when you just want to watch an in-flight movie or look out the window."

    mk "Huh. So it's not all that great, then."

    hi "It's incredibly cool. Despite all that, it still manages to be fantastic."

    "Hisao sounds really keyed up about it. Not that I don't understand; just the idea of a massive machine lifting hundreds of people into the sky and putting them back down again blows my mind."

    mk "So you'd be up for a sixteen hour flight to the Big Apple?"

    hi "...Maybe it's not that cool."

    scene bg edge with dissolve

    "My smile drops as I remember what part of the hike we're nearing. Sure enough, the next few yards mean walking along a particularly narrow ridge running alongside a steep drop. It'd be damn near suicidal in bad weather, as you'd be a goner if you slipped."

    show hisao_erm with dissolve

    "I reflexively step back as a familiar dropping feeling inside my gut comes over me. Hisao steps alongside, putting a hand on my shoulder to steady me as he peers over. The bastard doesn't look phased by the sight at all."

    show hisao_smile_teeth with charachange
    hide hisao_erm

    hi "Maybe a plane trip wouldn't be the best idea for someone like you."

    mk "Just shut up and let me focus."

    hide hisao_smile_teeth with dissolve

    "I pull my shoulder from his grasp and force myself to continue walking, doing my best not to look down. So what if I don't like heights; it's not that uncommon, right?"

    "My legs and arms are tense as I gingerly place step after step, every bit of my mental strength focused on keeping my eyes pinned forwards. Hisao, thankfully, keeps his mouth shut and lets me take this at my own pace."

    "This is fine. I can do this. Just one foot ahead of the other."

    show bg trail2 with dissolve

    "I breathe a sigh of relief as the path winds back away from the ledge, taking a few gasps of air as I lean against the trunk of a large tree and wait for Hisao to catch up."

    show hisao_smile with dissolve

    "He flashes a smile at me once he does, the two of us continuing on."

    hide hisao_smile with dissolve

    "The slowly rising angle we have to walk up does nothing to stop the wildlife, the undergrowth around us getting thicker if anything. The odd squawk and cry from this bird or that can be heard, and the shaking of a bush here and there reminds us that we're far from alone."

    "Noticing that Hisao's footsteps have stopped, I look back to see what's holding him up. Turns out he's paused to look at a lizard sunbathing on the side of a rock."

    show hisao_blush with dissolve

    "Looking slightly embarrassed at my having noticed him, he quickly falls in behind me once more."

    show hisao_erm with charachange
    hide hisao_blush

    hi "Are you sure you know where we're going?"

    mk "How long have I lived here? Of course I know the way."

    hi "If you say so. I know I said I hiked before, but there aren't any paths at all."

    mk "There are, you just need to know where to look."

    "My confidence seems to settle him down, and if we're where I think we are, it shouldn't take long to prove my case."

    "Sure enough, in the distance I can see sunlight breaking through the line of trees. Just a little further, and we should reach the spot."

    stop music fadeout 2.0

    scene bg camp with dissolve
    show hisao_erm with dissolve

    play music music_soothing fadein 2.0

    "Emerging from the forest into the clearing, Hisao and I stop side by side to take in the sight. A couple of fallen logs stripped of their branches and laid either side of a stone campfire pit lay in the centre, with an old tire hung from a branch by a fraying rope to the side."

    "Near my feet sits a faded 'keep out' sign, the pole attached to it having come out of the ground during some storm or another. We probably didn't follow building standards all that well when we hammered it into the ground."

    "A few other bits and pieces we dragged up here to make the place feel a little more like our own lie strewn about, though most have been blown away or stolen."

    "Still, I'm kind of impressed this much is left. A little testament to our friendship, still surviving so long after we left."

    hi "I'm guessing you had a hand in this?"

    mk "Sure did. Used to be more impressive, but the fact anything's still here is a bit of a surprise."

    mk "Now do you trust that I know my way around?"

    hi "Alright, you win. Let's eat."

    show hisao_erm at centersit with charamove

    "Sound like a solid plan. Hisao goes to one log as I walk to the other, propping my trusty stick against it and undoing the zip to my backpack and rifling around for the rice balls I packed. Managing to grasp the small bag they're in with the tips of my fingers, I pull them out as I take a seat."

    "Hisao unclips the bag slung around his shoulder, lifting the flap and grabbing a bottle filled with water. I'm glad to have a chance to rest my legs, but it's Hisao I'm more worried about. Now that he's seated, that terrible wheeze he sometimes gets has returned."

    mk "Doing okay? You look pretty beat."

    show hisao_declare at centersit with charachange
    hide hisao_erm at centersit

    "He takes a big gulp of water before answering, wiping his mouth with his sleeve."

    hi "Yeah, I'm fine. Just needed a breather."

    "I almost offer if he'd prefer to turn back after we're done here, but think better of it. He'd just say we should keep going, regardless of whether he was having chest problems or not."

    "It worries me, but it also makes me admire him a little. It's easy to be all gung-ho when you're a fit person in the prime of your life, but Hisao pushes himself hard all the time despite his condition, both around here and on the track at Yamaku."

    "Maybe that's why he's such a balanced person. After all, he has a good, sensible head on his shoulders, is reasonably fit given everything that's happened to him, and is smart enough to be Mutou's pet in class. He might be a bit awkward socially, but at least he tries to be outgoing."

    "Just an all-round good kid, really. Too bad that doesn't mean shit when life decides to screw you over."

    show hisao_talk_small at centersit with charachange
    hide hisao_declare at centersit

    hi "Any good?"

    mk "Hmm?"

    hi "The rice balls."

    mk "Oh, right. Guess they're okay."

    hi "Did you make them, or what?"

    mk "Yeah. It's kinda hard to mess up rice balls, though."

    show hisao_erm at centersit with charachange
    hide hisao_talk_small at centersit

    hi "True."

    "Well, there is one thing about him I don't like; that tendency of his to so visibly think about what he wants to say. The topic of cooking's put something into his head, but he won't come out with it."

    mk "What's up?"

    hi "I was trying to put this tactfully, but I guess that's unnecessary when it comes to you."

    "I give a disarming smile at his attitude. He takes it as permission to go on."

    hi "Is your mother, uh..."

    "Oh, it's just that. I probably should have said something about it to him before it became the elephant in the room."

    "Come to think of it, I wonder how long that's been on his mind, and Suzu's for that matter. Don't tell me he's been trying to ask me about that for the entire time he's been here..."

    mk "Man, you don't need to pussyfoot around that stuff."

    mk "It's not much of a story, to be honest. My mother ditched me and dad when I was really young. About three years old, I think."

    show hisao_talk_big at centersit with charachange
    hide hisao_erm at centersit

    hi "She just left?"

    mk "Yep, up and left. Got her stuff, walked out the door, and that was the last either of us ever saw or heard of her again."

    show hisao_frown at centersit with charachange
    hide hisao_talk_big at centersit

    hi "Geez. That's rough."

    "I just shrug. It is what it is. Not like I was old enough to understand what was going on, or even to really remember the event in the first place."

    "Leaning forwards with my arm outstretched to offer some rice balls to Hisao, he takes a couple and starts grazing on them."

    show hisao_talk_small at centersit with charachange
    hide hisao_frown at centersit

    hi "Do you ever wonder where she is now? Whether you might be able to contact her somehow?"

    mk "She could be dead in a ditch for all I care. Why would I give a shit about someone who abandoned their own baby and left her husband heartbroken?"

    show hisao_frown at centersit with charachange
    hide hisao_talk_small at centersit

    "I don't have any trace of anger in my voice, but the idea obviously puts Hisao off. I don't blame him; I've long since come to accept that my situation is different to the vast majority of people out there. That's not their fault, nor mine."

    hi "You might have a half-sister or half-brother, though."

    "That's not a terrible argument, but I already know my answer."

    mk "I guess I've never put that much weight on blood ties."

    mk "Having a sister would've been kinda nice, though. A younger one, so I could dote on her and be the cool older sis."

    show hisao_disappoint at centersit with charachange
    hide hisao_frown at centersit

    hi "Yeah, I could see that."

    mk "What about you? Only child, right?"

    hi "Yeah, no sisters or brothers for me."

    hi "I dunno, I think I'm pretty okay with it. I'm good with kids, but I don't know about growing up beside one."

    mk "So you're the fatherly type, huh?"

    show hisao_erm at centersit with charachange
    hide hisao_disappoint at centersit

    hi "I could see myself with kids, yeah. Having a family would be good."

    show hisao_talk_small at centersit with charachange
    hide hisao_erm at centersit

    hi "What's with that face?"

    mk "Were you born forty years old?"

    hi "Some of us can look further into the future than the next meal, you know."

    show hisao_erm at centersit with charachange
    hide hisao_talk_small at centersit

    "I just laugh. He's not wrong, really."

    show hisao_erm at center with charamove

    "Finishing his last rice ball and putting away his bottle, Hisao clips up his bag and takes to his feet, collecting his trekking pole before walking over and offering me a hand up."

    show hisao_smile with charachange
    hide hisao_erm

    hi "Good to go?"

    mk "You know it."

    stop music fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve
    scene bg trail3 with shorttimeskip
    play sound sfx_forest loop

    "The trek takes its toll on our legs as we push ourselves along, the incline up the hill now quite severe. Not only that, but the overgrown roots sticking out of the ground and uneven rocks leading upwards force us to be careful that we don't break or twist an ankle."

    show hisao_wtf with dissolve

    "It's painful, but not all pain is bad. From the way Hisao's holding onto his waist, it looks like he's in more pain than I, having developed a stitch. Better that than a heart problem, I suppose."

    hi "How... far is it... to go?"

    mk "Stop whining, you big baby."

    hi "That's easy... for you to say."

    "Hisao pushes himself a little harder after I've scolded him, despite what he says. At least his awkwardness about being beat out physically by a girl has finally disappeared."

    hide hisao_wtf with dissolve

    "More and more rays of sunshine manage to peek through the leaves overhead, casting spots of light on the lush green bushes around us."

    "My heart is beginning to beat faster and faster, but it isn't from exhaustion. We're so nearly there. Just a little further now."

    "The look of the area's changed a fair bit from when I was last in this spot, but that's only natural given the surroundings dying off and regrowing. Something about it feels familiar, though. I can't quite put my finger on it, but it's there."

    stop sound fadeout 3.0

    "The feeling of tiredness in my muscles slowly begins to fade from my mind, as do the sounds of the birds and other wildlife. Dropping my makeshift pole, it takes some effort not to run the last of the distance, anticipation filling my body."

    scene bg village with whiteout
    ##is there like a "blinded" effect that can be used?

    play music music_pearly

    "Sunlight assaults my eyes as I emerge through the tree line, forcing me to squint heavily. As my eyes adjust, the sight before me is just as tremendous as I'd hoped."

    "I hear Hisao come up behind me, gasping wordlessly at the view."

    "From where we stand, the entire town can be seen below. The breeze brushes past us as we stand and stare, taking in the vast fields and the narrow roads between them. Old wooden farmhouses, some newly restored, others run-down from old age. The river cutting through the valley, acting as a vital artery to the entire town. Telephone poles with wires hanging loosely, running alongside the streets."

    "I can't help but give a wistful smile as I turn back to Hisao."

    show hisao_wtf with dissolve

    mk "Welcome to my home, Hisao."

    mk "My entire life is down there, you know. Where I was born, where I played and where I went to school. Where I found a dream, and had it dashed. Where I made friends, and lost friends. It might not be much, but it's mine."

    "I take a long breath to steady myself. It's not often I get emotional, but after so long, I just can't help it."

    mk "This is why I brought you here, Hisao. I did get kinda wrapped up in my own nostalgia for the place, but in the end, we managed to get here."

    "I bring my arms out wide before letting them fall back to my sides."

    mk "This is me."

    play sound sfx_impact
    show hisao_wtf at centersit with charamovefast

    "Hisao just looks wordlessly at my smiling face, before letting himself fall to the ground with a thud. Completely exhausted, he just sits with his hands on the ground behind him, looking into my eyes as he pants and sweats heavily."

    "Now that I think of it, I must look a total mess right now, too. Sweat's all over me, and I can feel a couple of hairs stuck to my face. That fact quickly becomes unimportant as I look into Hisao's eyes, suddenly noticing something different inside of them."

    hi "I can't take this anymore! You win already!"

    mk "Huh? What're you goin' on about?"

    "He pauses to take some much-needed air, before looking to me with a face full of both exhaustion and... a warmth that I've never seen him have before."

    show hisao_talk_big at centersit with charachange
    hide hisao_wtf at centersit

    hi "I love you, Miki."

    "My heart stops. No, it would be more correct to say the whole world around me stops."

    "With me taken completely by surprise, it's Hisao who fills the silence."

    hi "I've completely fallen for you. I don't know if this can go anywhere, but I can't take this any longer."

    hi "You've shown me so much, that I feel like a child seeing the world for the first time all over again. I want to keep on seeing new things, too."

    hi "And I want to see them with you, together."

    "Questions slowly begin to fill my mind. How long has he liked me? What should I say? What do I do? Should I have noticed his feelings before now? We had a good thing going with our friendship, but could we ever go back to it now?"

    "But somehow... none of those questions really seem to matter. All that I can think about, is the boy sitting before me, eyes full of weariness, hope, and love. Nobody's ever looked at me with such a face before."

    "So that's Hisao's judgement, after seeing all this. I showed him everything, and what he felt from that, was love."

    show hisao_blush at centersit with charachange
    hide hisao_talk_big at centersit

    "It's kinda funny. So much so that I start laughing. I don't really know why it's funny at all, but it just so seems inexplicably hilarious that I can't stop. Hisao just looks up at me like a buffoon, unable to interpret my response at all."

    "I take a deep breath to collect myself, smiling down at him."

    mk "You sure make a terrible Romeo."

    "He just hangs his head at the quip. He might not exactly be the most poetic type, nor the most manly in sweeping me off my feet... but that's fine. For good or bad, he's Hisao."

    show hisao_blush at center with charamove

    "I offer him a hand, which he takes as he levers himself back up."

    "With the two of us side by side on the peak of the hill overlooking the town, I sling my arm around his neck."

    mk "'Together', huh?"

    mk "That doesn't sound so bad when you say it."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_H7:

    scene bg school_gate_ni_running
    with dissolve

    $ renpy.music.set_volume(0.8, 0.0, channel="ambient")
    play ambient sfx_running fadein 2.0

    play music music_running

    window show

    "Nothing gets me going like a good sprint. One foot hitting the ground quickly after the other, the buildings and plants around me seem to fly past. My breaths short but measured as I throw myself forwards with glee."

    "Guard" "Stop! I'm telling you, stop right there!"

    scene bg school_courtyard_ni_running
    with locationskip

    mk "Ah ha ha ha ha!"

    "I can't help but laugh at the fool. There's no way that old man could outrun someone like me, no matter how carefully ironed his poncy uniform is. He looks more like an office worker than security, not that it's easy to see him in this darkness."

    "To his credit, he is managing to keep up, going by the circle of torchlight swinging to and fro on the ground just before me as he frantically gives chase."

    "One problem with living in the country is that if you miss one train, the effect ripples down as you end up missing the next few connections as well. By the time we finally got back to Yamaku, it was well past curfew."

    "Not that I mind. After all, I'm having the time of my life right now."

    "The plus side to the night time darkness that's fallen over the school grounds is that it's trivial to sneak in. With me acting as a decoy to draw the guard away, Hisao and Suzu should be well on their way to their respective dormitory buildings by now."

    "The security guard yells out some more, but it only makes me go faster. My hair and shirt billow in the wind as I run through the grounds, the night air feeling wonderfully refreshing against my skin as I move."

    "Hello again, Yamaku."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    stop ambient fadeout 1.7
    with Pause(2.0)

    #centered "~ Timeskip ~" with dissolve

    #Maybe adding a timeskip in imachine instead of a locationskip would be better here? [AHA]

    scene bg school_hallway3 with shorttimeskip #locationskip

    play music music_normal

    window show
    show haru_yo with dissolve

    har "Yo, Miki."

    "Haru raises a hand in greeting as he notices me walking down the hallway towards class."

    mk "Hey. Unusual to see you here so early."

    show haru_smile with charamove
    hide haru_yo

    har "Had plenty of time to recharge over the holidays, after all. Ready and rearing to go."

    mk "Didn't you work in your family's bakery? How's that gonna recharge you?"

    har "Baking is fun, you know. Besides, it's not like I worked for free."

    "He reaches into his back pocket, pulling out his smart brown wallet. The number of bills he pulls out makes my heart skip a beat."

    mk "Dude..."

    har "This is what it's all about, girl. Fat stacks."

    mk "Gimme. Gimme, gimme. I want to touch it."

    show haru_serious with charamove
    hide haru_smile

    "He gingerly hands it over, my hands instinctively snatching the wad of cash from his fingers."

    "So this is what it feels like to be rich. I rub the notes between my fingers, taking in their texture before bringing them underneath my nose and taking a whiff."

    mk "Smells like... capitalism."

    har "And part of capitalism is paying the worker, so give me that back."

    "I frown as I dutifully hand him back his money. That was probably the most cash I've ever held in my hands at once."

    mk "Sounds like you enjoyed yourself, at least."

    show haru_basic with charamove
    hide haru_serious

    har "Sure did. You didn't kill Hisao and Suzu, did you?"

    mk "Haha, nah. They're still kicking around."

    scene bg school_scienceroom with locationchange

    "As we walk into the classroom, my point is made for me. Suzu sits at her desk while Hisao talks to her while standing in front of it. Everything really is back to normal."

    "Giving a hearty stretch, in part from lack of sleep, I walk over to the two as Haru takes a seat."

    show suzu_neutral at twoleftsit
    show hisao_smile_u at tworight
    with dissolve

    suz "So you managed to avoid the guard, then?"

    mk "C'mon, who do you take me for?"

    hi "Thanks for doing that, anyway. We'd have all been screwed if you didn't draw him away."

    mk "Eh, it was a nice run."

    mk "And besides, it's kinda hard to refuse you, now."

    "He just smiles and scratches his head. If I really wanted to torture him, I'd give him a big ol' kiss in front of the class, but I'll save him the embarrassment. For now."

    "Suzu just gives a sigh as she starts getting her things out for the day ahead."

    show hisao_erm_u at tworight with charachange
    hide hisao_smile_u at tworight

    hi "I probably should have asked, but are you okay with this, Suzu?"

    suz "It's not up to me."

    show suzu_normal at twoleftsit with charamove
    hide suzu_neutral at twoleftsit

    suz "Besides, I largely expected it. I just hope the influence you have over one another runs in one particular direction more than the other."

    "I stick my tongue out at the cheeky girl. I'm glad she doesn't seem to mind, though it would probably be best not to be too touchy feely around her, going by her reactions to it."

    hide hisao_erm_u at tworight with moveoutright
    hide suzu_normal at twoleftsit with dissolve
    show muto_normal with dissolve

    "As we talk, I look back to see Mutou striding into class, the day's teaching material held under his arm. As good as catching up with others might be, I suppose school wouldn't be school without the pain of classes."

    "As he deposits his folders and books on the desk, Mutou's head perks up as he notices that I'm here."

    show muto_smile with charachange
    hide muto_normal

    mu "Ah, Miura. Good morning."

    mk "Mornin'. All rested up after the holidays?"

    mu "Teachers don't get holidays."

    mk "Seriously?"

    mu "We take training, mark tests, and prepare lesson plans the next semester. As much as I'd like to rest, there isn't much time for it."

    mk "That's terrible. How can anyone live like that?"

    mu "It's the life I chose, so it's not that bad."

    mu "You seem quite tired, though. Not enough sleep?"

    mk "Ah ha, yeah. Got to sleep pretty late last night."

    show muto_normal

    "He doesn't say a word, content to simply stare at me intently. I keep smiling, but I know damn well that I just dug my own grave."

    mk "Shit..."

    stop music fadeout 1.0

    scene bg school_hallway2 with shorttimeskip

    #centered "~ Timeskip ~" with dissolve
    show hisao_erm_u with dissolve

    play music music_fripperies

    mk "Shit damn bloody shit."

    hi "Swearing's just going to get you more detention if a teacher hears you."

    "I continue grumbling under my breath as we walk, both of us loaded down with thick textbooks as we walk down the hallway to the library, the sounds of people outside enjoying their lunch break making this all the more dreary."

    "In the end, there just aren't that many girls here brazen enough to try outrunning the security guard at night, let alone doing it while laughing maniacally. Waltzing into Mutou's trap didn't help my case, either."

    "At least I'm not alone in my punishment, with Hisao having volunteered to take a load down there as well."

    mk "Thanks for offering to help me with these."

    hi "To be honest, that was just because I was going to the library anyway."

    mk "Nerd."

    "I keep watching him as we walk, losing my self-awareness a little as I do."

    show hisao_talk_small_u with charachange
    hide hisao_erm_u

    hi "Is there something on my face?"

    mk "I was just wondering how I ended up going out with a dork like you."

    show hisao_smile_teeth_u with charachange
    hide hisao_talk_small_u

    hi "What about me? A dedicated student hanging around a total delinquent's not a good look."

    "I bump him with my hip, earning a sigh. He might have roped me into a relationship, but I'm not gonna make it easy for him."

    scene bg school_library with locationchange
    show hisao_erm_u at left with dissolve

    "Walking into the library, it looks just as it always has. Students quietly read away, with the odd sign that this is unmistakably Yamaku lying around, like the cane propped against a desk, or braille book being scanned over by the fingers of a pretty blonde."

    "Hanako, as always is just visible in her little corner, burying her face in some novel or another while she sits on that big beanbag of hers. It's too bad the couple of times I tried to get closer to her failed so utterly."

    "Hisao quietly calls out that we've come with the textbooks, given that nobody's behind the counter to take them. Before I suggest we just dump them for the staff to sort out, a loud thump from under the counter gives us both a jump."

    play sound sfx_impact
    with vpunch
    show yuuko_neurotic_up at center with moveinbottom

    "Yuuko slowly emerges from the ground, rubbing her sore head as she stands. The poor girl never seems to have very much luck."

    hi "That sounded bad."

    show yuuko_cry_up at center with charachange
    hide yuuko_neurotic_up at center

    yu "That's the second time today..."

    mk "Maybe you should start wearing a helmet."

    show yuuko_worried_up at center with charachange
    hide yuuko_cry_up at center

    "The quip doesn't go over well, the librarian becoming even more depressed. I feel like I just kicked a puppy."

    "Having had enough of standing around with this weight in my arm, I sit the pile on the counter. Hisao quickly does the same, putting his stack beside mine."

    show yuuko_neutral_down at center with charamove
    hide yuuko_worried_up at center

    yu "Ah, these are the ones Mutou borrowed for class?"

    hi "Yeah. They should all be accounted for."

    "As Yuuko begins to count up the books, my interest in staying here starts rapidly dropping, my eyes drawn towards the door. The fact doesn't escape Hisao."

    show hisao_disappoint_u at left with charachange
    hide hisao_erm_u at left

    hi "You could at least try to hide your lack of interest."

    mk "I can't help it, I'm allergic to paper."

    hi "Oh really?"

    mk "Yes, really. I break out in a rash. The only cure..."

    show yuuko_neutral_down at right
    show hisao_disappoint_u at center
    with charamove

    "I shuffle a couple of steps towards the door."

    mk "...is to go..."

    show yuuko_neutral_down at rightedge
    show hisao_disappoint_u at right
    with charamove

    "A couple more steps. I've nearly managed to escape."

    mk "...Outside."

    show hisao_talk_big_u at right with charachange
    hide hisao_disappoint_u at right

    "I feel the tips of Hisao's fingers brush against my arm, but I slip from his grasp and slide out the door. I'm finally free."

    stop music fadeout 1.0

    #centered "~ Timeskip ~" with dissolve

    scene bg school_gardens3 with shorttimeskip

    play music music_tranquil

    "Wandering past the trees to the track, all the usual suspects are hanging around. Emi and the track captain pelt around at high speed, as if they had any other speed they go at, while most of the others are stretching and chatting between themselves."

    "As much as I'd like to call this familiar scene home, it's only going to last a few more months. When that time comes, this will all be gone, just like my life at the farm."

    "Not wanting to get caught up in my angst, I give a big stretch to try and ward off my tiredness before walking across the track and up to the assorted club members."

    scene bg school_track with locationchange
    show yukio_notimpressed at left
    show haru_smile at center
    with dissolve

    mk "Yo."

    yuk "I was wondering when you'd show up here again."

    mk "Is that in a good way, or a bad way?"

    yuk "Guess."

    show haru_annoyed at center with charamove
    hide haru_smile at center

    har "Can't you two get along just for a single day after the holidays?"

    mk "It's his fault."

    show yukio_eeh at left with charachange
    hide yukio_notimpressed at left

    yuk "What? No it's not."

    show haru_serious at center with charamove
    hide haru_annoyed at center

    har "Now, now, children. Stop fighting."

    mk "Fine. Too tired for this shit, anyway."

    show yukio_notimpressed at left with charachange
    hide yukio_eeh at left

    yuk "Tried to keep your holiday going a bit too long?"

    mk "Something like that. I think I need a holiday just to recover from my holiday."

    show haru_basic at center with charamove
    hide haru_serious at center

    har "A lot happened, then?"

    mk "You have no idea."

    "Yukio's gaze shifts over my shoulder. Turning to see what's take his attention, I see Hisao striding up. Guess he got bored of his precious books."

    mk "Speak of the devil."

    show hisao_smile_u at right with moveinright

    hi "Hey, guys."

    show yukio_smile at left with charachange
    hide yukio_notimpressed at left

    yuk "You managed to survive, then?"

    mk "Why does everyone say that?"

    show hisao_heh_u at right with charachange
    hide hisao_smile_u at right

    hi "After what happened? They're not exactly wrong to wonder."

    har "Can't leave us hanging, man. What's the story?"

    show hisao_erm_u at right with charachange
    hide hisao_heh_u at right

    hi "Uh, well..."

    show hisao_frown_u at right with charachange
    hide hisao_erm_u at right

    "He looks to me with a slightly questioning face, as if asking how best to break the news. It turns to a look of concern as the corners of my mouth curl upwards."

    #show hisao_wtf at right with charachange
    show hisao_wtf_close_u at right with charamove
    hide hisao_frown_u at right
    ##with upclose (screen filling?)

    "I grab his tie with my hand, yanking his face towards mine. Our mouths meet, my heart skipping a beat as I feel his soft lips press to mine. He gives a muffled mumble of surprise, but it only makes me kiss him all the harder."

    show hisao_wtf_u at right with charamove
    hide hisao_wtf_close_u at right
    ##show him back normal size as wtf

    "Letting go of his tie, he stumbles back and gasps for air. I can't wipe the toothy grin off my face, smiling so hard that my cheeks almost hurt."

    show yukio_huh at left with charachange
    hide yukio_smile at left

    yuk "Well, well."

    show haru_smile at center with charamove
    hide haru_basic at center

    har "You're a braver man than I."

    show hisao_smile_u at right with charachange
    hide hisao_wtf_u at right

    "As Yukio is left scratching his head, Haru steps forward and pats Hisao on the shoulder. Hisao finally manages to recollect himself after a few moments, though it's obvious his heart's still racing."

    hi "She's not that bad."

    show yukio_smile at left with charachange
    hide yukio_huh at left

    yuk "I hope it works out for you. If anyone could civilise this savage, it's you."

    mk "I'm right here, dude."

    yuk "I know that."

    hide yukio_smile with moveoutleft

    "Someone a few yards away calls for Yukio, and with a quick wave, he leaves us. Haru turns on the ball of his heel, about to follow."

    har "Good luck, you two."

    hide haru_smile with moveoutleft

    "He gives a wink, and with that, walks away. Hisao stays silent as I wave him off."

    mk "Got bored of the library, huh?"

    show hisao_erm_u at right with charachange
    hide hisao_smile_u at right
    show hisao_erm_u at center with charamove

    hi "Yeah."

    "The silence between us is all the more noticeable thanks to the noise from the other club members. Hisao's cheeks look slightly rosier than they did before, leading to only one conclusion."

    mk "You're not all embarrassed from that kiss, are you?"

    show hisao_blush_u at center with charachange
    hide hisao_erm_u at center

    "His face flowers into a scarlet blush as he buries it in his hands. I just laugh, partly at him, and partly to shrug off my own feelings. The feeling of his lips against mine still lingers in my mind, after all."

    mk "You're too soft, boy."

    hi "That was our first kiss..."

    mk "And it was a good one, too!"

    "The weariness in his eyes as he looks to me tells that he's finally coming to realise what he's got himself in for. Taking pity on him, I reach forwards and rub his hair."

    hi "Why do you keep doing that? It's embarrassing."

    mk "'Cause I like doing it, why else?"

    show hisao_frown_u at center with charachange
    hide hisao_blush_u at center

    "Hisao frowns, but I can tell he secretly enjoys it. He tends to be cutest when he's trying not to be."

    hi "There was something I wanted to ask you. Before you ran away from the library and left me standing there like a goose, that is."

    mk "Go on."

    show hisao_declare_u at center with charachange
    hide hisao_frown_u at center

    "He clears his throat and takes a breath before continuing on."

    hi "Do you have anything planned on Sunday?"

    mk "Not a thing. Why?"

    show hisao_smile_u at center with charachange
    hide hisao_declare_u at center

    hi "Then it's a date. I'll pick you up late morning."

    "Oh, right. We're going out now. That means dating."

    "I know what that entails, in a rough sense. Romance movies aren't really my thing, but I've seen a couple that show characters dating. It's just spending some time with the person you love, really. Time with the person you love. Person you love. Love."

    "That damn word keeps echoing around in my head. It actually feels kinda nice to think about, like rolling a tasty piece of candy about in my mouth."

    "Feeling a smile on my face, I know there's only one answer I can give."

    mk "Cool."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_H8:

    scene bg burgerk
    with dissolve

    $ renpy.music.set_volume(0.5, 0.0, channel="ambient")
    play ambient sfx_crowd_indoors

    window show
    show hisao_erm at centersit with dissolve

    play music music_miki

    "I have to admit, Hisao sure knows how to win me over."

    "The odd beep and boop from the computers behind the counter and chintzy pop playing over the speakers provide the soundtrack to our romantic meal of burgers and fries. People watching provides a nice source of entertainment as well, with the place being fairly full this time of day."

    "Office workers in their smart white shirts and contrasting black slacks and skirts tap away at their phones checking their stocks and emails, while kids chat between themselves about this idol group or that videogame. It's a nice atmosphere. Casual, informal, no pretence of fine dining or any of that crap. Just people having a bite while yakking to each other."

    "I take a good bite of my burger as Hisao slips a few fries into his mouth, both of us apparently being pretty hungry."

    mk "You know, this is kinda like when we first met."

    "Hisao pauses for a moment to think, looking like a squirrel with his cheeks full of fries. Eventually he gulps them down, having remembered that day."

    show hisao_talk_small at centersit with charachange
    hide hisao_erm at centersit

    hi "Oh, right. When you took me to the Shanghai."

    mk "Yeah. It's kinda cool."

    show hisao_smile_teeth at centersit with charachange
    hide hisao_talk_small at centersit

    hi "I meant to do that. Glad you noticed."

    "I flick a chip at his face in response, hitting him between his squinting eyes."

    mk "So, what's next? Wanna pop by that shrine we passed?"

    show hisao_erm at centersit with charachange
    hide hisao_smile_teeth at centersit

    hi "Not really into visiting shrines. I'm surprised you're interested, though."

    mk "Doesn't hurt to throw in a coin and do the ol' rituals every so often. Didn't work for my hand, but maybe it's given me a little luck in other places."

    "He looks interested, but very much in the politely nodding way."

    mk "I guess that sort of thing's more important to people who grew up with it."

    show hisao_talk_small at centersit with charachange
    hide hisao_erm at centersit

    hi "Yeah, I never really bothered much. The architecture's nice for temples and stuff, but that's about it."

    "I take another bite of my burger before continuing on, unsatisfied with his answer."

    mk "Do you actually believe in anything? Like, I dunno, stuff you can't see? God, spirits, karma, an afterlife, any of that stuff?"

    show hisao_hmpf at centersit with charachange
    hide hisao_talk_small at centersit

    hi "Not... really?"

    mk "So it's that simple."

    hi "It's not that I haven't done any thinking about it. Believe me, I did plenty of that while I was in hospital."

    mk "Nearly dying would do that."

    hi "Problem is, the more I read, the less I felt I knew. It's a funny thing, how the more you research anything, the more you realise just how little you actually understand."

    show hisao_erm at centersit with charachange
    hide hisao_hmpf at centersit

    hi "I absolutely devoured reading material, but in the end, I found a whole lot of questions, and not many answers. Pretty anticlimactic end for a quest to understand mortality, huh?"

    mk "At least all that reading filled in the time."

    hi "That's..."

    show hisao_declare at centersit with charachange
    hide hisao_erm at centersit

    "Hisao just sighs."

    hi "Yeah, you're right. I guess it did."

    show hisao_talk_small at centersit with charachange
    hide hisao_declare at centersit

    hi "How about we hit the castle once we're done here? Could have a good wander around."

    "He doesn't seem too interested in the suggestion, but nor am I. We both ponder a bit as we munch away at our food."

    "An idea begins to form in my head, going by how Hisao acted during our time back home. I don't know how far it is from here, or how expensive it is, but I think he'd like it."

    show hisao_erm at centersit with charachange
    hide hisao_talk_small at centersit

    hi "I always get worried when I see that grin."

    mk "Eat up, Hisao. We've got places to be."

    "He looks to me with concerned eyes, having no idea of what's to come."

    stop music fadeout 1.0

    stop ambient fadeout 1.0

    ##centered "~ Timeskip ~" with dissolve
    scene bg manta with shorttimeskip
    show hisao_talk_big with dissolve

    play music music_comfort

    "Cloaked in a deep blue glow, Hisao stands wide eyed as he stares up at the tank before him. I'd tease him for being so amazed, but I'm doing just the same."

    "A giant manta ray, impossibly huge, breezes past the window with its underside pointed at us. It's crazy how easily it cuts through the water with such small movements. Its mouth and gills look bizarre, so totally unlike anything that walks on land."

    mk "Animals are cool."

    hi "Sure are."

    "As it glides around to the back of the tank, we start walking to the next display."

    "A gaggle of teenage girls on the other side of the passage shriek in excitement, apparently overcome by the cuteness of a couple of turtles which swam up close to the window. You'd be forgiven for thinking they were fawning over a baby or something."

    show bg aquarium with dissolve
    show hisao_erm with dissolve
    hide hisao_talk_big

    "We join a father and his young son at a shark tank, several of them lazily swimming about their enclosure. They're not exactly at their most menacing when they're cooped up like this, looking more bored than ravenous."

    "Hisao doesn't seem to mind, though, still watching them float about with interest. Looks like I struck it out of the park on this one."

    mk "Having fun there?"

    hi "I had no idea this city had an aquarium. You ever come here before?"

    mk "Me? Nah. Probably should've."

    hide hisao_erm with dissolve

    "He goes back to looking at them swimming away after I give a shrug."

    show kid_staring with dissolve

    "It's now that I notice the young boy staring not at the sharks, but at the one-handed girl nearby. Maybe I should take pride in being more interesting than a few sharks."

    show kid_laugh with charachange
    hide kid_staring

    "I poorly mime clutching at my stump and yelling with pain, drawing a smile from the kid. The spaces where he's lost a couple of baby teeth make it look all the cuter."

    "I quickly step back and stiffen up as Hisao turns back around to see what the movement was, pretending nothing happened."

    show kid_mimic with charamove
    hide kid_laugh

    "Doubting me, Hisao looks over to the boy. He does just the same, though even less convincingly than my own act."

    hide kid_mimic with dissolve
    show hisao_smile with dissolve

    "Thoroughly beaten, Hisao moves on with me quickly falling in beside him. I think I see a smile there, no matter how much he might try to play it off."

    show hisao_talk_small with charachange
    hide hisao_smile

    hi "You don't seem all that interested in the sea life."

    mk "Just too used to seeing them, especially wild ones."

    hi "I guess when you grow up with something, it becomes the norm."

    mk "Sure does. The aquarium's pretty cool though; it's first time I've seen some of these critters."

    mk "You have a nice smile, you know that?"

    show hisao_erm with charachange
    hide hisao_talk_small

    hi "What brought this on?"

    mk "I was just thinking how different you are to when you first started in Yamaku. If you had a colour back then, it would've definitely been grey."

    hi "And now?"

    mk "Hmm... you look kinda blue right now."

    show hisao_hmpf with charachange
    hide hisao_erm

    "It takes a second for him to get it, but his face drops once he does."

    hi "Right, the light from the tanks. Very funny."

    hi "I don't think anybody would argue that your colour's red, as if it were ever a question."

    show hisao_talk_small with charachange
    hide hisao_hmpf

    hi "But yeah, I feel different to when I started at Yamaku as well. I can't see the entire path in front of me yet, but it feels like the fog is beginning to lift."

    hi "A lot of that is thanks to you, you know. The world didn't change after I had my heart attack, I just got to see a whole different part of it."

    hi "Maybe that's why I kinda get Mutou. When he goes on about how interesting this part of science is or that, he's really talking about a new way of seeing the world. Of understanding what's around us."

    mk "Understanding Mutou, now that's a scary thought."

    "I am glad, though. It feels less like I'm dragging Hisao along life with me, and more like he's back on his legs and starting to walk on his own. It reminds me of how Suzu and I ended up."

    "That I can be there for another person like that makes me pretty happy."

    scene bg giftshop with shorttimeskip

    "Eventually we reach the exit of the aquarium proper, entering the small gift shop. The two of us part to look at this knickknack or that, from small stuffed animals to phone straps and stickers."

    "I feel like I should buy something for Hisao given that he paid for both our tickets, but even if he hadn't offered to get them, I couldn't have afforded one. You can practically see the tumbleweeds blowing across the empty expanse of my wallet."

    "As I ponder my sadly lacking funds, I come across to the clothing section. It leaves me wondering who would want a hoodie with the name of an aquarium proudly displayed on it."

    "One thing does catch my interest, though. A baseball cap with a nice colour scheme and thankfully small logo. I pick it up to check the price, but end up sighing before putting it back on the shelf. Sometimes I can afford the odd luxury, but this isn't going to be one of those weeks."

    show hisao_talk_small with dissolve

    hi "What's up?"

    mk "Nothin'. Found something, did you?"

    scene bg plushie with dissolve

    "I point to the small stuffed turtle in his hand."

    hi "Just something small to remember the place. You going to grab anything?"

    mk "Nah. I'll wait outside for you, okay?"

    hi "Sure. See you there."

    stop music fadeout 1.0

    #centered "~ Timeskip ~" with dissolve

    scene bg school_gardens_ss
    with shorttimeskip
    show hisao_smile with dissolve

    play music music_soothing

    "Hisao and I slowly walk across the school grounds together, the oversized plastic bag at Hisao's side crunches away with each step. With the sun finally setting, it looks like our day together's finally over."

    mk "Whelp, that's that. I had a great day, Hisao."

    hi "What are you saying? The date's not over yet."

    "Now that was smooth. He doesn't quite manage to take it all the way, with his mouth giving a slight grin from nervousness at the suggestion, but he still gets an A for effort."

    mk "I might fall for you even harder if you keep that up. Mind if we stay in your room tonight?"

    hi "Sure."

    "With that, the two of us make our way to the male dormitory building."

    scene bg school_dormext_full_ss
    with locationchange
    scene bg school_dormhallground
    with locationchange

    "A couple of dudes lounge around in the bottom floor common area, sipping at cans of soft drink as they watch television. A nice lazy way to spend an evening, really."

    scene bg school_dormhallway
    with locationchange
    show hisao_erm with dissolve

    "We finally reach the floor of Hisao's room, the familiar poorly pinned sheets of paper still hanging onto the corkboard on the walls, albeit only barely. It's a pretty empty part of the dorms, but Hisao seems to like the quiet, so I'm not one to complain."

    mk "Maybe you should put something up on the boards."

    hi "Like what?"

    mk "I haven't thought that far ahead yet."

    show hisao_disappoint with charachange

    "He clips me over the back of the head as we continue down the hall."

    stop music fadeout 1.0

    scene bg school_dormhisao_ss
    with locationchange

    play music music_aria fadein 1.0

    "Entering his room, it looks the same as it always has. Spartan. A couple more bits and bobs have ended up on shelves and his desk, but nothing of much interest."

    "Not that I dislike it, though. It's almost charming in being such a good example of his orderly personality."

    show hisao_smile with dissolve

    scene black with shuteye

    ##do eyes closed fade to black thing

    "I feel his hands on my waist, and as I turn to see him, I find out lips pressed together. I just close my eyes, letting myself be taken in by the sensation."

    "His warm body held to mine, the tickling of his breath against my face, the brushing of his hair against my forehead.... Even if it's not exactly a passionate embrace, I can still feel my heart skip a beat."

    "It's terrible how I fold so quickly like that when taken off guard. It takes me a moment to notice Hisao's hand retrieving something from the bag, leaving me to look up stupefied as he plops the object onto my head."

    ##eyes open
    scene bg cap with openeye

    "My eyes open wide as I realise what it is."

    mk "How did you..."

    hi "I noticed you staring at it in the shop. I think it looks good on you."

    mk "You know what?"

    mk "So do I!"

    scene bg school_dormhisao_ss with dissolve
    show hisao_smile with dissolve
    show hisao_smile_close with charamove
    hide hisao_smile

    "I jump at him, wrapping him in a hug. It still doesn't quite feel like a natural thing to do, but I feel like there's no other way to channel the energy I feel right now."

    "This dork really can be something."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_H9:

    scene bg school_room34 #This time it's not Mutou's science class
    with dissolve

    window show
    show haru_serious #at right

    play music music_normal

    "Sitting on my desk as we wait for the teacher to show up, I find myself chatting away with Haru. Try as I might, I can't stop my fingers tapping on the desk beside me."

    har "You look nervous."

    mk "Nervous? Who do you take me for?"

    mk "I'm just so excited for the lesson ahead that I can't stop moving in anticipation."

    show haru_annoyed with charamove
    hide haru_serious

    har "You managed to find a lie even less believable than what I said. Impressive."

    mk "I hate the English teacher. She's even worse than Mutou."

    hi "The problem's with you, not him."

    "The voice calling from behind me induces a heavy sigh."

    mk "I didn't ask you..."

    show haru_serious with charamove
    hide haru_annoyed

    har "Maybe if you didn't go out of your way to annoy her, you would've have so many problems."

    mk "But I don't! I just don't care about English. I don't even get why it's mandatory to learn; does this look like America to you?"

    har "It's not just America, you know. There's Canada, Australia, New Zealand, England, Wales, Scotland, Ireland, uh..."

    show suzu_neutral at left with moveinleft

    suz "Singapore."

    mk "They speak English there too?"

    suz "Maybe you should pay more attention to geography as well as English."

    "I bring my forearms over my ears to try and block out everyone's voices. I feel like I'm being egged."

    "My attention is refocused as Haru takes out a particular worksheet. The sudden interest in it doesn't escape him."

    har "So that's why you're so antsy."

    mk "Okay, so I kinda, sorta, maybe didn't completely do all of the homework we were set."

    show haru_basic with charamove
    hide haru_serious

    "He just smiles at me knowingly."

    mk "I am two hundred percent screwed, yeah."

    mk "But you know, if you were so kind as to let me copy your homework super quickly..."

    har "I don't think there's a lot of point to using mine. I'm not much better at this than you."

    show haru_smile with charamove
    hide haru_basic

    har "Why don't you ask your boyfriend, anyway? At least that way you might scrounge up a decent mark."

    hide haru_smile
    hide suzu_neutral at left
    with dissolve
    show hisao_disappoint_u with dissolve

    "I turn my head back to Hisao, still standing next to his desk while busily looking over the very worksheet I need so badly."

    mk "Hey, Hisao? Let me copy your-{w=.5}{nw}"

    show hisao_declare_u with charachange
    hide hisao_disappoint_u

    hi "Do it yourself."

    hide hisao_declare_u with dissolve
    show suzu_concerned at left
    show haru_smile
    with dissolve

    mk "See? Maybe you can try getting that stick out of his ass."

    hi "I heard that."

    mk "It's lodged in there real tight."

    hide suzu_concerned at left
    hide haru_smile
    with dissolve
    show hisao_disappoint_u with dissolve
    with hpunch

    "He puts his hand on top of my head and latches down, dragging my head around with his grip tightening by the second."

    mk "That's kinda painful, dude."

    show hisao_frown_u with charachange
    hide hisao_disappoint_u

    hi "Good. Maybe if you did your homework sometimes this wouldn't be happening."

    "I get the feeling Hisao's holding back less and less when it comes to being rough with me, which suits me just fine. Even if it does mean suffering a little more."

    "But for all the teasing they may give me, I do have a lot of fun these days. Life became a lot easier once I stopped trying so hard. It's great for Hisao that he's finding his groove, but as for myself, my time has passed. The contentment I feel now is enough for me."

    "As the teacher finally shows up and begins to stride in, she gives me more than a passing glance. I have feeling this is going to be a very long lesson."

    stop music fadeout 1.0

    #scene black
    #with dissolve
    with Pause(0.3)

    scene bg school_track_on
    with shorttimeskip

    #centered "~ Timeskip ~" with dissolve

    play sound sfx_running loop

    play music music_running

    "A good jog around the track is probably one of the more productive ways to deal with stress. God knows I'd be in a world of hurt if I told that woman what I really thought of her."

    "Given the amount of sweat building up already, the thought passes my mind that I should actually count the number of laps I do one of these days, or time myself doing some sprints. Compared to people like Emi, though, I couldn't care less about records or self-improvement."

    "Running for the sake of running is a perfectly good way to spend the time, after all. Not that Hisao seems to really see it that way."

    "He might have cheated by joining me well after I'd started, but his heart having played up during the holidays has made me appreciate how he still throws himself at the track. He still doggedly tries to regain his previous physical fitness, or at least as much of it as he can."

    mk "You're keeping up well, Hisao."

    show hisao_frown_u with dissolve

    hi "That's because I'm trying, unlike you in class."

    "Trying so hard that he's doing this in his normal school uniform, unlike me in my proper gym gear."

    mk "Aw, c'mon. I don't need another person on my case."

    "He looks genuinely annoyed with me. That haughty sense of judgement towards what he thinks counts as an incorrectly-lived life reminds me a little of Shizune and her strict nature. Then again, as much as I may dislike living according to their standards, I can respect that disciplined attitude towards life."

    "I grin as I reach beside me and take his wrist in my hand."

    hi "You have some terrible idea again, don't you?"

    mk "Yup!"

    scene bg school_track_running
    with dissolve

    "With that, I speed up and drag him along behind me, the two of us breaking off the track and away from the school building."

    "The storage shed still gives me bad memories as we pass by, Hisao nearly getting dragged off his feet as I speed up to get past it. As we enter the greenery ahead, the both of us disappear from the sight of the others."

    scene bg school_forestclearing  #Or maybe plain black scene
    with locationskip
    stop sound fadeout 0.3
    stop music fadeout 0.3

    play music music_aria fadein 1.0

    "I start slowing down as we get deeper in, eventually letting go of his hand as the two of us start to walk the rest of the distance. There isn't really any singular spot I'm looking for, so we end up almost strolling in the undergrowth for while."

    show hisao_erm_u with dissolve

    "Still breathing a little heavier than usual thanks to my efforts on the track, I make do with watching Hisao. The way his eyes turn this way and that makes it obvious he's a tourist more than a local."

    mk "Never been here before?"

    hi "Nope. I'd occasionally wondered what it was like behind the track."

    mk "Well now you know. I'm not totally sure if this land is actually owned by the school, but they sure don't make much effort to clean it up if they do."

    hi "Still not a scratch on the forests back up north, though."

    mk "You got that right."

    "I run my hand through my hair as I look about, seeing little but trees, bushes, and undergrowth. Listening intently reveals that we're not quite alone, with fallen leaves shuffling in the distance from some squirrel darting about. As far as humans go, though, there are few who'd venture this far on a whim."

    play sound sfx_sitting
    show hisao_erm_u at centersit with charamove

    "My companion slowly stops walking as we reach the heart of the forest. Turning to see him, Hisao backs up to a tree and lets himself slide to the ground, letting his head fall back onto the trunk in defeat."

    show hisao_talk_small_u at centersit with charachange

    hi "You can't be serious."

    mk "What's up?"

    hi "Don't play innocent with me. There aren't that many reasons for a guy and a girl to sneak off alone. Especially when one of them is you."

    "I throw my arms up in surrender. It was only a matter of time until he worked it out."

    mk "Oh no, I've been caught. Whatever will I do?"

    show hisao_erm_u at centersit with charachange
    hide hisao_talk_small_u at centersit

    hi "Hell of a way to let off some stress..."

    mk "But very effective! Especially with someone else."

    mk "Your heart's racing, isn't it?"

    show hisao_frown_u at centersit with charachange
    hide hisao_erm_u at centersit

    hi "If we get caught, we'll be in for the high jump without any water."

    mk "There's nobody here, man. Besides, the fresh air will be a nice change to a stuffy bedroom."

    stop music fadeout 2.0

    scene black

    play music music_to_become_one fadein 3.0

    "Having had enough of talking, I wander over to him and turn about, sitting in his lap with my back to his chest."

    "As expected, the temptation soon becomes too great for him to resist. I let myself settle back into him as his hands come around my waist, his face coming beside mine."

    "The feeling of his large hands cupping my breasts makes me roll my head to the side, every muscle relaxing as he begins to knead and move them. There's a charming mix of curiosity and desire in his movements, which only makes this all the better."

    mk "Nice, aren't they?"

    hi "Wouldn't they be a pain while exercising?"

    mk "Worth it. Totally."

    "His hands snake underneath my gym top, the feeling of his skin against mine sending a shiver up my spine as he takes in the feeling of my taut stomach. I'm starting to think he likes it, with the way his hands linger over the area."

    "Slowly, teasingly, he moves his hands upward. I can't help but sigh as he begins to grope me directly, my bra doing little to lessen the sensation of his playing with my breasts."

    "This is the best. Just sitting here being played with, drifting on the current of pleasure without a care in the world. I don't think he's really trying to get me off so much as explore how my body feels, but I enjoy that fact."

    "With my hand and stump lying on my thighs, it's easy for my hand to absentmindedly slide down just an inch of two, the side of it settling between my legs. All it takes is the smallest movement to feel it rubbing through my spats, settling into a nice, regular rhythm."

    "It isn't until Hisao notices me getting a little too dreamy that he notices I'm masturbating in his lap."

    hi "Miki..."

    mk "Just keep going."

    "He obediently does so, and as I feel something against my butt, I can tell it's turning Hisao on like crazy. I can't help myself, and if it turns him on, all the better."

    "Wanting to do this himself, he shifts his left hand to continue kneading my right breast, his other hand moving downward."

    "Hisao manages to slide his fingers between my sweaty skin and the top of my spats, pausing a little as he feels how aroused I've become. Gathering the courage to try fingering me for the first time, he brings his middle finger over my lower hair and begins to stroke at the most important spot."

    "It's when he starts a slow circling motion that he really manages to nail it, making me practically melt."

    mk "Aaah... that's good..."

    mk "See? It was worth watching each other."

    "In a surprisingly quick movement, two of his fingers flick downward and slide into me, making a come hither motion with enough force to make me cringe from pain."

    mk "Ah! Ow! Too much!"

    hi "Then don't tease someone with their fingers between your legs."

    mk "Asshole..."

    hi "What did I say?"

    "Having had quite enough of his lip, I twist around and grab the knot of his tie. Hisao's surprise is met with a strong tug as I let myself fall to the ground, his body falling on top of me."

    hi "Hey, Miki-!"

    "He tries to pin me down out of frustration, but I manage to overpower him. With a bit of a scuffle, I free my arm and give a solid shove to his shoulder, using my stomach muscles to send him toppling over onto his back. I quickly follow, ending up on all fours above him. He gives a weak smile as I grin in victory."

    mk "I win."

    "I move my head down to kiss him, our tongues meeting as the experience begins to sweep us away. My heart beating away and body more than ready to ravage him, I slip off his tie and work away at his buttons."

    "I can feel myself panting as I move further and further down, finally undoing the last button. Hisao sits up and quickly shirks it as I continue to undress him, each piece of clothing ending up discarded without much thought. Eventually I manage to work off his underwear, the boy naked in the midsummer's day."

    "I move forwards to kiss him once more, but as our mouths meet, I'm taken off guard by his hands coming to my shoulders and throwing me down onto the ground. I've done it to him before, but now that the shoe's on the other foot, I'm left more dazed than anything."

    "His mouth is pushed onto mine, my breath stolen as his tongue darts in and moves about, tangling with my own and refusing to let go. I kick, jerk, and squirm under his grasp, but he keeps going, our saliva mixing as he takes his fill of me."

    "Eventually, finally, he breaks off. My heart's almost hurting from how fast it's beating, my attempts to speak amounting to little as my need for air takes precedence."

    mk "Hisao..."

    hi "There. I win."

    "I can't help but laugh, my body convulsing with hilarity at the ridiculous sight. It makes me glad to see him being forceful like this, taking what he wants. It sure is a change from the subdued and hesitant kid who so awkwardly introduced himself to class all that time ago."

    "I reach up and take the side of his cheek in my hand, quite taken with the fellow holding himself above me. My breathing finally under control, I smile and say four simple words."

    mk "Then take me, Hisao."

    "He needs no further urging, grabbing me and rolling my body about with a fair amount of force. Having ended up with my chest on the ground, I try to pick myself up, only to feel a hand grabbing the back of my spats."

    "With a strong tug, Hisao exposes my butt and crotch to the air."

    mk "Oh...!"

if persistent.adultmode:
    scene bg doggy_edited with dissolve

    "He jams himself into me with enough strength to cause a damn lot of pain, our hips hitting with a loud sound. The pain and surprising force that he's become comfortable in using against me combine to send my front falling back to the ground, the side of my face hitting the dirt as he pulls back and begins to thrust."

    "He grips my butt tightly as he hits himself against it, each thrust slow but powerful. I can't help but yelp and moan loudly, all of my senses overwhelmed by the strange mixture of pain and pleasure. He goes harder and harder if anything, his confidence and lust building within him."

    "With little to grip onto, my hand grabs into the dirt and dead leaves, sweat pouring off me. More, I want him to move more. I like this Hisao, I love this Hisao..."

    "His desire not sated by his current motions, he picks up a knee and uses one of his hands to push down hard between my shoulder blades. I try to squirm out reflexively, but he simply pushes harder while shoving his rod ever deeper into me."

    mk "Hisao... ahn...!"

    "He doesn't say a word as he grunts away, teeth sounding like they're clenched as he drives onward. I can't move from his grasp, left with the side of my face pressed against the ground as rapturous pleasure floods my body."

    "Keep going, Hisao! I want more of you, I want more...!"

    "A guttural growl rises in my throat as a familiar sensation begins to rise, my heart racing as every sense starts to converge into a raging torrent of euphoria. Try as I might, I can't hold back the surge quickly rising with me."

    "It's a bizarre but deeply satisfying mixture of bliss, pain, and exhaustion that I've never felt before, the adrenaline filling my body in response to being held down mixing with the arousal threatening to so quickly send me over the edge."

    "I can't stop myself at all, Hisao's hold over me total and unshakable. I feel my neck muscles tightening as I growl and dig my fingers into the dirt to frantically try and keep control of my body, but I can't... I can't stop... I can't...!"

    scene black with dissolve

    mk "Aaaahn!"

    "My mind blanks as every muscle tightens, fingers and toes curling as the pleasure of orgasm wracks my body. Every sense is washed away in an instant as pure wondrous joy floods every corner of my consciousness."

    "I don't know how long it lasts, nor do I care. I'm in bliss. I lose track of everything, even my own self, as I utterly surrender to the feeling washing over me."

    "As I take one step over that peak, the real world begins to rush in to the vacuum within my addled mind. My collapse is all but instantaneous, every last ounce of energy I'd had being utterly exhausted as my hormones, and emotions, crash."

    "I simply flop onto the ground face-first, my limbs having gone entirely limp. Every sense feels muddled and unclear, from the blurry and unfocused ground before me, to my sense of touch barely registering the sweat soaking my body and clothes, and the feeling of Hisao's thick member slipping out."

    "Something warm touching my butt and lower back vaguely registers in my mind, but I don't care. I can't think right now. I just want to lie here, holding on to this feeling."

    "Hisao enters my vision as he sits and then falls back onto the ground, his bare chest heaving from the effort. I try to reach out and brush a couple of hairs sticking to his cheek, but my hand barely gets halfway before flopping on the ground for lack of energy."

    "There we lie, with the boy on his back and I on my front, breathing heavily as we try to recuperate. I manage to weakly smile at him, his hand reaching out and gently brushing some hairs from my forehead."

    mk "You really went all out, didn't you?"

    hi "I was frustrated with you, I guess."

    mk "Still frustrated?"

    hi "I lost track of what I was even annoyed about."

    "As we lie there looking at each other, that sensation I felt on my behind slowly comes back to haunt me."

    mk "You didn't...?"

    "He just averts his eyes. So he did finish himself off onto my back. I just let out a long breath, completely unable to muster anything more notable."

    hi "I wasn't thinking."

    mk "Just get a tissue."

    hi "...I really wasn't thinking."

    mk "You suck."

    "I playfully bat him on the face with what little force I can muster. For all I chide him about thinking too much, he really chooses the worst times."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

else:
    scene bg doggo with dissolve

    "He jams himself into me with enough strength to cause a damn lot of pain, our hips hitting with a loud sound. The pain and surprising force that he's become comfortable in using against me combine to send my front falling back to the ground, the side of my face hitting the dirt as he pulls back and begins to thrust."

    "He grips my butt tightly as he hits himself against it, each thrust slow but powerful. I can't help but yelp and moan loudly, all of my senses overwhelmed by the strange mixture of pain and pleasure. He goes harder and harder if anything, his confidence and lust building within him."

    "With little to grip onto, my hand grabs into the dirt and dead leaves, sweat pouring off me. More, I want him to move more. I like this Hisao, I love this Hisao..."

    "His desire not sated by his current motions, he picks up a knee and uses one of his hands to push down hard between my shoulder blades. I try to squirm out reflexively, but he simply pushes harder while shoving his rod ever deeper into me."

    mk "Hisao... ahn...!"

    "He doesn't say a word as he grunts away, teeth sounding like they're clenched as he drives onward. I can't move from his grasp, left with the side of my face pressed against the ground as rapturous pleasure floods my body."

    "Keep going, Hisao! I want more of you, I want more...!"

    "A guttural growl rises in my throat as a familiar sensation begins to rise, my heart racing as every sense starts to converge into a raging torrent of euphoria. Try as I might, I can't hold back the surge quickly rising with me."

    "It's a bizarre but deeply satisfying mixture of bliss, pain, and exhaustion that I've never felt before, the adrenaline filling my body in response to being held down mixing with the arousal threatening to so quickly send me over the edge."

    "I can't stop myself at all, Hisao's hold over me total and unshakable. I feel my neck muscles tightening as I growl and dig my fingers into the dirt to frantically try and keep control of my body, but I can't... I can't stop... I can't...!"

    scene black with dissolve

    mk "Aaaahn!"

    "My mind blanks as every muscle tightens, fingers and toes curling as the pleasure of orgasm wracks my body. Every sense is washed away in an instant as pure wondrous joy floods every corner of my consciousness."

    "I don't know how long it lasts, nor do I care. I'm in bliss. I lose track of everything, even my own self, as I utterly surrender to the feeling washing over me."

    "As I take one step over that peak, the real world begins to rush in to the vacuum within my addled mind. My collapse is all but instantaneous, every last ounce of energy I'd had being utterly exhausted as my hormones, and emotions, crash."

    "I simply flop onto the ground face-first, my limbs having gone entirely limp. Every sense feels muddled and unclear, from the blurry and unfocused ground before me, to my sense of touch barely registering the sweat soaking my body and clothes, and the feeling of Hisao's thick member slipping out."

    "Something warm touching my butt and lower back vaguely registers in my mind, but I don't care. I can't think right now. I just want to lie here, holding on to this feeling."

    "Hisao enters my vision as he sits and then falls back onto the ground, his bare chest heaving from the effort. I try to reach out and brush a couple of hairs sticking to his cheek, but my hand barely gets halfway before flopping on the ground for lack of energy."

    "There we lie, with the boy on his back and I on my front, breathing heavily as we try to recuperate. I manage to weakly smile at him, his hand reaching out and gently brushing some hairs from my forehead."

    mk "You really went all out, didn't you?"

    hi "I was frustrated with you, I guess."

    mk "Still frustrated?"

    hi "I lost track of what I was even annoyed about."

    "As we lie there looking at each other, that sensation I felt on my behind slowly comes back to haunt me."

    mk "You didn't...?"

    "He just averts his eyes. So he did finish himself off onto my back. I just let out a long breath, completely unable to muster anything more notable."

    hi "I wasn't thinking."

    mk "Just get a tissue."

    hi "...I really wasn't thinking."

    mk "You suck."

    "I playfully bat him on the face with what little force I can muster. For all I chide him about thinking too much, he really chooses the worst times."

    stop music fadeout 1.0

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_H10:

    scene bg school_track
    with dissolve

    window show

    play music music_miki

    "I idly watch the scene before me from afar, an impenetrable wall standing between they and I."

    "About seven boys, likely first years by the looks of them, seem to have gotten their hands on a baseball bat and gloves from the storage shed. With their blazers piled near a tree, they've taken to the field with gusto. Not a bad way to kill some time after school's finished for the day, really."

    "The batter lowers himself and brings his bat into position, preparing for the pitch. The posture of his upper body is pretty much right, but his footwork is horrible."

    "The pitcher's tongue flicks along his lips as he focuses himself. A quick look around the field betrays his lack of confidence, needing to reassure himself of where his few friends are standing. Going by the hand he's repeatedly dropping the ball into, it looks like he's a southpaw."

    "I'd put money on the pitcher being the weak link in the game, despite the short-staffed fielding team. They manage to have left field, right field, and the shortstop position covered between them, waiting with ready hands and focused eyes."

    "The catcher nods, and with a long breath, the pitcher pulls his arm back. Everyone, including me, tenses up, waiting for the critical moment."

    "With little warning, that moment arrives. His left arm flies forwards in an unmistakable fastball, his entire body moving with the one goal of getting as much speed on the thing as possible. While he's no professional, the sight of a fit body in such fluid, practiced motion is one of the most impressive things to watch."

    "For an amateur just messing around, he sure put some steam on it. The batter's eyes remain steadfastly on the ball, not shrinking from the challenge."

    play sound sfx_bat_hit

    "The sound of impact echoes around the field as he nails a solid hit, the ball shooting flat and just to the right."

    "...And straight into the stomach of one very unfortunate fielder. Everyone around cringes at the sight."

    "The force of the blow dazes him for a moment before he crumples to the ground, arms clutching at his sore torso. It doesn't take long for his friends to quickly jog over."

    hi "That didn't look fun."

    show hisao_erm_u with dissolve

    "I turn to see Hisao having coming up behind me, eyes still watching the events unfolding ahead."

    mk "Couple o' bruised ribs at least, I'd imagine. That's what happens when you try to play like a pro without the practice to back it up."

    hi "Or the protective gear."

    mk "That too."

    hide hisao_erm_u with dissolve

    "He turns on his heel and gestures for me to follow. Without anything else to do, I shrug and obediently do so."

    scene bg school_dormhisao
    with shorttimeskip

    "As we arrive in Hisao's room, it's his desk that immediately catches my attention. On it sits a couple of textbooks, one open to a bookmarked page, and a notebook before the chair. As Hisao steps back to allow a better view of them, it's hard not to be suspicious."

    show hisao_talk_small_u with dissolve

    hi "Take a seat. Your afterschool study lessons begin today."

    mk "Really?"

    hi "Yes, really."

    hi "I'm not much good at humanities, but since you're managing to just pass those, we can probably afford to skip them."

    mk "Can't we just have some fun in bed, instead? Maybe watch a movie on your laptop or something?"

    show hisao_frown_u with charachange
    hide hisao_talk_small_u

    "He just crosses his arms in response. He's really set his mind to this."

    "Another glance at his desk shows one possible reason. Peeking out from beneath the heavy chemistry textbook lies a couple of glossy university brochures."

    stop music fadeout 3.0

    mk "So this is what brought this on."

    show hisao_erm_u with charachange
    hide hisao_frown_u

    hi "In part. I do want to help, you know."

    mk "You've been doing great at tutoring Suzu, isn't that enough?"

    hi "That's completely beside the point. Why are you so hesitant about applying yourself at school work?"

    mk "I'm not hesitating. I just don't care. There's a difference."

    show hisao_talk_small_u with charachange
    hide hisao_erm_u

    hi "I've heard that before. You'll care an awful lot in a few months, I can tell you that now."

    mk "I already know I'll get some crappy job. Boo hoo."

    play music music_drama fadein 1.0
    show hisao_disappoint_u with charachange
    hide hisao_talk_small_u

    hi "So that's what you think about first..."

    mk "What, you mean this is about us? Together? Come on, I know you'd be cool with being around each other a bit less if we end up in different places."

    hi "But you wouldn't."

    hi "I don't even know why I'm telling you all this. You already knew, didn't you?"

    "Hisao can be sharp when he puts his mind to it, much to my annoyance. As much as I might try to dance around the elephant in the room, he's not letting up in pursuing it."

    mk "This is fun, isn't it? We make a good pair, and life with Haru, Yukio, Suzu, and everyone else is great, too. Even if it can't last forever, can't we just enjoy the time we have?"

    show hisao_frown_u with charachange
    hide hisao_disappoint_u

    hi "So that's all this ever was, in your mind? Just a fling before we gave up and parted at graduation?"

    mk "I'm just being realistic."

    "Those three words hurt him more than I think I've ever managed to in the past. Maybe I didn't understand just how much sway I had over his emotions until now."

    "It's he who breaks the silence."

    hi "Was I ever anything special to you? Something more than some chew toy to throw out once you got bored with it?"

    mk "That's not fair..."

    show hisao_talk_big_u with charachange
    hide hisao_frown_u

    hi "I'm being perfectly fair. I lost everything that was precious to me, but I worked damn hard to get myself back together. Now you're just going to flake out on me? Shrug and say you've had enough?"

    mk "Well pardon me for drawing the short straw in life!"

    mk "You have money, a normal family, you're smart, and you'll probably get into some nice, poncy university. You won, well done. Teacher Nakai has a nice ring to it, doesn't it?"

    mk "I tried, man. I worked my guts out, and look at where it got me. Stop being a dick just because not all of us can be as lucky as you."

    show hisao_frown_u with charachange
    hide hisao_talk_big_u

    hi "Yeah... real lucky."

    mk "I-"

    "Apologising is the last thing I want to do, but I didn't mean to wound him like that. All I can do is grit my teeth, accepting the anger he must feel in me right now."

    hi "I just want to help you. I love you, Miki."

    mk "Really? 'Cause from where I'm standing, it looks more like you fell for who you thought you could make me into."

    show hisao_talk_big_u with charachange
    hide hisao_frown_u

    hi "So it's my fault you only want to be around me for a few months? Is that what you call love?"

    mk "I thought you'd finally become someone pretty cool after all this time, but it turns out you're just a bore who hides behind his arrogance."

    show hisao_frown_u with charachange
    hide hisao_talk_big_u

    hi "Take that back."

    mk "Piss off. You're the one talking down to me."

    "It's only by clenching my fist until my knuckles whiten that I stave off the adrenaline coursing through me, but as he continues looking at me with eyes of pure contempt, I feel my body preparing to lash out."

    play sound sfx_doorslam

    scene bg school_dormhallway
    with locationchange

    "Left with no other outlet, I quickly turn around and punch his door on the way out of his dormitory room. Arguing with the asshole any longer isn't going to change his mind."

    hi "Miki, come back!"

    "I don't bother turning back as I hear his voice coming from behind me. I don't even want to see his stupid mug right now."

    mk "Like Hell I will. Have a nice life at university, asshole!"

    scene black
    with dissolve

    "I misjudged him. I took his changing personality to mean he was like me, relearning how to enjoy life after such radical change, but it looks like he's more interested in lording himself over others."

    "I don't need someone like that."

    stop music fadeout 2.0
    with Pause(3.0)

    window hide

    scene black
    with dissolve

    scene black with fadeslow
    $stop_music()
    $renpy.pause(1.0)
    $start_music(music_timeskip)
    show kslogoheart at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    show kslogowords at Position(xpos=158, ypos=150, xanchor=0, yanchor=0) with passingoftime
    $renpy.pause(2.0)
    $renpy.music.stop(fadeout=2.0)
    show solid_black with passingoftime

    ##return

label en_H11:

    scene school_dormmiki
    with dissolve

    $ renpy.music.set_volume(0.6, 0.0, channel="ambient")

    queue ambient [ sfx_impact, sfx_void, sfx_void ]

    window show
    show haru_serious at leftsit with dissolve
    show yukio_notimpressed at right with dissolve

    play music music_caged_heart

    "I idly hit the back of my head repeatedly against a dresser in my room, sitting on the floor as Yukio leans against my desk and Haru sits on the side of my bed. It's been a while since we had an impromptu meeting like this, but they soon agreed after I recounted what happened."

    har "That ain't gonna help."

    stop ambient fadeout 0.3

    mk "It doesn't hurt, either."

    "Yukio just crosses his arms, moving on to more important matters."

    yuk "You screwed up."

    mk "Tell me something I don't know."

    show haru_annoyed at leftsit with charamove
    hide haru_serious at leftsit

    har "Are you two gonna fight again? Right now?"

    yuk "I'm just telling her the truth."

    yuk "To be honest, I saw this coming. I don't think I'm the only one, either."

    show haru_serious at leftsit with charamove
    hide haru_annoyed at leftsit

    har "You're not the type to be tied down, that's for sure."

    "I give a grin at the at the comment, which earns a quick rebuke from the other."

    show yukio_angry at right with charachange
    hide yukio_notimpressed at right

    yuk "That's not a good thing. For all the fun you're having now, eventually you'll need to face life outside. You might have your head on straight compared to your early days in Yamaku, but that doesn't mean anything in the outside world."

    yuk "Quite frankly, I don't blame Hisao for trying to slap that into you."

    "So he's taking Hisao's side in this. That's not a shock given Yukio's straight-laced nature, but it still sucks."

    show haru_basic at leftsit with charamove
    hide haru_serious at leftsit

    "Haru's impish smile takes my mind off the unwanted lecture I'm getting."

    mk "What's with you?"

    har "This isn't about some attempt to get you to study, is it?"

    "I move to protest, but a little voice at the back of my mind tells me that he's not entirely wrong. It is true that I don't care about my academic results; I'm too far gone to recover my grades now, and what's the point anyway when one unlucky turn could take it all away again?"

    "I don't think I'd have the strength to endure that. Not again."

    "What most echoes in my mind since our argument, though, isn't the words spoken. It's the way Hisao looked. I don't think I've ever hurt a person like that before."

    mk "Why does everyone else seem more clued in to this than me?"

    show yukio_huh at right with charachange
    hide yukio_angry at right

    yuk "Sometimes looking in from the outside is what's needed. We can get stuck in our own heads and unable to view a situation objectively."

    mk "I don't get it."

    show haru_sad at leftsit with charamove
    hide haru_basic at leftsit

    har "Yeah, me neither."

    show yukio_angry at right with charachange
    hide yukio_huh at right

    yuk "I'm surrounded by idiots..."

    yuk "I don't know what you really expect from us, Miki. As much as I'd like to wave a magic wand and make this all go away, you're gonna have to deal with him eventually."

    show haru_serious at leftsit with charamove
    hide haru_sad at leftsit

    har "He's right, you know."

    har "You know, it's not like you have to be going out to be together. You got along just fine as friends, didn't you?"

    show yukio_notimpressed at right with charachange
    hide yukio_angry at right

    yuk "The oaf is right; being friends isn't any better or worse than lovers."

    mk "You say that like you have experience. Hitting on random girls doesn't count."

    show yukio_angry at right with charachange
    hide yukio_notimpressed at right

    yuk "You shouldn't make assumptions."

    mk "Oh?"

    "Yukio just closes his eyes, frustrated with me for trying to change the topic onto him. As much as we may fight, his uncompromising attitude can be helpful sometimes."

    "With a snort, he stops leaning on the desk and starts to leave."

    har "Where're you goin'?"

    yuk "Far as I see it, there's not much point being here."

    yuk "I don't mind being used as a scratching post, Miki, but you don't even know what it is you want to do."

    mk "What should I do?"

    yuk "I don't know, and neither would Haru. Work out whatever will leave you with no regrets, that's all I can tell you."

    hide yukio_angry with moveoutright

    queue sound [ sfx_dooropen, sfx_void, sfx_doorclose ]

    "With that, he leaves. Haru just stays where he is, doing his best to not look too serious about all this."

    mk "Why do I feel like I just got scolded."

    har "Because you did."

    mk "So what do you think about all this?"

    har "I just want everyone to be happy. That's pretty much it."

    mk "I don't think I've ever seen you anything other than happy. How do you manage that all the time?"

    show haru_smile at leftsit with charamove
    hide haru_serious at leftsit

    har "You just gotta smile. It's hard to feel sad when you have a big grin on your face."

    mk "Yeah... I guess."

    show haru_smile at left with charamove

    "He brings his legs out before levering himself off the bed, clapping me on the shoulder as I take to my feet."

    show haru_basic at left with charamove
    hide haru_smile at left

    har "You shouldn't worry so much. It's weird to see you so concerned about something."

    mk "I know..."

    har "You'll work it out. If there's one thing I've learned about you, it's that you're a stronger person than most."

    har "To be honest, I've always admired that about you."

    mk "Thanks. You're a good friend. And Yukio too, when he isn't being an ass."

    show haru_smile at left with charamove
    hide haru_basic at left

    "Haru just laughs."

    har "That's more like it. Good luck, Miki."

    hide haru_smile with moveoutright
    queue sound [ sfx_dooropen, sfx_void, sfx_doorclose ]

    stop music fadeout 3.0

    "We give our goodbyes to each other as he leaves, my room becoming empty once again."

    "I might not know what I want, but I do know what I don't want. The silence of an empty room. The loneliness of being without friends. In other words, the life I'd lived before in Yamaku."

    "As I look out my window, a decision soon forms in my mind."

    "After all, one thing has always stayed constant, no matter what's happened around me in life."

    ##centered "~ Timeskip ~" with dissolve
    scene bg roadside with shorttimeskip

    play music music_lullaby

    "It's been a damn long time since I've punished my body like this before. I don't even know precisely where this is, my legs carrying me a good distance beyond the small town below Yamaku."

    play sound sfx_pillow

    "I barely even managed to get off the road before collapsing beside it, utterly drained of every ounce of energy I had."

    "Try as I might, my arms and legs simply refuse to move. All I can do is lay helplessly on my back, chest heaving as my body grabs at any oxygen it can."

    scene bg misc_sky
    with dissolve

    "My eyes have trouble focusing, but it's not like there's much to look at. Just a blue, cloudless sky looming above, impossibly vast compared to the insignificance of me and my collapsed body."

    "I've seen this sight before, come to think of it. After I'd messed up once again. Guess that's a pretty shitty thing to associate with a nice summer's day."

    "A bird soars overhead, squawking as it reaches out with its great wings and begins to glide on the air. I briefly wonder if it's teasing me."

    "That is, before I get a solid kick directed at the side of my ribs."

    with hpunch

    mk "Ow!"

    "I roll my head slightly to see who's stuck their foot into me, only to find the wind taken out of my sails."

    mk "Oh. It's you."

    show hisao_disappoint_u with dissolve

    "Hisao just looks down at me, his face flat. Try as I might, I just can't get a read on him at all, and he isn't saying anything."

    mk "So why are you here?"

    hi "To make things clear. I've had enough of being dumped the easy way."

    play sound sfx_sitting

    show hisao_disappoint_u at centersit with charamove

    "He lowers himself to the ground, taking a seat beside my slowly recovering body. Silence ensues as we both end up watching the bird hovering above us, barely making any headway as it rides the breeze."

    mk "How'd you find me?"

    hi "A one-handed girl running through the campus and local town in the male uniform isn't exactly subtle."

    "He has a point. I never have been the subtle type, after all."

    "The letter of his I managed to find bubbles into my memory. I can't remember much of it, but I can see his point. Getting dumped would be hard enough, let alone when the other side doesn't care enough about you to do it properly."

    mk "You came all this way to make sure it was you who was dumping me. How terrible."

    show hisao_talk_small_u at centersit with charachange
    hide hisao_disappoint_u at centersit

    hi "Don't put words in my mouth."

    "I never thought it would happen, but Hisao's completely managed to take hold of the conversation. Between his placid face, brief replies, and near-monotone voice, I've little choice but to let him talk as he wants."

    show hisao_disappoint_u at centersit with charachange
    hide hisao_talk_small_u at centersit

    hi "It's a funny place, this."

    hi "Half in the country, half in the city. A school for students with disabilities; an idea strange enough to feel surreal when you first enrol, but utterly normal once you've been here a while. Isolated enough that some are dumped here to hide them away, but with staff and facilities so good that others think it's their kid's best chance."

    mk "I have to admit, I've only ever seen it as just another school. Sure, most of the students have disabilities of whatever kind, but it's still just a bunch of regular teenagers, and some teachers trying and make them learn."

    hi "All depends on your point of view, I guess. Just like everything."

    mk "Are we seriously gonna do the 'say sorry to each other and make up' thing?"

    hi "Not at all. I stand by what I said."

    mk "Well... Good, because I stand by what I said, too."

    "The silence afterwards makes me wonder if I said the right thing. I'm still confused why he's even wanting to talk to me, or why I'm not questioning him about it. I've totally let myself get caught in his pace."

    "Unless he's just dancing around what he really wants to say. Now that I think about it... that really is something he'd do."

    play sound sfx_sitting

    scene bg roadside with dissolve
    show hisao_disappoint_u at centersit with dissolve

    "Still sore from my running, I manage to sit myself up with some difficulty."

    mk "I'm not buying the poker face thing. Out with it, Hisao."

    hi "In the end, I just can't keep up with you. You might want me to run about and play rough, but I just can't do that anymore. I wish I could."

    mk "Well what about me? It's too late for me to rescue my studies, and I'm an idiot anyway. Sure, I might get some scholarship or another, but I'd just flunk the academics anyway."

    mk "We started from such a similar place, but our paths are already drifting apart so fast..."

    "This always happens, after all. Given enough time, everyone I enjoy spending life with slips from my fingers. It's just the same for him, given his friends and his ex. Is it really so wrong to admit that, and just enjoy the present?"

    show hisao_frown_u at centersit with charachange
    hide hisao_disappoint_u at centersit

    hi "I don't want to let go, Miki. I know you don't either, no matter what you said."

    mk "It's going to happen again. It always does."

    hi "So you're not going to even try? That's not the Miki I fell for."

    show hisao_talk_small_u at centersit with charachange
    hide hisao_frown_u at centersit

    hi "You worked so hard in your baseball team, and your body is proof you kept working hard at staying physically strong. You made such tight bonds with the friends you had back home, and with the ones at Yamaku, too."

    hi "Maybe you're right, and it will fall apart. Maybe we might get into the same university, or we might not. We might not stay together even if we do."

    hi "But I want to try, Miki. Because I love you."

    stop music fadeout 5.0

    "It feels like Hisao has my heart in his hands, gently squeezing as he stares at me with those eyes. It's not that he's begging, but... hoping. This is what hope looks like."

    "After all this time, I'd forgotten what that was like. All I can do in response is give a long sigh."

    mk "It's ironic, isn't it? The first time we truly feel like a couple, is after we've broke up."

    play music music_pearly fadein 3.0

    show hisao_smile_u at centersit with charachange
    hide hisao_talk_small_u at centersit

    hi "We don't need to stay that way."

    mk "You really are a hopeless romantic, you know that?"

    hi "Is that a bad thing?"

    mk "Don't put words in my mouth."

    "There is it again; I really do like that smile of his. I could forgive a lot about him, just for the chance to see more of that face."

    play sound sfx_rustling

    show hisao_smile_u at center with charamove

    "As I take to my feet and dust myself off, Hisao doing the same. For some reason, I don't feel tired at all."

    mk "Whatever am I gonna do with you, boy?"

    hi "Perhaps... go out with me again, together?"

    mk "'Together', huh?"

    "I give a grin as I swing my arm around Hisao's neck."

    mk "That doesn't sound so bad when you say it."

    "With that, I put one foot ahead of the other as I begin to walk once more, Hisao being dragged along. I don't think I've seen where this road leads ahead of here, after all."

    show hisao_wtf_u with charachange
    hide hisao_smile_u

    hi "Wait, hold on! Where are we even going!?"

    mk "Anywhere we want to, boy!"

    show hisao_smile_u with charachange
    hide hisao_wtf_u

    "He just gives a snort of laughter, smiling as I drag him along."

    "I guess we're both going to change in the weeks, months, and years ahead. That's how life is, though. You can't just set things up the way you want them, and expect it to go on forever."

    "Like this, the two of us will walk towards that unknown future ahead of us. Together."

    window hide

    stop ambient fadeout 2.0

    stop music fadeout 2.0

    scene black
    with Fade(2.0, 0.5, 0)

    play sound sfx_whiteout

    play music music_credits fadein 2.0

    call credits from _call_credits_1

    return
