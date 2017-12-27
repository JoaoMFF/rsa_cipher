#João Filipe, 13568
import random
import math
import sys
import os
import tkinter as tk              
from tkinter import font  as tkfont
from tkinter import *

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
letters_len = len(letters)
randomMinVal = int
randomMaxVal = int
#GUI

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("350x295")
        self.title("RSA Cipher")

        self.title_font = tkfont.Font(family='Helvetica', size=15, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageKeys, PageEncrypt, PageDecrypt):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="RSA Cipher", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Set Keys", borderwidth= 4, 
                            command=lambda: controller.show_frame("PageKeys"))
        button2 = tk.Button(self, text="Encrypt", borderwidth= 4,
                            command=lambda: controller.show_frame("PageEncrypt"))
        button3 = tk.Button(self, text="Decrypt", borderwidth= 4,
                            command=lambda: controller.show_frame("PageDecrypt"))
        button4 = tk.Button(self, text="Exit", borderwidth= 4,
                            command=exit)
        button1.pack(fill="x", padx=30, pady=10)
        button2.pack(fill="x", padx=30, pady=10)
        button3.pack(fill="x", padx=30, pady=10)
        button4.pack(fill="x", padx=30, pady=10)


class PageKeys(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Key Generator", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        #Set Min and Max values
        treshold1 = tk.Label(self, text="Threshold: ")
        treshold1.pack(anchor=W, fill="x", padx=30)
        self.tresholdInput1 = tk.Entry(self, textvariable=randomMinVal, justify='center')

        self.tresholdInput1.pack(anchor=W, fill="x", padx=35)

        label = tk.Label(self, text="&")
        label.pack(anchor=W, fill="x", pady=5)

        self.tresholdInput2 = tk.Entry(self, textvariable=randomMaxVal, justify='center')

        self.tresholdInput2.pack(anchor=W,fill="x", padx=35)

        exebtn = tk.Button(self, text="Create Keys", borderwidth= 4, 
                           command=self.keys)
        exebtn.pack(fill="x", padx=30)

        self.dataLbl = tk.Label(self)
        self.dataLbl.pack(anchor=CENTER, padx=30, fill="x", pady=5)

        self.confirm = tk.Label(self)
        self.confirm.pack(anchor=CENTER, padx=30, fill="x")

        button = tk.Button(self, text="<- Start Page", borderwidth= 4,
                           command=restart_program)
        button.pack(side="bottom",fill="x", padx=30, pady=(0,10))

    def keys(self):
    	minValue = int(self.tresholdInput1.get())
    	maxValue = int(self.tresholdInput2.get())

    	p = randomPrime(minValue, maxValue)
    	q = randomPrime(minValue, maxValue)

    	while p == q:
    		q = randomPrime(minValue, maxValue)
    	else:
    		#print("\n")
    		#print("p: ", p)
    		#print("q: ", q)

    		modulusN = modulus(p, q)
    		#print("n: ", modulusN)

    		toti = totient(p, q)
    		#print("phi(n): ", toti)

    		e = intE(toti, modulusN)
    		#print("e: ", e)

    		d = intD(e, toti)
    		#print("d: ", d)

    		variables = "p: " + str(p) + "			" + "q: " + str(q) + "\n" + "n: " + str(modulusN) + "			" + "φ: " + str(toti) + "\n" + "e: " + str(e) + "			" + "d: " + str(d)

    		self.dataLbl.config(text=variables)
    		self.confirm.config(text="Keys have been saved", foreground="green")
    		#print("\n")
    		#print("KU = {",e,",",modulusN,"}")
    		#print("KR = {",d,",",modulusN,"}")
    		#print("\n")

    		#Save Keys to .txt files
    		filePub = open("RSA_PubKey.txt","w")
    		filePub.write(str(e)+"\n")
    		filePub.write(str(modulusN)+"\n")
    		filePub.close()

    		filePriv = open("RSA_PrivKey.txt", "w")
    		filePriv.write(str(d)+"\n")
    		filePriv.write(str(modulusN)+"\n")
    		filePriv.close()

class PageEncrypt(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #Mostrar Msg
        msg = rsaMsg()
        msgTxt = " ".join(str(x) for x in msg)
        msgTxt = msgTxt.replace(',', ' ')

        label = tk.Label(self, text="Encrypt", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.msg = tk.Label(self, text=msgTxt)
        self.msg.pack(anchor=CENTER, padx=30, fill="x", pady=(30,10))

        exebtn = tk.Button(self, text="Start", borderwidth= 4, 
                           command=self.encrypt)
        exebtn.pack(fill="x", padx=30)

        self.cipherLbl = tk.Label(self)
        self.cipherLbl.pack(anchor=CENTER, padx=30, fill="x", pady=(25,10))

        self.confirm = tk.Label(self)
        self.confirm.pack(anchor=CENTER, padx=30, fill="x")

        button = tk.Button(self, text="<- Start Page", borderwidth= 4,
                           command=restart_program)
        button.pack(side="bottom",fill="x", padx=30, pady=(0,10))

    def encrypt(self):
        cipher = []
        msg = rsaMsg()
        pos_text = find_pos(msg)

        publicKey = pubKey()

        i = 0
        loop_pass = 0
        while loop_pass < len(pos_text):
            try:
                c = (pow(pos_text[i], publicKey[0])) % publicKey[1]

                cipher.append(c)

                i = i + 1
                loop_pass = loop_pass + 1

            except:
                print("Oops Something went Wrong!")
                exit()

        with open ('RSA_Cipher.txt', 'w') as file:
            file.write(','.join([str(n) for n in cipher]))

        self.confirm.config(text="Encryption Successfully Saved", foreground="green")

        self.cipherLbl.config(text=cipher)

class PageDecrypt(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        rsaCipher()
        #Mostrar Msg
        cipher = rsaCipher()
        cipherTxt = " ".join(str(x) for x in cipher)
        cipherTxt = cipherTxt.replace(',', ' ')

        label = tk.Label(self, text="Decrypt", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.msg = tk.Label(self, text=cipherTxt)
        self.msg.pack(anchor=CENTER, padx=30, fill="x", pady=(30,10))

        exebtn = tk.Button(self, text="Start", borderwidth= 4, 
                           command=self.decrypt)
        exebtn.pack(fill="x", padx=30)

        self.msgLbl = tk.Label(self)
        self.msgLbl.pack(anchor=CENTER, padx=30, fill="x", pady=(25,10))

        self.confirm = tk.Label(self)
        self.confirm.pack(anchor=CENTER, padx=30, fill="x")

        button = tk.Button(self, text="<- Start Page", borderwidth= 4,
                           command=restart_program)
        button.pack(side="bottom",fill="x", padx=30, pady=(0,10))

    def decrypt(self):
        message = []

        privateKey = privKey()
        cipherTxt = rsaCipher()

        i = 0
        loop_pass = 0

        while loop_pass < len(cipherTxt):
            try:
                m = (pow(cipherTxt[i],privateKey[0])) % privateKey[1]

                message.append(letters[m])

                i = i + 1
                loop_pass = loop_pass + 1

            except:
                print("Oops Something went Wrong!")
                exit()

        with open('RSA_Msg.txt','w') as file:
            file.write(','.join([str(n) for n in message]))

        self.confirm.config(text="Decryption Successfully Saved", foreground="green")

        self.msgLbl.config(text=message)

def rsaMsg():
	f = open('RSA_Msg.txt',"r")
	line = f.readlines()
	f.close()
	msg = [x for x in line[0]]

	return msg

def rsaCipher():
	f = open('RSA_Cipher.txt',"r")
	line = f.readlines()
	f.close()
	#Split the string by the comma (,)
	cipherTxt = [x.strip() for x in line[0].split(',')]
	#Convert items on the list to int
	cipherInt = list(map(int, cipherTxt))

	return cipherInt

def randomPrime(minV, maxV):
	prime = False
	while prime == False:
		n = 2
		while n % 2 == 0:
		  n = random.randint(minV, maxV)
		  #print("RANDOM", n)
		s = math.trunc(n**0.5)
		s = int(s)
		x = 3
		# While n doesn't exactly divide to equal 0, and x is less then the sqrt of n
		while ( n % x != 0 ) and (x <= s):
		  x = x + 2
		# if n is greater than s, it means it has run out of numbers to test, so is prime
		if x > s:
	  		prime = True
	return n

def modulus(p, q):
	N = p * q
	return N

def totient(p, q):
	T =((p - 1) * (q-1))
	return T

def intE(T,N):
	prime = False
	while prime == False:
		e = 2
		while e % 2 == 0:
		  	e = random.randint(3, T)
		s = math.trunc(e**0.5)
		s = int(s)
		x = 3
		# Conferir se N é divisil por e
		if (N % e != 0):
			while ( e % x != 0 ) and (x <= s):
			  x = x + 2
			if x > s:
			  prime = True
	return e

def intD(e, T):
	for x in range(1, T):
		if (e * x) % T == 1:
			return x
	return None

def find_pos(value):
    temp = []
    i=0
    while i<len(value):
        j=0
        while j<letters_len:
            if value[i] == letters[j]:
                temp.append(j)
            j = j+1
        i= i+1
        #print(temp)
    return temp

def pubKey():
	f = open('RSA_PubKey.txt',"r")
	pubKeyInfo = f.readlines()
	f.close()

	e = pubKeyInfo[0]
	n = pubKeyInfo[1]
	info = [e, n]
	infoInt = list(map(int, info))
	return infoInt

def privKey():
	f = open('RSA_PrivKey.txt',"r")
	privKeyInfo = f.readlines()
	f.close()

	d = privKeyInfo[0]
	n = privKeyInfo[1]
	info = [d, n]
	infoInt = list(map(int, info))

	return infoInt

def restart_program():
    #Restarts the current program.
    python = sys.executable
    os.execl(python, python, * sys.argv)

if __name__=='__main__':
	app = SampleApp()
	app.mainloop()