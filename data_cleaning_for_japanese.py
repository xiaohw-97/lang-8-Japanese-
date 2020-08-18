import sys
import platform
import codecs
import mojimoji
import levenshtein_distance as ld
import utils
import re
d_num = 6
i_num = 6
lang = "ja"
numlist = ['0','1','2','3','4','5','6','7','8','9']
#####

def process(text):
    a = None
    b = None
    err_corr = text.split("\t")
    if len(err_corr) == 2:
        err = mojimoji.zen_to_han(err_corr[0].rstrip('\n'), kana=False)
        err = mojimoji.han_to_zen(err, ascii=False, digit=False)
        corr = mojimoji.zen_to_han(err_corr[1].rstrip('\n'), kana=False)
        corr = mojimoji.han_to_zen(corr, ascii=False, digit=False)
        err_lang = utils.lang_check(err, lang)
        corr_lang = utils.lang_check(corr, lang)


        if err_lang and corr_lang:

            errs = list(err)
            corrs = list(corr)
            del_num, ins_num = ld.levenshtein_distance(errs, corrs)
            del_portion = del_num / len(errs)
            ins_portion = ins_num / len(corrs)


            if (del_num < d_num and ins_num < i_num and del_portion < 0.4 and ins_portion < 0.4)\
                    and (corrs[-1]== '。' or corrs[-1]== '?' or corrs[-1]== '!') \
                    and (corrs[-2] not in numlist) and ('__' not in corr) and (len(corr)>6):
                #cleaning the dataset like: 1)
                 err = re.sub("\d+\)\s+", "", err)
                 corr = re.sub("\d+\)\s+", "", corr)
                 err = re.sub("\(\s", "", err)
                 corr = re.sub("\(\s", "", corr)
                 err = re.sub("\s\)", "", err)
                 corr = re.sub("\s\)", "", corr)
                 #cleaning the string like: 1.)
                 err = re.sub("\d+\.\)\s*", "", err)
                 corr = re.sub("\d+\.\)\s*", "", corr)
                 #cleaning the string like: 1.
                 err = re.sub("\d+\.\s*", "", err)
                 corr = re.sub("\d+\.\s*", "", corr)
                 #cleaning the strings begin with ・
                 err = re.sub("・\s+", "", err)
                 corr = re.sub("・\s+", "", corr)
                 # cleaning the strings begin with *
                 err = re.sub("\*\s+", "", err)
                 corr = re.sub("\*\s+", "", corr)
                 # cleaning the strings begin with *
                 err = re.sub("\*\*\s+", "", err)
                 corr = re.sub("\*\*\s+", "", corr)
                 # cleaning the strings begin with -
                 err = re.sub("-\s+", "", err)
                 corr = re.sub("-\s+", "", corr)
                 # cleaning the tag for conversation:
                 err = re.sub("A:\s*","", err)
                 corr = re.sub("A:\s*","", corr)
                # cleaning the tag for conversation:
                 err = re.sub("B:\s*", "", err)
                 corr = re.sub("B:\s*", "", corr)
                 a = err
                 b = corr

                 return a, b




corr_cache = None
if __name__ == "__main__":
    assert platform.python_version_tuple()[0] == '3', 'This program supports only python3'
    file = sys.argv[1]
    err_file = open('Jan.err', 'w', encoding='utf8')
    corr_file = open('Jan.corr', 'w', encoding='utf8')
    with codecs.open(file, 'r', encoding='utf8') as f:
        for text in f:
            if process(text) is not None:

                err, corr = process(text)
                if corr != corr_cache:
                    corr_cache = corr
                    err_file.write(err+'\n')
                    corr_file.write(corr+'\n')
    err_file.close()
    corr_file.close()