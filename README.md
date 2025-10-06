# Agentic Gmail (MCP + Gmail API)

A small MVP that
1) Takes a natural language request
2) Extracts the intent using an LLM agent
3) Calls an MCP server tool to send email via Gmail

### Running the MCP server
python -m venv venv<br />
.\venv\Scripts\activate<br />
pip install -r requirements.txt

#### Authorize once and create a token
python -m src.mcp_server.gmail_auth