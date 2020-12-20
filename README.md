# JnX-interpreter
The JnX ! Interpreter is a XML++ (maybe even XML# !) interpreter. Its purpose is to add some structure control to XML documents (for and foreach)\
JnX means Jnx is the New XML

## JnX syntaxe
JnX is a layer above XML. It's purpose is to facilitate XML writing by automatising template generation using predetermined data.\
Let's say you have a pirate. You have the list of his purses values, and you want to put them in the pirate.\
First, you declare your attributes in a "var" jnx block :

```
<jnx:var name="test">
    <jnx:value>132</jnx:value>
    <jnx:value>112</jnx:value>
    <jnx:value>12</jnx:value>
</jnx:var>
```
\
Then, you can use it inside a jnx:foreach, using jnx:get
```
<history-pieces>
    <jnx:foreach name="itVal" in="test" >
        <pieces>
            <jnx:get name="itVal">
        </pieces>
    </jnx:foreach>
</history-pieces>
```
\
Feel free to generate datas on-the-fly using the "for" range !
```
<history-object>
    <jnx:for from="1" to="4" step="2" name="it" >
        <object>
            <jnx:get name="it">
        </object>
    </jnx:for>
</history-object>
```

## Jnx semantic verifiation
//TODO complete when "back part" is done, here are some hints/ideas :
Jinx give you the warnings :
* "Get" not used in for/foreach
* "foreach"/"for" is empty 
* "for" is going to do an infinite loop

Jinx throw compilation errors when :
* XML is not structured correctly
* Trying to do a "get" on an invalid var

## JnX utilisation
see userguide