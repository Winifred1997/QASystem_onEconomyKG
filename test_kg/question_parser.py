class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'executive_information':
                sql = self.sql_transfer(question_type, entity_dict.get('executive'))

            elif question_type == 'stock_status':
                sql = self.sql_transfer(question_type, entity_dict.get('stock'))

            elif question_type == 'executive_stock':
                sql = self.sql_transfer(question_type, entity_dict.get('executive'))

            elif question_type == 'stock_concept':
                sql = self.sql_transfer(question_type, entity_dict.get('stock'))

            elif question_type == 'stock_industry':
                sql = self.sql_transfer(question_type, entity_dict.get('stock'))

            elif question_type == 'stock_executive':
                sql = self.sql_transfer(question_type, entity_dict.get('stock'))

            elif question_type == 'concept_stock':
                sql = self.sql_transfer(question_type, entity_dict.get('concept'))

            elif question_type == 'industry_stock':
                sql = self.sql_transfer(question_type, entity_dict.get('industry'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询高管信息
        if question_type == 'executive_information':
            sql = ["MATCH (m:高管) where m.name = '{0}' return m.name, m.sex, m.age".format(i) for i in entities]

        #查询公司经营状况
        elif question_type == 'stock_status':
            sql = ["MATCH (m:企业) where m.name = '{0}' return m.name, m.status".format(i) for i in entities]

        #查询高管属于哪个公司
        elif question_type == 'executive_stock':
            sql = ["MATCH (m:高管)-[r:董事会成员]->(n:企业) where m.name = '{0}' return m.name, n.name, m.job".format(i) for i in entities]

        #查询公司属于哪个概念
        elif question_type == 'stock_concept':
            sql = ["MATCH (m:企业)-[r:概念属于]->(n:概念) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        #查询公司属于哪个行业
        elif question_type == 'stock_industry':
            sql = ["MATCH (m:企业)-[r:行业属于]->(n:行业) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        #查询某公司下包含的高管
        elif question_type == 'stock_executive':
            sql = ["MATCH (m:企业)<-[r:董事会成员]-(n:高管) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        #查询某概念下包含的公司
        elif question_type == 'concept_stock':
            sql = ["MATCH (m:概念)<-[r:概念属于]-(n:企业) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        #查询某行业下包含的公司
        elif question_type == 'industry_stock':
            sql = ["MATCH (m:行业)<-[r:行业属于]-(n:企业) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        return sql



if __name__ == '__main__':
    handler = QuestionPaser()
