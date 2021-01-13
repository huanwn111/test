# coding: utf-8
from py2neo import Graph, Node, Relationship
import pandas as pd
import re
import os
import json

'''
将json格式关系数据读取，cypher语句写入neo4j图数据库。
原理：将json格式中的一对多关系中的多存成数组。
写方法遍历一对应多中的每个创建关系；
涉及到的实体全部各自归到各自的实体数组中，创建实体；
'''
class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # self.data_path = os.path.join(cur_dir, 'data/diseaseShort.csv')
        self.data_path_man = os.path.join(cur_dir,'data/medical.json')#读慢病管理原如数据
		#本地
        self.graph = Graph("http://localhost:7474", username="neo4j", password="123")#生成图数据存储地址

    

    def read_file(self):
        # 实体
        drugs = []#药物，包括commin_drug和recommand_drug
        # common_drug = []
        # recommand_drug = []
        foods = [] #食物
        # not_eat = []
        # doe_at = []
        # recommand_eat = []
        checks = []#检查
        departments = []#科室
        producers = []#药品厂商
        diseases = []  # 疾病
        symptoms = []  # 症状，包含并发症
        # acompany = [] #并发症
        #以下几项描述性的不做为节点发出内容
        # desc = []
        # prevent = []
        # cause = []
        # 每一条疾病节点汇总列表
        diseases_infos = []

        # 关系
        category_to_department = []#一级科室 - 二级科室关系
        disease_to_noteat = []#病 - 禁吃
        disease_to_doeat = []#病 - 宜吃
        disease_to_recommandeat = []#病 - 推荐食物
        disease_to_commondrug = []#病 - 通用药品
        disease_to_recommanddrug = []#病 - 热点药品
        disease_to_check = []#病 - 检查项
        drug_to_producer = []#厂商 - 药物
        disease_to_symptom = []  # 疾病 - 症状
        disease_to_acompany = []# 疾 - 并发症
        disease_to_category = []# 病 - 科室

        # all_data = pd.read_csv(self.data_path, encoding='utf8').loc[:, :].values
        all_data = open(self.data_path_man,"r",encoding='UTF-8')

        print("00000o json数据信息 000000",all_data)

        count = 0
        for data in all_data:
            disease_dict = {}  # 疾病信息
            count += 1
            print(count)
            data_json = json.loads(data)
            #==单一属性，无一对多关系的，直接 k-v对 加入字典
            # 疾病
            disease = data_json['name']
            disease_dict["name"] = disease#加节点
            #disease加入疾病列表
            diseases.append(disease)
            #初始化其它疾病属性
            disease_dict['desc'] = ''
            disease_dict['prevent'] = ''
            disease_dict['cause'] = ''
            disease_dict['easy_get'] = ''
            disease_dict['cure_department'] = ''
            disease_dict['cure_way'] = ''
            disease_dict['cure_lasttime'] = ''
            disease_dict['symptom'] = ''
            disease_dict['cured_prob'] = ''
            
            #==单纯一对一属性节点,没有关系的==
            # 描述
            if 'desc' in data_json:
                disease_dict["desc"] = data_json['desc']
            # 预防
            if 'prevent' in data_json:
                disease_dict["prevent"] = data_json['prevent']
            # 病因
            if 'cause' in data_json:
                disease_dict["cause"] = data_json['cause']
            # 患病率
            if 'get_prob' in data_json:
                disease_dict["get_prob"] = data_json['get_prob']
            # 易感人群
            if 'easy_get' in data_json:
                disease_dict["easy_get"] = data_json['easy_get']
            # 治疗方法
            if 'cure_way' in data_json:
                disease_dict["cure_way"] = data_json['cure_way']
            # 治愈周期
            if 'cure_lasttime' in data_json:
                disease_dict["cure_lasttime"] = data_json['cure_lasttime']
            # 治愈率
            if 'cured_prob' in data_json:
                disease_dict["cured_prob"] = data_json['cured_prob']


            #==有多个属性（如症状）的拆分，加对应关系数组==
            # 症状
            if 'symptom' in data_json:
                symptom_list = data_json['symptom']
                for symptom in symptom_list:
                    # symptoms.append(symptom)#【加节点，此病有关的症状加入数组】
                    disease_to_symptom.append([disease, symptom])#【拼接关系数组，前后为两者实体】
                symptoms += symptom_list#症状列表数组拼接
            # 并发症
            if 'acompany' in data_json:
                acompanyList = data_json['acompany']
                for acompany in acompanyList:
                    # acompany.append(acompany)#【加节点，此病有关的症状加入数组】
                    disease_to_acompany.append([disease, acompany])#【拼接关系数组，前后为两者实体】
                symptoms += acompanyList#for外面整个数组拼接
            # 用药
            if 'common_drug' in data_json:
                for common_drug in data_json['common_drug']:
                    # common_drug.append(common_drug)
                    disease_to_commondrug.append([disease, common_drug])
                drugs += data_json['common_drug']
            #推荐用药
            if 'recommand_drug' in data_json:
                recommand_drugList = data_json['recommand_drug']
                for recommand_drug in recommand_drugList:
                    # common_drug.append(common_drug)
                    disease_to_recommanddrug.append([disease, recommand_drug])
                drugs += recommand_drugList
            # 禁忌食物
            if 'not_eat' in data_json:
                not_eatList = data_json['not_eat']
                for not_eat in not_eatList:
                    # not_eat.append(not_eat)#【不用for出来一个个加，在循环外面数组整个拼接即可】
                    disease_to_noteat.append([disease, not_eat])
                foods += not_eatList#for里面append，外面整个数组可直接拼接
            #宜吃食物
            if 'do_eat' in data_json:
                do_eatList = data_json['do_eat']
                for do_eat in do_eatList:
                    disease_to_doeat.append([disease, do_eat])
                foods += do_eatList#for里面append，外面整个数组可直接拼接
            #推荐食物
            if 'recommand_eat' in data_json:
                recommand_eatList = data_json['recommand_eat']
                for recommand_eat in recommand_eatList:
                    disease_to_recommandeat.append([disease, recommand_eat])
                foods += recommand_eatList
            # 检查项
            if 'check' in data_json:
                checkList = data_json['check']
                for check in checkList:
                    disease_to_check.append([disease,check])
                checks += checkList #for里面append，外面整个数组可直接拼接
            #药品细节
            if 'drug_detail' in data_json:
                drug_detail = data_json['drug_detail']
                #思力华(噻托溴铵粉吸入剂)
                producer = [ i.split('(')[0] for i in drug_detail]
                producers += producer#本身是数组，数组拼接不用append
                #厂商和药品关系，数组拼接用+=，不用append
                drug_to_producer += [ [i.split('(')[0],i.split('(')[-1].replace(')','')] for i in drug_detail]
            #科室['内科','神经内科']有二级科室有只有一级科室，分开处理，一二级科室分别加与疾病的关系，一二级科室之间加关系
            if 'cure_department' in data_json:
                cure_department = data_json['cure_department']
                if len(cure_department) == 1:#只有一级科室
                    disease_to_category.append([disease,cure_department[0]])
                if len(cure_department) == 2:#有二级科室
                    big = cure_department[0]
                    small = cure_department[1]
                    category_to_department.append([small,big])
                    disease_to_category.append([disease,small])

                disease_dict['cure_department'] = cure_department
                departments += cure_department

            diseases_infos.append(disease_dict)#【存放属性节点，本条病数据append进列表】
        
        return set(drugs),set(foods),set(checks),set(departments),set(producers),set(symptoms),set(diseases),diseases_infos,\
        category_to_department,disease_to_noteat,disease_to_doeat,disease_to_recommandeat,disease_to_commondrug,disease_to_recommanddrug,\
        disease_to_check,drug_to_producer,disease_to_symptom,disease_to_acompany,disease_to_category

    #创建节点方法 - 包含一个name的节点
    def create_node(self,label,nodes):#label标签名称，node节点集合，如 症状{'鼻衄', '血糖值升高', '步态异常'

        count = 0
        for node_name in nodes:#遍历每个症状词，创建加到symptom节点中
            node = Node(label,name = node_name)
            self.graph.create(node)#创建节点 self.graph数据库对象创建节点。
            count += 1
            print(count,len(nodes))
        return

    #创建疾病节点方法-中心节点（包含多个属性的复合节点）
    def create_diseases_nodes(self,disease_info):#参数：所有疾病对象列表，如[{'name': '中耳炎'}, {'name': '1型糖尿病'},
        count = 0
        for disease_dict in disease_info:
            node = Node("Disease", name = disease_dict['name'], desc = disease_dict['desc'], 
            prevent = disease_dict['prevent'], cause = disease_dict['cause'],
            easy_get = disease_dict['easy_get'], cure_lasttime = disease_dict['cure_lasttime'],
            cure_department = disease_dict['cure_department'],cure_way = disease_dict['cure_way'],
            cured_prob = disease_dict['cured_prob'])

            self.graph.create(node)
            count +=1
            print(count)

        return


    #创建关系方法
    def create_relationship(self,start_node,end_node,edges,rel_type,rel_name):
        #参考：起始节点，尾节点，关系数组，关系类型，关系名
        count = 0
        #对edges关系数组去重处理，以###拼接数组的两项，去重后再拆分开
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge_ = edge.split('###')
            p = edge_[0]
            q = edge_[1]
            #创建关系sypher语句
            query = "match(p:%s),(q:%s) where p.name = '%s' and q.name = '%s' create (p) - [rel:%s{name:'%s'}] -> (q)" % (start_node
            , end_node, p, q, rel_type, rel_name)
            #执行sypher语句
            try:
                self.graph.run(query)
                count += 1
                print(rel_type,count,all)
            except Exception as e:
                print(e)
        return

    #加图谱实体
    def create_graphNodes(self):

        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos,category_to_department,disease_to_noteat,disease_to_doeat,disease_to_recommandeat,disease_to_commondrug,disease_to_recommanddrug,disease_to_check,drug_to_producer,disease_to_symptom,disease_to_acompany,disease_to_category = self.read_file()
        #加疾病实体
        self.create_diseases_nodes(disease_infos)
        #加其它实体
        self.create_node("Drug",Drugs)
        self.create_node("Food",Foods)
        self.create_node("Check",Checks)
        self.create_node("Drug",Drugs)
        self.create_node("Department",Departments)
        self.create_node('Producer', Producers)
        self.create_node("Symptom",Symptoms)
    
        return

    #加图谱关系
    def create_graphRels(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos,category_to_department,disease_to_noteat,disease_to_doeat,disease_to_recommandeat,disease_to_commondrug,disease_to_recommanddrug,disease_to_check,drug_to_producer,disease_to_symptom,disease_to_acompany,disease_to_category = self.read_file()

        self.create_relationship("Disease","Food",disease_to_recommandeat,"recommand_eat","推荐食谱")
        self.create_relationship("Disease","Food",disease_to_noteat,"no_eat","忌吃")
        self.create_relationship("Disease","Food",disease_to_doeat,"do_eat","宜吃")
        self.create_relationship('Department','Department',category_to_department,'belongs_to','属于')#一级科室与二级科室关联
        self.create_relationship('Disease','Department',disease_to_category,'belongs_to','所属科室')#疾病所属科室
        self.create_relationship('Disease','Drug',disease_to_commondrug,'common_drug','常用药品')
        self.create_relationship('Producer','Drug',drug_to_producer,'drugs_of','生产药品')#厂商生产药品
        self.create_relationship('Disease','Drug',disease_to_recommanddrug,'recommand_drug','好评药品')
        self.create_relationship('Disease','Check',disease_to_check,'need_check','诊断检查')
        self.create_relationship("Disease","Symptom",disease_to_symptom,"has_symptom","症状")
        self.create_relationship("Disease","Symptom",disease_to_acompany,"acompany_with","并发症")


    #创建图谱关系

    #静态测试方法
    def test(self):
        #静态测试创建节点cypher语句
        # node = Node("测试结点",name = "我是测试节点111")
        # self.graph.create(node)
        # node2 = Node("测试结点",name = "我是测试节点222")
        # self.graph.create(node2)
        #创建复合节点测试
        # node = Node("病",name = "病一", age ="15岁")
        # self.graph.create(node)

        #关系创建cypher语句-去重处理
        # set_edges = []
        # edges = [['中耳炎', '耳内流脓'], ['1型糖尿病', '多尿']]
        # for edge in edges:
        #     set_edges.append('###'.join(edge))
        # print("3333333",set_edges)
        # for edge in set(set_edges):
        #     rel_st = edge.split("###")[0]
        #     rel_ed = edge.split("###")[1]
        #     query = "match(p:)"……

        #关系创建cypher语句
        #先建两个示例节点中耳炎，耳内流脓，建立它们的关系。
        # node = Node("Disease",name="中耳炎")
        # self.graph.create(node)
        # node = Node("Symptom",name="耳内流脓")
        # self.graph.create(node)
        #建立 中耳炎 和 耳内流脓 的关系
        # query = "match(p:Disease),(q:Symptom) where p.name = '中耳炎' and q.name = '耳内流脓' create (p) - [rel:HAS_SYMPTOM{name:'症状'}]->(q)"
        # self.graph.run(query)

        return
    '''导出数据'''
    # def export_data(self):
    #     return

if __name__ == "__main__":
    #==测试各方法==
    graphNew = MedicalGraph()
    Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos,category_to_department,disease_to_noteat,disease_to_doeat,disease_to_recommandeat,disease_to_commondrug,disease_to_recommanddrug,disease_to_check,drug_to_producer,disease_to_symptom,disease_to_acompany,disease_to_category = graphNew.read_file()
    # print("33333333 Drugs 333333333",Drugs,"\n")
    # print("33333333 disease_infos 333333333",disease_infos,"\n")
    # print("33333333 disease_to_check 333333333",disease_to_check,"\n")
    # print("33333333 disease_to_category  333333333",disease_to_category ,"\n")
    # graphNew.create_node("symptom",symptom)#开始创建节点
    # 静态测试方法
    # graphNew.test()
    #加图谱实体、关系
    graphNew.create_graphNodes()
    graphNew.create_graphRels()
    pass    