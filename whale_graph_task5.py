#===Task 5 Neo4j 图数据库查询===

#***===总
# 用户query实体识别（匹配）、意图识别（问题分类）后，
# 用图谱query查询构造cypher语句；
# 将问题转为CQL（cypher查询语句）；
# 查询返回结果；
# 根据不同意图返回不同模板答案；===*

class AnswerSearching:
    def __init__(self):
        pass
    # 主要是根据不同的实体和意图构造cypher查询语句

    def question_parser(self, data):
        """
        主要是根据不同的实体和意图构造cypher查询语句
        :param data: {"Disease":[], "Alias":[], "Symptom":[], "Complication":[]}
        :return:
        """
        pass
    
        # 将问题转变为cypher查询语句
    def transfor_to_sql(self, label, entities, intent):
        """
        将问题转变为cypher查询语句
        :param label:实体标签
        :param entities:实体列表
        :param intent:查询意图
        :return:cypher查询语句
        """
        pass

        # 将问题转变为cypher查询语句
    def transfor_to_sql(self, label, entities, intent):
        """
        将问题转变为cypher查询语句
        :param label:实体标签
        :param entities:实体列表
        :param intent:查询意图
        :return:cypher查询语句
        """
        pass

        # 根据不同意图，返回不同模板的答案
    def answer_template(self, intent, answers):
        """
        根据不同意图，返回不同模板的答案
        :param intent: 查询意图
        :param answers: 知识图谱查询结果
        :return: str
        """
        pass

#关于Neo4j:
# Neo4j是一个世界领先的开源图形数据库，由Java编写。图形数据库也就意味着它的数据并非保存在表或集合中，而是保存为节点以及节点之间的关系；
# Neo4j的数据由下面3部分构成：节点边和属性；
# Neo4j除了顶点（Node）和边（Relationship），还有一种重要的部分——属性。无论是顶点还是边，都可以有任意多的属性。属性的存放类似于一个HashMap，Key为一个字符串，而Value必须是基本类型或者是基本类型数组。
# 在Neo4j中，节点以及边都能够包含保存值的属性，此外：可以为节点设置零或多个标签（例如Author或Book）每个关系都对应一种类型（例如WROTE或FRIEND_OF）关系总是从一个节点指向另一个节点（但可以在不考虑指向性的情况下进行查询）

# Cypher 介绍：
# 是Neo4j的查询语言，“Cypher”是一个描述性的图形查询语言，允许不必编写图形结构的遍历代码对图形存储有表现力和效率的查询。
# 适合于开发者和在数据库上做点对点模式（ad-hoc）查询的专业操作人员，它的构念是基于英语单词和灵巧的图解。
# 它的焦点在于从图中如何找回（what to retrieve），而不是怎么去做。不对用户公布的实现细节里关心的是怎么优化查询。
# 连库，查看，查询
# 例：MATCH (d:Disease)-[:HAS_SYMPTOM]->(s) WHERE d.name='糖尿病' RETURN d.name,s.name
