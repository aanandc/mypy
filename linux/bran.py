#! /usr/bin/python
from random import choice

def query(prompt):
   return raw_input(prompt)


def respond(question):
    question = question.lower()
    keywords={"your|ur:name":"you can call me bran:i am bran:my friends call me bran","your:age":"i am 7","how:old:u":"i am two years younger than Arya","how:old:are:u":"7 years old","my:mom|mother|father|dad|wife|sister|son|daughter|brother:hates|loves:me":"who else in your family does the same?","i love:u|you":"isn't it a too early ? i hardly know you:you make me blush:i hope you are a girl","u:love|like":"i love climbing","u:climb":"i dont climb anymore.i fell down from a tower in winterfell.. i dont remember how..","who:your|ur:dad|father":"my father is lord eddard stark an honourable man:lord eddark stark","winterfell":"I could perch for hours among the shapeless, rain-worn gargoyles that brooded over the First Keep, watching it all the men drilling with wood and steel in the yard, the cooks tending their vegetables in the glass garden, restless dogs running back and forth in the kennels, the silence of the godswood, the girls gossiping beside the washing well. It made me feel like I was lord of the castle, in a way even Robb would never know.:my home:i grew up in winterfell","winter":"winter is coming","hello|hi|hi there":"hello:hi:aloha:hey there:hello there..","eddard|eddard stark|ned stark":"Eddard Stark,my lord father,an honourable man.","who:are:u":"bran:brandon:bran named after brandon the builder of the wall and winterfell","tell:me:about:summer":"summer is my pet direwolf","what|who:summer":"summer is a direwolf,my pet direwolf","how:are:u":"ok...seen better days before my fall","how:did:u:fall|fell":"i dont remember about that except dreams of a three eyed crow","three:eye:crow":"its just a three eyed crow in my dreams.. thats all","who:ur:mother|mom":"catelyn stark my mother","who:arya|arya stark":"she is my sister:Arya is my sister","who:sansa|sansa stark":"my eldest sister","who:rikkon|younger brother":"Rikkon is my baby brother:rikkon my baby brother:my naughty baby brother rikkon","who:robb|elder brother":"robb is my eldest brother","who:ur:brothers":"Robb,Jon and Rikkon","who:ur:sisters":"Arya and Sansa","what:do:u":"nothing in particular","hodor":"hodor:he helps me","my:fav:book|movie|song|food":"how the hell do i know that:(scratches the head) your favourite ? i dont know","ur:fav:food":"lemon cakes","ur:fav:book":"winds of winter","ur:fav:song":"500 miles","will:rain:today|tomorrow":"you must ask this to ur maester:this is a question for a maester, not for me","who|what:maester":"a very learned man","what:happen:ur:dad|father|mom|mother|brother|sister":"something sad... i dont know exactly.. please dont talk about it","what:happen:winterfell":"winterfell is not dead,like me its just broken","how:weather|climate:today|tomorrow":"its just like dragons,unpredictable","do:u:like|love:dragon|adventure":"yes,very much.","why:do:u:like|love":"its just the way it is.i just do.:i dont know:its not rational ..so cant be explained","where|are:r|you:u":"winterfell"}
    resp = None
    match=False
    for k in keywords:
       words=k.split(':')
       num=0
       num_words=len(words)
       for w in words:
         altwords=w.split('|')
         onematch=False
         for a in altwords:
           if a in question:
             onematch=True
             break
         if onematch:
             num = num + 1
       if num == num_words :
            match = True
            break
    if match:
        resp=keywords[k]
        resp=choice(resp.split(':'))
    return resp
         
  
def std_replace(statement):
    replaced = {"my":"your","your":"my"}
    for k in replaced.keys():
       if k in statement:
         val=replaced[k]
         statement=statement.replace(k,val)
         break         
    return statement

def alter(statement):
    retval = None
    statement = statement.lower()
    replaced = {"i am":"you are","you are":"am i","i ":"you "}
    stub =	"why :why did you think that "
    for k in replaced.keys():
        if k in statement:
            val=replaced[k]
            retval = statement.replace(k,val)
            #retval =	choice(stub.split(':')) + retval
            retval = std_replace(retval)
            retval = choice(stub.split(':')) + retval
            break
    return retval
    
def greet():
    print choice(["hello sweet summer child"])
    
def exit_greet():
  print choice(["see you later","goodbye","catch you later"])

def casual():
   print choice(["i did not understand","i wish i knew that","explain more on this"])

def stub():
   greet()
   while True: 
     resp=query(">>")
     if resp in ["quit","exit"]:
         exit_greet()
         break
     val = respond(resp)
     if val != None:
        print val
        continue
     val = alter(resp)
     if val == None :
         casual()
     else:
         print val
   
stub()
