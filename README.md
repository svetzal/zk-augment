# Information Architectural Extraction

Challenges:
- when picking up on a partial entity reference, how to root around the context to find the full entity reference
  - eg a reference to Mike, ultimately within that context meaning specifically Mike Bowler rather than Mike Kaufman
  - eg a reference to Jan 8, ultimately within that context meaning specifically Jan 8, 2025
  - eg a reference to Friday, ultimately within that context meaning specifically Jan 3, 2025
    - pull in parsedatetime module to help with disambiguating time references
  - most text snippets are highly contextual, meaning the interpretation changes according to their context
  - this is the way in which GraphRAG is able to provide a more accurate interpretation of the text,
    - making it possible to consider the context of the snippet by summarizing increasingly large bodies of related text
  - Should we be assessing entity type framing in the context of the summaries rather than the individual snippets?

- Considering the authoritativeness of knowledge
  - do we trust a single person's statement? why do we trust one person's statement over another's?
    - what about when they conflict?
  - how do we detect conflict in knowledge statements?
    - eg interpreting what is "good" or "bad" can be very different when considered in a Liberal or a Conservative context

To Do
- [ ] A way to incrementally index new or updated documents
  - re-chunk updated documents, replace old chunks with new chunks
  - drop the indexes for the old chunks and create new indexes for the new chunks
  - update the graph with changes
- [ ] A way to manage entity types as the dataset gets large
  - treating them as a single flat list is outstretching the limits of the LLM context with my personal zk
- [ ] Filesystem document store, build out the API

Achieved
- [x] Explore the LLMRegistry and how to reference OpenAI's models
- How to make any or all of this agentic
  - [x] a chat LLM can use tools for things like relative date resolution, but can't do structured output
    - an instruct LLM can't use tools, but can do structured output
