from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
load_dotenv()

llm1 = ChatOpenAI(model="openai/gpt-4o-mini", base_url="https://openrouter.ai/api/v1")

p1 = PromptTemplate(
    template='Generate the short simple notes from the following text. {text}',
    input_variables=['text']
)

p2 = PromptTemplate(
    template='Generate 2 short questions and answers from the following text.{text}',
    input_variables=['text']
)

p3 = PromptTemplate(
    template='Merger the following notes and quiz into a singlle document \n notes->{notes} and quiz->{quiz}',
    input_variables=['notes','quiz']
)

parser = StrOutputParser()

parallel_chain = RunnableParallel({
    'notes' : p1 | llm1 | parser,
    'quiz' : p2 | llm1 | parser
})

merge_chain = p3 | llm1 |parser

chain = parallel_chain | merge_chain


text = """Least-angle regression (LARS) is a regression algorithm for high-dimensional data, developed by Bradley Efron, Trevor Hastie, Iain Johnstone and Robert Tibshirani. LARS is similar to forward stepwise regression. At each step, it finds the feature most correlated with the target. When there are multiple features having equal correlation, instead of continuing along the same feature, it proceeds in a direction equiangular between the features.

The advantages of LARS are:

It is numerically efficient in contexts where the number of features is significantly greater than the number of samples.

It is computationally just as fast as forward selection and has the same order of complexity as ordinary least squares.

It produces a full piecewise linear solution path, which is useful in cross-validation or similar attempts to tune the model.

If two features are almost equally correlated with the target, then their coefficients should increase at approximately the same rate. The algorithm thus behaves as intuition would expect, and also is more stable.

It is easily modified to produce solutions for other estimators, like the Lasso.

The disadvantages of the LARS method include:

Because LARS is based upon an iterative refitting of the residuals, it would appear to be especially sensitive to the effects of noise. This problem is discussed in detail by Weisberg in the discussion section of the Efron et al. (2004) Annals of Statistics article.

The LARS model can be used via the estimator Lars, or its low-level implementation lars_path or lars_path_gram."""

re = chain.invoke({'text': text})

#print(re)

chain.get_graph().print_ascii()