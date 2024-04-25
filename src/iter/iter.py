# from cluster import cluster
import knowledge_data
from datetime import datetime
import doc_classify



# 1.拿到db数据
db_data_savepath = '/data/lj/src/iter/data/pre_data/0409-0415kb_data.xlsx'# data/post_data/kb_update_' + datetime.now().strftime('%Y-%m-%d') + '.xlsx'
excluding_dir = None #  已经存进知识库的文件的过滤，暂时没用
# kb_path = knowledge_data.main(db_data_savepath,excluding_dir)

# 迭代次数
iter_num = 1.8

# 2.分类后聚类
# cluster_num  = 4
# type = 1
# doc_classify.main(db_data_savepath, cluster_num,type,iter_num)

# 3.分类后规则匹配
type = 2
doc_classify.main(db_data_savepath, 0,type,iter_num)