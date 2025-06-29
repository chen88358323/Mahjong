def format_dictionary_entry(word, pronunciation, definitions):
    """格式化单个字典条目"""
    result = [f"{word}\n{pronunciation}"]
    for pos, meaning in definitions:
        result.append(f"{pos}.{meaning}")
    return "\n".join(result)


def process_dictionary_text(input_text):
    """处理原始字典文本"""
    entries = []
    lines = [line.strip() for line in input_text.strip().split('\n') if line.strip()]

    i = 0
    while i < len(lines):
        # 获取单词
        word = lines[i]
        i += 1

        # 收集所有词性定义
        definitions = []
        pronunciation = None

        while i < len(lines) and '/' in lines[i]:
            line = lines[i]
            if './' in line:
                pos_part, rest = line.split('./', 1)
                pron, meaning = rest.split('/', 1)
            else:
                parts = line.split('/')
                pos_part = parts[0].strip()
                pron = parts[1]
                meaning = parts[2] if len(parts) > 2 else ""

            if pronunciation is None:
                pronunciation = f"/{pron}/"
            elif pronunciation != f"/{pron}/":
                print(f"警告: 单词'{word}'的音标不一致: {pronunciation} vs /{pron}/")

            definitions.append((pos_part, meaning))
            i += 1

        if word and pronunciation and definitions:
            entries.append(format_dictionary_entry(word, pronunciation, definitions))

    return '\n\n'.join(entries)


if __name__ == "__main__":
    input_text = """

acute
adj./əˈkjuːt/急性的；剧烈的；敏锐的
chronic
adj./ˈkrɑːnɪk/慢性的；长期的
clinic
n./ˈklɪnɪk/诊所
corpus
n./ˈkɔːrpəs/文集；语料库；人体
cure
v./kjʊr/治愈；治疗
n./kjʊr/治疗；疗法
curative
adj./ˈkjʊrətɪv/治疗的；有疗效的
death
n./deθ/死亡
demise
n./dɪˈmaɪz/死亡；终止
doom
n./duːm/厄运；劫数
v./duːm/注定
exhaust
v./ɪɡˈzɔːst/使精疲力尽；耗尽
n./ɪɡˈzɔːst/废气
faint
v./feɪnt/昏厥；变得微弱
adj./feɪnt/微弱的；模糊的
fatal
adj./ˈfeɪtl/致命的；灾难性的
fatigue
n./fəˈtiːɡ/疲劳；疲惫
v./fəˈtiːɡ/使疲劳
feeble
adj./ˈfiːbl/虚弱的；无力的
fitness
n./ˈfɪtnəs/健康；健壮
heal
v./hiːl/治愈；康复
health care
n./ˈhelθ keər/医疗保健
hospital
n./ˈhɑːspɪtl/医院
hygiene
n./ˈhaɪdʒiːn/卫生
lament
v./ləˈment/哀悼；悲叹
n./ləˈment/挽歌；哀叹
lethal
adj./ˈliːθl/致命的
medical
adj./ˈmedɪkl/医疗的；医学的
mortal
adj./ˈmɔːrtl/必死的；致命的
n./ˈmɔːrtl/凡人
operation
n./ˌɑːpəˈreɪʃn/手术；操作
overwork
v./ˌoʊvərˈwɜːrk/使工作过度
n./ˌoʊvərˈwɜːrk/过度劳累
pain
n./peɪn/疼痛；痛苦
physician
n./fɪˈzɪʃn/医生
sanitary
adj./ˈsænɪteri/卫生的；清洁的
sore
adj./sɔːr/疼痛的；酸痛的
n./sɔːr/痛处
sorrow
n./ˈsɔːroʊ/悲伤；忧愁
suffering
n./ˈsʌfərɪŋ/痛苦；折磨
surgeon
n./ˈsɜːrdʒən/外科医生
therapy
n./ˈθerəpi/治疗；疗法
tire
v./ˈtaɪr/使疲劳；厌倦
treatment
n./ˈtriːtmənt/治疗；疗法
uncomfortable
adj./ʌnˈkʌmftəbl/不舒服的；令人不适的
unconscious
adj./ʌnˈkɑːnʃəs/无意识的；昏迷的
weary
adj./ˈwɪri/疲倦的；厌倦的
v./ˈwɪri/使疲劳
weaken
v./ˈwiːkən/削弱；变弱

acupuncture
n./ˈæk.jə.pʌŋk.tʃər/针灸
alleviate
v./əˈliː.vi.eɪt/减轻；缓解
antibiotic
n./ˌæn.taɪ.baɪˈɑː.tɪk/抗生素
check
v./tʃek/检查；核对
n./tʃek/检查；支票
common
adj./ˈkɑː.mən/常见的；普通的
dose
n./doʊs/剂量
v./doʊs/服药
drug
n./drʌɡ/药物；毒品
ease
v./iːz/减轻；缓解
n./iːz/轻松；舒适
injection
n./ɪnˈdʒek.ʃən/注射
isolate
v./ˈaɪ.sə.leɪt/隔离；孤立
medicine
n./ˈmed.ə.sɪn/药物；医学
morphine
n./ˈmɔːr.fiːn/吗啡
normal
adj./ˈnɔːr.məl/正常的；标准的
penicillin
n./ˌpen.əˈsɪl.ɪn/青霉素
pharmacy
n./ˈfɑːr.mə.si/药房
pill
n./pɪl/药丸
precaution
n./prɪˈkɔː.ʃən/预防措施
prescription
n./prɪˈskrɪp.ʃən/处方
quarantine
n./ˈkwɔːr.ən.tiːn/隔离；检疫
v./ˈkwɔːr.ən.tiːn/隔离；检疫
recovery
n./rɪˈkʌ.vəri/恢复；康复
refresh
v./rɪˈfreʃ/使恢复活力；刷新
relief
n./rɪˈliːf/缓解；减轻
relieve
v./rɪˈliːv/减轻；缓解
remedy
n./ˈrem.ə.di/治疗方法；药物
v./ˈrem.ə.di/治疗；补救
resume
v./rɪˈzuːm/重新开始；恢复
segregate
v./ˈseɡ.rɪ.ɡeɪt/隔离；分离
transplant
v./trænsˈplænt/移植
n./ˈtræns.plænt/移植
usual
adj./ˈjuː.ʒu.əl/通常的；平常的
vaccinate
v./ˈvæk.sə.neɪt/接种疫苗
X-ray
n./ˈeks.reɪ/X光
v./ˈeks.reɪ/用X光检查

agreeable
adj./əˈɡriːəbl/令人愉快的；同意的
apathetic
adj./ˌæpəˈθetɪk/冷漠的；无动于衷的
cheer
n./tʃɪr/欢呼；愉快
v./tʃɪr/欢呼；使高兴
delight
n./dɪˈlaɪt/快乐；愉快
v./dɪˈlaɪt/使高兴
desirable
adj./dɪˈzaɪrəbl/令人渴望的；合意的
enthusiastic
adj./ɪnˌθuːziˈæstɪk/热情的；热心的
exciting
adj./ɪkˈsaɪtɪŋ/令人兴奋的；刺激的
favour
n./ˈfeɪvər/偏爱；恩惠
v./ˈfeɪvər/偏爱；赞同
fond
adj./fɑːnd/喜欢的；钟爱的
fun
n./fʌn/乐趣；玩笑
adj./fʌn/有趣的
happiness
n./ˈhæpinəs/幸福；快乐
indifferent
adj./ɪnˈdɪfrənt/冷漠的；不关心的
joy
n./dʒɔɪ/欢乐；喜悦
joke
n./dʒoʊk/笑话；玩笑
v./dʒoʊk/开玩笑
keen
adj./kiːn/热切的；渴望的；敏锐的
laughter
n./ˈlæftər/笑声
lively
adj./ˈlaɪvli/活泼的；生动的
lovely
adj./ˈlʌvli/可爱的；美丽的
merry
adj./ˈmeri/快乐的；愉快的
negative
adj./ˈneɡətɪv/消极的；负面的
n./ˈneɡətɪv/否定
negligible
adj./ˈneɡlɪdʒəbl/可以忽略的；微不足道的
optimistic
adj./ˌɑːptɪˈmɪstɪk/乐观的
passive
adj./ˈpæsɪv/被动的；消极的
pessimistic
adj./ˌpesɪˈmɪstɪk/悲观的
please
v./pliːz/使高兴；请
pleasure
n./ˈpleʒər/快乐；乐趣
positive
adj./ˈpɑːzətɪv/积极的；肯定的
n./ˈpɑːzətɪv/积极
rejoice
v./rɪˈdʒɔɪs/欢庆；欣喜
satisfactory
adj./ˌsætɪsˈfæktəri/令人满意的
thrill
n./θrɪl/兴奋；激动
v./θrɪl/使兴奋
zeal
n./ziːl/热忱；热情


admire
v./ədˈmaɪr/钦佩；赞赏
amazing
adj./əˈmeɪzɪŋ/令人惊奇的；了不起的
apologise
v./əˈpɑːlədʒaɪz/道歉
apology
n./əˈpɑːlədʒi/道歉
astound
v./əˈstaʊnd/使震惊
careful
adj./ˈkerfl/小心的；仔细的
concern
n./kənˈsɜːrn/担忧；关心；涉及
v./kənˈsɜːrn/涉及；使担忧
confidence
n./ˈkɑːnfɪdəns/信心；信任
considerate
adj./kənˈsɪdərət/体贴的；周到的
curious
adj./ˈkjʊriəs/好奇的；求知的
daring
adj./ˈderɪŋ/大胆的；勇敢的
n./ˈderɪŋ/胆量；勇气
direct
adj./dəˈrekt/直接的；直率的
v./dəˈrekt/指导；指挥
earnest
adj./ˈɜːrnɪst/认真的；真诚的
n./ˈɜːrnɪst/认真；诚挚
frank
adj./fræŋk/坦率的；真诚的
freedom
n./ˈfriːdəm/自由
friendly
adj./ˈfrendli/友好的
generous
adj./ˈdʒenərəs/慷慨的；大方的
gentle
adj./ˈdʒentl/温和的；温柔的
grateful
adj./ˈɡreɪtfl/感激的；感谢的
gratitude
n./ˈɡrætɪtuːd/感激；感谢
hectic
adj./ˈhektɪk/忙乱的；繁忙的
honesty
n./ˈɑːnəsti/诚实；正直
hospitable
adj./hɑːˈspɪtəbl/好客的；殷勤的
humble
adj./ˈhʌmbl/谦逊的；卑微的
v./ˈhʌmbl/使谦卑；贬低
humorous
adj./ˈhjuːmərəs/幽默的
liberal
adj./ˈlɪbərəl/自由的；慷慨的；开明的
manly
adj./ˈmænli/有男子气概的
mercy
n./ˈmɜːrsi/仁慈；宽恕
modest
adj./ˈmɑːdɪst/谦虚的；适度的
mysterious
adj./mɪˈstɪriəs/神秘的；难以理解的
polite
adj./pəˈlaɪt/有礼貌的；客气的
proud
adj./praʊd/自豪的；骄傲的
rational
adj./ˈræʃnəl/理性的；合理的
ready
adj./ˈredi/准备好的；乐意的
remarkable
adj./rɪˈmɑːrkəbl/非凡的；值得注意的
romantic
adj./roʊˈmæntɪk/浪漫的
seriously
adv./ˈsɪriəsli/认真地；严肃地
startle
v./ˈstɑːrtl/使惊吓；使吃惊
stern
adj./stɜːrn/严厉的；严肃的
surprising
adj./sərˈpraɪzɪŋ/令人惊讶的
sympathetic
adj./ˌsɪmpəˈθetɪk/同情的；体谅的
thoughtful
adj./ˈθɔːtfl/体贴的；深思的


arduous
adj./ˈɑːrdʒuəs/艰巨的；费力的
awesome
adj./ˈɔːsəm/令人惊叹的；极好的
childish
adj./ˈtʃaɪldɪʃ/幼稚的；孩子气的
delicate
adj./ˈdelɪkət/脆弱的；精致的
eager
adj./ˈiːɡər/渴望的；热切的
enterprising
adj./ˈentərpraɪzɪŋ/有进取心的；有事业心的
liable
adj./ˈlaɪəbl/有责任的；易于…的
mundane
adj./mʌnˈdeɪn/世俗的；平凡的
naive
adj./naɪˈiːv/天真的；幼稚的
picturesque
adj./ˌpɪktʃəˈresk/如画的；风景优美的
prominent
adj./ˈprɑːmɪnənt/突出的；显著的
promising
adj./ˈprɑːmɪsɪŋ/有希望的；有前途的
robust
adj./roʊˈbʌst/强壮的；健壮的
sane
adj./seɪn/神志清醒的；明智的
sincere
adj./sɪnˈsɪr/真诚的；诚挚的
sound
n./saʊnd/声音
adj./saʊnd/健全的；完好的
v./saʊnd/发声
steadfast
adj./ˈstedfæst/坚定的；不动摇的
sturdy
adj./ˈstɜːrdi/结实的；坚固的
temperate
adj./ˈtempərət/温和的；适度的
tender
adj./ˈtendər/温柔的；嫩的
v./ˈtendər/提出；投标
tough
adj./tʌf/坚韧的；困难的
trustworthy
adj./ˈtrʌstwɜːrði/值得信赖的；可靠的

好的，我将只提供您要求的第六项内容，即这些单词的美式音标、词性以及牛津词典中的中文解释。

agony
n./ˈæɡəni/极度痛苦
anger
n./ˈæŋɡər/愤怒
v./ˈæŋɡər/使生气
bare
adj./ber/赤裸的；光秃的
bore
v./bɔːr/使厌烦
n./bɔːr/令人厌烦的人或事
disappoint
v./ˌdɪsəˈpɔɪnt/使失望
discourage
v./dɪsˈkɜːrɪdʒ/使气馁；阻止
disgust
n./dɪsˈɡʌst/厌恶
v./dɪsˈɡʌst/使厌恶
distress
n./dɪˈstres/忧虑；悲伤
v./dɪˈstres/使忧虑；使悲伤
fancy
n./ˈfænsi/想象力；爱好
v./ˈfænsi/想象；想要
adj./ˈfænsi/精致的；昂贵的
fate
n./feɪt/命运
familiar
adj./fəˈmɪliər/熟悉的
fortune
n./ˈfɔːrtʃən/财富；运气
frown
v./fraʊn/皱眉
n./fraʊn/皱眉
frustrating
adj./ˈfrʌstreɪtɪŋ/令人沮丧的
furious
adj./ˈfjʊriəs/狂怒的
gloomy
adj./ˈɡluːmi/阴郁的；沮丧的
grief
n./ɡriːf/悲伤
grieve
v./ɡriːv/悲伤
harass
v./həˈræs/骚扰
hate
v./heɪt/憎恨
n./heɪt/憎恨
hatred
n./ˈheɪtrɪd/憎恨
illusion
n./ɪˈluːʒn/错觉；幻想
imaginary
adj./ɪˈmædʒəneri/想象中的
implicit
adj./ɪmˈplɪsɪt/含蓄的；不言明的
intuition
n./ˌɪntuˈɪʃn/直觉
irritate
v./ˈɪrɪteɪt/使恼怒；刺激
miserable
adj./ˈmɪzərəbl/悲惨的；痛苦的
mourn
v./mɔːrn/哀悼
mutual
adj./ˈmjuːtʃuəl/相互的
naked
adj./ˈneɪkɪd/赤裸的；坦诚的
nuisance
n./ˈnuːsns/麻烦事；讨厌的人
private
adj./ˈpraɪvət/私人的；秘密的
rage
n./reɪdʒ/盛怒
v./reɪdʒ/发怒；肆虐
resemble
v./rɪˈzembl/像；相似
rigorous
adj./ˈrɪɡərəs/严格的；严密的
sadness
n./ˈsædnəs/悲伤
severe
adj./sɪˈvɪr/严重的；严厉的
similar
adj./ˈsɪmələr/相似的
spontaneous
adj./spɑːnˈteɪniəs/自发的
strenuous
adj./ˈstrenjuəs/费力的；艰苦的
strict
adj./strɪkt/严格的
vex
v./veks/使烦恼
wretched
adj./ˈretʃɪd/悲惨的；糟糕的


adverse
/ædˈvɜːrs/
adj. 不利的；有害的
anxiety
/æŋˈzaɪəti/
n. 焦虑；忧虑
awful
/ˈɔːfl/
adj. 可怕的；糟糕的
bother
/ˈbɑːðər/
v. 打扰；烦扰 n. 麻烦；烦恼
confuse
/kənˈfjuːz/
v. 使困惑；使糊涂
crazy
/ˈkreɪzi/
adj. 疯狂的；荒唐的
doubt
/daʊt/
n. 怀疑；疑问 v. 怀疑；不确定
ego
/ˈiːɡoʊ/
n. 自我；自尊心
envy
/ˈenvi/
n. 嫉妒；羡慕 v. 嫉妒；羡慕
excessive
/ɪkˈsesɪv/
adj. 过度的；过分的
fear
/fɪr/
n. 恐惧；害怕 v. 害怕；畏惧
fuss
/fʌs/
n. 大惊小怪；小题大做 v. 忙乱；焦躁
guilty
/ˈɡɪlti/
adj. 有罪的；内疚的
hesitate
/ˈhezɪteɪt/
v. 犹豫；迟疑
hostile
/ˈhɑːstl/
adj. 敌对的；不友好的
indignant
/ɪnˈdɪɡnənt/
adj. 愤慨的；义愤填膺的
insult
/ɪnˈsʌlt/
v. 侮辱；辱骂 n. 侮辱；凌辱
jealous
/ˈdʒeləs/
adj. 嫉妒的；猜忌的
mad
/mæd/
adj. 疯狂的；生气的
mean
/miːn/
adj. 吝啬的；卑鄙的 v. 意思是；意味着
nasty
/ˈnæsti/
adj. 令人不快的；恶劣的
radical
/ˈrædɪkl/
adj. 激进的；根本的 n. 激进分子
rash
/ræʃ/
adj. 轻率的；鲁莽的 n. 皮疹
reluctant
/rɪˈlʌktənt/
adj. 不情愿的；勉强的
restless
/ˈrestləs/
adj. 焦躁不安的；静不下来的
sceptical
/ˈskeptɪkl/
adj. 怀疑的；持怀疑态度的
selfish
/ˈselfɪʃ/
adj. 自私的
suspicion
/səˈspɪʃn/
n. 怀疑；猜疑
timid
/ˈtɪmɪd/
adj. 胆小的；羞怯的
troublesome
/ˈtrʌblsəm/
adj. 麻烦的；讨厌的
uneasy
/ʌnˈiːzi/
adj. 不安的；忧虑的
unkind
/ʌnˈkaɪnd/
adj. 不友善的；刻薄的
unpleasant
/ʌnˈpleznt/
adj. 令人不快的；讨厌的
unstable
/ʌnˈsteɪbl/
adj. 不稳定的；不牢固的
unsuitable
/ʌnˈsuːtəbl/
adj. 不合适的；不适宜的
unwilling
/ʌnˈwɪlɪŋ/
adj. 不情愿的；不愿意的
vicious
/ˈvɪʃəs/
adj. 恶毒的；凶残的
volatile
/ˈvɑːlətl/
adj. 易变的；不稳定的
vulgar
/ˈvʌlɡər/
adj. 粗俗的；庸俗的
weird
/wɪrd/
adj. 奇怪的；怪异的
wicked
/ˈwɪkɪd/
adj. 邪恶的；缺德的






arbitrary
adj./ˈɑːrbɪtreri/任意的；武断的
ashamed
adj./əˈʃeɪmd/惭愧的；羞耻的
awkward
adj./ˈɔːkwərd/笨拙的；尴尬的
careless
adj./ˈkerləs/粗心的；漫不经心的
clumsy
adj./ˈklʌmzi/笨拙的；不老练的
cunning
adj./ˈkʌnɪŋ/狡猾的；精明的
n./ˈkʌnɪŋ/狡猾；诡计
embarrass
v./ɪmˈbærəs/使尴尬；使难堪
endure
v./ɪnˈdʊr/忍受；持续
greedy
adj./ˈɡriːdi/贪婪的；渴望的
ignorant
adj./ˈɪɡnərənt/无知的；愚昧的
impulse
n./ˈɪmpʌls/冲动；推动力
naughty
adj./ˈnɔːti/淘气的；调皮的
oblivious
adj./əˈblɪviəs/未察觉的；健忘的
obtrusive
adj./əbˈtruːsɪv/唐突的；冒失的
regret
v./rɪˈɡret/后悔；遗憾
n./rɪˈɡret/后悔；遗憾
repent
v./rɪˈpent/忏悔；悔改
ridiculous
adj./rɪˈdɪkjələs/荒谬的；可笑的
rigid
adj./ˈrɪdʒɪd/僵硬的；严格的
sigh
v./saɪ/叹气
n./saɪ/叹息
slothful
adj./ˈsloʊθfl/懒惰的；迟缓的
sluggish
adj./ˈslʌɡɪʃ/行动迟缓的；懒散的
sly
adj./slaɪ/狡猾的；偷偷摸摸的
stereotype
n./ˈsteriətaɪp/刻板印象；老套的模式
v./ˈsteriətaɪp/使定型；对…形成刻板印象
stupid
adj./ˈstuːpɪd/愚蠢的；笨的
stubborn
adj./ˈstʌbərn/顽固的；固执的
tolerance
n./ˈtɑːlərəns/容忍；宽容
weep
v./wiːp/哭泣；流泪

"""
    formatted_text = process_dictionary_text(input_text)
    print(formatted_text)
