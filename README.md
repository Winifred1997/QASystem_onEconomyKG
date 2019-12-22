# QASystem_onEconomyKG
本项目以垂直网站为数据来源，构建起以企业-高管-行业-概念为中心的知识图谱。并基于此，搭建起了一个可以回答8类问题的自动问答机器人

项目结构：
|——QASystem_Economy_KG
    |——dict
        |——executive.txt        #高管实体库
        |——stock.txt            #企业实体库
        |——concept.txt          #概念实体库
        |——industry.txt         #行业实体库
    |——question_classifier.py   #问句类型分类脚本
    |——question_parser.py       #问句解析脚本
    |——answer_search.py         #问题查询及返回脚本
    |——chatbot.graph.py         #问答程序脚本
