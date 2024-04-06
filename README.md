# Laboratorio D
Se construyo el cgenerador de analizadores léxicos y de generó un analizador léxico para
el siguiente archivo yalex:

```lex
(* Lexer para Gramática No. 3 - Variación expresiones aritméticas simples *)

(* Introducir cualquier header aqui *)

{
print("Este es un intendo de header")
variableheader = "hola desde el header"
}

%%

let delimitador = ["\s\t\n"]
let espacioEnBlanco = delimitador+
let digito = ['0'-'9']
let numero = '-'?digito+ (*comentario que estorba*)
let hex = 0xdigito+
let letra = ['a'-'z''A'-'Z']
let identificador = letra(letra|numero)+

rule tokens =
    espacioEnBlanco    { print("WS") }
  | if                { print("IF") }
  | else                { print("ELSE") }
  | then                { print("THEN") }
  | numero            { print("NUMBER") }
  | '=''='                { print("EQUALS") }
  | '!''='                { print("NOT_EQUALS") }
  | '>'                { print("GREATER") }
  | '<'                { print("LESS") }
  | '>''='                { print("GREATER_EQUALS") }
  | '<''='                { print("LESS_EQUALS") }
  | identificador    { print("ID") }

%%

{
print("Este es un intendo de trailer")
print("variableheader = ", variableheader)
}
```

Asi se ve el automata generado por el Yalex:
![automatalexical5.png](images%2Fautomatalexical5.png)


## Ejecución

Entrada de archivo de texto:
```txt
if 2 < 3 then
    ident1
else
    ident2
```

Salida del analizador léxico:
```txt
Este es un intendo de header
Enter the file name: >? text.txt
t: if IF
t:   WS
t: 2 NUMBER
t:   WS
t: < LESS
t:   WS
t: 3 NUMBER
t:   WS
t: then THEN
t: 
     WS
t: ident1 ID
t: 
 WS
t: else ELSE
t: 
     WS
t: ident2 ID
Este es un intendo de trailer
variableheader =  hola desde el header
```