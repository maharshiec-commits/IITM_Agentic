# Ornativa Jewels — Retrieval-Based Chatbot

**Course**: Professional Certificate Programme in Agentic AI  
**Week 20: Graded Mini Project**  
**Brand**: Ornativa Jewels (Hyderabad, India)  
**Tools**: Langflow / Flowise Visual RAG Pipeline  
**Student**: Maharshi  

---

## Executive Summary

This project implements a visual-pipeline retrieval-based conversational chatbot for **Ornativa Jewels**, a luxury retail jewellery brand based in Hyderabad, India. The chatbot answers customer inquiries using the official product catalogue provided in `Jewellery Details.pdf`. 

Built according to the visual drag-and-drop RAG pipeline architecture of **Langflow** and **Flowise**, the system features:
1. **Accurate PDF Ingestion & Semantic Chunking**: Chunk size `1000`, overlap `200` to maintain atomic product specifications.
2. **Dense Vector Indexing**: OpenAI `text-embedding-3-small` stored in vector storage with top-$k=4$ retrieval.
3. **Conversational Memory**: Sliding-window buffer memory retaining multi-turn context for natural pronoun resolution.
4. **Brand Tone & Grounded Prompting**: Polite, concise, and factual Hyderabad luxury brand persona.
5. **Dynamic Out-of-Stock Fallback Logic**: Automatically detects out-of-stock items (e.g., Ruby Solitaire Ring, Emerald Cuff Bracelet) and recommends catalogue-grounded alternatives.

---

## 1. Visual Pipeline Architecture & Component Choices

The chatbot pipeline follows the modular visual design pattern common to both Langflow and Flowise:

```
┌────────────────────────────────┐
│   Jewellery Details.pdf        │ (Document Loader: File / pdfFile)
└───────────────┬────────────────┘
                │ Raw document
                ▼
┌────────────────────────────────┐
│   Recursive Character Splitter │ (SplitText: Chunk=1000, Overlap=200)
└───────────────┬────────────────┘
                │ Semantic chunks
                ▼
┌────────────────────────────────┐       ┌───────────────────────────────┐
│   OpenAI Embeddings            │──────>│   Chroma / FAISS Vector Store │
│   (text-embedding-3-small)     │       │   (Similarity Search, Top-K=4)│
└────────────────────────────────┘       └──────────────┬────────────────┘
                                                        │ Relevant catalogue context
                                                        ▼
┌────────────────────────────────┐       ┌───────────────────────────────┐
│   Chat Input (Customer Query)  │──────>│   Ornativa Brand Prompt       │
└────────────────────────────────┘       │   - Grounded facts only       │
                                         │   - Out-of-stock alternatives │
┌────────────────────────────────┐       │   - Polite & concise tone     │
│   Chat Memory (Buffer Window)  │──────>│                               │
│   (Last 6 conversation turns)  │       └──────────────┬────────────────┘
└────────────────────────────────┘                      │
                                                        ▼
                                         ┌───────────────────────────────┐
                                         │   Chat Model (gpt-4o-mini)    │
                                         │   Temperature: 0.1            │
                                         └──────────────┬────────────────┘
                                                        │ Grounded response
                                                        ▼
                                         ┌───────────────────────────────┐
                                         │   Chat Output (Customer UI)   │
                                         └───────────────────────────────┘
```

### Component Breakdown & Role Justification

| Pipeline Stage | Langflow Component | Flowise Node | Configuration | Role / Justification |
|---|---|---|---|---|
| **Data Ingestion** | `File` | `pdfFile` | `Jewellery Details.pdf` | Extracts clean product text from the single-page catalogue PDF. |
| **Text Splitting** | `SplitText` | `recursiveCharacterTextSplitter` | Chunk: `1000`, Overlap: `200` | Separates product entries cleanly while keeping product IDs, materials, weights, prices, and stock together. |
| **Embeddings** | `OpenAIEmbeddings` | `openAIEmbeddings` | `text-embedding-3-small` | High-dimensional dense representation capturing jewellery terminology (carats, cuts, purity, gemstones). |
| **Vector Storage** | `Chroma` / `FAISS` | `faiss` / `Chroma` | Metric: Cosine, $k=4$ | Indexes all catalogue chunks for fast sub-second semantic retrieval. |
| **Conversational Memory**| `ChatMemory` | `bufferMemory` | Window: `6` turns, `chat_history` | Maintains multi-turn context allowing follow-ups (e.g., *"What is the price of the ring?"*). |
| **Prompt Engineering** | `Prompt` | `promptTemplate` | Custom Ornativa System Prompt | Enforces brand voice, zero-hallucination policy, and explicit out-of-stock alternative recommendations. |
| **Language Model** | `OpenAIModel` | `chatOpenAI` | `gpt-4o-mini`, Temp: `0.1` | Low temperature ensures strict fidelity to retrieved prices, weights, and stock status. |

---

## 2. Chunking Approach & Rationale

- **Chunk Size**: `1000` characters
- **Chunk Overlap**: `200` characters
- **Separators**: `["\n\n", "\n", "ProductID:", " ", ""]`

### Why This Strategy?
1. **Atomic Product Integrity**: Each product entry in `Jewellery Details.pdf` spans approximately 110–135 characters (ProductID, Name, Category, Material, Weight, Price, Stock). A chunk size of 1000 characters encompasses 6 to 8 adjacent items, ensuring that the semantic relationship between complementary items (such as the `R101 Classic Diamond Ring` and `R102 Ruby Solitaire Ring`) remains within the same retrieval context.
2. **Preventing Boundary Splitting**: An overlap of 200 characters prevents individual product specifications (e.g., price or stock availability) from being truncated across boundaries.
3. **Retrieval Density**: With the entire catalogue being 1,343 characters, this strategy produces 2 cohesive chunks that provide 100% catalogue recall with top-$k=4$.

---

## 3. Prompt Design & Brand Voice

The system prompt was engineered to establish a luxury retail persona representing **Ornativa Jewels (Hyderabad, India)**:

```text
You are Ornativa's virtual jewellery expert for Ornativa Jewels, a premier fine jewellery brand based in Hyderabad, India.
Your mission is to provide polite, concise, and factual assistance to customers browsing our catalogue.

GUIDELINES & RULES:
1. Factual Grounding: Answer strictly using the catalogue data provided in the context. Do not invent products, prices, or specifications.
2. Brand Tone: Be polite, warm, luxurious, concise, and factual. Greet customers appropriately.
3. Out-of-Stock Handling & Alternative Suggestions:
   - If a customer inquires about an item that is "Out of Stock" (e.g., Ruby Solitaire Ring [R102] or Emerald Cuff Bracelet [B402]), clearly inform them that the item is currently out of stock.
   - Immediately suggest a relevant available alternative from the catalogue based on similar category, material, or style (e.g., suggest Classic Diamond Ring [R101] for the Ruby Solitaire Ring, or Gold Chain Bracelet [B401] for the Emerald Cuff Bracelet).
4. Multi-Turn Context: Maintain short-term conversational context. If the customer refers to "the ring", "it", or "earrings" in follow-ups, resolve it using previous turns.
5. Missing / Non-Catalogue Items: If a requested item (e.g., silver anklets, platinum watch) is not present in the catalogue, politely state that Ornativa Jewels does not currently carry it in our collection.
6. Currency & Specifications: Always quote prices in Indian Rupees (INR / ₹) and include material details (e.g., 22K Gold, 18K Gold, Diamond, Pearl) when relevant.
```

---

## 4. Conversational Memory Setup

The system incorporates a **Sliding Window Buffer Memory** (`ConversationBufferWindowMemory` with $k=6$ turns).

### Multi-Turn Context Workflow:
1. **Turn 1**: The user asks: *"Show me diamond products."*
   - Chatbot lists the Classic Diamond Ring (R101), Diamond Stud Earrings (E302), and Lotus Pendant (P501).
   - This interaction is recorded in the buffer memory.
2. **Turn 2**: The user asks: *"What's the price of the ring?"*
   - The question condenser evaluates the chat history, resolves *"the ring"* to *"Classic Diamond Ring"*, and retrieves the exact pricing: **₹1,35,000**.
   - Without memory, a standard single-turn RAG model would ask the customer to clarify which ring they meant.

---

## 5. Out-of-Stock Handling & Alternative Recommendations

In luxury jewellery retail, simply stating *"Out of stock"* results in lost customer interest. The prompt logic mandates proactive alternative recommendation based on:
1. **Category Alignment**: Suggesting a ring for an out-of-stock ring; a bracelet for an out-of-stock bracelet.
2. **Material Affinity**: Matching gold purity (18K/22K) or precious stones.
3. **Availability Verification**: Verifying that the proposed alternative is strictly listed as *"Available"*.

### Verified Out-of-Stock Scenarios in Catalogue:
- **Scenario A**: `Ruby Solitaire Ring` (R102, 22K Gold + Ruby, ₹98,500) $\rightarrow$ **Out of Stock**.  
  *Alternative Suggested*: `Classic Diamond Ring` (R101, 18K Gold + Diamond, ₹1,35,000, Available).
- **Scenario B**: `Emerald Cuff Bracelet` (B402, 18K Gold + Emerald, ₹1,50,000) $\rightarrow$ **Out of Stock**.  
  *Alternative Suggested*: `Gold Chain Bracelet` (B401, 22K Gold, ₹87,500, Available).

---

## 6. Testing & Evaluation Evidence

Below is the verified test log from running `python test_flow.py` against `Jewellery Details.pdf`:

| Query # | Category | User Query | Chatbot Response Summary | Verification Outcome |
|---|---|---|---|:---:|
| **1** | Material & Availability | *"List all available diamond items."* | Lists Classic Diamond Ring (₹1,35,000), Diamond Stud Earrings (₹1,05,000), and Lotus Pendant (₹72,000). All marked Available. | ✅ PASS |
| **2** | Price Lookup | *"What is the price of the Pearl Necklace?"* | Returns exact price: ₹245,000, 18K Gold + Pearl, 28.5 g. | ✅ PASS |
| **3** | Material Classification | *"Which products are made of 22K gold?"* | Correctly identifies 22K gold items: Gold Chain Bracelet (₹87,500), Om Symbol Pendant (₹48,000), Emerald Choker (₹3,10,000), Daily Wear Earrings (₹55,000). | ✅ PASS |
| **4** | Multi-Turn Memory (Turn 1) | *"Show me diamond products."* | Lists all diamond products with prices and specifications. Sets conversational memory context. | ✅ PASS |
| **5** | Multi-Turn Memory (Turn 2) | *"What's the price of the ring?"* | Memory correctly resolves *"the ring"* to Classic Diamond Ring (R101) and returns ₹135,000. | ✅ PASS |
| **6** | Out-of-Stock Handling 1 | *"I want to buy the Ruby Solitaire Ring. Is it in stock?"* | Informs customer that R102 is out of stock. Proactively recommends Classic Diamond Ring (R101) for ₹135,000. | ✅ PASS |
| **7** | Out-of-Stock Handling 2 | *"Can I purchase the Emerald Cuff Bracelet?"* | Informs customer that B402 is out of stock. Recommends Gold Chain Bracelet (B401) for ₹87,500. | ✅ PASS |
| **8** | Hallucination / Fallback | *"Do you sell silver anklets or platinum chains?"* | Polite refusal: Ornativa Jewels does not carry silver anklets or platinum chains in the catalogue. Zero hallucination. | ✅ PASS |

---

## 7. Low-Code / No-Code Tools vs. Code-Based Approaches

As addressed in the weekly learning outcomes, this project highlights key trade-offs between visual flow builders and code-based implementations:

| Dimension | Low-Code / Visual Builders (Langflow / Flowise) | Code-Based Approaches (LangChain / LlamaIndex / Python) |
|---|---|---|
| **Speed to Prototype** | **Very High**: Visual drag-and-drop connectors enable building an end-to-end RAG flow in minutes without boilerplate. | **Moderate**: Requires writing ingestion loops, imports, state handlers, and API wrappers. |
| **Accessibility** | **Broad**: Product managers, domain experts, and prompt engineers can inspect and tweak prompts/parameters visually. | **Specialized**: Requires software engineering skills, virtual environments, and debugging tools. |
| **Custom Control & Branching** | **Constrained**: Complex conditional routing (e.g., custom regex validation or specialized error handlers) can be cumbersome in visual graphs. | **Unlimited**: Complete algorithmic flexibility, custom classes, unit testing, and dynamic control loops. |
| **CI/CD & Version Control** | **Challenging**: Large JSON flow exports are hard to diff and merge in Git; automated regression testing is less mature. | **Excellent**: Python code diffs cleanly, integrates seamlessly with GitHub Actions, pytest, and linting pipelines. |
| **Production Scalability** | **Good for standard flows**: Suitable for internal tools and straightforward retrieval endpoints. | **Superior**: Custom async pools, thread safety, microservices deployment, and containerization. |

---

## 8. Setup & Execution Instructions

### Option 1: Import into Langflow
1. Launch Langflow (Desktop app, or `langflow run` at `http://127.0.0.1:7860`).
2. Click **Import / New Flow** $\rightarrow$ select [`ornativa_jewels_langflow.json`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week20/work/ornativa_jewels_langflow.json).
3. Ensure the File loader node points to `Jewellery Details.pdf`.
4. Add your OpenAI API key in the OpenAI Embeddings and OpenAI Model nodes.
5. Open the **Playground** to test queries!

### Option 2: Import into local Flowise
1. Start Flowise (`npx flowise start` or local Docker at `http://localhost:3000`).
2. Go to **Chatflows** $\rightarrow$ **Add New** $\rightarrow$ **Load Chatflow** $\rightarrow$ select [`ornativa_jewels_flowise.json`](file:///c:/Users/Maharshi/Documents/IITM_Agentic/Week20/work/ornativa_jewels_flowise.json).
3. Configure the OpenAI credentials.
4. Click **Save** and test in the chat popup!

### Option 3: Local Python Verification & Evaluation Suite
Run the automated verification script:
```powershell
cd C:\Users\Maharshi\Documents\IITM_Agentic\Week20\work
python test_flow.py
```

### Option 4: Interactive Streamlit Visual Dashboard
Launch the custom customer UI:
```powershell
streamlit run app.py
```

---

## 9. Submission File Manifest

```
Week 20_Graded Mini Project_Maharshi.zip
├── ornativa_jewels_langflow.json     # Exported Langflow visual pipeline flow
├── ornativa_jewels_flowise.json      # Exported Flowise chatflow
├── README.md                         # Architecture explanation, rubric details, & comparison
├── test_evidence.md                  # Complete log of all 8 evaluation test scenarios
├── app.py                            # Interactive Streamlit visual customer application
├── test_flow.py                      # Automated test suite and pipeline execution script
├── Jewellery Details.pdf             # Original catalogue dataset
└── vectorstore/                      # Pre-indexed FAISS vectors
```

