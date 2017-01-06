import math
import operator

def brevity_penalty(c, r):
    if c > r:
        bp = 1
    else:
        bp = math.exp(1-(float(r)/c))
    return bp

def clip_count(cand_d, ref_d):
    """Count the clip count for each ngram considering all references"""
    count = 0
    for m in cand_d.keys():
        m_w = cand_d[m]
        m_max = ref_d.get(m,0)
        m_w = min(m_w, m_max)
        count += m_w
    return count

def count_ngram(cand, ref, n):
    clipped_count = 0
    count = 0
    r = 0
    c = 0
    # Build dictionary of ngram counts
    ref_d = {}
    words = ref.strip().split()
    r += len(words)
    limits = len(words) - n + 1
    # loop through the sentance consider the ngram length
    for i in range(limits):
        ngram = ' '.join(words[i:i+n]).lower()
        ref_d[ngram] = ref_d.get(ngram,0) + 1
    # cand
    cand_d = {}
    words = cand.strip().split()
    c += len(words)
    limits = len(words) - n + 1
    for i in range(0, limits):
        ngram = ' '.join(words[i:i + n]).lower()
        cand_d[ngram] = cand_d.get(ngram,0) + 1
    clipped_count += clip_count(cand_d, ref_d)
    count += limits
    '''
    if clipped_count == 0:
        pr = 0
    else:
        pr = float(clipped_count) / count
    '''
    bp = brevity_penalty(c, r)
    return clipped_count, count, bp

def geometric_mean(precisions):
    return (reduce(operator.mul, precisions)) ** (1.0 / len(precisions))

def cal_bleu(cand,ref):
    precisions = []
    k = 1
    for i in range(4):
        #pr, bp = count_ngram(cand,ref,i+1)
        #precisions.append(pr)
        n, d, bp = count_ngram(cand,ref,i+1)
        if n == 0:
            precisions.append(1.0 / (2**k * d))
            k += 1
        else:
            precisions.append(float(n)/d)
    bleu = geometric_mean(precisions)*bp
    return bleu

for sc,sr in zip(open('03.out'),open('03.ref')):
    print cal_bleu(sc,sr)
