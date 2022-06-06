# -*- coding: utf-8 -*-

# SuspendExceptions and hold and release are the only dependencies for pyautogui
# If you want to use a different automation library, you only need to reimplement them
import pyautogui
SuspendExceptions = (KeyboardInterrupt, pyautogui.FailSafeException)

def hold(button):
  pyautogui.keyDown(button.value)

def release(button):
  pyautogui.keyUp(button.value)



import time, random, json, enum, os, math
random = random.SystemRandom()

with open('config.json', 'r') as f: CONFIG = json.load(f)

with open('text.txt', 'r') as f:
  TEXT = {}
  for line in filter(len, (i.strip() for i in f)):
    if line.endswith(':'):
      current = line[:-1]
      TEXT[current] = []
    else:
      TEXT[current].append(line)

Button = enum.Enum('Button', CONFIG['Keys'])

def tap(button):
  hold(button)
  time.sleep(CONFIG['Tap Duration'])
  release(button)
  time.sleep(CONFIG['Post Tap Duration'])

def tap_n_times(button, n):
  for _ in range(n):
    tap(button)

def countdown(n = 5):
  for i in range(n, 0, -1):
    vprint(i)
    time.sleep(1)

def vprint(*msgs):
  if CONFIG['Verbose']:
    print(*msgs)

def get_weight(item):
  try:
    return CONFIG[item.name.replace('_', ' ')+' Weight']
  except AttributeError:
    return CONFIG[item['name']+' Weight']


def weighted_random_choice(choices):
  total = sum((get_weight(i) for i in choices))
  r = random.uniform(0, total)
  for i in choices:
    weight = get_weight(i)
    if r < weight:
      return i
    r -= weight


def set_slider_value(initial_value, desired_value, rate):
  vprint(f'  Setting to {desired_value} from {initial_value}')

  delta = desired_value - initial_value
  if delta == 0:
    return

  button = Button.Left if delta < 0 else Button.Right
  hold(button)
  time.sleep(abs(delta)/rate)
  release(button)

def set_slider_value_with_taps(initial_value, desired_value):
  delta = desired_value - initial_value
  if delta == 0:
    return
  button = Button.Left if delta < 0 else Button.Right
  tap_n_times(button, abs(delta))


class KeyboardMode(enum.Enum):
  LOWER = 0
  FOREIGN = 1
  SYMBOLS = 2
  ALL_CAPS = 3
  ALL_MODES = 4 # Special case for numbers

KEYBOARD_LAYOUT = {
  '1': (KeyboardMode.ALL_MODES, 0, 0),
  '2': (KeyboardMode.ALL_MODES, 1, 0),
  '3': (KeyboardMode.ALL_MODES, 2, 0),
  '4': (KeyboardMode.ALL_MODES, 3, 0),
  '5': (KeyboardMode.ALL_MODES, 4, 0),
  '6': (KeyboardMode.ALL_MODES, 5, 0),
  '7': (KeyboardMode.ALL_MODES, 6, 0),
  '8': (KeyboardMode.ALL_MODES, 7, 0),
  '9': (KeyboardMode.ALL_MODES, 8, 0),
  '0': (KeyboardMode.ALL_MODES, 9, 0),
  'a': (KeyboardMode.LOWER, 0, 1),
  'b': (KeyboardMode.LOWER, 1, 1),
  'c': (KeyboardMode.LOWER, 2, 1),
  'd': (KeyboardMode.LOWER, 3, 1),
  'e': (KeyboardMode.LOWER, 4, 1),
  'f': (KeyboardMode.LOWER, 5, 1),
  'g': (KeyboardMode.LOWER, 6, 1),
  'h': (KeyboardMode.LOWER, 7, 1),
  'i': (KeyboardMode.LOWER, 8, 1),
  'j': (KeyboardMode.LOWER, 9, 1),
  'k': (KeyboardMode.LOWER, 0, 2),
  'l': (KeyboardMode.LOWER, 1, 2),
  'm': (KeyboardMode.LOWER, 2, 2),
  'n': (KeyboardMode.LOWER, 3, 2),
  'o': (KeyboardMode.LOWER, 4, 2),
  'p': (KeyboardMode.LOWER, 5, 2),
  'q': (KeyboardMode.LOWER, 6, 2),
  'r': (KeyboardMode.LOWER, 7, 2),
  's': (KeyboardMode.LOWER, 8, 2),
  't': (KeyboardMode.LOWER, 9, 2),
  'u': (KeyboardMode.LOWER, 0, 3),
  'v': (KeyboardMode.LOWER, 1, 3),
  'w': (KeyboardMode.LOWER, 2, 3),
  'x': (KeyboardMode.LOWER, 3, 3),
  'y': (KeyboardMode.LOWER, 4, 3),
  'z': (KeyboardMode.LOWER, 5, 3),
  'A': (KeyboardMode.ALL_CAPS, 0, 1),
  'B': (KeyboardMode.ALL_CAPS, 1, 1),
  'C': (KeyboardMode.ALL_CAPS, 2, 1),
  'D': (KeyboardMode.ALL_CAPS, 3, 1),
  'E': (KeyboardMode.ALL_CAPS, 4, 1),
  'F': (KeyboardMode.ALL_CAPS, 5, 1),
  'G': (KeyboardMode.ALL_CAPS, 6, 1),
  'H': (KeyboardMode.ALL_CAPS, 7, 1),
  'I': (KeyboardMode.ALL_CAPS, 8, 1),
  'J': (KeyboardMode.ALL_CAPS, 9, 1),
  'K': (KeyboardMode.ALL_CAPS, 0, 2),
  'L': (KeyboardMode.ALL_CAPS, 1, 2),
  'M': (KeyboardMode.ALL_CAPS, 2, 2),
  'N': (KeyboardMode.ALL_CAPS, 3, 2),
  'O': (KeyboardMode.ALL_CAPS, 4, 2),
  'P': (KeyboardMode.ALL_CAPS, 5, 2),
  'Q': (KeyboardMode.ALL_CAPS, 6, 2),
  'R': (KeyboardMode.ALL_CAPS, 7, 2),
  'S': (KeyboardMode.ALL_CAPS, 8, 2),
  'T': (KeyboardMode.ALL_CAPS, 9, 2),
  'U': (KeyboardMode.ALL_CAPS, 0, 3),
  'V': (KeyboardMode.ALL_CAPS, 1, 3),
  'W': (KeyboardMode.ALL_CAPS, 2, 3),
  'X': (KeyboardMode.ALL_CAPS, 3, 3),
  'Y': (KeyboardMode.ALL_CAPS, 4, 3),
  'Z': (KeyboardMode.ALL_CAPS, 5, 3),
  '.': (KeyboardMode.SYMBOLS, 0, 1),
  ',': (KeyboardMode.SYMBOLS, 1, 1),
  '!': (KeyboardMode.SYMBOLS, 2, 1),
  '?': (KeyboardMode.SYMBOLS, 3, 1),
  '-': (KeyboardMode.SYMBOLS, 4, 1),
  '|': (KeyboardMode.SYMBOLS, 5, 1),
  "'": (KeyboardMode.SYMBOLS, 6, 1),
  '+': (KeyboardMode.SYMBOLS, 7, 1),
  '/': (KeyboardMode.SYMBOLS, 8, 1),
  '^': (KeyboardMode.SYMBOLS, 9, 1),
  '#': (KeyboardMode.SYMBOLS, 0, 2),
  '$': (KeyboardMode.SYMBOLS, 1, 2),
  '{': (KeyboardMode.SYMBOLS, 2, 2),
  '*': (KeyboardMode.SYMBOLS, 3, 2),
  '@': (KeyboardMode.SYMBOLS, 4, 2),
  '`': (KeyboardMode.SYMBOLS, 5, 2),
  '&': (KeyboardMode.SYMBOLS, 6, 2),
  ':': (KeyboardMode.SYMBOLS, 7, 2),
  '<': (KeyboardMode.SYMBOLS, 8, 2),
  '>': (KeyboardMode.SYMBOLS, 9, 2),
  '_': (KeyboardMode.SYMBOLS, 0, 3),
  '—': (KeyboardMode.SYMBOLS, 1, 3),
  '¡': (KeyboardMode.SYMBOLS, 2, 3),
  '=': (KeyboardMode.SYMBOLS, 3, 3),
  '(': (KeyboardMode.SYMBOLS, 4, 3),
  ')': (KeyboardMode.SYMBOLS, 5, 3),
  # TODO FOREIGN
}

BACKSPACE_X = 6
BACKSPACE_Y = 3

DONE_Y = 5

KEYBOARD_WIDTH = 10
KEYBOARD_HEIGHT = 4

DEFAULT_NAME_LIMIT = 16

class KeyboardManager(object):
  def __init__(self):
    self.x = 0
    self.y = 0
    self.mode = KeyboardMode.LOWER

  # XXX Will leave x and y in invalid states, only call when done (natch)
  def navigate_to_done(self):
    if self.x >= 8:
      tap_n_times(Button.Right, KEYBOARD_WIDTH-self.x)
    elif self.x == 7:
      tap_n_times(Button.Left, 2)
    elif self.x == 6:
      tap(Button.Left)

    tap_n_times(Button.Down, DONE_Y - self.y)

  def navigate_to_x(self, x):
    delta = x - self.x
    button = Button.Left if delta < 0 else Button.Right
    tap_n_times(button, abs(delta))
    self.x = x

  def navigate_to_y(self, y):
    delta = y - self.y
    button = Button.Up if delta < 0 else Button.Down
    tap_n_times(button, abs(delta))
    self.y = y

  # XXX keys and modes wrap around so this could be optimized to reduce button presses
  def navigate_to(self, character):
    mode, x, y = KEYBOARD_LAYOUT[character]
    if mode != KeyboardMode.ALL_MODES and mode != self.mode:
      delta = mode.value - self.mode.value
      button = Button.L if delta < 0 else Button.R
      tap_n_times(button, abs(delta))
      self.mode = mode
    
    if self.y == BACKSPACE_Y:
      self.navigate_to_y(y)
      self.navigate_to_x(x)
    else:
      self.navigate_to_x(x)
      self.navigate_to_y(y)


def type_text(text, characters_to_clear=0):
  tap(Button.Cross)
  
  # Delete pre-exisiting text
  tap_n_times(Button.Square, characters_to_clear)

  keyboard = KeyboardManager()
  for c in text:
    if c == ' ':
      tap(Button.Circle)
    else:
      keyboard.navigate_to(c)
      tap(Button.Cross)
  keyboard.navigate_to_done()
  tap(Button.Cross)

def get_place_duration(button):
  if button.name.lower().startswith('analog'):
    return random.uniform(CONFIG['Min Analog Place Duration'], CONFIG['Max Analog Place Duration'])
  return random.uniform(CONFIG['Min Place Duration'], CONFIG['Max Place Duration'])

def randomly_place_item(ensure_on_ground=False):
  remaining_buttons = [Button.Up, Button.Down, Button.Left, Button.Right, Button.AnalogRight]
  remaining_buttons *= math.ceil(CONFIG['Place Iterations']/len(remaining_buttons))
  random.shuffle(remaining_buttons)
  for button in remaining_buttons[:CONFIG['Place Iterations']]:
    t = get_place_duration(button)
    vprint(f'  Holding {button.name} for {t} seconds')
    hold(button)
    time.sleep(t)
    release(button)
  if ensure_on_ground:
    hold(Button.Circle)
    time.sleep(CONFIG['Ensure On Ground Duration'])
    release(Button.Circle)
  tap(Button.Cross)


# This function tries to randomly move items in case they are stuck in an invalid position
# If it is called from the Edit Goals screen or if the Edit Goals screen is opened while it is running it should do nothing
# This should ensure that when the function returns we are at the Edit Goals screen and the first selection is highlighted
def fix_any_stuck_items(iterations, ensure_on_ground=False, positions_offset=0, time_limit_offset=1, kb_offset=2):
  for i in range(iterations):
    vprint('Making sure no items are stuck in an invalid position, iteration', i + 1)
    tap_n_times(Button.Down, positions_offset)         # move item down or move the cursor to Edit Position
    hold(Button.AnalogRight)                           # rotate the item right or do nothing
    time.sleep(get_place_duration(Button.AnalogRight))
    release(Button.AnalogRight)
    hold(Button.Left)                                  # move the item left or do nothing
    time.sleep(get_place_duration(Button.Left))
    release(Button.Left)
    if ensure_on_ground:
      hold(Button.Circle)                              # move the item down or do nothing
      time.sleep(CONFIG['Ensure On Ground Duration'])
      release(Button.Circle)
    tap_n_times(Button.Down, time_limit_offset)        # move the item down or move the cursor to Set Time Limit
    tap(Button.Cross)                                  # place the item or do nothing
    tap_n_times(Button.Down, kb_offset)                # move the item down or move the cursor to an option that will open the keyboard
    tap(Button.Cross)                                  # place the item or open the keyboard
    tap(Button.Triangle)                               # go back to the previous item or close the keyboard
                                                       #   closing the keyboard will reset the cursor to the first item on the Edit Goals screen


# Call with time limit selected
def set_common_values_and_press_done(offset, kind, skip_time_limit = False):
  if not skip_time_limit:
    vprint('Setting time limit')
    set_slider_value(120, 
                     random.randint(CONFIG[kind+' Min Time Limit'], CONFIG[kind+' Max Time Limit']),
                     CONFIG['Time Limit Slider Hz'])
  
  vprint('Entering goal name')
  tap(Button.Down)
  type_text(random.choice(TEXT[kind+' Goal Names']), characters_to_clear = DEFAULT_NAME_LIMIT)

  vprint('Entering ped name')
  tap_n_times(Button.Down, 1 + offset)
  type_text(random.choice(TEXT['Ped Names']))

  vprint('Entering goal text')
  tap_n_times(Button.Down, 2 + offset)
  type_text(random.choice(TEXT[kind+' Goal Texts']))

  vprint('Entering win message')
  tap_n_times(Button.Down, 3 + offset)
  type_text(random.choice(TEXT[kind+' Win Messages']))

  vprint('Selecting done')
  tap(Button.Up)
  tap(Button.Cross)


def add_skate_letters():
  for c in 'SKATE':
    vprint('Placing', c)
    randomly_place_item(ensure_on_ground = CONFIG['Ensure SKATE Letters on Ground'])

  fix_any_stuck_items(CONFIG['Letter Fix Iterations'],
                      ensure_on_ground = CONFIG['Ensure SKATE Letters on Ground'],
                      positions_offset = 0,
                      time_limit_offset = 1,
                      kb_offset = 2)

  tap(Button.Down)
  set_common_values_and_press_done(2, 'SKATE')

def add_combo_letters():
  for c in 'COMBO':
    vprint('Placing', c)
    randomly_place_item(ensure_on_ground = CONFIG['Ensure SKATE Letters on Ground'])

  fix_any_stuck_items(CONFIG['Letter Fix Iterations'],
                      ensure_on_ground = CONFIG['Ensure COMBO Letters on Ground'],
                      positions_offset = 0,
                      time_limit_offset = 1,
                      kb_offset = 2)

  tap(Button.Down)
  set_common_values_and_press_done(2, 'COMBO')


def add_high_score():
  fix_any_stuck_items(CONFIG['Fix Iterations'],
                      ensure_on_ground = True,
                      positions_offset = 1,
                      time_limit_offset = 1,
                      kb_offset = 3)

  vprint('Setting high score')
  set_slider_value(15000,
                   random.randint(CONFIG['Min High Score'], CONFIG['Max High Score']),
                   CONFIG['Score Slider Hz'])
  
  tap_n_times(Button.Down, 2)
  set_common_values_and_press_done(3, 'High Score')
  
def add_high_combo():
  fix_any_stuck_items(CONFIG['Fix Iterations'],
                      ensure_on_ground = True,
                      positions_offset = 1,
                      time_limit_offset = 1,
                      kb_offset = 3)

  vprint('Setting high combo')
  set_slider_value(10000,
                   random.randint(CONFIG['Min High Combo'], CONFIG['Max High Combo']),
                   CONFIG['Score Slider Hz'])

  tap_n_times(Button.Down, 2)
  set_common_values_and_press_done(3, 'High Combo')

def select_key_combos_and_spin(mode):
  vprint('Selecting Key Combos')
  tap(Button.Cross)
  for double in ('', 'Double Tap '):
    for kind in ('Flip', 'Grab'):
      for level in ('Basic', 'Diagonal'):
        if CONFIG[f'{mode} {double}{level} {kind} Tricks']:
          tap(Button.Cross)
        tap(Button.Down)
  tap(Button.Cross)

  vprint('Setting Spin')
  tap(Button.Down)
  if CONFIG[mode+' Spin'].lower() == 'off':
    tap(Button.Left)
  elif int(CONFIG[mode+' Spin']) == 540:
    tap(Button.Right)
  elif int(CONFIG[mode+' Spin']) == 720:
    tap_n_times(Button.Right, 2)
  elif int(CONFIG[mode+' Spin']) == 900:
    tap_n_times(Button.Right, 3)


def add_skate_tricks():
  fix_any_stuck_items(CONFIG['Fix Iterations'],
                      ensure_on_ground = True,
                      positions_offset = 1,
                      time_limit_offset = 1,
                      kb_offset = 3)

  select_key_combos_and_spin('Skate-Tricks')
  
  vprint('Setting Acceleration Interval')
  tap(Button.Down)
  set_slider_value_with_taps(5, random.randint(CONFIG['Skate-Tricks Min Acceleration Interval'], CONFIG['Skate-Tricks Max Acceleration Interval']))
  
  vprint('Setting Acceleration Percent')
  tap(Button.Down)
  set_slider_value_with_taps(10, random.randint(CONFIG['Skate-Tricks Min Acceleration Percent'], CONFIG['Skate-Tricks Max Acceleration Percent']))

  vprint('Setting Trick Time')
  tap(Button.Down)
  set_slider_value(3000,
                   random.uniform(CONFIG['Skate-Tricks Min Trick Time'], CONFIG['Skate-Tricks Max Trick Time']),
                   CONFIG['Time Limit Slider Hz'])
  
  vprint('Setting stop adding tricks at time')
  tap(Button.Down)
  set_slider_value_with_taps(1, random.randint(CONFIG['Skate-Tricks Min Stop Adding Tricks at Time'], CONFIG['Skate-Tricks Max Stop Adding Tricks at Time'])//5)
  
  vprint('Setting Max Tricks')
  tap(Button.Down)
  set_slider_value_with_taps(11, random.randint(CONFIG['Skate-Tricks Min Max Tricks'], CONFIG['Skate-Tricks Max Max Tricks']))
  tap(Button.Down)
  tap(Button.Cross)

  tap_n_times(Button.Down, 2)
  set_common_values_and_press_done(3, 'Skate-Tricks')


def add_combo_skate_tricks():
  fix_any_stuck_items(CONFIG['Fix Iterations'],
                      ensure_on_ground = True,
                      positions_offset = 1,
                      time_limit_offset = 1,
                      kb_offset = 3)

  select_key_combos_and_spin('Combo Skate-Tricks')
  
  vprint('Setting Single Combo')
  if CONFIG['Combo Skate-Tricks Single Combo']:
    tap(Button.Down)
    tap(Button.Cross)
    tap_n_times(Button.Down, 3)
  else:
    tap_n_times(Button.Down, 2)
  
  vprint('Setting Combo Size')
  set_slider_value_with_taps(2, random.randint(CONFIG['Combo Skate-Tricks Min Combo Size'], CONFIG['Combo Skate-Tricks Max Combo Size']))
  
  if not CONFIG['Combo Skate-Tricks Single Combo']:
    vprint('Selecting Acceleration Interval')
    tap(Button.Down)
    set_slider_value_with_taps(5, random.randint(CONFIG['Combo Skate-Tricks Min Acceleration Interval'], CONFIG['Combo Skate-Tricks Max Acceleration Interval']))
    
    vprint('Setting Acceleration Percent')
    tap(Button.Down)
    set_slider_value_with_taps(10, random.randint(CONFIG['Combo Skate-Tricks Min Acceleration Percent'], CONFIG['Combo Skate-Tricks Max Acceleration Percent']))
    
    vprint('Setting Trick Time')
    tap(Button.Down)
    set_slider_value(3000,
                     random.uniform(CONFIG['Combo Skate-Tricks Min Trick Time'], CONFIG['Combo Skate-Tricks Max Trick Time']),
                     CONFIG['Time Limit Slider Hz'])
    
    vprint('Setting stop adding tricks at time')
    tap(Button.Down)
    set_slider_value_with_taps(1, random.randint(CONFIG['Combo Skate-Tricks Min Stop Adding Tricks at Time'], CONFIG['Combo Skate-Tricks Max Stop Adding Tricks at Time'])//5)
    
    vprint('Setting Max Tricks')
    tap(Button.Down)
    set_slider_value_with_taps(2, random.randint(CONFIG['Combo Skate-Tricks Min Max Tricks'], CONFIG['Combo Skate-Tricks Max Max Tricks']))

  vprint('Selecting Done')
  tap(Button.Down)
  tap(Button.Cross)

  tap_n_times(Button.Down, 2)
  set_common_values_and_press_done(3, 'Combo Skate-Tricks')
  

def add_tricktris():
  fix_any_stuck_items(CONFIG['Fix Iterations'],
                      ensure_on_ground = True,
                      positions_offset = 1,
                      time_limit_offset = 1,
                      kb_offset = 3)

  select_key_combos_and_spin('Tricktris')

  vprint('Setting Block Size')
  tap(Button.Down)
  set_slider_value_with_taps(3, random.randint(CONFIG['Tricktris Min Block Size'], CONFIG['Tricktris Max Block Size']))

  vprint('Setting Total to Win')
  tap(Button.Down)
  set_slider_value_with_taps(8, random.randint(CONFIG['Tricktris Min Total to Win'], CONFIG['Tricktris Max Total to Win']))
  tap(Button.Down)
  tap(Button.Cross)

  tap_n_times(Button.Down, 2)
  set_common_values_and_press_done(3, 'Tricktris')


def add_trick_to_the_beat():
  fix_any_stuck_items(CONFIG['Fix Iterations'],
                      ensure_on_ground = True,
                      positions_offset = 1,
                      time_limit_offset = 1,
                      kb_offset = 3)

  vprint('Editing tricks')
  tap(Button.Cross)
  if CONFIG['Trick to the Beat Basic Flip Tricks']:
    tap(Button.Cross)
  tap(Button.Down)
  if CONFIG['Trick to the Beat Diagonal Flip Tricks']:
    tap(Button.Cross)
  tap(Button.Down)
  if CONFIG['Trick to the Beat Basic Grab Tricks']:
    tap(Button.Cross)
  tap(Button.Down)
  if CONFIG['Trick to the Beat Diagonal Grab Tricks']:
    tap(Button.Cross)
  tap(Button.Down)
  tap(Button.Cross)
  
  tap_n_times(Button.Down, 2)
  set_common_values_and_press_done(3, 'Trick to the Beat')


def add_checkpoint_race():
  for i in range(11):
    print(f'Placing checkpoint {i+1}')
    randomly_place_item(ensure_on_ground=True)

  fix_any_stuck_items(CONFIG['Letter Fix Iterations'],
                      ensure_on_ground = True,
                      positions_offset = 0,
                      time_limit_offset = 1,
                      kb_offset = 4)

  vprint('Setting time limit')
  tap(Button.Down)
  set_slider_value(120,
                   random.randint(CONFIG['Checkpoint / Race Min Time Limit'], CONFIG['Checkpoint / Race Max Time Limit']),
                   CONFIG['Time Limit Slider Hz'])

  vprint('Setting Time / Checkpoint')
  tap(Button.Down)
  tap_n_times(Button.Right, random.randint(CONFIG['Checkpoint / Race Min Time / Checkpoint'], CONFIG['Checkpoint / Race Max Time / Checkpoint']))
  
  vprint('Setting Laps')
  tap(Button.Down)
  tap_n_times(Button.Right, random.randint(CONFIG['Checkpoint / Race Min Laps'], CONFIG['Checkpoint / Race Max Laps']) - 1)

  set_common_values_and_press_done(4, 'Checkpoint / Race', skip_time_limit = True)


def add_gap():
  fix_any_stuck_items(CONFIG['Fix Iterations'],
                      ensure_on_ground = True,
                      positions_offset = 2,
                      time_limit_offset = 1,
                      kb_offset = 4)

  vprint('Picking gap')
  tap(Button.Cross)
  hold(Button.Down)
  time.sleep(random.uniform(CONFIG['Min Gap Selection Time'], CONFIG['Max Gap Selection Time']))
  release(Button.Down)
  tap(Button.Cross)
  tap(Button.Triangle)
  
  vprint('Entering required trick')
  tap(Button.Down)
  type_text(random.choice(CONFIG['Gap Required Tricks']))
  
  tap_n_times(Button.Down, 3)
  set_common_values_and_press_done(4, 'Gap')


GOALS = [
  {'name': 'SKATE letters', 'index': 0, 'func': add_skate_letters},
  {'name': 'COMBO letters', 'index': 1, 'func': add_combo_letters},
  {'name': 'High Score', 'index': 2, 'func': add_high_score},
  {'name': 'High Combo', 'index': 3, 'func': add_high_combo},
  {'name': 'Skate-Tricks', 'index': 4, 'func': add_skate_tricks},
  {'name': 'Combo Skate-Tricks', 'index': 5, 'func': add_combo_skate_tricks},
  {'name': 'Tricktris', 'index': 6, 'func': add_tricktris},
  {'name': 'Trick to the Beat', 'index': 7, 'func': add_trick_to_the_beat},
  {'name': 'Checkpoint / Race', 'index': 8, 'func': add_checkpoint_race},
  {'name': 'Gap', 'index': 9, 'func': add_gap},
]


def add_a_goal():
  vprint('Opening the pause menu')
  tap(Button.Start)

  vprint('Selecting Create A Goal')
  tap_n_times(Button.Down, 2)
  tap(Button.Cross)

  vprint('Selecting Create new goal')
  tap(Button.Cross)

  goal = weighted_random_choice(GOALS)
  vprint('Selecting', goal['name'])
  tap_n_times(Button.Down, goal['index'])
  tap(Button.Cross)

  vprint('Placing Ped')
  randomly_place_item(ensure_on_ground=True)

  vprint('Placing Starting Position')
  randomly_place_item(ensure_on_ground=True)

  goal['func']()

  vprint('Resume the game')
  tap_n_times(Button.Triangle, 2)

  vprint('Trying to quit in case we got stuck placing something')
  for _ in range(2):
    tap_n_times(Button.Triangle, 5)
    tap(Button.Start)
    tap(Button.Down)
    tap(Button.Cross)
    tap_n_times(Button.Triangle, 5)


def add_goals():
  for _ in range(min(random.randint(CONFIG['Min Goals per Level'], CONFIG['Max Goals per Level']), 10)):
    try:
      add_a_goal()
    except SuspendExceptions:
      print('\n [SUSPENEDED] ')
      print('Press ENTER when the game is unpaused.')
      print('You will have 5 seconds to give the game back focus.')
      print('If you want to quit, press Ctrl + C again.')
      input()
      countdown()


class Level(enum.Enum):
  TRAINING = 0
  SANTA_CRUZ = 1
  BOSTON = 2
  ATLANTA = 3
  BARCELONA = 4
  BERLIN = 5
  KYOTO = 6
  AUSTRAILIA = 7
  NEW_ORLEANS = 8
  LAS_VEGAS = 9
  SKATOPIA = 10
  PRO_SKATER = 11
  THE_TRIANGLE = 12
  SCHOOL = 13
  PHILADELPHIA = 14
  DOWNHILL_JAM = 15
  LOS_ANGELES = 16
  CANADA = 17
  AIRPORT = 18

def iterate_through_levels_and_save_a_goal_file():
  current_level = Level.TRAINING

  # Do a weighted random shuffle then truncate to a length between min and max levels
  remaining_levels = list(filter(get_weight, Level))
  for _ in range(len(Level)):
    remaining_levels.insert(0, remaining_levels.pop(remaining_levels.index(weighted_random_choice(remaining_levels))))
  remaining_levels = remaining_levels[:random.randint(CONFIG['Min Levels'], CONFIG['Max Levels'])]

  while len(remaining_levels):
    level = remaining_levels.pop()
    vprint('Selecting Level:', level.name)
    set_slider_value_with_taps(current_level.value, level.value)
    tap(Button.Cross)
    time.sleep(CONFIG['Load Duration'])
    current_level = level

    add_goals()

    if len(remaining_levels):
      print('Returning to level select')
      tap(Button.Start)
      tap_n_times(Button.Up, 4)
      tap(Button.Cross)

  vprint('Saving goals')
  tap(Button.Start)
  tap_n_times(Button.Down, 4)
  tap(Button.Cross)
  time.sleep(CONFIG['Load Duration'])
  type_text('Generator ' + os.urandom(2).hex().upper(), characters_to_clear = DEFAULT_NAME_LIMIT)
  time.sleep(CONFIG['Load Duration'])
  tap(Button.Cross)
  time.sleep(CONFIG['Load Duration'])
  tap(Button.Circle)
  time.sleep(CONFIG['Fade Duration'])
  
  # XXX may want to check that the file was actually created here


def iterate_through_goal_sets():
  for i in range(random.randint(CONFIG['Min Goals Sets'], CONFIG['Max Goals Sets'])):
    if CONFIG['Use Reset Key'] or i == 0:
      vprint('Waiting for game to load')
      time.sleep(CONFIG['Load Duration'])
    
      vprint('Skipping intro cutscenes')
      tap_n_times(Button.Square, 3)
    
      vprint('Waiting for game to load again')
      time.sleep(CONFIG['Load Duration'])
    
      vprint('Selecting career data to load')
      tap(Button.Cross)
      time.sleep(CONFIG['Load Duration'])
      tap(Button.Circle)
    
      vprint('Waiting for game to load yet again')
      time.sleep(CONFIG['Load Duration'])
    
      vprint('Selecting Create-A-Modes')
      tap_n_times(Button.Up, 2)
      tap(Button.Cross)
      time.sleep(CONFIG['Fade Duration'])
    
      vprint('Selecting Create-A-Goal')
      tap_n_times(Button.Down, 2)
      tap(Button.Cross)
    
    vprint('Selecting Create New Goals')
    tap(Button.Cross)
    
    vprint('Selecting skater')
    set_slider_value_with_taps(0, CONFIG['Skater Index'])
    tap(Button.Cross)
    
    vprint('Select Play Level')
    tap(Button.Cross)
    
    iterate_through_levels_and_save_a_goal_file()
    
    if not CONFIG['Use Reset Key']:
      vprint('Select Quit')
      tap(Button.Start)
      tap(Button.Up)
      tap(Button.Cross)
      tap(Button.Up)
      tap(Button.Cross)
      time.sleep(CONFIG['Load Duration'])
      
      vprint('Select Create-A-Goal')
      tap_n_times(Button.Down, 2)
      tap(Button.Cross)
      
      vprint('Nuke All Goals')
      tap(Button.Up)
      tap(Button.Cross)
      tap(Button.Up)
      tap(Button.Cross)
    else:
      if Button['Reset Modifier'].value: hold(Button['Reset Modifier'])
      tap(Button.Reset)
      if Button['Reset Modifier'].value: release(Button['Reset Modifier'])


def validate_settings():
  has_errors = False
  
  for strs in TEXT.values():
    for s in strs:
      if any((c not in KEYBOARD_LAYOUT for c in s.replace(' ', ''))):
        print("Text contains a character that isn't on the keyboard:", s)
        has_errors = True

  if (CONFIG['Max Levels'] * CONFIG['Max Goals per Level']) > 50:
    print('The game has a limit of 50 goals per save. Please decrease either Max Levels or Max Goals per Level.')
    has_errors = True

  # XXX Could check save count here too since there's a limit of 75 saves

  if has_errors:
    print('\nPlease fix the above settings and rerun the script.')
    exit(-1)


def main():
  print(" -= Tony Hawk's Underground 2: Remix - Random Goal Generator =- ")
  validate_settings()
  
  print('  See readme.md before continuing.')
  print('  Press Ctrl + C to abort if you have not read it.')
  print('  Press ENTER to begin the countdown.')
  input()

  countdown()

  iterate_through_goal_sets()
  
  print('Done!')


if __name__ == '__main__':
  main()
