from time import sleep

import CWClient

c = CWClient.CWClient('localhost', int(666))
while 1:
	c.Loop()
	sleep(0.001)