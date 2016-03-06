import hashlib
mystring = raw_input('Enter String to hash: ')
# Assumes the default UTF-8
hash_object = hashlib.md5(mystring.encode())

print(hash_object.hexdigest())
print 'Hash of "hello world"'
print(hashlib.md5(b'Hello World').hexdigest())

