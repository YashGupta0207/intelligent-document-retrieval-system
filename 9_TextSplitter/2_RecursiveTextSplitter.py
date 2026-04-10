from langchain_text_splitters import RecursiveCharacterTextSplitter

text = '''Cricket is played with a bat and ball and involves two competing sides (teams) of 11 players. The field is oval with a rectangular area in the middle, known as the pitch, that is 22 yards (20.12 metres) by 10 feet (3.04 metres) wide. Two sets of three sticks, called wickets, are set in the ground at each end of the pitch. Across the top of each wicket lie horizontal pieces called bails. The sides take turns at batting and bowling (pitching); each turn is called an “innings” (always plural). Sides have one or two innings each, depending on the prearranged duration of the match, the object being to score the most runs. The bowlers, delivering the ball with a straight arm, try to break (hit) the wicket with the ball so that the bails fall.'''

spliter = RecursiveCharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap = 0
)

re = spliter.split_text(text)

print(len(re))
print(re)



## we can also split by coding language and markdown by language

## SemanticTextSplitter  this divides the text with the help of embeding checks the cosine value and split the text 