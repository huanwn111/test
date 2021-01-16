#==用python操作Neo4j==

#一、neo4j模块执行CQL（cypher）,GraphDatabase 
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7699/", auth = ("neo4j","123"))
#【注意看neo4j.conf，bolt的端口是7699，http端口是7878】

#==先定义函数，再用with driver.session() as session: session.write_transaction(函数名,参数)运行==
#添加结点函数
def addPerson(tx,name):
    tx.run("CREATE (a:Person{name:$name})",name = name)
#打印查询
def printPerson(tx,name):
    for rs in tx.run("MATCH(a:Person) where a.name = $name "#换行时两行分两个双引号括起。
    "RETURN a.name",name = name):
        print(rs["a.name"])#带头大哥

def main_neo4j():
    # print(driver)
    with driver.session() as session:
        # session.write_transaction(addPerson,"带头大哥")
        session.write_transaction(printPerson,"带头大哥")
#总结核心代码
#neo4j.GraphDatabase.driver(xxxx).session().write_transaction(函数(含tx.run(CQL语句)))
#或
#neo4j.GraphDatabase.driver(xxxx).session().begin_transaction.run(CQL语句)

#二、py2neo模块, Graph,Node,Relationship
from py2neo import Graph,Node,Relationship
g = Graph("http://localhost:7878/", auth = ("neo4j","123"))

def main_py2eo():
    tx = g.begin()
    #创建节点
    a = Node("Person",name="慕容复")
    b = Node("Person", name = "王语嫣")
    #创建关系
    ab = Relationship(a,"表哥",b)
    tx.create(a)
    tx.create(b)
    tx.create(ab)
    tx.commit()
    #查询
    CQL = "Match (n:Person) where n.name = '王语嫣' Return n.name"
    rs = g.run(CQL).data()#[{'n.name': '王语嫣'}, {'n.name': '王语嫣'}, {'n.name': '王语嫣'}]
    print(rs)
    
#总结：Graph(url,auth).begin().create(Node("Person",name="慕容复")).commit()
#Graph(url,auth).begin().create(Relation(Node("Person",name="慕容复"),"表哥",Node("Person",name="王语嫣")).commit()

if __name__ == "__main__":
    #neo4j模块测试
    # main_neo4j()

    main_py2eo()

    # pass

