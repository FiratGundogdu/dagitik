__author__ = 'firatlepirate'

alfabe = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']


'''input_str = raw_input("Give me a word: ")
print input_str
print type(input_str)'''


alfabe_key = input("Give me number: ")
alfabe_cryt=[0]*26

for i in range(len(alfabe)):
    alfabe_cryt[i]=alfabe[((i-alfabe_key)%26)]
    alfabe_cryt[i]=alfabe_cryt[i].upper()

print (alfabe)
print alfabe_cryt


text = "lorem ipsum dolor sit amet"
text_crypt = ""

for i in range(len(text)):
    if  text[i] in alfabe:
        text_crypt = text_crypt + alfabe_cryt[alfabe.index(text[i])]
    else:
        text_crypt = text_crypt + text[i]

print text_crypt
