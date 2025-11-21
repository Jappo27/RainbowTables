#https://aams-eam.pages.dev/posts/the-art-of-password-cracking_rainbow-tables/
#https://kestas.kuliukas.com/RainbowTables/

import hashlib

class Rainbow:
    def __init__(self, chainLength = 10):
        self.table = {}
        self.chainLength = chainLength

    def insert(self, plaintext, previousHashValue):
        #inserts into dictionary 
        # previousHashValue is the final reduced has
        #plaintext is the original text
        self.table[previousHashValue] = plaintext
            
    def search(self, target_hash):
        #searches through the keys to detect if in dict
        return self.table.get(target_hash)
    
    def chaining(self, plainText):
        # (Kuliukas , K) https://kestas.kuliukas.com/RainbowTables/
        # store original text
        startPlainText = plainText

        #for declared chain length
        for i in range(self.chainLength):
            newHash = self.hash(plainText) #hash text
            plainText = self.reduction(newHash) #reducde hash ==> new plain text
            #print(plainText) #!* For markers to play with chains *!

        #store new plain text as key and original plain text
        self.table[plainText] = startPlainText

    def createRainbow(self, plainList):
        #for each elment needing to be hashed
        for plain in plainList:
            self.chaining(plain) # create chain

    def hash(self, plaintext):
        #hash plaintext into cipher text
        str = hashlib.sha512(f"{plaintext}".encode('ascii'))
        ciperText = str.hexdigest()
        return ciperText

    def reduction(self, hash, n = 5):
        #reduction function 

        # reduction functions can be as simple as first n numbers or use a complex formula
        # the simpler a reduction function the more likelt collisions are to occour
        newPlainText = str(hash)[:n]
        return newPlainText
    
    def cycle(self, cipherText):
        # (Luc Gommans 2017) https://gist.github.com/lgommans/83cbb74a077742be3b31d33658f65adb
        #reduce ciphertext and
        currentHash = self.reduction(cipherText)

        #for the length of the chain
        for i in range(self.chainLength):
            #if the chain is in the table
            if currentHash in self.table:
                plainText = self.table[currentHash] # set current password as original plaintext in table
                for j in range(self.chainLength): # for each link in the chain
                    hash = self.hash(plainText) # hash the current plaintext
                    if hash == cipherText: # if the hash equals input cipherText return plaintext
                        return plainText 
                    else:
                        plainText = self.reduction(hash) # else reduce and repeat
            else: 
                #else rehash, reduce and repeat
                currentHash = self.hash(currentHash)
                currentHash = self.reduction(currentHash)

        #if not in table return None
        return None
    
    def display(self):
        print(self.table)

# *!The class names below is just for thematic fun!*
# The reduction functions are for example only

class red(Rainbow):
    def reduction(self, hash, n = 5):
        #Takes the first 5 digits
        newPlainText = str(hash)[:n]
        return newPlainText
    
class orange(Rainbow):
    def reduction(self, hash, n = 5):
        #takes the last five digits
        newPlainText = str(hash)[-n:]
        return newPlainText
    
class yellow(Rainbow):
    def reduction(self, hash):
        # takes the digits
        newPlainText = ""
        for i in range(len(hash)):
            if hash[i].isdigit():
                newPlainText = f"{newPlainText}{hash[i]}"
        newPlainText = str(newPlainText)
        return newPlainText
    
class green(Rainbow):
    def reduction(self, hash):
        # takes the characters
        newPlainText = ""
        for i in range(len(hash)):
            if hash[i].isalpha():
                newPlainText = f"{newPlainText}{hash[i]}"
        newPlainText = str(newPlainText)
        return newPlainText
    
class blue(Rainbow):
    def reduction(self, hash):
        # takes the even characters
        newPlainText = ""
        for i in range(len(hash)):
            if hash[i].isalpha() and i % 2 == 0:
                newPlainText = f"{newPlainText}{hash[i]}"
        newPlainText = str(newPlainText)
        return newPlainText
    
class indigo(Rainbow):
    def reduction(self, hash):#
        # takes the odd characters
        newPlainText = ""
        for i in range(len(hash)):
            if hash[i].isalpha() and i % 2 != 0:
                newPlainText = f"{newPlainText}{hash[i]}"
        newPlainText = str(newPlainText)
        return newPlainText
    
class violet(Rainbow):
    def reduction(self, hash):
        #takes the first and last 3 digits
        newPlainText = f"{hash[:3]}{hash[-3:]}"
        newPlainText = str(newPlainText)
        return newPlainText
    
class spectrum:
    # When we introduce multiple reduction functions, we can then composite the chains into a new table
    # You would typically use multiple reduciton functions to reduce collisions (otus 2017) https://crypto.stackexchange.com/questions/47731/multiple-rainbow-tables-and-their-success-probability

    def __init__(self, chains):
        #contains all the chains
        self.chains = chains

    def insert(self, chain):
        # adds to table
        self.chains.append(chain)

    def cycle(self, cipherText):
        #for each chain, use each reduction function
        for i in range(len(self.chains)):
            currentHash = self.chains[i].reduction(cipherText)

            #for the length of the chain
            for j in range(self.chains[i].chainLength):
                #if the chain is in the table
                if currentHash in self.chains[i].table:
                    plainText = self.chains[i].table[currentHash] # set current password as original plaintext in table
                    for j in range(self.chains[i].chainLength): # for each link in the chain
                        hash = self.chains[i].hash(plainText) # hash the current plaintext
                        if hash == cipherText: # if the hash equals input cipherText return plaintext
                            return plainText 
                        else:
                            plainText = self.chains[i].reduction(hash) # else reduce and repeat
                else: 
                    #else rehash, reduce and repeat
                    currentHash = self.chains[i].hash(currentHash)
                    currentHash = self.chains[i].reduction(currentHash)

        #if not in table return None
        return None
    
HashChainRed = red()
HashChainOrange = orange()
HashChainYellow = yellow()
HashChainGreen = green()
HashChainBlue = blue()
HashChainIndigo = indigo()
HashChainViolet = violet()

colourSpectrum = spectrum([HashChainRed, HashChainOrange, HashChainYellow, HashChainGreen, HashChainBlue, HashChainIndigo, HashChainViolet])

HashChainRed.createRainbow(["a", "b", "c", "d"])
HashChainOrange.createRainbow(["0", "1", "2", "3"])
HashChainYellow.createRainbow(["m", "mc", "555", "admi"])
HashChainGreen.createRainbow(['M$T$C123', 'Hetzneronline!@1234', 'Server!@#$', 'Welcome!'])
HashChainBlue.createRainbow(['Admin121!@#$%^', 'Zxcv123$', 'G00dluck', 'Vps@@##11', 'Winner!@#', 'Lovemyself'])
HashChainIndigo.createRainbow(['45678', '~!@#$%^&*()_+', 'admin$', 'Behappy', 'Blessing', 'Passw0rd!@#'])
HashChainViolet.createRainbow(['Qwertyuiop2016', 'Unicorn@1234', 'Windows10', 'Zxc123!@#'])

HashChainRed.display()
"""
HashChainOrange.display()
HashChainYellow.display()
HashChainGreen.display()
HashChainBlue.display()
HashChainIndigo.display()
HashChainViolet.display()
"""

"""Example"""

# !* Single Reduction chain table !*

chain = [
    "a",
    "1f40f",
    "564af",
    "2239e",
    "5070e",
    "bddcd",
    "7b984",
    "293fc",
    "d3752",
    "fd562",
    "a2813" #!* This won't work as it will then hash and reduce to a value outside of the chain !*
]

cipherText = chain[9]
newHash = HashChainRed.hash(cipherText)

print(f"\n We have: {newHash}\n This is our cipher text.")
print(f" When we reduce this repeqtedly it will eventually match a key in the table: a2813")
print(f" After identifying that we can iterate through the chain to find the matching cipherText = hash.")
print(f" Then we take the previous Plaintext value of {HashChainRed.cycle(newHash)}\n")
print(HashChainRed.cycle(newHash))

#*!You can experiment with any of the above variables by replacing cipherText = chain[x]!*
#*!comment on Line 29 allows you to print out the chain if you want to test any of the other subclasses !*


"""Example"""

# !* Multi Reduction chain table !*

cipherText = "Hetzneronline!@1234"
newHash = HashChainGreen.hash(cipherText)

print(f"\n We have: {newHash}\n This is our cipher text.")
print(f" When we reduce this repeqtedly it will eventually match a key in the table: Hetzneronline!@1234")
print(f" After identifying that we can iterate through the chain to find the matching cipherText = hash.")
print(f" Then we take the previous Plaintext value of {HashChainGreen.cycle(newHash)}\n")
print(colourSpectrum.cycle(newHash))

cipherText = "Behappy"
newHash = HashChainIndigo.hash(cipherText)

print(f"\n We have: {newHash}\n This is our cipher text.")
print(f" When we reduce this repeqtedly it will eventually match a key in the table: Behappy")
print(f" After identifying that we can iterate through the chain to find the matching cipherText = hash.")
print(f" Then we take the previous Plaintext value of {HashChainIndigo.cycle(newHash)}\n")
print(colourSpectrum.cycle(newHash))