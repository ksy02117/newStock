import numpy as np

from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import re



def getKeyword(title : str):
    title = re.sub("<b>.*?</b>", "", title)

    tokenized_doc = getKeyword.okt.pos(title)
    tokenized_nouns = ' '.join([word[0] for word in tokenized_doc if word[1] == 'Noun'])

    try:
        count = CountVectorizer(ngram_range=getKeyword.n_gram_range).fit([tokenized_nouns])
    except ValueError:
        return []
    candidates = count.get_feature_names_out()

    doc_embedding = getKeyword.model.encode([title])
    candidate_embeddings = getKeyword.model.encode(candidates)

    distances = cosine_similarity(doc_embedding, candidate_embeddings)
    keywords = [candidates[index] for index in distances.argsort()[0]]
    return keywords

getKeyword.okt = Okt()
getKeyword.n_gram_range = (3, 3)
getKeyword.model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
