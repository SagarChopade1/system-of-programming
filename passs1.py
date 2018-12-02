from mainfile import *
from pass1 import *
#This code for Second pass
macro_flag=0
paralist=[]
def text2(r,line_no):
	global Symbol_NO
	opcodeG2(r,line_no)
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
					intermed['Iline'].append(string)  #for lable import in intermediate
					occure=occure+1;
					flaglbl=0
					break
				elif(occure>=1 and flaglbl==1 and i==0):
					print("Symbol `",string,"` Redefine")
					break
				if(ft==1 and string!="global"):
					lst_table['line_num'].append(line_no)
					lst_table['hex'].append(' ')
					lst_table['instruction'].append(r)
					#intermed['Iline'].append(r)
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
				#intermed['Iline'].append(r)

				
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
					intermed['Iline'].append(string)
					Symbol_NO=Symbol_NO+1
					break

		else:
			strn+=s[i]	
		i+=1	
								
def opcodeG2(r,line_no):
	global Literal_NO
	opcodeforreg=temp=singleregistervalue=""
	stri=""
	s=r.strip()
	s=s+'?'
	strn=interme=modrm=""
	slen=len(s)
	count=flag=flagforO=byte=0
	for i in range(0,slen):
		stf=0
		if(s[i]==':' or s[i]==' ' or s[i]==',' or s[i]==';' or s[i]=='[' or s[i]==']' or s[i]=='?'):
			if(strn==""):
				continue
			if(s[i]==':'):											
				lst_table['line_num'].append(line_no)
				lst_table['hex'].append(' ')
				lst_table['instruction'].append(strn)
				strn=""
				continue
			if(strn!=""):
				for j in ins:	
					if(strn==j):
						stri=stri+strn
						interme=interme+strn
						#print(interme)     #   int intermediate
						strn=""
						break
					
				a,b=check_sym(strn)
				if(s[i]=='['):     #for memory operation
					for ty in mem:
						if(strn==ty):
							byte=mem[ty]
							interme=interme+' '+strn+s[i]
					if(opcodeforreg!=""):
						singleregistervalue=opcodeforreg
						opcodeforreg=""
						#print(singleregistervalue)
					
					
				elif(s[i]==']'):
				#	tp,cal=addrcal(strn)  
				#	print("TP:",tp,"CAL:",cal,"Return") #temp
					ct,base,modrm_in,interme=oprationcode(strn,interme,line_no)
				#	print(opcodeforreg,"ca=",ca)
					modrm=modrm+modrm_in
					if(len(ct)==2):
						opcodeforreg=ct+base
					#print(opcodeforreg,"after")
					interme=interme+s[i]
					if(len(strn.split('+') or strn.split('*') or strn.split('-'))>=1):
						stri=stri+' '+'memsib'
					else:
						stri=stri+' '+'mem'					

					#print(opcodeforreg,"opcodeforregopcodeforregopcodeforregopcodeforreg",modrm)
				elif('y'==a and dic['seg'][b]!='code'):
					tp=dic['ele'][b]
					if(dic['seg'][b]=='bss'):
						tp=str(dic['size'][b])
					interme=interme+' '+tp
					stri=stri+' '+'mem'

				#print(strn)		
				#handel jump line number
				if(s[i]!=']'):
					for i in range(len(dic['sym']) ):
						if(dic['sym'][i]==strn and dic['type'][i]=='lbl'):
							stf=1
							opcodeforreg=opcodeforreg+'lineNo'+str(dic['lineNo'][i]) 
						
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
					c=str(hex(int(strn))[2:])
					for i in range(len(str(dic['addr'][b])),8):
						c='0'+c
					if(opcodeforreg!=""):
						singleregistervalue=opcodeforreg
						opcodeforreg=""
					opcodeforreg='['+c+']'+' '#+opcodeforreg  #this for the literal values constant  also represent [ ] bracket 


				if('y'==check_reg(strn)):
					stri=stri+' '+rs[strn][0]
					interme=interme+' '+rs[strn][2]
					opcodeforreg=opcodeforreg+' '+format(rs[strn][1],'03b')
					modrm=modrm+format(rs[strn][1],'03b')

				#	print("modrm----====",modrm)
				#	print(opcodeforreg,"gh")
				if(strn=='0x80'):
					interme=interme+' '+'0x80'
					stri=stri+' '+'0x80'

				a,b=check_sym(strn)
				if('y'==a and (dic['seg'][b]!='code') ):
					if(opcodeforreg!=""):
						singleregistervalue=opcodeforreg
						opcodeforreg=""
						#print(singleregistervalue)
					stf=0
					c=str(dic['addr'][b])
					for i in range(len(str(dic['addr'][b])),8):
						c=c+'0'
					if(('{' in opcodeforreg)==False):
						if('sib' in stri):
							opcodeforreg=opcodeforreg+'{'+c+'}'
						else:
							opcodeforreg=opcodeforreg+'('+c+')'
				if('y'==check_con(strn)):
					stri=stri+' '+'mem'
					interme=interme+' '+'mem'
					opcodeforreg=opcodeforreg+' '+'(00000000)'
					break
				if('%' in strn and macro_flag):
					#print(paralist[int(strn[1:])-1],r)#take parmeter number %1 -1 and access element from parameter array paralist[1-1]
					interme=interme+' '+paralist[int(strn[1:])-1]
					#print(lit_table['Literal'][int(paralist[int(strn[1:])-1][4:])-1])
					if(lit_table['Literal'][int(paralist[int(strn[1:])-1][4:])-1].isdigit()):
						stri=stri+' '+'lit32'
					else:
						stri=stri+' '+'mem'
			strn=""		

		else:
			strn+=s[i]
		i+=1
	st=stri.split()
	tp=(' '.join(r.split(','))).split()
	for cl in range(len(st)):			#Not validation of literal constant values.
		if(st[cl][:3]=='lit'):
			#print(tp[cl],lit_table['Literal'])
			for k in range(len(lit_table['Literal'])):
				if(tp[cl]==lit_table['Literal'][k]):
					interme=interme+' '+str(lit_table['Symbol'][k])
					break
			#dym='lit#'+str(Literal_NO)
			#interme=interme+' '+dym
			Literal_NO=Literal_NO+1
	#print(stri,"intermediate",interme,"Line_no",line_no)		lst_tablelst_talst_tableble
	for i in range(len(macro)):
		if(macro[i]==stri[:stri.find(' ')]):
			instruction_type['ist'].append(interme)
			lst_table['line_num'].append(line_no)
			lst_table['instruction'].append(r)
			intermed['Iline'].append(interme)
			lst_table['hex'].append(' ')
			d=(' '.join(r.split(','))).split()
			del(d[0])
			#print(interme[interme.find(' ')+1:].split(),r[r.find(' ')+1:].split(),r,"ASDFASDFASFDSF")
			callmacfunc(interme[interme.find(' ')+1:].split(),d)#parameter of macros
	#print("stri:=",stri,"interme:=",interme,"opcode:=",r)
	coun=op=tt=0
	for opcode in instruction_type['ist']:
		tt=tt+1    
		if(opcode==stri):
			if(len(stri.split())==2):
				(stri.split()[1:][0])[:3]
			else:
				for i in modR:
					if((i==(stri.split()[1:][0])[:3]+' '+(stri.split()[1:][1])[:3])):
						op=modR[i]
						if(op==0 or op==1):
							modrm=format(op,'02')+modrm
						if(len(modrm)==8):
							temp=hex(int(modrm,2))[2:]
							if(len(temp)==1):
								temp='0'+temp
							opcodeforreg=opcodeforreg+' '+temp
			lst_table['line_num'].append(line_no)
			ls=opcodeforreg.split() #swap of register binary values
			#print(ls)
			if(len(ls)>=2):
				ls[0],ls[1]=ls[1],ls[0]
				opcodeforreg=''.join(ls)
				  #for register to register opcode 
				
			if(op!=0):
				op=str(bin(op)[2:])
				s=""
				if('{' in opcodeforreg ):
					s=opcodeforreg
					opcodeforreg=opcodeforreg[:opcodeforreg.index('{')]
					s=s[s.index('{'):s.index('}')+1]
				opcodeforreg=op+opcodeforreg
				opcodeforreg=format(int(opcodeforreg,2),'02x')+s
			else:	
				op=''
			if(singleregistervalue!=""): # purpose of add register to opcode of main instruction opcode
				if((interme[len(interme)-1])==']'):
					ope=hex(int(instruction_type['code'][coun]))[2:]
				else:
					ope=hex(int(singleregistervalue,2)+int(instruction_type['code'][coun]))[2:]

				if(len(ope)==1):
					ope='0'+ope
				lst_table['hex'].append((ope+str(opcodeforreg)).upper())
			else:
				ope=hex(int(instruction_type['code'][coun]))[2:]
				if(len(ope)==1):
					ope='0'+ope
				if(len(opcodeforreg)==4):
					lst_table['hex'].append((hex(int(ope,16)+int(opcodeforreg,2)))[2:].upper()) # for push reg32 or push reg16 opcode
				else:
					lst_table['hex'].append((ope+str(opcodeforreg)).upper())
			lst_table['instruction'].append(r)
			intermed['Iline'].append(interme)	
		coun=coun+1
	#End of opcode generation 
#----------------
def callmacfunc(param,oriparam):
	global macro_flag,paralist
	paralist=param
	for j in range(1,len(mline)-1,1):
		#macro_flag=1
		d=(' '.join(mline[j].split(','))).split()
		if("%" in mline[j]):
			for i in range(len(d)):
				if('%' in d[i]):
					d[i]=oriparam[int(d[i][1:])-1]
			d.insert(1,' ')
			d.insert(3,',')
			mline[j]=''.join(d)
		text2(mline[j],line_no)
	macro_flag=0
	paralist=[]
#===============
def oprationcode(exp,interme,line_no):
	global Literal_NO
	s=exp
	b=opr=tp=[]
	t=base=modrm_in=""
	sm=rg=0
	for i in ex:
		if((i in exp)==True):
			b=s.split(i)
			opr.append(i)
			s=' '.join(b)
	l=s.split()
#	print(l ,"in oprationcode",len(l))
	for i in l:
		a,b=check_sym(i)
		if('y'==a):			#[num1+eax*scale]
			for k in range(len(dic['sym'])):
				if(dic['sym'][k]==i):
					interme=interme+' ['+dic['ele'][k]			
					if(len(tp)!=0):
						interme=interme+tp.pop()
					break
			sm=1
			t='101'	
			base=hex(int(str(dic['addr'][b]),16)+1)[2:]
			for i in range(len(str(dic['addr'][b])),8):
				base=base+'0'
			base='{'+base+'}'
		elif('y'==check_reg(i)):
			for k in rs[i]:
				interme=interme+rs[i][2]
				if(len(tp)!=0):
					interme=interme+tp.pop()
				break
			rg=1
			t=format(int(rs[i][1]),'03b')+t
		elif(i.isdigit()==True):
			scale=int(i)
			lit_table['Line No'].append(line_no)
			lit_table['Literal_NO'].append(lit_table['Literal_NO'][len(lit_table['Literal_NO'])-1]+1)
			lit_table['Symbol'].append('lit'+str(lit_table['Literal_NO'][len(lit_table['Literal_NO'])-1]))
			lit_table['Literal'].append(scale)
			lit_table['Hex'].append(scale)
			lit_table['Type'].append('-')
			interme=interme+'lit'+str(lit_table['Literal_NO'][len(lit_table['Literal_NO'])-1])
			if(scale==0 or scale==2 or scale==4 or scale==8):
				for i in ad:
					if(i==str(scale)):	
						t=format(int(bin(ad[i])[2:]),'02')+t
						t=hex(int(t,2))[2:]
						if(len(t)==1):
							t='0'+t
						
						if(len(l)==1):
							if(rg==1 and sm!=1):
								modrm_in='100'
							elif(sm==1 and rg!=1):
								modrm_in='101'
							else:
								print("invalide paramerters :",l)
						else:
							modrm_in='100'
						return t,base,modrm_in,interme
						print("address of [ ] is ",t)  #[eax+ebx+scale]
	
	if(len(t)==6): #if =[eax+ebx]
		t='00'+t
		t=hex(int(t,2))[2:]
		if(len(t)==1):
			t='0'+t
	if(len(l)==1):
		if(rg==1 and sm!=1):
			modrm_in='100'
		elif(sm==1):
			modrm_in='101'
		else:
			print("invalide paramerters :",l)
	else:
		modrm_in='100'
	return t,base,modrm_in,interme	
	
		
	
#===============
def addrcal(exp):
#	oprationcode(exp)
	s=exp
	b=opr=[]
	for i in ex:
		if((i in exp)==True):
			b=s.split(i)
			opr.append(i)
			s=' '.join(b)
	l=s.split()
	a='n'
	scale=base=index=0
	for j in range(0,len(l)):
		if(l[j].isdigit()==True):
			scale=int(l[j])
			a=l[j]
			l[j]=str(l[j])
			if(scale==0 or scale==2 or scale==4 or scale==8):		#validation of scale
				for i in ad:
					if(i==str(scale)):	
						scale=ad[i]
			else:
				print("Scale values not valide ")
				exit()
		
		elif('y'==check_reg(l[j])):
			index=int(rs[l[j]][1])
			indexreg=l[j]
			regis=l[j]
			l[j]=str(rs[l[j]][1])
		a,b=check_sym(l[j])
		if('y'==a):
			base=str(dic['addr'][b])
			for i in range(len(str(dic['addr'][b])),8):
				base=base+'0'
			base='{'+base+'}'
	scale=format(scale,'02b')#scale in binary
	index=format(index,'03b')	#scale in binary
	if(base!=0):
		cal=str(scale)+str(index)
	#	print(base,cal,"IF")
		return base,cal
	else:
	#	print(str(scale)+' '+str(index),str(""),"ELSE")
		return str(scale)+' '+str(index),str("")

#-------------------for the : [var+eax*2]------------
	
def expres(exp,byte):
	s=exp
	b=opr=[]
	for i in ex:
		if((i in exp)==True):
			b=s.split(i)
			opr.append(i)
			s=' '.join(b)
	l=s.split()
	base=l[0]
	a='n'
	#print(l)
	for j in range(0,len(l)):
		if(l[j].isdigit()==True):
			a=l[j]
			l[j]=str(l[j])
		elif('y'==check_reg(l[j])):
			b=l[j]
			l[j]=str(rs[l[j]][1])

			
		a,b=check_sym(l[j])
		if('y'==a):
			c=str(dic['addr'][b])
			for i in range(len(str(dic['addr'][b])),8):
				c=c+'0'
			#print(l[j],str(dic['addr'][b]))
			l[j]=str(int(str(dic['addr'][b]),16))

	if(len(l)==1):
		return (hex(int(l[0]))[2:]),0,1
	
	pos=1
	for i in range(0,len(exp)):
		for j in ex:
			if(exp[i]==j):
				l.insert(pos,j)
				pos=pos+2

	exp=hex(eval(''.join(l)))
	hval=addresstohex(base,(int(exp,16)-int(l[0])),byte)
	#print(hval)
	val=addresstoval(base,(int(exp,16)-int(l[0])),byte)
	#print(val)
	return exp,val,hval

#------------------------function give address return values--------
def addresstohex(base,scale,byte):
	for i in range(len(dic['sym'])):
		if(base==dic['sym'][i]):
			litelement=dic['ele'][i]
			break
	for i in range(len(lit_table['Symbol'])):
		if(lit_table['Symbol'][i]==litelement):
			return lit_table['Hex'][i][scale*2:((scale*2)+(byte*2))]
			break
def addresstoval(base,scale,byte):
	s=""
	for i in range(len(dic['sym'])):
		if(base==dic['sym'][i]):
			litelement=dic['ele'][i]
			size=dic['size'][i]
			break
	for i in range(len(lit_table['Symbol'])):
		if(lit_table['Symbol'][i]==litelement):
			if(size!=1):
				lis=lit_table['Literal'][i].split(',')
				return lis[int(scale/4)]
			else:
				for j in range(len(lit_table['Literal'])):
					if(j>=scale):
						s=s+lit_table['Literal'][i][j]
				return s
			breakf
