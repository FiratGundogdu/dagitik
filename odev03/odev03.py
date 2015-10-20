__author__ = 'firatlepirate'


alfabe = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

alfabe_key = input("Give me a number to make new alphabet: ")
alfabe_cryt=[0]*26

for i in range(len(alfabe)):
    alfabe_cryt[i]=alfabe[((i-alfabe_key)%26)]
    alfabe_cryt[i]=alfabe_cryt[i].upper()

print (alfabe)
print alfabe_cryt


file = open('metin.txt', 'r')
text = file.read()
text=text.lower()
text_crypt = ""

for i in range(len(text)):
    if  text[i] in alfabe:
        text_crypt = text_crypt + alfabe_cryt[alfabe.index(text[i])]
    else:
        text_crypt = text_crypt + text[i]

file_name= "crypted_<%d>.txt" %(alfabe_key)
print file_name
file = open(file_name,'w')
file.write(text_crypt)
file.close()
