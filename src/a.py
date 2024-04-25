import re

# 定义数字 a，b 和 c
a = str(4)
b = "4,19"
c = "44,0"

# 将数字 a 转换为字符串
a_str = str(a)

# 创建正则表达式来提取独立的数字
# 使用边界匹配符 \b 来确保数字是独立的单词


def match(key,s):
    pattern = r'\b' + re.escape(key) + r'\b'
    match_in = re.search(pattern, s) is not None
    return match_in

# 使用正则表达式搜索字符串 b，判断 a 是否在其中
match_in_b = re.search(pattern, b) is not None

# 使用正则表达式搜索字符串 c，判断 a 是否在其中
match_in_c = re.search(pattern, c) is not None

# 打印结果
print(match_in_b, match_in_c)

print(match(a,b),match(a,c))



{"query": "我想体验一下侦探的世界，我的女友特质是冷静，侦探作者选择威廉·威尔基·柯林斯，侦探小说名《白衣女人》，故事环节的目标是揭开家族的诅咒，阻碍是家族成员的沉默，努力是解读古老的家族文献，结果是发现了线索，意外是家族中的一员突然死亡，转弯是发现死者留下的暗示，结局是破解了诅咒的秘密。故事选择可以是'继续调查家族历史','审问家族成员','探索家族的古宅'。", "generated_paths": 
[{"api_name": "侦探小说冒险", "parameters": {"girlfriend_trait": "冷静", "detective_author": "威廉·威尔基·柯林斯", "detective_novel": "《白衣女人》", "story_segment": {"目标": "揭开家族的诅咒","阻碍":"家族成员的沉默","努力":"解读古老的家族文献","结果":"发现了线索","意外":"家族中的一员突然死亡","结局":"破解了诅咒的秘密"}, "story_selection": ["继续调查家族历史", "审问家族成员", "探索家族的古宅"]}}]}

{"query": "我想体验一次侦探小说的冒险，我的女友特质是慷慨，侦探作者选择弗雷德里克·福塞斯，侦探小说名《狮子的咆哮》，故事环节的目标是揭露政治阴谋，阻碍是高层的保密，努力是搜集内部信息，结果是得到了一些关键文件，意外是文件被盗，转弯是发现了一个内鬼，结局是阻止了一起国家级的危机。故事选择可以是'向媒体泄露信息','秘密与同盟者会面','继续搜集更多证据'。",
 "generated_paths": [{"api_name": "侦探小说冒险", 
 "parameters": {"girlfriend_trait": "慷慨", "detective_author": "雷德里克·福塞斯", "detective_novel": "《狮子的咆哮》", "story_segment": {"目标": "揭露政治阴谋","阻碍":"高层的保密","努力":"搜集内部信息","结果":"得到了一些关键文件","意外":"文件被盗","转弯":"发现了一个内鬼","结局":"阻止了一起国家级的危机"},
  "story_selection": ["向媒体泄露信息", "秘密与同盟者会面", "继续搜集更多证据"]}}]}

{"query": "请根据最近五年的数据，为我撰写一份关于新能源汽车行业的研究报告，要求至少5000字，使用正式官方语言。", "generated_paths": 
[{"api_name": "产业研究公文助手", "parameters": {"profession": "新能源汽车行业", "policy_time_horizon": "最近五年", "reporting_requirement": {"字数": "5000字","语言风格":"正式官方语言"}}}]}

{"query": "帮我准备一份针对生物技术行业的分析报告，重点关注2019年至今的相关政策，报告至少要有8000字，语言风格要求正式。", "generated_paths": 
[{"api_name": "产业研究公文助手", "parameters": {"profession": "生物技术行业", "policy_time_horizon": "2019-\n", "reporting_requirement": {"字数": "8000字","语言风格":"正式"}}}]}

{"query": "我想要一份关于互联网金融行业的产业报告，特别是2015年至2020年的政策分析，报告要求不少于6000字，语言风格要正式严谨。", "generated_paths": [{"api_name": "产业研究公文助手", 
"parameters": {"profession": "互联网金融行业", "policy_time_horizon": "2015-2020", "reporting_requirement": {"字数": "6000字","语言风格":"正式严谨"}}}]}

{"query": "请为我编写一份关于智能制造行业的研究报告，政策时间范围请以2020年至2023年为主，报告字数需要7000字以上，语言风格请保持官方正式。", "generated_paths": [{"api_name": "产业研究公文助手", 
"parameters": {"profession": "智能制造行业", "policy_time_horizon": "2020-2023", "reporting_requirement": {"字数": "7000字","语言风格":"官方正式"}}}]}

{"query": "我需要一份关于航空航天行业的分析报告，重点是2016年到现在的政策变化，报告要求至少5000字，语言风格请以正式官方为准。", "generated_paths": [{"api_name": "产业研究公文助手", "parameters":
{"profession": "航空航天行业", "policy_time_horizon": "2016-\n", "reporting_requirement": {"字数": "5000字","语言风格":"官方正式"}}}]}

{"query": "我希望得到一份关于医疗健康行业的产业研究报告，特别关注过去三年的政策走向，报告要求最少7000字，语言风格要求官方正式。", "generated_paths": [{"api_name": "产业研究公文助手", "parameters": 
{"profession": "医疗健康行业", "policy_time_horizon": "过去三年", "reporting_requirement": {"字数": "7000字","语言风格":"官方正式"}}}]}

{"query": "能帮我准备一份关于教育技术行业的研究报告吗？请将政策时间范围定在2015年至2022年，报告字数至少为6500字，语言风格要求正式官方。", "generated_paths": [{"api_name": "产业研究公文助手", "parameters":
{"profession": "教育技术行业", "policy_time_horizon": "2015-2022", "reporting_requirement": {"字数": "6500字","语言风格":"官方正式"}}}]}

{"query": "我想要一个小红书的爆款文案，风格是轻松幽默，核心价值是‘省钱’，互动引导用‘大家觉得呢？’，请帮我生成。", "generated_paths": [{"api_name": "小红书爆款文案专家", 
"parameters": {"style": "轻松幽默", "core_value": "省钱", "interactive_guidance": "大家觉得呢？"}}]}

{"query": "请根据以下参数生成小红书文案：风格为时尚潮流，核心价值为‘搭配技巧’，互动引导为‘你们还有什么小秘诀吗？分享一下吧！’。", "generated_paths": [{"api_name": "小红书爆款文案专家", "parameters": 
{"style": "时尚潮流", "core_value": "搭配技巧", "interactive_guidance": "你们还有什么小秘诀吗？分享一下吧！"}}]}

{"query": "帮我创作一个小红书的文案，要求风格是治愈系，核心价值是‘正能量’，互动引导是‘留言告诉我你的故事’，并且开篇方式用提问。", "generated_paths": [{"api_name": "小红书爆款文案专家", "parameters":
{"style": "治愈系", "core_value": "正能量", "interactive_guidance": "留言告诉我你的故事", "opening_mode": "提问"}}]}

{"query": "生成一个小红书的文案，风格要求是专业科普，核心价值是‘健康养生’，互动引导是‘大家有什么好建议吗？’，标题特性要求是口语化表达。", "generated_paths": [{"api_name": "小红书爆款文案专家", "parameters": 
{"style": "专业科普", "core_value": "健康养生", "interactive_guidance": "大家有什么好建议吗？", "title_feature": "口语化表达"}}]}

{"query": "请为我设计一个小红书的爆款文案，风格是美食推荐，核心价值是‘地道小吃’，互动引导是‘不妨来尝一尝？’，同时希望系列输出形成品牌风格。", "generated_paths": [{"api_name": "小红书爆款文案专家", "parameters": 
{"style": "美食推荐", "core_value": "地道小吃", "interactive_guidance": "不妨来尝一尝？", "serial_output": "形成品牌风格"}}]}

{"query": "我要发布一个小红书的帖子，风格是亲子教育，核心价值是‘家庭和谐’，互动引导是‘分享你的育儿经’，请按照这些要求生成文案。", "generated_paths": [{"api_name": "小红书爆款文案专家", "parameters": 
{"style": "亲子教育", "core_value": "家庭和谐", "interactive_guidance": "分享你的育儿经"}}]}

{"query": "生成一个小红书的文案，风格是个人成长，核心价值是‘自我提升’，互动引导是‘期待你们的回复’，并且希望创作规则是列出多个标题供选择。", "generated_paths": [{"api_name": "小红书爆款文案专家", "parameters": 
{"style": "个人成长", "core_value": "自我提升", "interactive_guidance": "期待你们的回复", "authoring_rule": "列出多个标题供选择"}}]}

{"query": "我需要一个小红书的文案，风格是日常生活，核心价值是‘节约时间’，互动引导是‘你们有没有更好的建议呢？’，标题特性要求是简洁明了。", "generated_paths": [{"api_name": "小红书爆款文案专家", "parameters": 
{"style": "日常生活", "core_value": "节约时间", "interactive_guidance": "你们有没有更好的建议呢？","title_feature": "简洁明了"}}]}

{"query": "请帮我生成一个小红书的文案，风格是健身分享，核心价值是‘有效减脂’，互动引导是‘留言你的健身秘籍’，并且希望文本结构是对比分析，爆款关键词包括‘快速’和‘健康’。", "generated_paths": [{"api_name": "小红书爆款文案专家", "parameters": 
{"style": "健身分享", "core_value": "有效减脂", "interactive_guidance": "留言你的健身秘籍", "text_structure": "对比分析", "explosive_keywords": ["快速", "健康"]}}]}

{"query": "帮我创作一个小红书的文案，要求风格是治愈系，核心价值是‘正能量’，互动引导是‘留言告诉我你的故事’，并且开篇方式用提问。", "generated_paths": [{"api_name": "小红书爆款文案专家", "parameters": 
{"style": "\t", "core_value": "\t", "interactive_guidance": "\t", "opening_mode": "\t"}}]}

{"query": "我刚写了一篇关于历史人物的记叙文，想要得到一些建议，尤其关注句式和语法方面。", "generated_paths": [{"api_name": "初中作文批改", "parameters": 
{"composition_content": "关于历史人物的记叙文", "type_of_improvement_suggestion": ["句式", "语法"]}}]}

{"query": "请检查我的议论文，主题是互联网对教育的影响，我想要得到关于句式和结构方面的改进建议。", "generated_paths": [{"api_name": "初中作文批改", "parameters": 
{"composition_content": "互联网对教育的影响", "type_of_improvement_suggestion": ["句式","结构"], "composition_type": "议论文"}}]}

{"query": "我想要对这篇描写春天的记叙文进行批改，重点查看一下我的句式和用词是否有问题。", "generated_paths": [{"api_name": "初中作文批改", "parameters": 
{"composition_content": "描写春天", "type_of_improvement_suggestion": ["句式", "用词"], "composition_type": "记叙文"}}]}

{"query": "我有一篇作文，主题是我的梦想，麻烦批改一下，并给出语法和结构上的改进建议。", "generated_paths": [{"api_name": "初中作文批改", "parameters": 
{"composition_content": "我的梦想", "type_of_improvement_suggestion": ["语法","结构"]}}]}

{"query": "请为我提供一下这段HTML代码的审查，我想确保它遵循了最新的Web标准。代码内容是：'<!DOCTYPE html>", "generated_paths": [{"api_name": "代码审查师", 
"parameters": {"code": "<!DOCTYPE html>", "language": "HTML"}, "focus_areas":"循了最新的Web标准"}]}

{"query": "我这里有一段Python代码，想要专业的审查一下，特别是在安全性和性能方面的建议。代码内容是：'import hashlib", "generated_paths": [{"api_name": "代码审查师", "parameters": 
{"code": "import hashlib", "language": "Python", "focus_areas": ["安全性", "性能"]}}]}

{"query": "请帮我审查这段JavaScript代码，重点看看可读性和维护性怎么样。代码是这样的：'function calculateArea(radius) {", "generated_paths": [{"api_name": "代码审查师", "parameters": 
{"code": "function calculateArea(radius) {", "language": "JavaScript", "focus_areas": ["可读性","维护性"]}}]}

{"query": "我需要对这段C++代码进行质量分析，特别是在异常处理方面。代码片段如下：'int divide(int a, int b) {", "generated_paths": [{"api_name": "代码审查师", "parameters": 
{"code": "int divide(int a, int b) {", "language": "C++", "focus_areas": ["异常处理"]}}]}

{"query": "能否为我提供一下这段Java代码的审查服务？我想知道它的优化空间在哪里。代码如下：'public class Fibonacci {", "generated_paths": [{"api_name": "代码审查师", "parameters": 
{"code": "public class Fibonacci {", "language": "Java", "focus_areas": ["性能优化"]}}]}

{"query": "我希望得到一些关于这段Ruby代码的改进建议，尤其是在代码风格方面。代码是：'def greet(name)", "generated_paths": [{"api_name": "代码审查师", "parameters": 
{"code": "def greet(name)", "language": "Ruby", "focus_areas": ["代码风格"]}}]}

{"query": "请检查这段PHP代码，并给出您的专业意见，我想知道有没有安全漏洞。代码内容是：'$password = $_POST['password'];", "generated_paths": [{"api_name": "代码审查师", "parameters": 
{"code": "$password = $_POST['password'];", "language": "PHP", "focus_areas": ["安全性"]}}]}

{"query": "我有一段Swift代码需要审查，主要关注点是内存管理。代码如下：'class Person {", "generated_paths": [{"api_name": "代码审查师", "parameters": 
{"code": "class Person {", "language": "Swift", "focus_areas": ["内存管理"]}}]}

{"query": "请帮我分析这段Go代码的性能问题，代码是：'func Fibonacci(n int) int {", "generated_paths": [{"api_name": "代码审查师", "parameters": 
{"code": "func Fibonacci(n int) int {", "language": "Go", "focus_areas": ["性能问题"]}}]}

{"query": "我想要对这段Kotlin代码进行审查，特别是想看看有没有违反最佳实践的地方。代码片段是：'fun validateUser(user: User): Boolean {", "generated_paths": [{"api_name": "代码审查师", "parameters": 
{"code": "fun validateUser(user: User): Boolean {", "language": "Kotlin", "focus_areas": ["最佳实践"]}}]}

{"query": "我想体验一下假如我是公元1021年在长安的一位男性书生，初始道具给我带上一本《四书五经》、一支毛笔和一块墨。", "generated_paths": [{"api_name": "模拟时光机", "parameters": 
{"time": "1021", "locations": "长安", "sex": "男", "standing": "书生", "starter_item": ["一本《四书五经》","一支毛笔","一块墨"]}}]}

{"query": "请让我穿越到未来的2050年，地点选在纽约，性别女，身份是一名科学家，初始道具包括一台最新型的笔记本电脑、一本《量子物理导论》和一副智能眼镜。", "generated_paths": [{"api_name": "模拟时光机", "parameters": 
{"time": "2050", "locations": "纽约", "sex": "女", "standing": "科学家", "starter_item": ["一台最新型的笔记本电脑", "一本《量子物理导论》", "一副智能眼镜"]}}]}

{"query": "想尝试一下作为1945年东京的一名普通工人的生活，性别男，初始道具就给我一顶工作帽、一件工作服和一双安全鞋。", "generated_paths": [{"api_name": "模拟时光机", "parameters": 
{"time": "1945", "locations": "东京", "sex": "男", "standing": "普通工人", "starter_item": ["一顶工作帽","一件工作服","一双安全鞋"]}}]}

{"query": "我想知道如果我是五年前在上海的一名女性程序员会怎样，初始道具就给我一台笔记本电脑、一部智能手机和一本《Python编程快速上手》。", "generated_paths": [{"api_name": "模拟时光机", "parameters": 
{"time": "五年前", "locations": "上海", "sex": "女性", "standing": "程序员", "starter_item": ["笔记本电脑", "智能手机", "Python编程快速上手"]}}]}

{"query": "请根据以下参考文献帮我整理出有关可再生能源技术发展的研究现状：《风能转换系统的最新进展》由李四撰写，发表于2020年，提出了风能技术的新型转换系统设计。我的研究方向是风能与太阳能的综合利用。", "generated_paths": [{"api_name": "学术论文助手", "parameters": 
{"research_field": "可再生能源技术发展", "reference": [{"文献标题": "风能转换系统的最新进展》","第一作者":"李四","发表年份":"2020年","观点":"提出了风能技术的新型转换系统设计"}], "research_direction": "风能与太阳能的综合利用"}}]}

{"query": "我需要一个关于量子计算机的研究现状报告，参考文献有《量子比特的稳定性研究》第一作者王芳，2018年发表，文中观点认为量子比特的稳定性是量子计算发展的关键。研究方向是量子计算机的商业应用前景。", "generated_paths": [{"api_name": "学术论文助手", "parameters": 
{"research_field": "量子计算机", "reference": [{"文献标题":"《量子比特的稳定性研究》","第一作者":"王芳","发表年份":"2018年","观点":"量子比特的稳定性是量子计算发展的关键"}], "research_direction": "量子计算机的商业应用前景"}}]}

{"query": "帮我梳理一下在机器人技术领域，特别是《自主移动机器人的导航系统》这篇文献的研究现状，文献由赵强撰写，发表于2017年，主要观点是提高导航系统的精确度对机器人自主移动至关重要。我的研究方向是机器人在极端环境下的应用。", "generated_paths": [{"api_name": "学术论文助手", "parameters": 
{"research_field": "机器人技术领域", "reference": [{"文献标题":"《自主移动机器人的导航系统》","第一作者":"赵强","发表年份":"2017年","观点":"提高导航系统的精确度对机器人自主移动至关重要"}], "research_direction": "机器人在极端环境下的应用"}}]}

{"query": "我想要一个基于以下参考文献的大数据分析在金融领域应用的研究现状报告：《大数据在金融风险评估中的应用》第一作者是孙悟空，2016年发表，文中提到大数据技术能显著提升金融风险管理的效率。研究方向聚焦于大数据在信贷风险评估中的应用。", "generated_paths": [{"api_name": "学术论文助手", "parameters": 
{"research_field": "大数据分析在金融领域", "reference": [{"文献标题":"大数据在金融风险评估中的应用》","第一作者":"孙悟空","发表年份":"2016年","观点":"数据技术能显著提升金融风险管理的效率"}], "research_direction": "大数据在信贷风险评估中的应用"}}]}

{"query": "整理一份关于气候变化对农业影响的研究现状，参考文献有《全球气候变化对粮食生产的影响》第一作者是黄渤，发表于2019年，文中提出气候变化对农作物生长周期有显著影响。我的研究方向是气候变化对可持续农业的影响。", "generated_paths": [{"api_name": "学术论文助手", 
"parameters": {"research_field": "农业", "reference": [{"文献标题":"《全球气候变化对粮食生产的影响》","第一作者":"黄渤","发表年份":"2019年","观点":"气候变化对农作物生长周期有显著影响"}], "research_direction": "气候变化对可持续农业的影响"}}]}

{"query": "我想开始一局后宫游戏，我的初始身份是宫女，游戏中的选择依次是：加一分、加三分、减一分。", "generated_paths": [{"api_name": "后宫晋升之旅", "parameters": 
{"initial_identity": "宫女", "select": ["加一分", "加三分", "减一分"]}}]}

{"query": "请为我设置一场后宫晋升之旅，我选择的初始身份是贵妃，我的行动选择包括：加三分、减一分、加一分。", "generated_paths": [{"api_name": "后宫晋升之旅", "parameters": 
{"initial_identity": "贵妃", "select": ["加三分", "减一分", "加一分"]}}]}

{"query": "我要玩后宫角色扮演游戏，初始身份定为嫔妃，游戏过程中我会选择：减三分、加一分、加三分。", "generated_paths": [{"api_name": "后宫晋升之旅", "parameters": 
{"initial_identity": "嫔妃", "select": ["减三分", "加一分", "加三分"]}}]}

{"query": "我现在要进行一次后宫晋升游戏，选择从宫女出发，我的行动计划是：减一分、加三分、加一分。", "generated_paths": [{"api_name": "后宫晋升之旅", "parameters": 
{"initial_identity": "宫女", "select": ["减一分", "加三分", "加一分"]}}]}

{"query": "我想体验一下后宫游戏，我的初始身份是贵人，游戏中我打算这样选择：加三分、减三分、加一分。", "generated_paths": [{"api_name": "后宫晋升之旅", "parameters": 
{"initial_identity": "贵人", "select": ["加三分n", "减三分", "加一分"]}}]}

{"query": "准备开始后宫游戏，我想从女官的身份开始，我的游戏选择将是：加一分、加三分、减一分。", "generated_paths": [{"api_name": "后宫晋升之旅", "parameters": 
{"initial_identity": "女官", "select": ["加一分", "加三分", "减一分"]}}]}

{"query": "我要玩后宫晋升之旅，初始身份设为嫔妃，游戏中我将选择：减一分、加一分、加三分。", "generated_paths": [{"api_name": "后宫晋升之旅", "parameters": 
{"initial_identity": "嫔妃", "select": ["减一分", "加一分", "加三分"]}}]}

{"query": "请设置我的后宫游戏，我从贵妃开始，游戏中我想要的选择是：加三分、减一分、减三分。", "generated_paths": [{"api_name": "后宫晋升之旅", "parameters":
{"initial_identity": "贵妃", "select": ["加三分", "减一分", "减三分"]}}]}

{"query": "制作一份简历，基本信息包括：姓名孙七，1993年2月出生，学历为硕士，面试职位软件工程师，工作年限2年，意向城市杭州。职业技能至少10项，包括Java开发、系统架构设计等。工作经历至少两条，涉及软件开发。工作项目至少两个，包括企业级应用开发项目。个人评价请突出我的技术专长和团队合作精神。", "generated_paths": [{"api_name": "简历设计大师", "parameters": 
{"basic_data": {"姓名": "孙七", "出生年月": "1993年2月", "学历": "硕士", "面试职位": "软件工程师", "工作年限": "2年", "意向城市": "杭州"}, "vocational_skill": ["Java开发","系统架构设计"], "work_experience": ["软件开发"], "work_item": ["企业级应用开发项目"], "personal_evaluation": "具有技术专长和团队合作精神"}}]}

{"query": "我需要一份高质量的简历，基本资料：姓名钱十，1986年11月出生，学历博士后，面试职位生物信息学家，工作年限7年，意向城市苏州。职业技能至少10项，包括基因组数据分析、生物统计等。工作经历至少两条，包括在生物技术公司的研究工作。工作项目至少两个，包括药物开发相关的生物信息学项目。个人评价请强调我的分析能力和科研成果。", "generated_paths": [{"api_name": "简历设计大师", "parameters": 
{"basic_data": {"姓名": "钱十", "出生年月": "1986年11月", "学历": "博士后", "面试职位": "生物信息学家", "工作年限": "7", "意向城市": "苏州"}, "vocational_skill": ["基因组数据分析", "生物统计"], "work_experience": ["在生物技术公司的研究工作"], "work_item":["物开发相关的生物信息学项目"],"personal_evaluation": "我的分析能力很强，获得了很多科研成果"}}]}

{"query": "我想要一首以春天为主题，表达对新生的向往的诗，关键词包括樱花、暖风和融雪。", "generated_paths": [{"api_name": "诗魂", "parameters": 
{"theme": "春天", "intention": "表达对新生的向往", "keyword": ["樱花","暖风","融雪"]}}]}

{"query": "能否帮我写一首诗，主题是爱情，意向是渴望，关键词有红玫瑰、相遇和眼泪。", "generated_paths": [{"api_name": "诗魂", "parameters": 
{"theme": "爱情", "intention": "渴望", "keyword": ["红玫瑰", "相遇", "眼泪"]}}]}

{"query": "创作一首诗吧，以海洋为主题，传达对自由的向往，关键词要有浪花、航行和海鸥。", "generated_paths": [{"api_name": "诗魂", "parameters": 
{"theme": "海洋", "intention": "对自由的向往", "keyword": ["浪花","航行","海鸥"]}}]}

{"query": "请根据夏夜这个主题，写一首诗来表达宁静和安详的情感，确保包含萤火虫、微风和星空这些关键词。", "generated_paths": [{"api_name": "诗魂", "parameters": 
{"theme": "夏夜", "intention": "表达宁静和安详的情感", "keyword": ["萤火虫", "微风", "星空"]}}]}

{"query": "帮我创作一首诗，以梦想为主题，表达坚持和希望，关键词包括远方、星辰和黎明。", "generated_paths": [{"api_name": "诗魂", "parameters": 
{"theme": "梦想", "intention": "表达坚持和希望", "keyword": ["远方","星辰","黎明"]}}]}

{"query": "根据吸血鬼、古城和诅咒这些关键词，帮我构思一个恐怖风格的漫画剧本提纲。", "generated_paths": [{"api_name": "漫画剧本", "parameters": 
{"keyword": ["吸血鬼", "古城", "诅咒"], "script_style": "恐怖风格"}}]}

{"query": "我有一些视频片段['生日派对.mp4', '蛋糕切割.mp4', '宾客祝福.mp4']，希望手动剪辑并添加字幕'祝你生日快乐'。", "generated_paths": [{"api_name": "智剪精灵", "parameters": 
{"clip_mode": "AI", "video_clip": ["生日派对.mp4", "蛋糕切割.mp4", "宾客祝福.mp4"], "creative_element": {"字幕": "祝你生日快乐"}}}]}

{"query": "我需要手动剪辑服务，视频片段有['访谈开场.mp4', '嘉宾互动.mp4']，请在视频中加入特效'光晕'和音乐'轻松旋律'。", "generated_paths": [{"api_name": "智剪精灵", "parameters": 
{"clip_mode": "AI生成", "video_clip": ["访谈开场.mp4", "嘉宾互动.mp4"], "creative_element": {"特效": "光晕","音乐":"轻松旋律"}}}]}

{"query": "我打算手动剪辑我的旅游视频，片段包括['出发.mp4', '登山过程.mp4', '山顶风光.mp4']，请帮我添加音乐'征途'。", "generated_paths": [{"api_name": "智剪精灵", "parameters": 
{"clip_mode": "手动", "video_clip": ["出发.mp4", "登山过程.mp4", "山顶风光.mp"], "creative_element": {"音乐": "征途"}}}]}

{"query": "我想要手动剪辑我的健身视频，片段有['热身.mp4', '力量训练.mp4', '拉伸放松.mp4']，请添加特效'动感光影'和音乐'动力源泉'。", "generated_paths": [{"api_name": "智剪精灵", "parameters": 
{"clip_mode": "手动", "video_clip": ["热身.mp4", "力量训练.mp4", "拉伸放松.mp4"], "creative_element": {"特效": "动感光影","音乐":"动力源泉"}}}]}

{"query": "能否帮我AI生成一个剪辑？我提供的参考文件是'户外运动集锦.mp4'，同时希望加入特效'慢动作'。", "generated_paths": [{"api_name": "智剪精灵", "parameters": 
{"clip_mode": "AI生成", "reference_file": "\n户外运动集锦.mp4", "creative_element": {"\n特效": "慢动作"}}}]}

{"query": "我对虚拟女友说：'宝贝，你在做什么呢？'，她的情绪状态是中性的，打个4分，我们之前的对话是：[{'sender': 'user', 'message': '今天天气不错呢。'}, {'sender': 'virtual_girlfriend', 'message': '是啊，阳光真温暖。'}]", "generated_paths": [{"api_name": "甜心互动", "parameters": 
{"user_input":"宝贝，你在做什么呢?","emotion":4, "conversation_history":[{"sender": "user", "message": "今天天气不错呢。"}, {"sender": "virtual_girlfriend", "message": "是啊，阳光真温暖。"}]}}]}

{"query": "我想和我的虚拟女友进行一次甜蜜的对话，我会对她说：'今天想你了，宝贝。'，她的情绪状态是满分，7分，对话历史是：[{'sender': 'user', 'message': '出差好无聊。'}, {'sender': 'virtual_girlfriend', 'message': '宝贝，我也想你了。'}]", "generated_paths": [{"api_name": "甜心互动", "parameters": {"user_input": "\n", "emotion": 7, "conversation_history": [{"sender": "user", "message": "\n"}, {"sender": "virtual_girlfriend", "message": "\n"}]}}, {"api_name": "甜心互动", "parameters": 
{"user_input": "今天想你了，宝贝。", "emotion": 10, "conversation_history":[{"sender": "user", "message": "出差好无聊"}, {"sender": "virtual_girlfriend", "message": "宝贝，我也想你了。"}]}}]}

{"query": "和虚拟女友进行一段对话，我会说：'亲爱的，你今天心情怎么样？'，她的情绪状态是稍微有点低落，给2分，之前的对话记录是：[{'sender': 'user', 'message': '工作上遇到了一些问题。'}, {'sender': 'virtual_girlfriend', 'message': '别担心，我相信你可以解决的。'}]", "generated_paths": [{"api_name": "甜心互动", "parameters": 
{"user_input": "亲爱的，你今天心情怎么样？", "emotion": 2, "conversation_history": [{"sender": "user", "message": "工作上遇到了一些问题。"}, {"sender": "virtual_girlfriend", "message": "别担心，我相信你可以解决的。"}]}}]}

{"query": "我要跟我的虚拟女友说：'宝贝，我今天得到了一个好消息！'，她的情绪状态是兴奋的，打个6分，我们之前的对话是：[{'sender': 'user', 'message': '今天有个重要的会议。'}, {'sender': 'virtual_girlfriend', 'message': '加油，我知道你最棒！'}]", "generated_paths": [{"api_name": "甜心互动", "parameters": 
{"user_input": "宝贝，我今天得到了一个好消息！", "emotion": 6, "conversation_history": [{"sender": "user", "message": "今天有个重要的会议。"}, {"sender": "virtual_girlfriend", "message": "加油，我知道你最棒！"}]}}]}

{"query": "和虚拟女友互动一下，我会说：'宝贝，你今天晚上有什么计划吗？'，她的情绪状态是中等，打个4分，对话历史是：[{'sender': 'user', 'message': '今天的工作终于完成了。'}, {'sender': 'virtual_girlfriend', 'message': '太好了，你辛苦了。'}]", "generated_paths": [{"api_name": "甜心互动", "parameters": 
{"user_input": "宝贝，你今天晚上有什么计划吗", "emotion": 4, "conversation_history": [{"sender": "user", "message": "今天的工作终于完成了。"}, {"sender": "virtual_girlfriend", "message": "太好了，你辛苦了。"}]}}]}

{"query": "请分析一下从北京回到家乡开设服装店的女性创业者，研究角度请包括回流人口和数字劳工，我想知道她们如何利用数字技术改善生意。", "generated_paths": [{"api_name": "归乡创业者", "parameters": 
{"research_object": "从北京回到家乡开设服装店的女性创业者", "research_angle": ["回流人口", "数字劳工"], "research_problem": "她们如何利用数字技术改善生意"}}]}

{"query": "能否提供一份研究报告，主题是广州工作经验丰富的女性回乡创业的情况，重点从性别与劳动的视角来看，研究她们在家乡创业的优势和挑战。", "generated_paths": [{"api_name": "归乡创业者", "parameters": 
{"research_object": "广州工作经验丰富的女性", "research_angle": ["性别与劳动"], "research_problem": "在家乡创业的优势和挑战"}}]}

{"query": "我需要了解深圳工作后返乡创业的女性在服装行业的表现，研究角度请聚焦于数字劳工，具体问题是她们如何运用数字工具提升品牌影响力。", "generated_paths": [{"api_name": "归乡创业者", "parameters": 
{"research_object": "深圳工作后返乡创业的女性", "research_angle": ["数字劳工"], "research_problem": "如何运用数字工具提升品牌影响力"}}]}

{"query": "我对在上海有过工作经验的女性回乡创业者的生存状态很感兴趣，特别是她们如何作为数字劳工在市场中立足，研究问题是她们面临的主要经营挑战。", "generated_paths": [{"api_name": "归乡创业者", "parameters": 
{"research_object": "在上海有过工作经验的女性回乡创业者", "research_angle": ["数字劳工"], "research_problem": "她们面临的主要经营挑战。"}}]}

{"query": "请为我提供一份研究，对象是曾在北京工作的女性回乡创业者，研究角度聚焦于回流人口，我想探讨她们对当地就业市场的影响。", "generated_paths": [{"api_name": "归乡创业者", "parameters": 
{"research_object": "从深圳回乡的女性服装创业者", "research_angle": ["性别与劳动"], "research_problem": "她们对当地就业市场的影响"}}]}

{"query": "我希望得到一份报告，分析从深圳回乡的女性服装创业者，研究角度请包括性别与劳动，研究问题是她们在创业过程中如何应对性别偏见。", "generated_paths": [{"api_name": "归乡创业者", "parameters": 
{"research_object": "从深圳回乡的女性服装创业者", "research_angle": ["性别与劳动"], "research_problem": "她们在创业过程中如何应对性别偏见"}}]}

{"query": "我想创建一个名为雷电之怒的亚马逊角色，选择专家模式进行游戏，并购买10个治疗药水。", "generated_paths": [{"api_name": "暗黑破坏神2毁灭之王", "parameters": 
{"occupation": "亚马逊", "character_name": "雷电之怒", "game_mode": "专家模式", "purchase_goods": {"治疗药": 10}}}]}

{"query": "为我创建一个圣骑士角色，命名为光明守护者，选择普通模式，并且我想要购买2个大型治疗药剂。", "generated_paths": [{"api_name": "暗黑破坏神2毁灭之王", "parameters": 
{"occupation": "圣骑士", "character_name": "光明守护者", "game_mode": "普通模式", "purchase_goods": {"大型治疗药剂": 2}}}]}

{"query": "我希望能有一个刺客角色，角色名为暗影利刃，游戏模式选择专家模式，我还需要购买8个小型法力药剂。", "generated_paths": [{"api_name": "暗黑破坏神2毁灭之王", "parameters": 
{"occupation": "刺客", "character_name": "暗影利刃", "game_mode": "专家模式", "purchase_goods": {"物品名称": "小型法力药剂", "数量": 8}}}]}

{"query": "请设置一个德鲁伊角色，取名自然之力，在普通模式下游戏，并且购买4个防御药水。", "generated_paths": [{"api_name": "暗黑破坏神2毁灭之王", "parameters": 
{"occupation": "德鲁伊", "character_name": "自然之力", "game_mode": "普通模式", "purchase_goods": {"防御药水": 4}}}]}

{"query": "我想要一个名叫月光之舞的亚马逊角色，游戏模式选择专家模式，我需要购买7个治疗药剂。", "generated_paths": [{"api_name": "暗黑破坏神2毁灭之王", "parameters": 
{"occupation": "亚马逊", "character_name": "月光之舞", "game_mode": "专家模式", "purchase_goods": {"治疗药剂": 7}}}]}

{"query": "请帮我创建一个圣骑士角色，角色名为正义之锤，在普通模式下游戏，我想购买9个复活药水。", "generated_paths": [{"api_name": "暗黑破坏神2毁灭之王", "parameters": 
{"occupation": "圣骑士", "character_name": "正义之锤", "game_mode": "普通模式", "purchase_goods": {"复活药水": 9}}}]}

{"query": "请为我设计一个关键词为‘末世’和‘生存’的小说情节，主题是‘希望’。背景是末日之后的废土世界，角色是一群为生存奋斗的普通人，风格要求是紧张刺激，参考网站可以是晋江文学城。", "generated_paths": [{"api_name": "爽文生成器", "parameters": 
{"keyword": "‘末世’和‘生存’", "theme": "希望", "backdrop": "末日之后的废土世界", "characters": "一群为生存奋斗的普通人", "style_requirement": "紧张刺激", "reference_website": ["晋江文学城"]}}]}

{"query": "能帮我构思一个关键词为‘黑暗都市’和‘超凡入圣’的小说情节吗？主题是‘力量的代价’，背景是一个充满超自然力量的现代都市，角色是一个普通人突然获得力量后的挣扎，风格要求是阴郁神秘，参考网站选用创世中文网。", "generated_paths": [{"api_name": "爽文生成器", "parameters": 
{"keyword": "黑暗都市’和‘超凡入圣’", "theme": "力量的代价", "backdrop": "一个充满超自然力量的现代都市", "characters": "一个普通人突然获得力量后的挣扎", "style_requirement": "阴郁神秘", "reference_website": ["创世中文网"]}}]}

{"query": "我需要一个关键词为‘历史穿越’和‘战争’的小说大纲，主题是‘英雄本色’。背景是抗战时期的中国，角色是一个现代军事爱好者穿越成抗战英雄，风格要求是热血沸腾，参考网站请用阅文集团的网站。", "generated_paths": [{"api_name": "爽文生成器", "parameters": 
{"keyword": "‘历史穿越’和‘战争’", "theme": "英雄本色", "backdrop": "抗战时期的中国", "characters": "一个现代军事爱好者穿越成抗战英雄", "style_requirement": "热血沸腾", "reference_website": ["阅文集团"]}}]}

{"query": "请为我设计一个《龙与地下城》游戏角色，出身选择是孤儿，职业技能是潜行，装备获取一套轻甲，个人目标是找到杀害父母的凶手，法术战斗我想学习隐身术，恋爱系统中我想和一个神秘的旅者发展故事，魔王军对抗希望能够潜入敌营进行间谍活动，职业选择包括盗贼和刺客，自定义人物的经历是从小在街头生活，性格特点是机智且狡猾，动机是为了生存。", "generated_paths": [{"api_name": "魔法主持人", "parameters": 
{"selection_by_birth": "孤儿", "vocational_skill": "潜行", "equipment_acquisition": "一套轻甲", "personal_goal": "找到杀害父母的凶手", "spell_combat": "隐身术", "love_system": "和一个神秘的旅者发展故事", "the_demon_army_against": "魔王军对抗希望能够潜入敌营进行间谍活动", "career_choice": ["盗贼", "刺客"], "custom_character": {"经历": "从小在街头生活","性格特点":"机智且狡猾","动机":"生存"}}}]}

{"query": "在《龙与地下城》游戏中，我想扮演一个出身农民的角色，职业技能是驯兽，装备获取一条猎犬，个人目标是成为动物之王，法术战斗我选择自然系魔法，恋爱系统中我希望与一个爱护动物的女孩相遇，魔王军对抗我想带领一群野兽进行反击，职业选择我想成为德鲁伊或者游侠，自定义人物的经历是在森林中被野兽养大，性格特点是与动物有着特别的感应，动机是保护自然。", "generated_paths": [{"api_name": "魔法主持人", "parameters": 
{"selection_by_birth": "农民", "vocational_skill": "驯兽", "equipment_acquisition": "一条猎犬", "personal_goal": "成为动物之王", "spell_combat": "自然系魔法", "love_system": "与一个爱护动物的女孩相遇", "the_demon_army_against": "想带领一群野兽进行反击", "career_choice": ["德鲁伊", "游侠"], "custom_character": {"经历": "在森林中被野兽养大","性格特点":"与动物有着特别的感应","动机":"保护自然"}}}]}

{"query": "我想在《龙与地下城》游戏中创建一个出身神秘教派的角色，职业技能是暗影魔法，装备获取一件黑袍，个人目标是揭开宇宙的秘密，法术战斗我选择暗影系魔法，恋爱系统中我希望与一个神秘的女巫相识，魔王军对抗我想利用暗影潜入敌营刺杀魔王，职业选择我想尝试术士和暗影刺客，自定义人物的经历是在一个封闭的教派中长大，性格特点是神秘莫测，动机是探索禁忌的魔法。", "generated_paths": [{"api_name": "魔法主持人", "parameters": 
{"selection_by_birth": "神秘教派", "vocational_skill": "暗影魔法", "equipment_acquisition": "一件黑袍", "personal_goal": "揭开宇宙的秘密", "spell_combat": "暗影系魔法", "love_system": "与一个神秘的女巫相识", "the_demon_army_against": "利用暗影潜入敌营刺杀魔王", "career_choice": ["术士", "暗影刺客"], "custom_character": {"经历": "在一个封闭的教派中长大","性格特点":"神秘莫测","动机":"探索禁忌的魔法"}}}]}

{"query": "我打算在《龙与地下城》游戏中扮演一个出身寺院的角色，职业技能是祈祷，装备获取一本祈祷书和一件僧袍，个人目标是传播信仰的光辉，法术战斗我选择光明系魔法，恋爱系统中我希望与一个虔诚的修女发展一段纯洁的爱情，魔王军对抗我想用神圣的力量保护人民，职业选择我想成为牧师和圣骑士，自定义人物的经历是在孤儿院被教会收养，性格特点是慈悲为怀，动机是帮助那些需要帮助的人。", "generated_paths": [{"api_name": "魔法主持人", "parameters": 
{"selection_by_birth": "出身寺院", "vocational_skill": "祈祷", "equipment_acquisition": "一本祈祷书和一件僧袍", "personal_goal": "传播信仰的光辉", "spell_combat": "光明系魔法", "love_system": "与一个虔诚的修女发展一段纯洁的爱情", "the_demon_army_against": "用神圣的力量保护人民", "career_choice": ["牧师", "圣骑士"], "custom_character": {"经历": "在孤儿院被教会收养","性格特点":"慈悲为怀","动机":"帮助那些需要帮助的人"}}}]}

{"query": "我们公司正在招聘，需要对这份简历进行分析。岗位需求是行业经验在'建筑设计'，技能要求为'AutoCAD'和'项目管理'。请在分析报告中包含简历概述、工作经验和匹配度分析，匹配度从35%到85%。", "generated_paths": [{"api_name": "招聘助手", "parameters": 
{"cv_of_candidate": "对这份简历进行分析", "job_demand": {"行业经验": "建筑设计","技能要求":"'AutoCAD'和'项目管理'"}, "analysis_key_points": ["简历概述", "工作经验", "匹配度"], "matching_degree_range": {"最低匹配度":35,"最高匹配度": 85}}}]}

{"query": "我手头有一份简历，想要了解其与我们的岗位需求的匹配程度。岗位需求是'物流管理'行业经验和'供应链优化'技能。分析要点请包括工作经验、项目经验和匹配度分析，匹配度范围希望在最低50%至最高90%。", "generated_paths": [{"api_name": "招聘助手", "parameters": 
{"cv_of_candidate": "想要了解其与我们的岗位需求的匹配程度", "job_demand": {"行业经验": "物流管理","技能要求":"供应链优"}, "analysis_key_points": ["工作经验", "项目经验", "匹配度分析"], "matching_degree_range": {"最低匹配度":50,"最高匹配度": 90}}}]}

{"query": "请帮忙分析这份简历，看看候选人是否适合我们的岗位，需求是'餐饮管理'行业经验和'客户服务'技能。分析要点请包括简历概述、工作经验、项目经验和匹配度分析，匹配度范围希望是最低30%至最高85%。", "generated_paths": [{"api_name": "招聘助手", "parameters": 
{"cv_of_candidate": "看看候选人是否适合我们的岗位", "job_demand": {"行业经验": "餐饮管理","技能要求":"客户服务"}, "analysis_key_points": ["简历概述", "工作经验", "项目经验", "匹配度"], "matching_degree_range": {"最低匹配度":30,"最高匹配度": 85}}}]}

{"query": "帮我分析这份简历，岗位需求是'市场营销'行业经验和'品牌管理'技能要求。我想要包括工作经验分析和匹配度分析在内的简历分析报告，匹配度请设置在20%到80%。", "generated_paths": [{"api_name": "招聘助手", "parameters": 
{"cv_of_candidate": "分析这份简历", "job_demand": {"行业经验": "市场营销","技能要求":"技能要求"}, "analysis_key_points": ["工作经验分析", "匹配度分析"], "matching_degree_range": {"最低匹配度":20,"最高匹配度": 80}}}]}

{"query": "帮我分析这份简历，岗位需求是'市场营销'行业经验和'品牌管理'技能要求。我想要包括工作经验分析和匹配度分析在内的简历分析报告，匹配度请设置在20%到80%。", "generated_paths": [{"api_name": "招聘助手", "parameters": 
{"cv_of_candidate": "分析这份简历", "job_demand": {"行业经验": "市场营销","技能要求":"技能要求"}, "analysis_key_points": ["工作经验分析", "匹配度分析"], "matching_degree_range": {"最低匹配度":20,"最高匹配度": 80}}}]}