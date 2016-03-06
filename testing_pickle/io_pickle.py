import pickle
import hashlib

# The name of the file where we will store the object
shoplistfile = 'shoplist.data'
# The list of things to buy
shoplist = {'apple', 'mango', 'carrot'}
print 'shoplist:'
print(hashlib.md5(shoplist).hexdigest())
# Write to the file
f = open(shoplistfile, 'wb')
print 'f before dumping'
print(hashlib.md5(f).hexdigest())
# Dump the object to a file
pickle.dump(shoplist, f)
print 'f after dumping'
print(hashlib.md5(f).hexdigest())
f.close()

# Destroy the shoplist variable
del shoplist

# Read back from the storage
f = open(shoplistfile, 'rb')
print 'f after opening again'
print(hashlib.md5(f).hexdigest())
# Load the object from the file
storedlist = pickle.load(f)
print 'storedlist:'
print(hashlib.md5(storedlist).hexdigest())
print storedlist