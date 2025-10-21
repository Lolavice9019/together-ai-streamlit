# Together AI Chat Interface - Streamlit

A beautiful and user-friendly chat interface powered by Together AI, built with Streamlit.

## Features

- 🤖 **Multiple AI Models**: Access to 80+ Together AI models
- 📝 **Template System**: Pre-configured system prompts for different use cases
- 🎨 **Modern UI**: Clean, responsive interface with custom styling
- ⚡ **Real-time Responses**: Fast API integration with Together AI
- 🔒 **Secure**: API keys stored securely in Streamlit secrets
- 📊 **Request Details**: View model info and token usage

## Available Templates

1. **Default Assistant** - General-purpose helpful assistant
2. **Creative Writer** - Craft engaging stories and narratives
3. **Technical Expert** - Detailed explanations of complex topics
4. **Friendly Teacher** - Simple, easy-to-understand explanations
5. **Business Consultant** - Strategic advice and insights
6. **Code Expert** - Debug, optimize, and explain code

## Available Models

The application includes 80+ models from Together AI, including:

- Meta Llama 3.1/3.3 (70B, 405B)
- DeepSeek R1 and V3
- Qwen 2.5 and Qwen3 series
- Mistral and Mixtral models
- And many more...

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd together-ai-streamlit
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.streamlit/secrets.toml` and add your API key:
```toml
TOGETHER_API_KEY = "your-api-key-here"
```

4. Run the application:
```bash
streamlit run app.py
```

5. Open your browser to `http://localhost:8501`

## Deployment to Streamlit Cloud

1. Push your code to GitHub (make sure `.streamlit/secrets.toml` is in `.gitignore`)

2. Go to [share.streamlit.io](https://share.streamlit.io)

3. Click "New app" and select your repository

4. Set the main file path to `app.py`

5. Add your secrets in the Streamlit Cloud dashboard:
   - Go to App settings → Secrets
   - Add: `TOGETHER_API_KEY = "your-api-key-here"`

6. Click "Deploy"!

## Usage

1. **Enter API Key**: Add your Together AI API key in the sidebar (or configure in secrets)

2. **Select Template**: Choose a system prompt template that fits your use case

3. **Select Model**: Pick from 80+ available AI models (or use the default)

4. **Enter Prompt**: Type your question or prompt in the text area

5. **Send**: Click the "Send" button to get your response

6. **View Response**: The AI's response will appear below with formatting

## Configuration

### Customizing Templates

Edit the `TEMPLATES` list in `app.py`:

```python
TEMPLATES = [
    {"value": "Your system prompt here", "label": "Template Name"},
    # Add more templates...
]
```

### Adding/Removing Models

Edit the `MODELS` list in `app.py`:

```python
MODELS = [
    {"value": "model-id", "label": "Model Display Name"},
    # Add more models...
]
```

### Changing Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#6366f1"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

## API Reference

The application uses the Together AI Chat Completions API:

**Endpoint**: `https://api.together.xyz/v1/chat/completions`

**Request Format**:
```json
{
  "model": "model-id",
  "messages": [
    {"role": "system", "content": "system prompt"},
    {"role": "user", "content": "user prompt"}
  ]
}
```

**Headers**:
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

## Error Handling

The application handles various error scenarios:

- **401**: Invalid API key
- **400**: Bad request (invalid model or format)
- **429**: Rate limit exceeded
- **Timeout**: Request took too long
- **Connection Error**: Network issues

## Getting Your API Key

1. Visit [api.together.xyz](https://api.together.xyz)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and use in the application

## Project Structure

```
together-ai-streamlit/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   └── secrets.toml           # API keys (not in git)
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

## Troubleshooting

### API Key Issues
- Ensure your API key is valid and active
- Check that it's properly set in secrets or sidebar
- Verify you have sufficient credits

### Model Not Found
- Some models may require special access
- Try using the default model first
- Check the Together AI documentation for model availability

### Connection Errors
- Check your internet connection
- Verify Together AI service status
- Try again after a few moments

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this project for any purpose.

## Credits

- **Together AI** - AI model provider
- **Streamlit** - Web framework
- Built with ❤️ for the AI community

## Support

For issues with:
- **This application**: Open a GitHub issue
- **Together AI API**: Visit [Together AI Documentation](https://docs.together.ai)
- **Streamlit**: Visit [Streamlit Documentation](https://docs.streamlit.io)

