#### \# Limitation1: No Long-Term Memory



The chatbot developed in this project **can remember previous messages only during the current conversation session**. This is because the conversation history is stored temporarily in memory and is sent to the Groq model along with each new user message. Once the application is closed, refreshed, or restarted, this stored conversation history is lost.



* ###### *For example,* 



*suppose a user tells the chatbot:*



*## Day 1*



*\* \*\*User:\*\* "I am learning Python and Machine Learning."*

*\* \*\*Chatbot:\*\* "That's great. Python is widely used in Machine Learning."*



*During this session, the chatbot can remember that the user is learning Python and Machine Learning.*



*However, if the user returns the next day and asks:*



*## Day 2*



*\* \*\*User:\*\* "What should I learn next?"*



*The chatbot will not remember the previous conversation because the earlier chat history was not stored permanently. As a result, it will provide a general response instead of a personalized recommendation based on the user's learning background.*



*This limitation reduces the chatbot's ability to maintain continuity across sessions and provide personalized assistance.*

###### 

* ###### \# Possible Solutions



**## 1. Store Conversation History in a Database**



\* Save user conversations in a database such as SQLite or PostgreSQL.

\* When the user returns, retrieve the previous conversations and provide them to the chatbot.

\* This allows the chatbot to remember information across sessions.



**## 2. Conversation Summarization**



\* Instead of storing every message, generate a summary of important user information.

\* Example: \*"User is learning Python and Machine Learning."\*

\* Store this summary and use it in future conversations.

\* This reduces memory usage and avoids sending large amounts of text to the model.



**## 3. Memory Using Semantic Search**



\* Convert previous conversations into embeddings and store them in a vector database.

\* When a new query is received, perform semantic search to retrieve only the most relevant past conversations.

\* This approach provides better scalability and retrieves only useful information.



**## 4. Hybrid Memory System**



\* Combine short-term memory, conversation summaries, and semantic search.

\* The chatbot can use recent messages, stored summaries, and relevant past conversations together.

\* This approach is commonly used in advanced AI assistants and provides more accurate and personalized responses.



Implementing these solutions would improve the chatbot's ability to remember users, maintain conversational context across sessions, and provide more personalized responses.



\-----------------------------------



#### 

#### \# Limitation2: Top-k Retrieval May Miss the Correct Answer



In a Retrieval-Augmented Generation (RAG) system, relevant document chunks are retrieved based on semantic similarity between the user query and the stored embeddings. However, one major limitation is that the actual answer may not be present in the top-k retrieved chunks.



This occurs because the retrieval process selects chunks that are most similar to the query, not necessarily the chunks that contain the correct answer. In other words, \*\*similar does not always mean relevant\*\*.



* ###### \## Example Scenario



*Consider the following document chunks:*



*### Chunk 1*



*Attendance requirements for examinations...*



*### Chunk 2*



*Students must maintain at least 75% attendance...*



*### Chunk 3*



*Fee payment guidelines...*



*### Chunk 4*



*Attendance shortage condonation rules...*



*Suppose the user asks:*



*\*\*"Can attendance shortage be condoned?"\*\**



*The vector database performs semantic search and retrieves the top 3 most similar chunks:*



*1. Chunk 1*

*2. Chunk 2*

*3. Chunk 3*



*However, the actual answer is present in \*\*Chunk 4\*\*, which was ranked fourth.*



*Since the retrieval parameter is set to \*\*k = 3\*\*, Chunk 4 is never retrieved and therefore never sent to the Large Language Model (LLM).*

###### 

###### \## Result



\* The LLM does not receive the chunk containing the correct answer.

\* The chatbot may respond with incomplete information.

\* It may state that the information is unavailable.

\* In some cases, it may generate an incorrect answer (hallucination).

###### 

###### \## Why Not Simply Increase k?



One possible solution is to increase the value of k.



For example:



\* k = 3 → Retrieve 3 chunks

\* k = 10 → Retrieve 10 chunks

\* k = 20 → Retrieve 20 chunks



While this increases the chance of retrieving the correct chunk, it introduces new problems:



\### **Increased Noise**



Many retrieved chunks may be only loosely related to the query.



The LLM receives unnecessary information, making it harder to focus on the most relevant context.



\### H**igher Token Usage**



More chunks mean more text is sent to the LLM.



This increases:



\* Prompt size

\* Token consumption

\* Operational cost



\### **Slower Response Time**



The LLM must process a larger amount of information before generating an answer, which increases latency.



Therefore, simply increasing k is not an ideal solution.





###### \# Possible Solution: Reranking



A more effective solution is to use a \*\*reranker model\*\*.



Instead of directly sending the retrieved chunks to the LLM, the system performs an additional ranking step.



\## How It Works



\### Step 1: **Retrieve Many Chunks**



The vector database retrieves a larger set of candidate chunks.



Example:



\* Retrieve Top 20 chunks



\### Step 2: **Apply Reranking**



A reranker model evaluates the relationship between:



\* User query

\* Retrieved chunks



The reranker assigns a relevance score to each chunk and rearranges them based on actual relevance rather than embedding similarity alone.



\### Step 3: **Select Best Chunks**



Only the highest-ranked chunks are selected.



Example:



\* Retrieve 20 chunks

\* Rerank all 20 chunks

\* Send only the best 5 chunks to the LLM





\-----------------------------------------

##### 

##### \# Limitation3: No OCR Support for Scanned Documents



The current RAG system extracts text directly from PDF documents and creates embeddings from the extracted content. This approach works well for text-based PDFs where the content is stored as actual text.



However, the system does not support Optical Character Recognition (OCR). As a result, it cannot properly process scanned PDFs or image-based documents.



* ###### *## Example Scenario*



*Consider a PDF containing a scanned copy of a university regulation document.*



*Although the document appears readable to a human, the content is actually stored as images rather than text.*



*When the PDF is processed:*



*\* The document loader attempts to extract text.*

*\* No meaningful text is found.*

*\* Empty or incomplete content is obtained.*

*\* No useful embeddings are generated.*



*Suppose the document contains the following information:*



*\*"Students must maintain at least 75% attendance to appear for examinations."\**



*A user asks:*



*\*\*"What is the minimum attendance required for examinations?"\*\**



*Since the text was never extracted from the scanned document:*



*\* The information is not stored in the vector database.*

*\* No relevant chunks can be retrieved.*

*\* The LLM does not receive the required context.*



*## Result*



*\* Questions related to scanned PDFs cannot be answered correctly.*

*\* Important information may be completely missed.*

*\* The chatbot may respond with incorrect information or indicate that the answer is unavailable.*

*\* The overall retrieval accuracy decreases for image-based documents.*





\## Why Does This Happen?



The current system relies on PDF text extraction tools.



These tools can only read content that already exists as digital text inside the PDF.



They cannot understand text that is present as an image.





###### \## Possible Solution: Optical Character Recognition (OCR)



OCR is a technology that converts text present in images into machine-readable text.



Instead of directly processing the PDF, the system would first extract text from scanned pages using an OCR engine.



\## How It Works



\### Step 1: Upload PDF



The user uploads a scanned PDF.



\### Step 2: **OCR Processing**



**OCR software analyzes each page and identifies the text contained in the images.**



\### Step 3: Text Extraction



The detected text is converted into editable and searchable text.



\### Step 4: Create Embeddings



Embeddings are generated from the extracted text.



\### Step 5: Store in Vector Database



The embeddings are stored in the vector database.



\### Step 6: Retrieval and Answer Generation



The retrieved content is sent to the LLM to generate answers.



