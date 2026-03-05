#1 matches a string that has an 'a' followed by zero or more 'b''s.
import re
pattern = r"ab*"
text = input()
if re.fullmatch(pattern,text):
    print("Match")
else:
    print("no match")
#2 matches a string that has an 'a' followed by two to three 'b'.
import re
pattern = r"ab{2,3}"
text = input()
if re.fullmatch(pattern,text):
    print("match")
else:
    print("no match")
#3 find sequences of lowercase letters joined with a underscore.
import re
pattern = r"^[a-z]+_[a-z]+$"
text = input()
if re.fullmatch(pattern,text):
    print("match")
else:
    print("no match")
#4  find the sequences of one upper case letter followed by lower case letters.
import re 
pattern = r"[A-Z][a-z]+"
text = input()
result = re.findall(pattern, text)
print(result)
#5 matches a string that has an 'a' followed by anything, ending in 'b'.
import re
text = input()
pattern = r"a.*b"
if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")
#6 replace all occurrences of space, comma, or dot with a colon.
import re
text = input()
result = re.sub(r"[,\.]" , ":", text)
print(result)
#7 convert snake case string to camel case string.
import re
text = input()
parts = text.split("_")
camel = parts[0] + ''.join(word.capitalize() for word in parts[1:])
print(camel)
#8  split a string at uppercase letters.
import re
text = input()
result = re.split(r"?=[A-Z]", text)
print(result)
#9 insert spaces between words starting with capital letters.
import re
text = input()
result = re.sub(r"[A-Z]", r"\1", text)
print(result)
#10  convert a given camel case string to snake case
import re
text = input()
snake = re.sub(r"([A-Z])", r"_\1", text).lower()
print(snake)