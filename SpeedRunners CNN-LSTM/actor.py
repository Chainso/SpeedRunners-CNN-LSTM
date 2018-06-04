import pyvjoy
import time

class Actor():
    def __init__(self):
        self._vjoy = pyvjoy.VJoyDevice(2)
        self.reset_vjoy()

        self._min_vjoy = 0
        self._max_vjoy = 32786
        self._neutral_vjoy = self._max_vjoy // 2
        
        # All the buttons for the game configuration
        self._jump = 1
        self._grapple = 3
        self._slide = 4
        self._item = 2

        # All the buttons being used
        self._buttons = [self._jump, self._grapple, self._slide, self._item]

        # Reset the controller
        self.reset()
        self.reset_buts()
        self.reset_boost()

        # The last action that was taken
        self._last_command = ""

    def boost(self):
        self._vjoy.set_axis(pyvjoy.HID_USAGE_RZ, self._max_vjoy)

    def left(self):
        if(self._last_command != "left"):
            self.reset("left")
            self.reset_buts()
            self._vjoy.set_axis(pyvjoy.HID_USAGE_X, self._min_vjoy)
            self.reset_boost()

            time.sleep(0.00000001)

            self._last_command = "left"

    def left_boost(self):
        if(self._last_command != "left_boost"):
            self.reset()
            self.reset_buts()
            self._vjoy.set_axis(pyvjoy.HID_USAGE_X, self._min_vjoy)
            self.boost()

            time.sleep(0.00000001)

            self._last_command = "left_boost"

    def right(self):
        if(self._last_command != "right"):
            self.reset()
            self.reset_buts()
            self._vjoy.set_axis(pyvjoy.HID_USAGE_X, self._max_vjoy)
            self.reset_boost()

            time.sleep(0.00000001)

            self._last_command = "right"

    def right_boost(self):
        if(self._last_command != "right_boost"):
            self.reset()
            self.reset_buts()
            self._vjoy.set_axis(pyvjoy.HID_USAGE_X, self._max_vjoy)
            self.boost()

            time.sleep(0.00000001)

            self._last_command = "right_boost"

    def jump(self):
        if(self._last_command != "jump"):
            self.reset("right")
            self.reset_buts([self._jump])
            self._vjoy.set_button(self._jump, 1)
            self.reset_boost()

            time.sleep(0.00000001)

            self._last_command = "jump"

    def jump_boost(self):
        if(self._last_command != "jump_boost"):
            self.reset("right")
            self.reset_buts([self._jump])
            self._vjoy.set_button(self._jump, 1)
            self.boost()

            time.sleep(0.00000001)

            self._last_command = "jump_boost"

    def jump_left(self):
        if(self._last_command != "jump_left"):
            self.reset("left")
            self.reset_buts([self._jump])
            self._vjoy.set_axis(pyvjoy.HID_USAGE_X, self._min_vjoy)
            self._vjoy.set_button(self._jump, 1)
            self.reset_boost()

            time.sleep(0.00000001)

            self._last_command = "jump_left"

    def jump_left_boost(self):
        if(self._last_command != "jump_left_boost"):
            self.reset("left")
            self.reset_buts([self._jump])
            self._vjoy.set_axis(pyvjoy.HID_USAGE_X, self._min_vjoy)
            self._vjoy.set_button(self._jump, 1)
            self.boost()

            time.sleep(0.00000001)

            self._last_command = "jump_left_boost"


    def jump_right(self):
        if(self._last_command != "jump_right"):
            self.reset("right")
            self.reset_buts([self._jump])
            self._vjoy.set_axis(pyvjoy.HID_USAGE_X, self._max_vjoy)
            self._vjoy.set_button(self._jump, 1)
            self.reset_boost()

            time.sleep(0.00000001)

            self._last_command = "jump_right"

    def jump_right_boost(self):
        if(self._last_command != "jump_right_boost"):
            self.reset("right")
            self.reset_buts([self._jump])
            self._vjoy.set_axis(pyvjoy.HID_USAGE_X, self._max_vjoy)
            self._vjoy.set_button(self._jump, 1)
            self.boost()

            time.sleep(0.00000001)

            self._last_command = "jump_right_boost"

    def grapple(self):
        if(self._last_command != "grapple"):
            self.reset()
            self.reset_buts([self._grapple])
            self._vjoy.set_button(self._grapple, 1)
            self.reset_boost()

            time.sleep(0.00000001)

            self._last_command = "grapple"

    def grapple_left(self):
        if(self._last_command != "grapple_left"):
            self.reset("left")
            self.reset_buts([self._grapple])
            self._vjoy.set_axis(pyvjoy.HID_USAGE_X, self._min_vjoy)
            self._vjoy.set_button(self._grapple, 1)
            self.reset_boost()

            time.sleep(0.00000001)

            self._last_command = "grapple_left"

    def grapple_right(self):
        if(self._last_command != "grapple_right"):
            self.reset("right")
            self.reset_buts([self._grapple])
            self._vjoy.set_axis(pyvjoy.HID_USAGE_X, self._max_vjoy)
            self._vjoy.set_button(self._grapple, 1)
            self.reset_boost()

            time.sleep(0.00000001)

            self._last_command = "grapple_right"

    def item(self):
        if(self._last_command != "item"):
            self.reset()
            self.reset_buts([self._item])
            self._vjoy.set_button(self._item, 1)
            self.reset_boost()

            time.sleep(0.00000001)

            self._last_command = "item"

    def item_boost(self):
        if(self._last_command != "item_boost"):
            self.reset()
            self.reset_buts([self._item])
            self._vjoy.set_button(self._item, 1)
            self.boost()

            time.sleep(0.00000001)

            self._last_command = "item_boost"

    def item_left(self):
        if(self._last_command != "item_left"):
            self.reset("left")
            self.reset_buts([self._item])
            self._vjoy.set_axis(pyvjoy.HID_USAGE_X, self._min_vjoy)
            self._vjoy.set_button(self._item, 1)
            self.reset_boost()

            time.sleep(0.00000001)

            self._last_command = "item_left"

    def item_left_boost(self):
        if(self._last_command != "item_left_boost"):
            self.reset("left")
            self.reset_buts([self._item])
            self._vjoy.set_axis(pyvjoy.HID_USAGE_X, self._min_vjoy)
            self._vjoy.set_button(self._item, 1)
            self.boost()

            time.sleep(0.00000001)

            self._last_command = "item_left_boost"

    def item_right(self):
        if(self._last_command != "item_right"):
            self.reset("right")
            self.reset_buts([self._item])
            self._vjoy.set_axis(pyvjoy.HID_USAGE_X, self._max_vjoy)
            self._vjoy.set_button(self._item, 1)
            self.reset_boost()

            time.sleep(0.00000001)

            self._last_command = "item_right"

    def item_right_boost(self):
        if(self._last_command != "item_right_boost"):
            self.reset("right")
            self.reset_buts([self._item])
            self._vjoy.set_axis(pyvjoy.HID_USAGE_X, self._max_vjoy)
            self._vjoy.set_button(self._item, 1)
            self.boost()

            time.sleep(0.00000001)

            self._last_command = "item_right_boost"

    def slide(self):
        #if(self._last_command != "slide"):
        self.reset()
        self.reset_buts([self._slide])
        self._vjoy.set_button(self._slide, 1)
        self.reset_boost()
        time.sleep(0.00000001)

        self._last_command = "slide"

    def reset(self, direction = ""):
        if(not (((self._vjoy.data.wAxisX == self._min_vjoy) and direction == "left")
           or ((self._vjoy.data.wAxisX == self._max_vjoy) and direction == "right"))):
            self._vjoy.set_axis(pyvjoy.HID_USAGE_X, self._neutral_vjoy)

    def reset_buts(self, but=[]):
        for button in self._buttons:
            if(not button in but):
                self._vjoy.set_button(button, 0)

    def reset_vjoy(self):
        self._vjoy.reset()
        self._vjoy.reset_buttons()
        self._vjoy.reset_povs()

    def reset_boost(self):
        self._vjoy.set_axis(pyvjoy.HID_USAGE_RZ, 0)
