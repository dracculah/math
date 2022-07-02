# faster look-up of powers
powerz = {}

# a chain particle
class Chain:

	def __init__(self, base, power, times):
		self.base = base
		self.power = power
		self.times = times
		self.childChains = []

	def to_str(self):
		_str = ""
		if len(self.childChains) == 0:
			_str = "({} * {} ^ {})".format(self.times, self.base, self.power)
		else:
			_str = "({} * {}^({}))".format(self.times, self.base, self.printExpression())
		return _str
			
	def printExpression(self):
		_str = ""
		for k in self.childChains:
			_str += k.to_str()
			if k != self.childChains[-1]:
				_str += " + "
		return _str
			
# recursively get chain
def getChain(base, n, parentChain):
	# consistency check
	assert(base > 0)
	assert(n > 0)
	# find highest power
	high_power = -1
	for p in powerz.keys():
		if powerz[p] > n:
			high_power = p-1	
			break
	assert(high_power > -1)
	# now how many times
	times = -1
	val_power = powerz[high_power]
	for p in range(base+1):
		if p * val_power > n:
			times = p-1
			break
	assert(times > 0)
	new_chain = Chain(base, high_power, times) # a chain of `times * base ^ power` 
	parentChain.childChains.append(new_chain)
	if high_power > base: # power is too high, need to get a chain for it
		getChain(base, high_power, new_chain)

	# calc residual
	residue = n - powerz[high_power] * times
	if residue > base: # the residue is too high, need to get a whole new chain for it
		getChain(base, residue, parentChain)
	else: # the residue is < base, we just add it as a number
		parentChain.childChains.append(Chain(1,1,residue)) # 1^1 * residue = residue
	
# express the number n in hereditary `base` notation, get the tree of chains with all the factors and bases
def hereditaryNotation(base, n):
	# first let's build the power dict with numbers smaller than n (or maybe with one over, just to be sure)
	powerz.clear()
	powerz[0] = 1
	powerz[1] = base
	curr_n = base
	curr_power = 1
	while(curr_n <= n):
		curr_n *= base
		curr_power += 1
		powerz[curr_power] = curr_n
	# create the main chain
	main_chain = Chain(base, 0, None)
	# recursively get chains
	getChain(base, n, main_chain)
	return main_chain

# recursively change base
def changeBase(old_base, new_base, chainz):
	for chain in chainz:
		if chain.base == old_base:
			chain.base = new_base
		if chain.power == old_base:
			chain.power = new_base
		changeBase(old_base, new_base, chain.childChains)

# recursively calculate from the chain list
def calculateFromChain(chainz):
	sum = 0
	for chain in chainz:
		if len(chain.childChains) == 0:
			sum += chain.base ** chain.power * chain.times
		else:
			sum += chain.base ** calculateFromChain(chain.childChains) * chain.times
	return sum


# get next base and next number of goodstein series
def goodstein(base, n):
	mc = hereditaryNotation(base, n)
	changeBase(base, base+1, mc.childChains)
	sumz = calculateFromChain(mc.childChains)
	sumz -= 1
	return base+1, sumz

# do goodstein X times
def do_goodstein(base, n, x_times):
	print("goodstein from base: {}, n: {}, x times: {}".format(base,n,x_times))
	print("{}. (b:{})  {}".format(0,base,n))
	for i in range(x_times):
		base, n = goodstein(base, n)
		print("{}. (b:{})  {}".format(i+1,base,n))
		if n == 0:
			break

do_goodstein(2, 13, 40)

