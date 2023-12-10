'''
When running the code on linux, my bot prefix was messing up.
The file was becoming multiline and I didn't know why, so this is a temp fix for me.
You may ignore this file and run the main.py only.
'''

file = open("prefix.txt","w")
file.write(input("prefix: "))
file.close()
