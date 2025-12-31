from langsmith import Client
from tests.evaluation.target import rag_target
from tests.evaluation.datasets import DATASET_NAME
from tests.evaluation.evaluators.correctness import correctness
from tests.evaluation.evaluators.relevance import relevance
from tests.evaluation.evaluators.groundedness import groundedness
from tests.evaluation.evaluators.retrieval_relevance import retrieval_relevance

def run():
    client = Client()
    results = client.evaluate(
        rag_target,
        data=DATASET_NAME,
        evaluators=[
            correctness,
            relevance,
            groundedness,
            retrieval_relevance,
        ],
        experiment_prefix="cgu-rag-eval",
        metadata={"version": "langgraph-prod"}
    )
    print(results.to_pandas())

if __name__ == "__main__":
    run()
