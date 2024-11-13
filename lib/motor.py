from machine import Pin, PWM

class DCMotor:
  def __init__(self, in_gpio_pin_1: int, in_gpio_pin_2: int):
    self.in1 = Pin(in_gpio_pin_1, Pin.OUT)
    self.in2 = Pin(in_gpio_pin_2, Pin.OUT)
    self.stop()

  def forward(self):
    self.in1.value(1)
    self.in2.value(0)

  def reverse(self):
    self.in2.value(1)
    self.in1.value(0)

  def stop(self):
    self.in1.value(0)
    self.in2.value(0)

class DCMotorDuty(DCMotor):
  def __init__(self, in_gpio_pin_1: int, in_gpio_pin_2: int, min_duty: int = 700):
    super().__init__(in_gpio_pin_1, in_gpio_pin_2)
    self.min_duty = min_duty
    self.pwm_in_1= PWM(self.in1)
    self.pwm_in_2 = PWM(self.in2)
    self.duty = self.min_duty
    self.stop()

  def set_duty(self, duty: int = None):
    if duty > 1023 or duty < self.min_duty:
      return
    self.duty = duty

    for p in [self.pwm_in_1, self.pwm_in_2]:
      if p.duty() != 0:
        p.duty(self.duty)

  def forward(self):
    self.pwm_in_1.duty(self.duty)
    self.pwm_in_2.duty(0)

  def reverse(self):
    self.pwm_in_2.duty(self.duty)
    self.pwm_in_1.duty(0)

  def stop(self):
    self.pwm_in_2.duty(0)
    self.pwm_in_1.duty(0)

