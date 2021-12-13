# Stepper motor class
#
# Assumes the following is done in the calling code:
# import RPi.GPIO as GPIO
# import time
# GPIO.setmode(GPIO.BCM)

class stepper:
  def __init__(self,p1,p2,p3,p4):
    self.currentAngle = 0
    self.minDelayTime = 970   # shortest allowed delay (motor-specific)
    self.seq = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
                 [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]
    self.seq.reverse()      # reverse for CW = forward steps in seq
    self.currentState = 0   # track position in 8-step sequence

    # find number of halfsteps per degree of rotation, with
    # 512 cycle/rev * 1/360 rev/deg * 8 halfstep/cycle
    self.halfstepsPerDegree = 512*8/360

    self.pins = [p1,p2,p3,p4] # controller inputs: in1, in2, in3, in4
    for pin in self.pins:
      GPIO.setup(pin, GPIO.OUT, initial=0)

  # Private methods:

  def __delay_us(tus): # use microseconds to improve time resolution
    endTime = time.time() + float(tus)/ float(1E6)
    while time.time() < endTime:
      pass

  def __sgn(val):   # signum function
    return(int(val/abs(val)))

  def __halfStep(self, dir):
    self.currentState += dir
    if self.currentState > 7:
      self.currentState = 0
    elif self.currentState < 0:
      self.currentState = 7
    for pin in range(4):
      GPIO.output(self.pins[pin], self.seq[self.currentState][pin])
    self.currentAngle += dir/self.halfstepsPerDegree
    print("angle = {:.2f}".format(self.currentAngle))

  def __turnSteps(self, numSteps, dir, speed):
    for s in range(numSteps):
      self.__halfStep(dir)
      self.__delay_us(self.minDelayTime/speed)

  # Public methods:

  def goAngle(self, newAngle, speed):
    deltaAngle = newAngle - self.currentAngle
    if abs(deltaAngle) > 180:
      deltaAngle = (abs(deltaAngle)-180)*(-self.__sgn(deltaAngle))
    if speed > 1:
      speed = 1
    elif speed <= 0:
      speed = 0.05
    numSteps = abs(int(self.halfstepsPerDegree * deltaAngle))
    self.__turnSteps(numSteps, self.__sgn(deltaAngle), speed)

  def zero(self, pin, high_or_low=1, dir=1, speed=1):
    # pin = GPIO pin to check for zero state
    # high_or_low = value to trigger zero state (1 or 0)
    # dir = direction to seek zero (cw=1, ccw=-1)
    # speed = fractional movement speed (0->1)
    GPIO.setup(pin, GPIO.IN)
    while (GPIO.input(pin) ^ ~high_or_low) & 1:
      self.__turnSteps(1, dir, speed)
    self.currentAngle = 0

try:
  motor = stepper(18,23,24,25)
  motor.goAngle(90, 0.8)   # (angle, speed speed)
  motor.zero(pin=12, high_or_low=1, dir=-1, speed=0.5)
except Exception as e:
  print(e)
GPIO.cleanup()