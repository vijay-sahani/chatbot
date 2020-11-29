def sorting():
    with open("training_data.txt",encoding="utf8")as f:
        lines=f.readlines()
    data=[]
    for line in lines:
        parsed=line.split(".")
        data.extend(parsed)
    data=list(map(lambda x:x.lower().capitalize(),data))
    while("\n" in data) : 
        data.remove("\n")  
    # with open("data_1.txt","w")as f:
    #     f.write(str(data))
    return data

def matchingword(query,sentence):
    words1=query.split(" ")
    words2=sentence.split(" ")
    score=0
    for word1 in words1:
        for word2 in words2:
            if word1==word2:
                score+=1
    return score

def answers(query):
    sentences=sorting()
    query=query.capitalize()
    score=[matchingword(query,sentence) for sentence in sentences]
    sentscore=[sortsent for sortsent in sorted(zip(score,sentences),reverse=True)]
    for score,item in sentscore:
        if score>1:
            print("with score of",score)
            return item
        elif score==1:
            print("with score of ",score)
            return item
    return "No Data Available!"

if __name__ == "__main__":
    while True:
        query=input(">")
        print(answers(query))