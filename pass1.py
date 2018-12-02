from sys import argv
from dictionary import *
import passs1 as f1
flagformain=occure=lensr1=lensr2=line_no=0
Literal_NO=Symbol_NO=1	
def sym(filename):
	global line_no
	fp=open(filename,'r')
	cn=symNo=0
	count=1
	flag=-1
	for r in fp.readlines():
		line_no+=1
		r=r.strip()
		if(r==""):
			continue
		if(flag==(-1)):
			if(r!='section .bss'):
				if(r=='section .data'):
					intermed['Iline'].append('section .data')
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
				intermed['Iline'].append('section .bss')
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
					#print(line_no)
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
				if(string==j):
					#print("this symbol in symbol table",j)
					break
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
	intermed['Iline'].append(' '.join(temp))
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
	intermed['Iline'].append(' '.join(t))
	#interme=interme+'lit'+str(lit_table['Literal_NO'][len(lit_table['Literal_NO'])-1])
	return cn
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

