# Core Packages
import tkinter as tk
from tkinter import *
from tkinter import ttk 				#For tab creation using tkinter
from tkinter.scrolledtext import *
import tkinter.filedialog

# Other pkg
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

# NLP Pkgs
from spacy_summarization import text_summarizer
from gensim.summarization import summarize
from nltk_summarization import nltk_summarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

#packages for ECIES
from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
import binascii




###################################################################### 

def sumy_summary(docx):
	parser = PlaintextParser.from_string(docx, Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document, 3)
	summary_list = [str(sentence) for sentence in summary]
	result=''.join(summary_list)
	return result

# Structure and Layout
window = Tk()                       #Window for the GUI
window.title("Encryption/Decryption using ECIES")
window.geometry("1400x1200")                          #Window Settings
window.config(background='blue')

style = ttk.Style(window)                               #Position of tobs set to Top-Left
style.configure('lefttab.TNotebook', tabposition='wn') #tabs positioned west-north




################################################################### TAB LAYOUT
tab_control = ttk.Notebook(window,style='lefttab.TNotebook')
 
tab1 = ttk.Frame(tab_control)           #Home Tab
tab2 = ttk.Frame(tab_control)           
tab3 = ttk.Frame(tab_control)           #Plaint Text Tab
tab4 = ttk.Frame(tab_control)           #File Upload Tab
tab5 = ttk.Frame(tab_control)           #URL Summarisation tab
tab6 = ttk.Frame(tab_control)           

# ADD TABS TO NOTEBOOK
tab_control.add(tab1, text=f'{"Home":^40s}')
tab_control.add(tab3, text=f'{"Plain Text":^39s}')
tab_control.add(tab4, text=f'{"File Upload":^37s}')
tab_control.add(tab5, text=f'{"URL analysis":^36s}')

label1 = Label(tab1, text= 'About',font='Helvetica 18 bold',padx=5, pady=5)
label1.grid(column=1, row=0, pady=5)

label3 = Label(tab3, text= 'Plain Text Summarisation and Encryption/Decryption',font='Helvetica 16 bold',padx=5, pady=5)
label3.grid(column=1, row=0, pady=5)

label4 = Label(tab4, text= 'File Summarisation and Encryption/Decryption',font='Helvetica 16 bold',padx=5, pady=5)
label4.grid(column=1, row=0, pady=5)

label5 = Label(tab5, text= 'URL Summarisation and Encryption/Decryption',font='Helvetica 16 bold',padx=5, pady=5)
label5.grid(column=1, row=0, pady=5)

tab_control.pack(expand=1, fill='both')
###############################################################################



##################################################### Functions Plain Text Tab
def get_summary():
	raw_text = str(entry.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)             #Calling Summary Function
	print(final_text)
	result = '\nSummary:\n{}'.format(final_text)         #Displaying Sumamry
	tab3_display.insert(tk.END,result)

def clear_text():
	entry.delete('1.0',END)


def clear_display_result():
    tab3_display1.delete('1.0',END)
    tab3_display.delete('1.0',END)
    

def save_summary():                                         #Save Summary as text file
	raw_text = str(tab3_display.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)     
	file_name = 'File_'+ timestr + '.txt'                   #Setting File Name
	with open(file_name, 'w') as f:
		f.write(final_text)                                 #Writing File
	result = '\nName of file: {}'.format(file_name)
	tab3_display.insert(tk.END,result)
    
    

def encrypt_text():
	raw_text = str(entry.get('1.0',tk.END))                #Get input
	raw_text= bytes(raw_text,'utf-8')
	privKey = generate_eth_key()                           #Generate Private Key
	privKeyHex = privKey.to_hex()                          #Convert it to Hexadecimal
	pubKeyHex = privKey.public_key.to_hex()                #Make Public Key
	encrypted = encrypt(pubKeyHex, raw_text)
	encrypted = binascii.hexlify(encrypted)
	result = '\n\nEncrypted text:\n{}'.format(encrypted)       #Print Result
	tab3_display.insert(tk.END,result)
	result1 = '\n{}'.format(privKeyHex)
    #result1 = '\nPrivate Key: {}\nPublic Key: {}'.format(privKeyHex,pubKeyHex)
	tab3_display1.insert(tk.END,result1)

def decrypt_text():
	encrypted = str(entry.get('1.0',tk.END))               #Get input       
	encrypted= bytes(encrypted,'utf-8').strip()            #Convert to bytes and remove white spaces
	encrypted = binascii.unhexlify(encrypted)
	privKeyHex= str(tab3_display1.get('1.0',tk.END)).strip()
	decrypted = decrypt(privKeyHex, encrypted)
	result = '\n\nDecrypted text:\n{}'.format(decrypted)       #Print Result
	tab3_display.insert(tk.END,result)

##############################################################################






######################################################## Functions for File tab
def openfiles():
	file1 = tkinter.filedialog.askopenfilename(filetypes=(("Text Files",".txt"),("All files","*")))
	read_text = open(file1).read()
	displayed_file.insert(tk.END,read_text)

# for reset button
def clear_text_file():
	displayed_file.delete('1.0',END)

# Clear Result of Functions
def clear_text_result():
    tab4_display_text.delete('1.0',END)
    #tab4_display1.delete('1.0',END)
    

def get_file_summary():
	raw_text = displayed_file.get('1.0',tk.END)
	final_text = text_summarizer(raw_text)
	result = '\nSummary:\n{}'.format(final_text)
	tab4_display_text.insert(tk.END,result)

def save_summary1():
	raw_text = str(tab4_display_text.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)
	file_name = 'File_'+ timestr + '.txt'
	with open(file_name, 'w') as f:
		f.write(final_text)
	result = '\nName of file: {}'.format(file_name)
	tab4_display_text.insert(tk.END,result)


def encrypt_file():
	raw_text = str(displayed_file.get('1.0',tk.END))
	raw_text= bytes(raw_text,'utf-8')
	privKey = generate_eth_key()
	privKeyHex = privKey.to_hex()
	pubKeyHex = privKey.public_key.to_hex()
	encrypted = encrypt(pubKeyHex, raw_text)
	encrypted = binascii.hexlify(encrypted)
	result = '\n\nEncrypted text:\n{}'.format(encrypted)
	tab4_display_text.insert(tk.END,result)
	result1 = '\n{}'.format(privKeyHex)
    #result1 = '\nPrivate Key: {}\nPublic Key: {}'.format(privKeyHex,pubKeyHex)
	tab4_display1.insert(tk.END,result1)

def decrypt_file():
	encrypted = str(displayed_file.get('1.0',tk.END))
	encrypted= bytes(encrypted,'utf-8').strip()
	encrypted = binascii.unhexlify(encrypted)
	privKeyHex= str(tab4_display1.get('1.0',tk.END)).strip()
	decrypted = decrypt(privKeyHex, encrypted)
	result = '\n\nDecrypted text:\n{}'.format(decrypted)
	tab4_display_text.insert(tk.END,result)
##############################################################################






############################################### Functions for Candidate URL TAB
def clear_url_entry():
	url_entry.delete(0,END)

def clear_url_display():
    tab5_display1.delete('1.0',END)
    tab5_display_text.delete('1.0',END)
	
    

def get_text():                                     # Fetch Text From Url
	raw_text = str(url_entry.get())
	page = urlopen(raw_text)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	url_display.insert(tk.END,fetched_text)

def get_url_summary():
	raw_text = url_display.get('1.0',tk.END)
	final_text = text_summarizer(raw_text)
	result = '\nSummary:{}\n'.format(final_text)
	tab5_display_text.insert(tk.END,result)	

def save_summary2():
	raw_text = str(tab5_display_text.get('1.0',tk.END))
	final_text = text_summarizer(raw_text)
	file_name = 'File_'+ timestr + '.txt'
	with open(file_name, 'w') as f:
		f.write(final_text)
	result = '\nName of file: {}'.format(file_name)
	tab5_display_text.insert(tk.END,result)

def encrypt_url():
	raw_text = str(url_display.get('1.0',tk.END))
	raw_text= bytes(raw_text,'utf-8')
	privKey = generate_eth_key()
	privKeyHex = privKey.to_hex()
	pubKeyHex = privKey.public_key.to_hex()
	encrypted = encrypt(pubKeyHex, raw_text)
	encrypted = binascii.hexlify(encrypted)
	result = '\n\nEncrypted text:\n{}'.format(encrypted)
	tab5_display_text.insert(tk.END,result)
	result1 = '\n{} '.format(privKeyHex)
	tab5_display1.insert(tk.END,result1)

def decrypt_url():
	encrypted = str(url_display.get('1.0',tk.END))
	encrypted= bytes(encrypted,'utf-8').strip()
	encrypted = binascii.unhexlify(encrypted)
	privKeyHex= str(tab5_display1.get('1.0',tk.END)).strip()
	decrypted = decrypt(privKeyHex, encrypted)
	result = '\n\nDecrypted text:\n{}'.format(decrypted)
	tab5_display_text.insert(tk.END,result)
##############################################################################






##################################################################### Home tab
about_label = Label(tab1,text="Our Project:\n\nEncryption/Decryption using ECIES",pady=5,padx=5)
about_label.grid(column=1,row=1, pady=5)
about_label = Label(tab1,text="Made By:\n1. Ritika Kayal - 18BCE2518\n2. Srinivas - 18BCE0048 \n3. Amritanshi - 18BCE2524",pady=5,padx=5)
about_label.grid(column=1,row=2, pady=5)
about_label = Label(tab1,text="Abstract:\n\n With the rise of the internet, it has become more and more common for important, \ncritical documents to be shared through electronic means. \nThis means that it has become essential that documents and important \ndetails be kept confidential through the means of encryption. \nECC has risen in popularity and is dubbed “The Successor to RSA” \nas it is capable of achieving the same security of a 1024 bit RSA key with just 208 bits. \nThus, it is the most optimal method for securing data against breaches and unauthorized access. \nDocuments have also grown in size over time \nas more detail can be stored due to larger and faster storage availability. \nExcessive amounts of time is wasted on reading filler and unnecessary content in documents \nto understand them and this becomes an issue as it limits the productivity of an individual. \nSkimming through large documents may also lead to users missing important details. \nHence a smart Natural Language Processing system that can parse through \ndocuments / text file / URLs can help save precious time \nwhile also conveying all the important facts/details needed.",pady=5,padx=5)
about_label.grid(column=1,row=3, pady=5)
##############################################################################



##################################################################### BUTTONS
b0=Button(tab1,text="Close", width=12,command=window.destroy)
b0.grid(row=4,column=1,padx=10,pady=10)
##############################################################################




################################################################ Plain text Tab
l1=Label(tab3,text="Enter Text",font='Helvetica 14 bold')
l1.grid(row=2,column=1)
entry=ScrolledText(tab3,height=8)
entry.grid(row=3,column=0,columnspan=4,padx=5,pady=5)

button1=Button(tab3,text="Reset",command=clear_text, width=12)
button1.grid(row=4,column=0,padx=10,pady=10)

button2=Button(tab3,text="Summarize",command=get_summary, width=12)
button2.grid(row=4,column=2,padx=10,pady=10)

button5=Button(tab3,text="Encrypt", command=encrypt_text, width=12)
button5.grid(row=5,column=0,padx=10,pady=10)

button6=Button(tab3,text="Decrypt", command=decrypt_text, width=12)
button6.grid(row=5,column=2,padx=10,pady=10)

l1=Label(tab3,text="Private Key",font='Helvetica 14 bold')
l1.grid(row=6,column=1)
tab3_display1 = ScrolledText(tab3, height=1)
tab3_display1.grid(row=7,column=0, columnspan=3,padx=5,pady=5)

l1=Label(tab3,text="Output", font='Helvetica 14 bold')
l1.grid(row=8,column=1)
tab3_display = ScrolledText(tab3, height=8)
tab3_display.grid(row=9,column=0, columnspan=3,padx=5,pady=5)

button3=Button(tab3,text="Clear Result", command=clear_display_result, width=12)
button3.grid(row=10,column=2,padx=10,pady=10)

button4=Button(tab3,text="Save", command=save_summary, width=12)
button4.grid(row=10,column=0,padx=10,pady=10)
##############################################################################





##################################################### File Upload Summarisation
l1=Label(tab4,text="Open File To Summarize", font='Helvetica 14 bold')
l1.grid(row=1,column=1)
displayed_file = ScrolledText(tab4,height=8)
displayed_file.grid(row=2,column=0, columnspan=3,padx=5,pady=5)


b0=Button(tab4,text="Open File", width=12, command=openfiles)
b0.grid(row=3,column=0,padx=10,pady=10)

b2=Button(tab4,text="Summarize", width=12,command=get_file_summary)
b2.grid(row=3,column=2,padx=10,pady=10)

button5=Button(tab4,text="Encrypt", command=encrypt_file, width=12)
button5.grid(row=4,column=0,padx=10,pady=10)

button6=Button(tab4,text="Decrypt", command=decrypt_file, width=12)
button6.grid(row=4,column=2,padx=10,pady=10)

l1=Label(tab4,text="Private Key", font='Helvetica 14 bold')
l1.grid(row=5,column=1)
tab4_display1 = ScrolledText(tab4, height=1)            #Decryption Key display
tab4_display1.grid(row=6,column=0, columnspan=3,padx=5,pady=5)

l1=Label(tab4,text="Output", font='Helvetica 14 bold')
l1.grid(row=7,column=1)
# Display Screen
tab4_display_text = ScrolledText(tab4,height=8)
tab4_display_text.grid(row=8,column=0, columnspan=3,padx=5,pady=5)

# Allows you to edit
tab4_display_text.config(state=NORMAL)

b1=Button(tab4,text="Reset", width=12,command=clear_text_file)
b1.grid(row=9,column=0,padx=10,pady=10)

b5=Button(tab4,text="Save", command=save_summary1, width=12)
b5.grid(row=9,column=1,padx=10,pady=10)

b3=Button(tab4,text="Clear Result", width=12,command=clear_text_result)
b3.grid(row=9,column=2,padx=10,pady=10)
##############################################################################






###################################################################### URL TAB
l1=Label(tab5,text="Enter URL To Summarize")
l1.grid(row=1,column=0)

raw_entry=StringVar()
url_entry=Entry(tab5,textvariable=raw_entry,width=30)
url_entry.grid(row=1,column=1)

button2=Button(tab5,text="Get Text",command=get_text, width=12,bg='#03A9F4')
button2.grid(row=1,column=2,padx=10,pady=10)

# Display Screen For URL text
url_display = ScrolledText(tab5,height=8)
url_display.grid(row=2,column=0, columnspan=3,padx=5,pady=5)

button1=Button(tab5,text="Reset",command=clear_url_entry, width=12,bg='#03A9F4')
button1.grid(row=3,column=0,padx=10,pady=10)

button4=Button(tab5,text="Summarize",command=get_url_summary, width=12,bg='#03A9F4')
button4.grid(row=3,column=2,padx=10,pady=10)

button5=Button(tab5,text="Encrypt", command=encrypt_url, width=12)
button5.grid(row=4,column=0,padx=10,pady=10)

button6=Button(tab5,text="Decrypt", command=decrypt_url, width=12)
button6.grid(row=4,column=2,padx=10,pady=10)

l=Label(tab5,text="Private Key", font='Helvetica 14 bold')
l.grid(row=5,column=1)
tab5_display1 = ScrolledText(tab5, height=1)
tab5_display1.grid(row=6,column=0, columnspan=3,padx=5,pady=5)

l1=Label(tab5,text="Output", font='Helvetica 14 bold')
l1.grid(row=7,column=1)
tab5_display_text = ScrolledText(tab5,height=8)
tab5_display_text.grid(row=8,column=0, columnspan=3,padx=5,pady=5)

button3=Button(tab5,text="Clear Result", command=clear_url_display,width=12,bg='#03A9F4')
button3.grid(row=9,column=0,padx=10,pady=10)

b5=Button(tab5,text="Save", command=save_summary2, width=12)
b5.grid(row=9,column=2,padx=10,pady=10)
##############################################################################

window.mainloop()