# Scholarly KGQA using LLM
This repository contains our Scholarly KGQA system code, for the Scholarly-QALD-23 challenge.

Question Answering (QA) over scholarly Knowledge Graphs (KGs) is a challenging task, due to the complexity of the KGs and the variety of natural language questions that can be asked as well as the underlying ontologies. In this paper, we present a KGQA system that uses three components: (1) a question analyzer to identify similar questions from the training set, (2) a SPARQL generator to generate SPARQL queries for the test questions, and (3) an answer extractor to run the SPARQL queries against the underlying KG.
Our system was evaluated on the SciQA dataset, a challenging benchmark for question answering over scholarly KGs. Our system achieved an F1 score of 99.0\% on the SciQA test set which is comparable to the state of the art.

![sciqa_model_final](https://github.com/huntila/scholarly-kgqa/assets/58974800/195a5edd-0a54-4e6e-9e19-eb3741a8a688)

The full paper can be found [here](https://ceur-ws.org/Vol-3592/paper5.pdf).
