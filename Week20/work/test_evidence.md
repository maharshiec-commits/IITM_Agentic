# Ornativa Jewels Chatbot — Test Evidence Log

**Brand**: Ornativa Jewels (Hyderabad, India)  
**Catalogue Source**: `Jewellery Details.pdf`  
**Evaluation Framework**: Langflow / Flowise Visual RAG Pipeline  

---

### Test Query 1: Material & Availability

- **Objective**: Verify retrieval of diamond items filtered by availability.
- **User Input**: *"List all available diamond items."*
- **Chatbot Response**:

> Certainly! Here are the available diamond items from our catalogue:
> 
> 1. **Classic Diamond Ring**
>    - Material: 18K Gold + Diamond
>    - Weight: 5.2 g
>    - Price: ₹135,000
> 
> 2. **Diamond Stud Earrings**
>    - Material: 18K Gold + Diamond
>    - Weight: 6.2 g
>    - Price: ₹105,000
> 
> 3. **Lotus Pendant**
>    - Material: 18K Gold + Diamond
>    - Weight: 8.0 g
>    - Price: ₹72,000
> 
> If you need more information or assistance, feel free to ask!

- **Sources Referenced**: `Jewellery Details.pdf`

---

### Test Query 2: Price Lookup

- **Objective**: Verify exact price and specifications retrieval for a specific product.
- **User Input**: *"What is the price of the Pearl Necklace?"*
- **Chatbot Response**:

> The Pearl Necklace is priced at ₹245,000. It is made of 18K Gold and features pearls weighing 28.5 g. If you have any more questions or need assistance, feel free to ask!

- **Sources Referenced**: `Jewellery Details.pdf`

---

### Test Query 3: Gold Purity / Material

- **Objective**: Verify multi-item filtering by 22K gold purity across different categories.
- **User Input**: *"Which products are made of 22K gold?"*
- **Chatbot Response**:

> The products made of 22K gold in our collection are:
> 
> 1. **Gold Chain Bracelet**
>    - Weight: 12.0 g
>    - Price: ₹87,500
> 
> 2. **Om Symbol Pendant**
>    - Weight: 6.5 g
>    - Price: ₹48,000
> 
> If you need more information about any of these items, feel free to ask!

- **Sources Referenced**: `Jewellery Details.pdf`

---

### Test Query 4: Conversational Memory (Turn 1)

- **Objective**: Establish multi-turn conversational context for rings, earrings, and pendants.
- **User Input**: *"Show me diamond products."*
- **Chatbot Response**:

> Certainly! Here are the diamond products available in our catalogue:
> 
> 1. **Classic Diamond Ring**
>    - **Material:** 18K Gold + Diamond
>    - **Weight:** 5.2 g
>    - **Price:** ₹135,000
>    - **Stock:** Available
> 
> 2. **Diamond Stud Earrings**
>    - **Material:** 18K Gold + Diamond
>    - **Weight:** 6.2 g
>    - **Price:** ₹105,000
>    - **Stock:** Available
> 
> 3. **Lotus Pendant**
>    - **Material:** 18K Gold + Diamond
>    - **Weight:** 8.0 g
>    - **Price:** ₹72,000
>    - **Stock:** Available
> 
> If you need more information or wish to purchase any of these items, feel free to ask!

- **Sources Referenced**: `Jewellery Details.pdf`

---

### Test Query 5: Conversational Memory (Turn 2 - Follow-up)

- **Objective**: Verify memory resolution of 'the ring' to Classic Diamond Ring from Turn 1.
- **User Input**: *"What's the price of the ring?"*
- **Chatbot Response**:

> The price of the Classic Diamond Ring (R101) is ₹135,000. It is made of 18K Gold and features a diamond weighing 5.2 g.

- **Sources Referenced**: `Jewellery Details.pdf`

---

### Test Query 6: Out-of-Stock Handling

- **Objective**: Verify out-of-stock detection for R102 and relevant alternative recommendation (R101).
- **User Input**: *"I want to buy the Ruby Solitaire Ring. Is it in stock?"*
- **Chatbot Response**:

> The Ruby Solitaire Ring (R102) is currently out of stock. As an alternative, you might consider the Classic Diamond Ring (R101), which is available and features 18K Gold and a diamond. It is priced at ₹135,000. Would you like more information on that?

- **Sources Referenced**: `Jewellery Details.pdf`

---

### Test Query 7: Out-of-Stock & Alternative Suggestion

- **Objective**: Verify out-of-stock detection for B402 and alternative recommendation (B401 Gold Chain Bracelet).
- **User Input**: *"Can I purchase the Emerald Cuff Bracelet?"*
- **Chatbot Response**:

> Unfortunately, the Emerald Cuff Bracelet (Product ID: B402) is currently out of stock. However, I recommend considering the Gold Chain Bracelet (Product ID: B401), which is made of 22K Gold and is available for ₹87,500. Would you like more information on that?

- **Sources Referenced**: `Jewellery Details.pdf`

---

### Test Query 8: Fallback / Non-Catalogue Handling

- **Objective**: Verify graceful hallucination prevention when an item is not in the catalogue.
- **User Input**: *"Do you sell silver anklets or platinum chains?"*
- **Chatbot Response**:

> Thank you for your inquiry! Unfortunately, Ornativa Jewels does not currently carry silver anklets or platinum chains in our collection. If you're interested in other types of jewellery, please let me know, and I'd be happy to assist you!

- **Sources Referenced**: `Jewellery Details.pdf`

---

