import os
import ahocorasick


class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.executive_path = os.path.join(cur_dir, 'dict/executive.txt')
        self.stock_path = os.path.join(cur_dir, 'dict/stock.txt')
        self.concept_path = os.path.join(cur_dir, 'dict/concept.txt')
        self.industry_path = os.path.join(cur_dir, 'dict/industry.txt')
        # 加载特征词
        self.executive_wds= [i.strip() for i in open(self.executive_path,encoding='utf-8') if i.strip()]
        self.stock_wds= [i.strip() for i in open(self.stock_path,encoding='utf-8') if i.strip()]
        self.concept_wds= [i.strip() for i in open(self.concept_path,encoding='utf-8') if i.strip()]
        self.industry_wds= [i.strip() for i in open(self.industry_path,encoding='utf-8') if i.strip()]
        self.region_words = set(self.executive_wds + self.stock_wds + self.concept_wds + self.industry_wds)
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.details_qwds = ['个人信息', '状况', '情况']
        self.stock_qwds = ['什么', '属于', '哪个','哪个公司']
        self.concept_qwds = ['概念', '哪个概念', '什么概念']
        self.industry_qwds = ['什么行业', '行业', '哪个行业']
        self.include_qwds = ['哪些公司', '所有', '哪些高管', '包括', '有哪些']

        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        medical_dict = self.check_key(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 详情
        if self.check_words(self.details_qwds, question) and ('executive' in types):
            question_type = 'executive_information'
            question_types.append(question_type)

        if self.check_words(self.details_qwds, question) and ('stock' in types):
            question_type = 'stock_status'
            question_types.append(question_type)

        # 属于
        if self.check_words(self.stock_qwds, question) and 'executive' in types:
            question_type = 'executive_stock'
            question_types.append(question_type)

        if self.check_words(self.concept_qwds, question) and 'stock' in types:
            question_type = 'stock_concept'
            question_types.append(question_type)

        if self.check_words(self.industry_qwds, question) and 'stock' in types:
            question_type = 'stock_industry'
            question_types.append(question_type)

        #包含
        if self.check_words(self.include_qwds, question) and 'stock' in types:
            question_type = 'stock_executive'
            question_types.append(question_type)

        if self.check_words(self.include_qwds, question) and 'concept' in types:
            question_type = 'concept_stock'
            question_types.append(question_type)

        if self.check_words(self.include_qwds, question) and 'industry' in types:
            question_type = 'industry_stock'
            question_types.append(question_type)


        # 若没有查到相关的外部查询信息，那么则将该高管的描述信息返回
        if question_types == [] and 'executive' in types:
            question_types = ['executive_information']

        # 若没有查到相关的外部查询信息，那么则将该公司的描述信息返回
        if question_types == [] and 'stock' in types:
            question_types = ['stock_status']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.executive_wds:
                wd_dict[wd].append('executive')
            if wd in self.stock_wds:
                wd_dict[wd].append('stock')
            if wd in self.concept_wds:
                wd_dict[wd].append('concept')
            if wd in self.industry_wds:
                wd_dict[wd].append('industry')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_key(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)