# ChatBot-QwenAgent

A powerful AI chatbot system built with Qwen Agent framework, featuring RAG (Retrieval-Augmented Generation) capabilities and multiple integrated tools.

## Features

- 🤖 Powered by Qwen Agent framework
- 🔍 RAG (Retrieval-Augmented Generation) system for knowledge-based responses
- 🛠️ Multiple integrated tools:
  - Image generation
  - MySQL database querying
  - Code interpretation
  - Knowledge base management
- ⚡ MCP (Model Control Protocol) Services:
  - Real-time time service with timezone support
  - Server-Sent Events (SSE) for live data streaming
- 🌐 FastAPI-based RAG service
- 📚 Vector-based knowledge storage using FAISS

## Project Structure

```
.
├── assets/              # Static assets
├── docs/               # Documentation
├── knowledge_base/     # Vector store for RAG
├── scripts/           # Utility scripts
├── workspace/         # Working directory
├── client.py          # Main client implementation
└── rag_service.py     # RAG service implementation
```

## Prerequisites

- Python 3.10+
- DashScope API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ChatBot-QwenAgent.git
cd ChatBot-QwenAgent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your environment:
- Set up your DashScope API key
- Configure MySQL database connection in `client.py`

## Usage

1. Start the RAG service:
```bash
python rag_service.py
```
2. Run scripts to add documents to knowledge base
```bash
python scripts/add_document.py docs/我的世界观.txt
```
3. Run the client:
```bash
python client.py
```

## Features in Detail

### RAG Service
- FastAPI-based service for document retrieval
- Uses HuggingFace embeddings for semantic search
- Supports document addition and retrieval
- Configurable chunk size and overlap

### Tools
- **Image Generation**: Generate images from text descriptions
- **MySQL Query**: Execute SQL queries on your database
- **RAG Search**: Search through your knowledge base
- **Knowledge Base Management**: Add and manage documents in your knowledge base
- **MCP Services**:
  - **Time Service**: Real-time time information with timezone support (Asia/Shanghai), enabling accurate time-based operations
  - **Fetch Service**: Advanced Server-Sent Events (SSE) integration for real-time data streaming and live updates

## Configuration

### RAG Service Configuration
- Default port: 8000
- Embedding model: shibing624/text2vec-base-chinese
- Chunk size: 500
- Chunk overlap: 50

### Client Configuration
- Model: Qwen3-235b-a22b (DashScope)
- Customizable tools and system instructions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
