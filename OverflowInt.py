class OverflowInt:
	def __init__(self, val=0, maxValue=1):
		self.value = val
		self.max = maxValue

	def setValue(self, val):
		self.value = val % self.max
		return val // self.max

	def getValue(self):
		return self.value

	def add(self, other):
		if isinstance(other, OverflowInt):
			return self.setValue(self.value + other.value)

		elif isinstance(other, int):
			return self.setValue(self.value + other)

		else:
			raise Exception(f"Cannot add a value of type {self.__class__.__name__} "
							f"to a value of type {other.__class__.__name__}")

	def __str__(self):
		return str(self.value)

	def __lt__(self, other):
		if self.max == other.max:
			return self.value < other.value

	def __le__(self, other):
		if self.max == other.max:
			return self.value <= other.value

	def __eq__(self, other):
		return self.max == other.max and \
			   self.value == other.value

	def __ge__(self, other):
		if self.max == other.max:
			return self.value >= other.value

	def __gt__(self, other):
		if self.max == other.max:
			return self.value > other.value
