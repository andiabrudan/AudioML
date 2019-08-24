from Utils import timestampMatch
from OverflowInt import OverflowInt


class TimeStamp:
	def __init__(self, milliseconds=0):
		self.milliseconds = OverflowInt(0, 1000)
		self.seconds = OverflowInt(0, 60)
		self.minutes = OverflowInt(0, 60)
		self.hours = 0
		if milliseconds:
			self.add(milliseconds)

	def get(self):
		return TimeStamp._toMilliseconds(self)

	def set(self, other):
		if isinstance(other, int):
			other = self.milliseconds.setValue(other)
			other = self.seconds.setValue(other)
			other = self.minutes.setValue(other)
			self.hours = other
		elif isinstance(other, TimeStamp):
			self.milliseconds.setValue(other.milliseconds.getValue())
			self.seconds.setValue(other.seconds.getValue())
			self.minutes.setValue(other.minutes.getValue())
			self.hours = other.hours
		elif isinstance(other, str):
			self.set(TimeStamp.parse(other))
		else:
			raise Exception(f"Cannot assign a value of type {other.__class__.__name__} "
							f"to a value of type {self.__class__.__name__}")

	def add(self, other):
		if isinstance(other, TimeStamp):
			remainder = self.milliseconds.add(other.milliseconds.getValue())
			remainder = self.seconds.add(other.seconds.getValue() + remainder)
			remainder = self.minutes.add(other.minutes.getValue() + remainder)
			self.hours += other.hours + remainder

		elif isinstance(other, int):
			remainder = self.milliseconds.add(other)
			remainder = self.seconds.add(remainder)
			remainder = self.minutes.add(remainder)
			self.hours += remainder

		else:
			raise Exception(f"Cannot add a value of type {self.__class__.__name__} "
							f"to a value of type {other.__class__.__name__}")

	@staticmethod
	def parse(string):
		values = timestampMatch(string)
		# To avoid bad formats like: HH:MMM:S:mmmm
		# First convert the results to a number
		# and let the class take care of the rest
		ms = values["Hours"] * 3600000 + \
			 values["Minutes"] * 60000 + \
			 values["Seconds"] * 1000 + \
			 values["Milliseconds"]
		return TimeStamp(ms)

	def __str__(self):
		return f"{self.hours:02}:" \
			   f"{self.minutes.getValue():02}:" \
			   f"{self.seconds.getValue():02}." \
			   f"{self.milliseconds.getValue():02}"

	def __lt__(self, other):
		if isinstance(other, TimeStamp):
			return TimeStamp._toMilliseconds(self) < TimeStamp._toMilliseconds(other)

		elif isinstance(other, int):
			return TimeStamp._toMilliseconds(self) < other

		else:
			raise Exception(f"Cannot compare a value of type {self.__class__.__name__} "
							f"to a value of type {other.__class__.__name__}")

	@staticmethod
	def _toMilliseconds(stamp):
		return stamp.hours * 3600000 + \
			   stamp.minutes.getValue() * 60000 + \
			   stamp.seconds.getValue() * 1000 + \
			   stamp.milliseconds.getValue()

	def __floordiv__(self, other):
		if not isinstance(other, TimeStamp):
			raise Exception(f"Cannot divide a value of type {self.__class__.__name__} "
							f"to a value of type {other.__class__.__name__}")
		return TimeStamp._toMilliseconds(self) // TimeStamp._toMilliseconds(other)

	def __truediv__(self, other):
		if not isinstance(other, TimeStamp):
			raise Exception(f"Cannot divide a value of type {self.__class__.__name__} "
							f"to a value of type {other.__class__.__name__}")
		return TimeStamp._toMilliseconds(self) / TimeStamp._toMilliseconds(other)

	def __mod__(self, other):
		if not isinstance(other, TimeStamp):
			raise Exception(f"Cannot divide a value of type {self.__class__.__name__} "
							f"to a value of type {other.__class__.__name__}")
		return TimeStamp._toMilliseconds(self) % TimeStamp._toMilliseconds(other)


if __name__ == "__main__":
	t1 = TimeStamp.parse("00:00:01.00")
	t2 = TimeStamp.parse("00:00:02.00")
	print(t2 < t1)
