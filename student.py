import pigo
import time  # import just in case students need
import random

# setup logs
import logging
LOG_LEVEL = logging.INFO
LOG_FILE = "/home/pi/PnR-Final/log_robot.log"  # don't forget to make this file!
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


class Piggy(pigo.Pigo):
    """Student project, inherits teacher Pigo class which wraps all RPi specific functions"""

    def __init__(self):
        """The robot's constructor: sets variables and runs menu loop"""
        print("I have been instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 90
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 30
        self.HARD_STOP_DIST = 15
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 80
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 70
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.menu()

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "c": ("Calibrate", self.calibrate),
                "t": ("Test restore heading", self.test_restore_heading),
                "s": ("Check status", self.status),
                "q": ("Quit", quit_now)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    # YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        """executes a series of methods that add up to a compound dance"""
        print("\n---- LET'S DANCE ----\n")
        ##### WRITE YOUR FIRST PROJECT HERE
        if self.safety_check():
            self.to_the_right()
            self.to_the_left()
            self.now_kick()
            self.walk_it_by_yourself()
            self.electric_slide()

    def obstacle_count(self):
        """scans and estimates the number of obstacles within sight"""
        for x in range(1):
            self.wide_scan()
            found_something = False
            counter = 0
            for distance in self.scan:
                if distance and distance < 60 and not found_something:
                    found_something = True
                    counter += 1
                    print("Object # %d found, I think" % counter)
                if distance and distance > 60 and found_something:
                    found_something = False
            print("\n----I SEE %d OBJECTS----\n" % counter)

    def safety_check(self):
        self.servo(self.MIDPOINT)   # look straight ahead
        for x in range(4):
            if not self.is_clear():
                print("NOT GOING TO DANCE")
                return False
            print("Check #%d" % (x + 1))
            self.encR(8)  # figure out 90 deg
            """moves in a 360 degree circle while moving servo to check for obstacles"""
        print("Safe to dance!")
        return True

        #loop 3 times
            #  turn 90 deg
        # scan again

    def to_the_right(self):
        """subroutine of dance method"""
        for x in range(4):
            self.encR(10)
            self.encF(5)

    def to_the_left(self):
        """subroutine of dance method"""
        for x in range(4):
            self.encL(10)
            self.encF(5)

    def now_kick(self):
        """subroutine of dance method"""
        for ang in range(60, 120, 10):
            """loops in an arc and moves servo"""
            self.servo(ang)
            time.sleep(.2)

    def walk_it_by_yourself(self):
        """subroutine of dance method"""
        for x in range(4):
            self.encF(5)
            self.encB(5)

    def electric_slide(self):
        """subroutine of dance method"""
        for x in range(4):
            self.servo(40)
            self.encL(5)
            self.servo(10)
            self.encR(5)
            self.encF(5)
            self.servo(40)
            self.encB(5)
            self.servo(60)
            self.encR(5)

        print("\n--- Ta-Da! ---\n")

    def restore_heading(self):
        """
        Uses self.turn_track to reorient to original heading
        """
        print("Restoring heading!")
        if self.turn_track > 0:
            self.encL(abs(self.turn_track))
        elif self.turn_track < 0:
            self.encR(abs(self.turn_track))

    def test_restore_heading(self):
        self.encR(5)
        self.encL(13)
        self.encR(10)
        self.encR(9)
        self.encL(3)
        self.restore_heading()

    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        self.obstacle_count()
        # counts obstacles before beginning nav
        while True:
            if self.is_clear():
                self.cruise()
            else:
                self.encR(8)
                if self.is_clear():
                    self.cruise()
                else:
                    self.encB(4)
                    # backs up to scan surroundings and find clear path
                    self.encL(27)
                    if self.is_clear():
                        self.cruise()
                    # check right and go if clear
                    # look left twice and then go



    def cruise(self):
        """drive straight while path is clear"""
        self.fwd()
        print("\n---- I'M ABOUT TO DRIVE FORWARD! ----\n")
        while(self.dist() > self.SAFE_STOP_DIST):
            time.sleep(.5)
        self.stop()




####################################################
############### STATIC FUNCTIONS

def error():
    """records general, less specific error"""
    logging.error("ERROR")
    print('ERROR')


def quit_now():
    """shuts down app"""
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy


try:
    g = Piggy()
except (KeyboardInterrupt, SystemExit):
    pigo.stop_now()
except Exception as ee:
    logging.error(ee.__str__())
