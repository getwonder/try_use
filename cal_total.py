import re 
import sys

def file_to_dict(filePath="./data.py"):
    with open(filePath,"r", encoding='UTF-8') as f:  #UnicodeDecodeError: 'gbk' codec can't decode byte
        lines=f.readlines()
    #文件中的数据写入字典
    data_dict={}
    reg_str1="^\s*(\d+\.\d+)\s*$"
    reg_str2="\s*(.+)\s+(.+)$"
     
    for line in lines:
        tmp=re.findall(reg_str1,line)    #['9.1']
        if tmp:
            key=tmp[0]
            if key not in data_dict:
                data_dict[key]={}
        
        value=re.findall(reg_str2,line)  #[('矿泉水\xa0', '2.5+2')]
        if value:
            if value[0][0] in data_dict[key]:
                raise Exception(str(key)+" 已经存在该项记录: "+str(value[0][0]))
            data_dict[key][value[0][0]]=value[0][1]
    return data_dict



def sum_arr(arr):
    sum=0
    for i in arr:
        sum+=float(i)
    return sum

# arr=['2.5', '2', '16', '16', '18.8', '11.4', '20', '21', '160']
# sum=sum_arr(arr)
# print(sum)

# a={'9.1': {'矿泉水\xa0': '2.5+2', '生煎\xa0\xa0': '16+16', '桃和橘子': '18.8', '水蜜桃': '11.4', '剪头发': '20', '鲜之恋情水蜜桃雪梨汁': '21', '江边城外烤鱼2.5斤': '160'}, '9.2': {'梦之城超市': '58', '顺丰快递': '16+14'}}
def sum_all(a_dict):
    num_arr=[]
    for key1 in a_dict:
        for key2 in a_dict[key1]:
            nums=re.findall("[\d\.]+",a_dict[key1][key2])
            num_arr+=nums
        
    # print(num_arr)
    sum=sum_arr(num_arr)
    return sum
    
# sum=sum_all(a)
# print(sum)


    

def main():
	try:
		print(111111)
		data_dict=file_to_dict(sys.argv[1])
	except Exception:
		data_dict=file_to_dict()
	print(data_dict)
	sum=sum_all(data_dict)
	print(sum)
	
	with open("./result.txt","w", encoding='UTF-8') as f:
		f.write(str(sum))


main()

























