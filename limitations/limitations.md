#### 1.RAG PDF CHATBOT

##### 

##### Top-k retrieval may miss the answer 



* When we ask a question the answer to it may be present at the end of document. So there is a possibility that the answer may not be present in it. This happens because while retrieving chunks, the most relevant chunks are not actually returned. The problem is similar doesn't always means relevant. 



* example scenario: 



*Chunk 1*



*Attendance requirements for examinations...*



*Chunk 2*



*Students must maintain at least 75% attendance...*



*Chunk 3*



*Fee payment guidelines...*



*Chunk 4*



*Attendance shortage condonation rules...*



*User asks:*



*"Can attendance shortage be condoned?"*



*The embedding search might retrieve:*



*Chunk 1*

*Chunk 2*

*Chunk 3*



*But the actual answer is in Chunk 4, which was ranked 4th.*



*Since k=3, Chunk 4 is never sent to the LLM.*



*Result:*



*The LLM doesn't see the answer.*

*It may say "I don't know" or hallucinate.*



* The **problem** in increasing k is that it increases the noise ie the LLM gets flooded with irrelevant chunks and it takes more time. 



* The **solution** is reranker - ie, retrieve k chunks cheaply and rerank those and send only top 5 to the llm.

