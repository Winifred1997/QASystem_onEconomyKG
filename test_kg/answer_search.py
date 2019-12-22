from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="123")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return str(final_answers)


    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'executive_information':
            desc1 = [i['m.sex'] for i in answers]
            desc2 = [i['m.age'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}——性别：{1}、年龄: {2}'.format(subject,
                            '；'.join(list(set(desc1))[:self.num_limit]),
                            '；'.join(list(set(desc2))[:self.num_limit]))

        elif question_type == 'stock_status':
            desc = [i['m.status'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '企业{0}的股票状态：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'executive_stock':
            desc1 = [i['n.name'] for i in answers]
            desc2 = [i['m.job'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}任职于公司：{1}、职位：{2}'.format(subject, '；'.join(list(set(desc1))[:self.num_limit]), '；'.join(list(set(desc2))[:self.num_limit]))

        elif question_type == 'stock_concept':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}所属的概念是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'stock_industry':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}所属的行业是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'stock_executive':
            desc = [''.join(i['n.name']) for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的董事会成员如下：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'concept_stock':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}下的公司包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'industry_stock':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}下的公司包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))


        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()