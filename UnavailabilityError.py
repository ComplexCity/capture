class UnavailibilityError (Exception):
	def __init__(self, origin, code, message):
		self.origin = origin
		self.code = code
		self.message = message
		Exception.__init__(self, '%s Error %s: %s' % (origin, code, message))