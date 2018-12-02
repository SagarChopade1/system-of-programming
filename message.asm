   %macro write_string 2 
      mov   eax, 4
      mov   ebx, 1
      mov   ecx, %1
      mov   edx, %2
      int   0x80
   %endmacro
section .data
	msg2 db "sum is=%d",0,10
	msg db "hi sagar chopade",0,10
	num1 dd 150
	num2 dd 150
section .bss
	res resd 1
section .text 
	global main
	extern printf
main:
	xor eax,eax
	mov eax,[num1]
	mov ebx,num2
	mov ebx,[num2]
	add eax,ebx
	mov edx,eax
	mov eax,100
	mov ebx,200
	mov ecx,msg
	mov edx,18
abc:
	write_string msg,18
	write_string msg,18
	mov eax,1
	int 0x80


	
