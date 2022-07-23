import csv

def list_words(text):
  words=[]
  words=text
  return words

def training(texts):
    c_words ={}
    c_categories ={} # number of items in each category
    c_texts = 0
    c_tot_words =0 # total number words being processed
    

    for t in texts:# cool/cute
        words = list_words(t[0])
        c_texts = c_texts + 1
        if t[1] not in c_categories:
            c_categories[t[1]] = 1
        else:
            c_categories[t[1]]= c_categories[t[1]] + 1

   
    for p in texts:# keyword
        if p not in c_words:
            c_tot_words = c_tot_words +1
            c_words[p] = {}
            for c in c_categories:
                c_words[p][c] = 0

        c_words[p][t[1]] = c_words[p][t[1]] + 1


    #print( c_words )
    # c_words  = { 'word':{'spam': num ,'nopam': num}}
    return (c_words, c_categories, c_texts, c_tot_words)


def classifier(subject_line, c_words, c_categories, c_texts, c_tot_words):
    category =""
    category_prob = 0

    for c in c_categories:
      
        prob_c = float(c_categories[c])/float(c_texts)
        words = list_words(subject_line)
        prob_total_c = prob_c
        for p in words:
            if p in c_words:
                prob_p= float(c_words[p][c])/float(c_tot_words)
                # for example c_words['important']['spam'] -> 1
                prob_cond = prob_p/prob_c
                prob =(prob_cond * prob_p)/ prob_c # = tp
                prob_total_c = prob_total_c * prob

            if category_prob < prob_total_c:
                category = c # decision is made here
                category_prob = prob_total_c
    return (category, category_prob)


if __name__ == "__main__":

    #First Training
    with open('training.csv') as f:
    #with open('dataSpam.out') as f:
      subjects = dict(csv.reader(f, delimiter=','))
      p,c,t,tp = training(subjects.items())
      # p c_words  = { 'word':{'spam': num ,'nopam': num}}
      # c c_categories total number of {'spam':num,'nospam':num}
      # t  number of sentences
      # tp number of words 
     

    #Test the accuracy 
    with open("test.csv") as f:
        correct = 0
        count=0
        tests = csv.reader(f)
        for subject in tests:
            clase = classifier(subject[0],p,c,t,tp)
            print( clase )
            count += 1
            if clase[0] == subject[1]:
                correct += 1        
        print("Efficiency {0} %".format(100*correct/count))