from typing import Any, Dict, List, Optional, Union

from llama_index.core.async_utils import asyncio_run
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.base.llms.types import ChatMessage, ContentBlock
from llama_index.core.bridge.pydantic import Field
from llama_index.core.llms import LLM
from llama_index.core.memory.waterfall.base import BaseMemoryBlock
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores.types import BasePydanticVectorStore, VectorStoreQuery


class StaticMemoryBlock(BaseMemoryBlock):
    """A memory block that returns static text.
    
    This block is useful for including constant information or instructions
    in the context without relying on external processing.
    """
    
    static_text: str = Field(
        description="Static text content to be returned by this memory block."
    )
    include_conditions: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional conditions for when to include this block. Keys should be keywords to match in messages.",
    )

    async def aget(self, input: Optional[List[ChatMessage]] = None, **kwargs: Any) -> str:
        """Return the static text, potentially filtered by conditions."""
        if self.include_conditions and input:
            # Check if any message contains keywords in conditions
            last_message = input[-1] if input else None
            
            if last_message and last_message.content:
                if not any(keyword.lower() in last_message.content.lower() 
                          for keyword in self.include_conditions.keys()):
                    return ""  # Don't include if conditions not met
                
        return self.static_text

    async def aput(self, messages: List[ChatMessage]) -> None:
        """No-op for static blocks as they don't change."""
        pass


class SummarizeMemoryBlock(BaseMemoryBlock):
    """A memory block that summarizes conversation history using an LLM.
    
    This block incrementally updates a summary of the conversation,
    focusing on key information that might be useful long-term.
    """
    
    llm: LLM = Field(
        description="The LLM to use for summarization."
    )
    current_summary: str = Field(
        default="",
        description="The current summary of the conversation."
    )
    max_summary_length: int = Field(
        default=500,
        description="Maximum length of the summary in characters."
    )
    focus_on_recent: bool = Field(
        default=True,
        description="Whether to focus more on recent messages."
    )
    summary_prompt_template: str = Field(
        default="""You are a helpful assistant that creates concise summaries of conversations.

INSTRUCTIONS:
1. Review the current summary and new conversation
2. Create a new summary that integrates important information
3. Focus on key facts, user preferences, and context that may be useful later
4. Be concise and well-organized
5. Limit your summary to {max_length} characters

<current_summary>
{current_summary}
</current_summary>

<new_conversation>
{conversation}
</new_conversation>

New summary:""",
        description="Template for the summarization prompt."
    )

    async def aget(self, input: Optional[List[ChatMessage]] = None, **kwargs: Any) -> str:
        """Return the current summary."""
        if self.current_summary:
            return self.current_summary
        return ""

    async def aput(self, messages: List[ChatMessage]) -> None:
        """Update the summary with new messages."""
        # Skip if no messages
        if not messages:
            return
            
        # Format conversation for summarization
        conversation = "\n".join([
            f"{message.role}: {message.content}" for message in messages
        ])
        
        # Create the prompt
        prompt = self.summary_prompt_template.format(
            current_summary=self.current_summary or "No previous summary available.",
            conversation=conversation,
            max_length=self.max_summary_length
        )
        
        # Get the summary
        summary_message = ChatMessage(role="user", content=prompt)
        response = await self.llm.achat(messages=[summary_message])
        
        # Update the summary
        new_summary = response.message.content
        
        # Enforce length limit
        if len(new_summary) > self.max_summary_length:
            new_summary = new_summary[:self.max_summary_length] + "..."
            
        self.current_summary = new_summary

    async def atruncate(self, content: Union[List[ContentBlock], List[ChatMessage]]) -> Union[List[ContentBlock], List[ChatMessage]]:
        """If needed, reduce the size of the summary."""
        # For a simple truncation, just cut the summary in half
        if self.current_summary:
            self.current_summary = self.current_summary[:len(self.current_summary)//2] + "..."
            
        # Return what was passed in, as our state is stored internally
        return content


class RetrievalMemoryBlock(BaseMemoryBlock):
    """A memory block that retrieves relevant information from a vector store.
    
    This block stores conversation history in a vector store and retrieves
    relevant information based on the most recent messages.
    """
    
    vector_store: BasePydanticVectorStore = Field(
        description="The vector store to use for retrieval."
    )
    embed_model: BaseEmbedding = Field(
        description="The embedding model to use for encoding queries and documents."
    )
    similarity_top_k: int = Field(
        default=3,
        description="Number of top results to return."
    )
    relevance_threshold: Optional[float] = Field(
        default=None,
        description="Optional threshold for relevance scores (0-1). If set, only results above this threshold are included."
    )
    context_window: int = Field(
        default=5,
        description="Number of messages to include for context when retrieving."
    )
    format_template: str = Field(
        default="RELEVANT MEMORY:\n{text}",
        description="Template for formatting the retrieved information."
    )
    metadata_filter: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional filter to apply to metadata when retrieving."
    )

    async def aget(self, input: Optional[List[ChatMessage]] = None, **kwargs: Any) -> str:
        """Retrieve relevant information based on recent messages."""
        if not input or len(input) == 0:
            return ""
        
        # Use the last message or a context window of messages for the query
        if self.context_window > 1 and len(input) >= self.context_window:
            context = input[-self.context_window:]
            query_text = " ".join([msg.content for msg in context if msg.content])
        else:
            query_text = input[-1].content if input[-1].content else ""
            
        if not query_text:
            return ""
        
        # Create and execute the query
        query_embedding = await self.embed_model.aget_query_embedding(query_text)
        query = VectorStoreQuery(
            query_str=query_text,
            query_embedding=query_embedding,
            similarity_top_k=self.similarity_top_k,
            filters=self.metadata_filter,
        )
        
        results = await self.vector_store.aquery(query)
        
        if not results.nodes:
            return ""
        
        # Filter by relevance if threshold is set
        if self.relevance_threshold is not None:
            filtered_nodes = [
                node for i, node in enumerate(results.nodes)
                if results.similarities and results.similarities[i] >= self.relevance_threshold
            ]
            if not filtered_nodes:
                return ""
            nodes = filtered_nodes
        else:
            nodes = results.nodes
        
        # Format the results
        retrieved_text = "\n\n".join([node.get_content() for node in nodes])
        formatted_text = self.format_template.format(text=retrieved_text)
        
        return formatted_text

    async def aput(self, messages: List[ChatMessage]) -> None:
        """Store messages in the vector store for future retrieval."""
        if not messages:
            return
            
        # Format messages with role and content
        texts = []
        metadatas = []
        
        for message in messages:
            content = message.content if message.content else ""
            if not content:
                continue
                
            text = f"{message.role}: {content}"
            texts.append(text)
            
            # Store additional metadata
            metadata = {"role": message.role}
            if message.additional_kwargs:
                for key, value in message.additional_kwargs.items():
                    if isinstance(value, (str, int, float, bool)):
                        metadata[key] = value
            
            metadatas.append(metadata)
        
        if not texts:
            return
            
        # Get embeddings
        node_embeddings = await self.embed_model.aget_text_embedding_batch(texts)
        
        # Create nodes with metadata
        nodes = [
            TextNode(text=text, embedding=embedding, metadata=metadata)
            for text, embedding, metadata in zip(texts, node_embeddings, metadatas)
        ]
        
        # Add to vector store
        await self.vector_store.async_add(nodes)

    async def atruncate(self, content: Union[List[ContentBlock], List[ChatMessage]]) -> Union[List[ContentBlock], List[ChatMessage]]:
        """Reduce the number of retrieved items if needed."""
        # Simply reduce the number of results we'll return next time
        self.similarity_top_k = max(1, self.similarity_top_k // 2)
        
        # Return what was passed in, as our state is stored internally
        return content
