# system-of-programming
Built functionality of Assembler using python3 language
Implepented code of i386 assebly language code combile and show how internal processing done.
1)  you want to run code simply run below command 
    see the symbol table 
        >> python3 mainfile.py -s anyFileToInput.asm message.asm
		 python3 mainfile.py -s  message.asm
	  see literal table 
		>> python3 mainfile.py -l message.asm
	  -you want to see the intermediate code 
		  >python3 mainfile.py -intr message.asm
	-you want to see file of '_.lst' file
		>> python3 mainfile.py -lst add1.asm
		in lst file squere bracket define constant '[constant]',{with scale index and base},(define with without scale index and base)
2) working process:
	- read line by line of .asm file and input to code 
		-check in data section
			-data(read_line)  # perform data section code and add in to symbol table and literal table
		- check is bss section
			-bss(read_line) # prerform bss code to evaluate accordingly
		-check is data section
			- data(read_line) # perfor operation accordingly
		1st pass complited
	2-passes:
		again same process done from data section read code and update address of jump instruction
		
3) macro:
	-function like structure of macro implmented in assebly code
4) debugger :
	find line by line executions of your mnemonics code. 
