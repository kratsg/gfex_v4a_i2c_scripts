from __future__ import print_function
from i2cdev import I2C
from configurations import *
from time import sleep

i2c = I2C(0x68, 0) # device @ 0x68, bus 0

config = clock_config['120MHz']

def batch(iterable, n=1):
  l = len(iterable)
  for ndx in range(0, l, n):
    yield iterable[ndx:min(ndx+n, l)]

def set_page(i2c, page):
  print('  Writing page: {0:02x}'.format(page))
  i2c.write(bytearray([0x01, page]))

def do_i2c_block_write(i2c, block):
  page, register, value = block
  if page != do_i2c_block_write.page:
    set_page(i2c, page)
    do_i2c_block_write.page = page
  print('  Writing     : {0:02x}{1:02x}'.format(register, value))
  i2c.write(bytearray([register, value]))

do_i2c_block_write.page = 0x00

def do_i2c_write(i2c, configurations):
  for block in batch(configurations, 3): do_i2c_block_write(i2c, block)

print('Handling preamble')
do_i2c_write(i2c, config['preamble'])
sleep(0.3) # 300 ms delay
print('Handling modifications')
do_i2c_write(i2c, config['modifications'])
print('Handling soft reset')
do_i2c_write(i2c, config['soft reset'])
print('Handling postamble')
do_i2c_write(i2c, config['postamble'])

i2c.close()
