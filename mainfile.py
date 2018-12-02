from sys import argv
from dictionary import *
import passs1 as f1
flagformain=occure=lensr1=lensr2=line_no=0
Literal_NO=Symbol_NO=1	
#----------------------------------------------
def macroodfun(r,line_no):
	global Literal_NO
	tp=(' '.join(r.split(','))).split()
	for i in range(len(tp)):
		if(tp[i].isdigit()):
			dym='lit#'+str(Literal_NO)
			lit_table['Line No'].append(line_no)
			lit_table['Literal_NO'].append(Literal_NO)
			lit_table['Symbol'].append(dym)	
			l=hexconvert(tp[i],line_no,2)
			lit_table['Literal'].append(tp[i])
			lit_table['Hex'].append(l)
			lit_table['Type'].append('-')
			Literal_NO=Literal_NO+1
	
#----------------------------------------------
def sym(filename):
	global line_no
	fp=open(filename,'r')
	cn=symNo=0
	count=1
	flag=-1
	macroend=""
	for r in fp.readlines():
		line_no+=1
		r=r.strip()
		if(r==""):
			continue
		if(("%macro" in r) or macroend!='%endmacro'): # skip macro function
			mline.append(r)
			if('%macro' in r):
				s=r.split()
				if(s[0]!='%macro'):
					print("Macro name wrong");
					exit()
				macro.append(s[1])
				ins.append(s[1])
				macropara.append(int(s[2]))
				continue
			if(('%endmacro' in r)):
				#print(macro,macropara)
				macroend='%endmacro'
				continue
			macroodfun(r,line_no)
			continue
		#print(mline)
		if(flag==(-1)):
			if(r!='section .bss'):
				if(r=='section .data'):
					#intermed['Iline'].append('section .data')
					lst_table['line_num'].append(line_no-1)
					lst_table['hex'].append(' ')
					lst_table['instruction'].append(r)
					
				else:
					err=cn=data(r,cn)
					dic['lineNo'].append(line_no)
					if(err==0):
						return 0
			else:
				lst_table['line_num'].append(line_no)
				lst_table['hex'].append(' ')
				lst_table['instruction'].append(r)
				#intermed['Iline'].append(r)
				#intermed['Iline'].append('section .bss')
				flag=0

		elif(flag==0):
			#intermed['Iline'].append(r)
			if(r!='section .bss'):
				if(r=='section .text'):
					lst_table['line_num'].append(cn)
					lst_table['hex'].append(' ')
					lst_table['instruction'].append(r)
					#intermed['Iline'].append(r)
					dic['addr'].pop()
					flag=1
				else:
					dic['lineNo'].append(line_no)
					err=cn=bss(r,cn)
					if(err==0):
						return 0
		elif(flag==1):
			err=text(r,line_no)
			
			if(err==0):
				return 0


#--------------------------------------------------------------------------------------------
def text(r,line_no):
	global Symbol_NO
	opcodeG(r,line_no)
	ft=flaglbl=jmp_status=js=flag=ext=0
	s=r.strip()
	strn=""
	t=r.split()
	s=s+' '
	slen=len(s)
	for i in range(0,slen):
		if(s[i]==':' or s[i]==' ' or s[i]=='\n'):
			string=strn.strip()
			if(s[i]==':'):
				flaglbl=1
			strn=""	
			if(string==""):
				continue
			CT=0
			for j in dic['sym']:	#for lebale check before colon(:)
				global flagformain,occure
				if(j==string and flagformain!=string and occure<1 and flaglbl==1):
					dic['status'][CT]='D'
					dic['lineNo'][CT]=line_no
					occure=occure+1;
					flaglbl=0
					break
				elif(occure>=1 and flaglbl==1 and i==0):
					print("Symbol `",string,"` Redefine")
					break
				if(ft==1 and string!="global"):
					dic['sym'].append(string)
					dic['symN'].append('sym'+str(Symbol_NO))
					dic['type'].append('_start')
					dic['size'].append('-')
					dic['addr'].append('-')
					dic['status'].append('-')
					dic['ele'].append('-')
					dic['seg'].append('code')
					dic['lineNo'].append(line_no)
					Symbol_NO=Symbol_NO+1
					ft=2
					flagformain=string
				if(string=='global'):
					ft=1
				if(string=='extern'):
					ext=1
				CT=CT+1
			if(ext==1 and string!='extern'):
				constart.extend(string.split(','))
			#jump statement handalsym
			if(jmp_status==1):
				CT=0				
				for j in dic['sym']:
					if(string==j):
						dic['status'][CT]='D'
						jmp_status=0
						js=1
						CT=CT+1
						break
				if(js!=1):
					js=0
					dic['sym'].append(string)
					dic['symN'].append('sym'+str(Symbol_NO))
					dic['type'].append('lbl')
					dic['size'].append('-')
					dic['addr'].append('-')
					dic['status'].append('U')
					dic['ele'].append('-')
					dic['seg'].append('code')
					dic['lineNo'].append(line_no)
					jmp_status=0
					Symbol_NO=Symbol_NO+1
					break

			for symbol in jm:
				if(symbol==string):
					jmp_status=1
				elif(flaglbl==1 and flagformain!=string ):
					flaglbl=0
					dic['sym'].append(string)
					dic['symN'].append('sym'+str(Symbol_NO))
					dic['lineNo'].append(line_no)			
					dic['type'].append('lbl')
					dic['size'].append('-')
					dic['addr'].append('-')
					dic['status'].append('-')
					dic['ele'].append('-')
					dic['seg'].append('code')
					Symbol_NO=Symbol_NO+1
					break
		else:
			strn+=s[i]	
		i+=1	

								
#------------------------------------------------------------------------------------------------------------------------------	
					

def data(r,cn):
	global Symbol_NO
	dic['seg'].append('data')
	t=r.split()
	st=""
	size=-1
	count=0
	cn=cn+1
	#dataLiteral(r,cn)
	lst_table['line_num'].append(cn)
	for s in t:
		if(count==0):
			for i in dic['sym']:
				if(i==s):
					print("symbol ",s," redefined")
					return 0
			else:		
				dic['sym'].append(s)
				dic['symN'].append('sym'+str(Symbol_NO))
				Symbol_NO=Symbol_NO+1
				count+=1
		elif(count==1):
			for tp in typeofdata:
				if(tp==s):
					dic['type'].append(s)
					size=typeofdata[tp]
					dic['size'].append(size)
					dic['status'].append('D')
		
			count+=1
		elif(count>1):
			if(size==4 or size==8 or size==10):
				dic['addr'].append(hex(size*len(s.split(','))+int(str(dic['addr'][cn-1]),16))[2:])
				#dic['ele'].append(s)
			elif(size==1):
				st=st+' '+t[count]
				count+=1
				if(count==len(t)):
					le=sc=c=0
					for ch in st:
						if((ch==str('"') and sc < 2)):
							sc+=1
							le=le
						elif(ch==str(',') or c==0):
							c+=1
						else:
							le+=1
						
			elif(size==0):
				if(s=='$' or s=='-' or s=='$-'):
					size=0
				else:
					c=0
					for i in dic['sym']:
						if(i==s):
							dic['addr'].append(hex(int(str(dic['addr'][c]),16)+int(str(dic['addr'][cn-1]),16))[2:])
							dic['ele'].append('-')
						c+=1
	if(size==1):
		dataLiteral(st,cn,size)
		lst_table['instruction'].append(st)
		dic['addr'].append(hex(int(lensr1)+int(str(dic['addr'][cn-1]),16))[2:])
		#dic['ele'].append(st)
		
	elif(size>1):
		dataLiteral(s,cn,size)
		lst_table['instruction'].append(s)
	temp=r.split()
	temp[0]=dic['symN'][len(dic['symN'])-1]
	#intermed['Iline'].append(' '.join(temp))
	return cn

#-------------------------------------------------------------------------------

def dataLiteral(r,cn,size):
	global Literal_NO
	dym='lit#'+str(Literal_NO)
	lit_table['Line No'].append(cn)
	lit_table['Literal_NO'].append(Literal_NO)
	lit_table['Symbol'].append(dym)	
	#dic['ele'].pop()
	dic['ele'].append(dym)
	l=hexconvert(r,cn,size)
	lit_table['Literal'].append(r)
	lst_table['hex'].append(l)
	lit_table['Hex'].append(l)
	lit_table['Type'].append('-')
	Literal_NO=Literal_NO+1

def hexconvert(r,cn,size):
	global lensr1,lensr2
	lensr1=lensr2=0
	sringofhex=sr1=sr2=""
	sringofhexlist=[]
	d=r
	dw=dd=0
	if(size==1):
		for e in range(len(d)-1,0,-1):
			if((d[e]=='"'and dd!=1) or dd==1):
				if((d[e]=='"' or d[e]=="'") and dd!=1 ):
						dd=1
						dw=1
						sr1=sr1+sringofhex
						sringofhex=""
						continue
				if(dd==1):
					if(d[e]=='"' or d[e]=='"'):
						continue
					sr2=d[e]+sr2
					sringofhexlist.append(sr2)
			else:
			  sringofhex=d[e]+sringofhex

		sre=0
		if(sr1==''):
			sre=1
			lensr2=0
		sr1=sr1.split(',')
		st=""
		for sr2in in sr2:
			st=st+charTohex(sr2in)
			lensr2=lensr2+1

		if(sre!=1):
			for s in sr1:
				if(s==''):
					continue
				elif(True==s.isdigit()):
					st=st+intTohex(s,size)
					lensr2=lensr2+1
		lensr1=(lensr1+lensr2)-1		
		return st
	else:
		lensr1=0
		st=""
		d=d.split(',')
		for ed in d:
			st=st+intTohex(ed,size)
			lensr1=lensr1+1
		lensr1
		return st
		
	
def charTohex(word):
	return hex(ord(word))[2:]
			
def intTohex(word,size):
	lk=size*2
	v=str(hex(int(word))[2:])
	for k in range(0,lk-len(v)):
		v=v+'0'
	return v
def opcodeG(r,line_no):
	global Literal_NO
	opcodeforreg=""
	stri=""
	s=r.strip()
	s=s+'?'
	strn=interme=""
	slen=len(s)
	count=flag=flagforO=0
	for i in range(0,slen):
		if(s[i]==':' or s[i]==' ' or s[i]==',' or s[i]==';' or s[i]=='[' or s[i]==']' or s[i]=='?'):
			if(strn==""):
				continue
			if(s[i]==':'):
				strn=""
				continue
			if(strn!=""):
				for i in range(len(macro)):
					if(strn==macro[i]):
						interme=interme+strn
				for j in ins:	
					if(strn==j):
						stri=stri+strn
						interme=interme+strn
						strn=""
						break

				if(True==(strn.isdigit())):  #for the literal values
					digi=strn
					l=len(strn)
					if(True==stri[-2:].isdigit()):
						l=stri[-2:]
					elif(l<=3):
						l='08'
					elif(l<=5):
						l='16'
					elif(l<=10):
						l='32'
					stri=stri+' '+'lit'+l
					opcodeforreg=opcodeforreg+' '+hex(int(strn))  #this for the literal values constant 
				if('y'==check_reg(strn)):
					opcodeforreg=opcodeforreg+' '+format(rs[strn][1],'03b')
					
				if('y'==check_con(strn)):
					opcodeforreg=opcodeforreg+' '+'(00000000)'
					break
			strn=""		
		else:
			strn+=s[i]
		i+=1
	st=stri.split()
	for cl in st:
		if(cl[:3]=='lit'):
			dym='lit#'+str(Literal_NO)
			interme=interme+' '+dym
			lit_table['Line No'].append(line_no)
			lit_table['Literal_NO'].append(Literal_NO)
			lit_table['Literal'].append(digi)
			lit_table['Hex'].append(hex(int(digi)))
			lit_table['Symbol'].append(dym)
			lit_table['Type'].append(stri[stri.index(' ')+1:])
			Literal_NO=Literal_NO+1

	
#-------------------------------------------------------------------------------
def check_reg(var):
	for reg in rs:
		if(var==reg):
			return 'y'
	return 'n'
def check_sym(sym):
	ct=0
	for sy in dic['sym']:
		if(sy==sym):
			return 'y',ct
		ct=ct+1
	return 'n',0
def check_con(con):
	for i in constart:
		if(con==i):
			return 'y'
	return 'n'
#-----------------------
#-------------------------------------------------------------------------------
def bss(r,cn):
	#print(r)
	global line_no,Symbol_NO
	lst_table['line_num'].append(cn)
	lst_table['hex'].append(' ')
	lst_table['instruction'].append(r)
	dic['seg'].append('bss')
	t=r.split()
	ct=0
	size=0
	for e in t:
		if(ct==0):
			dic['sym'].append(e)
			dic['symN'].append('sym'+str(Symbol_NO))
			Symbol_NO=Symbol_NO+1
			ct+=1
		elif(ct==1) :
			ct+=1
			for typebs in typeofbss:
				if(typebs==e):
					dic['type'].append(e)
					size=typeofbss[e]
					dic['size'].append(size)
					dic['status'].append('R')
		elif(ct==2):	
			dic['addr'].append(hex(int(size*int(e))+int(str(dic['addr'][cn]),16))[2:])	
			cn=cn+1			
			dic['ele'].append('-')
	t[0]='sym'+str(Symbol_NO)
	t[2]=str(size)		
	#print(' '.join(t))
	#intermed['Iline'].append(' '.join(t))
	#interme=interme+'lit'+str(lit_table['Literal_NO'][len(lit_table['Literal_NO'])-1])
	return cn
#----------------------------------------------

	
#----------------------------------------------
def MergeTwoSymTable(dic,dic1,lineNo,sym,line_no):
	#print("last line number of 1st program: ",line_no)
	for i in range(len(dic1['sym'])):
		dic['lineNo'].append(line_no+dic['lineNo'][i])
		dic['symN'].append('sym'+str((lineNo+i+1)))
		dic['sym'].append(dic1['sym'][i])
		dic['type'].append(dic1['type'][i])
		dic['size'].append(dic1['size'][i])
		dic['addr'].append(dic1['addr'][i])
		dic['status'].append(dic1['status'][i])
		dic['seg'].append(dic1['seg'][i])
		dic['ele'].append(dic1['ele'][i])
	
	for i in range(len(dic['sym'])):
		print(dic['lineNo'][i],'\t',dic['symN'][i],'\t',dic['sym'][i],'\t',dic['type'][i],'\t',dic['size'][i],'\t',dic['addr'][i],'\t',dic['status'][i],'\t',dic['seg'][i],'\t',dic['ele'][i])


#------------------------------------
def TwoPass():
	for i in range(len(dic['status'])):
		if(dic['status'][i]=='U'):
			print("Symbol `",dic['sym'][i],"` not defined ")
			exit()
		if(dic['type'][i]=='_start'):
			main=dic['sym'][i]
	flag=line=0
	fp=open(filename,'r')
	for r in fp.readlines():
		line=line+1
		r=r.strip()
		if(r.find("section .text")!=-1):
			flag=1
		if(flag==1):
			f1.text2(r,line)
#------------------------------------
def calldefunction():
	regval={'er0':'0','er1':'0','er2':'0','er3':'0','er4':'0','er5':'0','er6':'0','er7':'0'}
	breakpoint=[]
	showregis=[]
	backtrace="No stack"
	print("debugger start: ",'\n')
	print("(gdb)")
	inp=input()
	inp=inp.split()
	if('q'==inp[0]):
		exit()
	while('r'!=inp[0]):
		if('b'==inp[0]):	
			for j in range(len(dic['sym'])):
				if(inp[1]==dic['sym'][j]):
					breakpoint.append(inp[1])
					print("break point", len(breakpoint),"at '",inp[1],"'")
					break
				if(len(dic['sym'])-1==j):
					print("Function ","'",inp[1],"'"," not defined.")
					print("Make breakpoint pending on future shared library load? (y or [n])")
					if('y'==input()):
						breakpoint.append(inp[1])
		elif(inp[0]=='p' or inp[0]=='disp'):
			showregis.append(inp[1])
			for j in regval:
				if(inp[1][1:]==j):
					print(inp[1],"=",regval[j])
		elif('q'==inp[0]):
			print("A debugging session is active.")
			print("Quit anyway? (y or n)")
			print(exit() if(input()=='y') else print("continue"))

		print("(gdb)")
		inp=input()
		inp=inp.split()
	if(inp[0]=='r'):
		for i in showregis:
			print(i,"=",regval[i[1:]])
		for i in intermed['Iline']:
			s=i.split()
			print("(gdb)")
			inp=input()
			inp=inp.split()
			if('ni'==inp[0]):
				print("next instruction : " ,i)
				for i in showregis:
					print(i,"=",regval[i[1:]])
				for j in macro:
					if(s[0]==j):
						True
				if(s[0]=='xor'): 
					if(regval[s[1]].isdigit()==regval[s[2]].isdigit()):
						regval[s[1]]=str(int(regval[s[1]])^int(regval[s[2]]))
					#print( "xor operation",regval[s[1]]); 
				elif(s[0]=='mov'):
					if('[' in s[2]):
						for j in range(len(lit_table['Symbol'])):
							if(lit_table['Symbol'][j]==s[2][1:len(s[2])-1]):
								s[2]=str(lit_table['Literal'][j])
								break
					if('[' not in s[2] and 'lit#' in s[2]):
						for j in range(len(lit_table['Symbol'])):
							if(lit_table['Symbol'][j]==s[2]):
								s[2]=str(lit_table['Literal'][j])
								break
	
					for j in regval: 
						if(s[2]==j):
							s[2]=regval[s[2]]
							#print("move operarion")
							break	
					for j in regval: 
						if(s[1]==j):
							regval[s[1]]=s[2]
							#print("move operarion",regval[s[1]])
							break
					if('[' in s[1]):
						if('[' in s[1]):
							for j in range(len(lit_table['Symbol'])):
								if(lit_table['Symbol'][j]==s[1][1:len(s[2])-1]):
									lit_table['Literal'][j]=s[2]
									break
					#print(regval,"SFGSGFSD",i)
				elif(s[0]=='add'): 
					for j in regval: 
						if(s[2]==j):
							s[2]=regval[s[2]]
							#print("add operarion")
							break	
					for j in regval: 
						if(s[1]==j):
							regval[s[1]]=str(int(regval[s[1]])+int(s[2]))
							#print("add operarion",regval[s[1]])
							break
				elif(s[0]=='int' and s[1]=='0x80'):
						#print(regval)
						if(regval['er0']=='4'):
							if(regval['er3']=='0' or regval['er3']=='1' ):	
								if(regval['er1']!=""):
									print(regval['er1'][1:int(regval['er2'])])
		
				elif(s[0]=='sub'): 
					for j in regval: 
						if(s[2]==j):
							s[2]=regval[s[2]]
							#print("add operarion")
							break	
					for j in regval: 
						if(s[1]==j):
							regval[s[1]]=str(int(regval[s[1]])-int(s[2]))
							#print("add operarion",regval[s[1]])
							break
				elif(s[0]=='mul'): 
					return "two";

			elif('backtrace'==inp[0]):
				print(backtrace)   # previous command executed structure
			elif(inp[0] in breakpoint):
				print('reatch breackpoint')
		print("The program is not being run.")
						
#------------------------------------
if __name__ == '__main__': 
	arg=argv
	length=len(arg)
	if(length==2):
		filename=argv[1]
		err=sym(filename)
		#print("End of program")
	elif(length==3):
		filename=argv[2]
		err=sym(filename)
		err=TwoPass()
		if(err==0):
			err=1
		fp1=open("symbol.txt",'w')
		fp2=open("objectcode","w+")
		fp3=open("interme",'w')
		if(arg[1]=='-s'):
			i=0
			print("----------------*Symbol table*-----------------")	
			print('L_no','\t','SymNa','\t','sym','\t','type','\t','size','\t','addr','\t','status','segment','\t','ele','\n')
			for i in range(len(dic['sym'])):
				print(dic['lineNo'][i],'\t',dic['symN'][i],'\t',dic['sym'][i],'\t',dic['type'][i],'\t',dic['size'][i],'\t',dic['addr'][i],'\t',dic['status'][i],'\t',dic['seg'][i],'\t',dic['ele'][i])
				i=i
				sym=dic['symN'][i]
			print('\n')
			#MergeTwoSymTable(dic,dic,i+1,sym,line_no)
				
		elif(arg[1]=='-l'):	
			print("----------------*literal table*-----------------")
			print('LineNo','\t','LitNo','\t','Sym','\t','Lial','\t\t\t','Hex','\t\t\t\t','Type')
			for lit in range(0,len(lit_table['Line No'])):
				print(lit_table['Line No'][lit],'\t',lit_table['Literal_NO'][lit],'\t',lit_table['Symbol'][lit],'\t',lit_table['Literal'][lit],'\t\t\t',lit_table['Hex'][lit],'\t\t\t',lit_table['Type'][lit])
				
		elif(arg[1]=='-lst'):
			print('\n',"----------------*lst file table*-----------------")
			print('line_num','\t\t',' ','\t','instruction')
			for i in range(0,len(lst_table['line_num'])):
				print(lst_table['line_num'][i],' ',lst_table['hex'][i],'\t\t',lst_table['instruction'][i])
		elif(arg[1]=="-intr"):
			print('\n',"----------------*intermediate file *-----------------")
			for i in intermed['Iline']:
				if(len(i.split())==1):
					print(i)
					continue
				print('\t'+i)
		else:
			print("Your enter invalide argument")
	fp1.write('LineNo'+'\t'+'LitNo'+'\t'+'Sym'+'\t'+'Lial'+'\t\t\t'+'Hex'+'\t\t\t\t'+'Type'+'\n')
	for lit in range(0,len(lit_table['Line No'])):
		fp1.write(str(lit_table['Line No'][lit])+'\t'+str(lit_table['Literal_NO'][lit])+'\t'+str(lit_table['Symbol'][lit])+'\t'+str(lit_table['Literal'][lit])+'\t\t\t'+str(lit_table['Hex'][lit])+'\t\t\t'+str(lit_table['Type'][lit])+'\n')

	for i in range(0,len(lst_table['line_num'])):
		if(lst_table['hex'][i].strip()!=""):
				fp2.write(lst_table['hex'][i].strip()+'\n')
	fp2.close()
	for i in intermed['Iline']:
		if(len(i.split())==1):
			fp3.write(i+'\n')
			continue
		fp3.write('\t'+i+'\n')
	fp3.close()
	print("You want to debug it: y/n:")
	if('y'==input()):
		calldefunction()

