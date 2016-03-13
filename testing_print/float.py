import sys, time
from decimal import Decimal

if __name__ == "__main__":
	start = time.time()
	interval = float(raw_input("Enter time interval (sec): "))
	print interval
	time_passed = time.time() - start
	print "time passed: ", time_passed
	print float(interval/time_passed)

	time_interval  = 0
	start_time = time.time()
	print "Start time: ", start_time
	test = 1
	while (time_interval < test):
		print "Am printing"
		print time.time()
		time_interval = time.time() - start_time
		print time_interval

