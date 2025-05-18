stored,ú,i,ü,ũ,ū,len,ů,ű,range,list,ṷ,ụ=chr,ord,abs,input,all,print,len,input,pow,range,list,dict,set
stored=[12838,1089,16029,13761,1276,14790,2091,17199,2223,2925,17901,3159,18135,18837,3135,19071,4095,19773,4797,4085,20007,5733,20709,17005,2601,9620,3192,9724,3127,8125]
three,_256=3,256
ṷ=input()
res=list(ụ([pow(three,i,_256) for i in(range(_256))]))[three:len(stored)+three]
zip=zip
ṷ=[ú(i) for i in(ṷ)]
assert(len(stored)==len(ṷ))
assert(ũ([i*j==k for i,j,k in(zip(res,ṷ,stored))]))
