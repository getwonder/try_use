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


    
#获取一个月账本的总数目
def get_total():
	try:
		data_dict=file_to_dict(sys.argv[1])
	except Exception:
		data_dict=file_to_dict()
	print(data_dict)
	sum=sum_all(data_dict)
	print(sum)
	
	with open("./result.txt","w", encoding='UTF-8') as f:
		f.write(str(sum))


# get_total()

#对数据进行分类
'''
项目:
衣服
超市
医
零食和水果
外出就餐
耐用品
其他
回桐城
车（行）
手机
'''
#对账本进行分类，并打印
def classfy():
    try:
        data_dict=file_to_dict(sys.argv[1])
    except Exception:
        data_dict=file_to_dict()
    
    #设置不同的类对应的关键字
    class_types=["超市","衣服","医","零食和水果","外出就餐","耐用品","车和出行","手机"]  #回家，特殊的先拎出来+其他  
    included_types=[
        "(超市|大润发|梦之城超市)",
        "(袜子|内裤|衣|裤)",
        "(医|医院|孕前检查|药)",
        "(桃|橘|板栗|柚子|水果|枣)",
        "(江边城外|生煎|汁|汤|饭|餐|馍|馄饨|小吃|羊肉|牛肉|煎饼)",
        "(手机|U盘|耐用品)",
        "(加油|过路)",
        "(话费)"]
    
    result_dict={}
    result_dict["其他"]={}     #收集未被匹配的项
    for class_type in class_types:
        result_dict[class_type]={}
    for momth_date in data_dict:    #迭代每一天的数据
        for consume in data_dict[momth_date]:    #迭代每一天的各项数据
            for i in range(len(class_types)):
                tmp=re.findall(included_types[i],consume)     #对各个类进行匹配
                if tmp:
                    key=tmp[0]
                    if momth_date not in result_dict[class_types[i]]:
                        result_dict[class_types[i]][momth_date]={}
                    result_dict[class_types[i]][momth_date][consume]=data_dict[momth_date][consume]
                    break
                elif i==(len(class_types)-1):
                    if momth_date not in result_dict["其他"]:
                        result_dict["其他"][momth_date]={}
                    result_dict["其他"][momth_date][consume]=data_dict[momth_date][consume]
                    
    class_types.append("其他")     #添加剩余的所有数据
    #分类打印,分类求和
    for class_type in class_types:
        print ("*"*10+class_type+"*"*10)
        for momth_date in result_dict[class_type]:     #分类打印
            print(momth_date)
            for consume in result_dict[class_type][momth_date]:
                print(consume,result_dict[class_type][momth_date][consume])
        sum=sum_all(result_dict[class_type])           #分类求和
        print("total: ",sum)  


def  main():
    classfy() #对账本进行分类，并打印
    print("#"*10+"消费总数"+"#"*10)
    get_total() #获取一个月账本的总数目

main()




































