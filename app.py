import streamlit as st
import requests
import os

# Page configuration
st.set_page_config(
    page_title="Together AI Chat Interface",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .response-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    .error-box {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f44336;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Templates
TEMPLATES = [
    {"value": "You are a helpful assistant.", "label": "Default Assistant"},
    {"value": "You are a creative writer who helps craft engaging stories and narratives.", "label": "Creative Writer"},
    {"value": "You are a technical expert who provides detailed, accurate explanations of complex topics.", "label": "Technical Expert"},
    {"value": "You are a friendly teacher who explains concepts in simple, easy-to-understand terms.", "label": "Friendly Teacher"},
    {"value": "You are a professional business consultant who provides strategic advice and insights.", "label": "Business Consultant"},
    {"value": "You are a code expert who helps debug, optimize, and explain programming concepts.", "label": "Code Expert"},
]

# Models - comprehensive list from Together AI
MODELS = [
    {"value": "meta-llama/Llama-Guard-3-11B-Vision-Turbo", "label": "Llama Guard 4 12B"},
    {"value": "openai/gpt-oss-20b", "label": "OpenAI GPT-OSS 20B"},
    {"value": "moonshot/kimi-k2-instruct-0905", "label": "Kimi K2‑Instruct 0905"},
    {"value": "Qwen/Qwen3-Next-80B-A3b-Instruct", "label": "Qwen3 Next 80B A3b Instruct"},
    {"value": "Qwen/Qwen3-Next-80B-A3b-Thinking", "label": "Qwen3 Next 80B A3b Thinking"},
    {"value": "Qwen/Qwen3-235B-A22B-Thinking-2507-FP8", "label": "Qwen3 235B A22B Thinking 2507 FP8"},
    {"value": "Qwen/Qwen3-Coder-480B-A35B-Instruct-Fp8", "label": "Qwen3 Coder 480B A35B Instruct Fp8"},
    {"value": "deepseek-ai/DeepSeek-R1-0528", "label": "DeepSeek R1‑0528"},
    {"value": "moonshot/kimi-k2-instruct", "label": "Kimi K2 Instruct"},
    {"value": "deepseek-ai/DeepSeek-V3-0324", "label": "DeepSeek V3‑0324"},
    {"value": "Qwen/Qwen3-235B-A22B-Instruct-2507-FP8-Throughput", "label": "Qwen3 235B A22B Instruct 2507 FP8 Throughput"},
    {"value": "meta-llama/Llama-4-Maverick-Instruct-17Bx128E", "label": "Llama 4 Maverick Instruct (17Bx128E)"},
    {"value": "google/gemma-3n-e4b-instruct", "label": "Gemma 3N E4B Instruct"},
    {"value": "meta-llama/Meta-Llama-3.3-70B-Instruct-Turbo", "label": "Meta Llama 3.3 70B Instruct Turbo"},
    {"value": "zhipu/glm-4.5-air-fp8", "label": "Glm 4.5 Air Fp8"},
    {"value": "meta-llama/Meta-Llama-3.3-70B-Instruct-Turbo-Free", "label": "Meta Llama 3.3 70B Instruct Turbo Free"},
    {"value": "mistralai/Mixtral-8x7B-Instruct-v0.1", "label": "Mixtral‑8x7B Instruct v0.1"},
    {"value": "mistralai/Mistral-7B-Instruct-v0.1", "label": "Mistral (7B) Instruct v0.1"},
    {"value": "Qwen/Qwen2.5-VL-72B-Instruct", "label": "Qwen2.5‑VL (72B) Instruct"},
    {"value": "meta-llama/Llama-4-Scout-Instruct-17Bx16E", "label": "Llama 4 Scout Instruct (17Bx16E)"},
    {"value": "marin/marin-8b-instruct", "label": "Marin 8B Instruct"},
    {"value": "intfloat/multilingual-e5-large-instruct", "label": "Multilingual E5 Large Instruct"},
    {"value": "deepseek-ai/DeepSeek-R1-0528-Throughput", "label": "DeepSeek R1 0528 Throughput"},
    {"value": "answerdotai/gte-modernbert-base", "label": "Gte Modernbert Base"},
    {"value": "refuel-ai/Refuel-LLM-V2-Small", "label": "Refuel LLM V2 Small"},
    {"value": "refuel-ai/Refuel-LLM-V2", "label": "Refuel LLM V2"},
    {"value": "mistralai/Mistral-Small-24B-Instruct-25.01", "label": "Mistral Small (24B) Instruct 25.01"},
    {"value": "Qwen/QwQ-32B", "label": "Qwen QwQ‑32B"},
    {"value": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B", "label": "DeepSeek R1 Distill Llama 70B"},
    {"value": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B", "label": "DeepSeek R1 Distill Qwen 14B"},
    {"value": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-Free", "label": "DeepSeek R1 Distill Llama 70B Free"},
    {"value": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo", "label": "Meta Llama 3.1 405B Instruct Turbo"},
    {"value": "Qwen/Qwen3-235B-A22B-FP8-Throughput", "label": "Qwen3 235B A22B FP8 Throughput"},
    {"value": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo", "label": "Meta Llama 3.1 70B Instruct Turbo"},
    {"value": "Qwen/Qwen2.5-72B-Instruct-Turbo", "label": "Qwen2.5 72B Instruct Turbo"},
    {"value": "Qwen/Qwen2.5-7B-Instruct-Turbo", "label": "Qwen2.5 7B Instruct Turbo"},
    {"value": "meta-llama/Meta-Llama-3.2-3B-Instruct-Turbo", "label": "Meta Llama 3.2 3B Instruct Turbo"},
    {"value": "meta-llama/Meta-Llama-Guard-3-11B-Vision-Turbo", "label": "Meta Llama Guard 3 11B Vision Turbo"},
    {"value": "salesforce/llama-rank-v1-8b", "label": "Salesforce Llama Rank V1 (8B)"},
    {"value": "meta-llama/Meta-Llama-Guard-3-8B", "label": "Meta Llama Guard 3 8B"},
    {"value": "meta-llama/Meta-Llama-3-70B-Instruct-Turbo", "label": "Meta Llama 3 70B Instruct Turbo"},
    {"value": "meta-llama/Meta-Llama-3-8B-Instruct-Lite", "label": "Meta Llama 3 8B Instruct Lite"},
    {"value": "meta-llama/Meta-Llama-3-70B-Instruct-Reference", "label": "Meta Llama 3 70B Instruct Reference"},
    {"value": "mistralai/Mistral-7B-Instruct-v0.3", "label": "Mistral (7B) Instruct v0.3"},
    {"value": "meta-llama/Meta-Llama-Guard-2-8B", "label": "Meta Llama Guard 2 8B"},
    {"value": "meta-llama/Llama-2-70b-hf", "label": "LLaMA‑2 (70B)"},
    {"value": "arcee-ai/arcee-virtuoso-large", "label": "Arcee AI Virtuoso‑Large"},
    {"value": "arcee-ai/arcee-coder-large", "label": "Arcee AI Coder‑Large"},
    {"value": "arcee-ai/arcee-maestro", "label": "Arcee AI Maestro"},
    {"value": "scb10x/typhoon-2.1-12b", "label": "Typhoon 2.1 12B"},
    {"value": "mixedbread-ai/mxbai-rerank-large-v2", "label": "Mxbai Rerank Large V2"},
    {"value": "openai/whisper-large-v3", "label": "Whisper large‑v3"},
    {"value": "virtueguard/virtueguard-text-lite", "label": "Virtueguard Text Lite"},
    {"value": "deepcogito/cogito-v2-preview-deepseek-671b-moe", "label": "Cogito V2 Preview Deepseek 671B MoE"},
    {"value": "deepcogito/cogito-v2-preview-llama-109b-moe", "label": "Cogito V2 Preview Llama 109B MoE"},
    {"value": "arize-ai/Qwen2-1.5B-Instruct", "label": "Arize AI Qwen 2 1.5B Instruct"},
    {"value": "jinaai/m2-bert-retrieval-32k", "label": "M2‑BERT‑Retrieval‑32k"},
    {"value": "deepcogito/cogito-v2-preview-llama-70b", "label": "Deepcogito Cogito V2 Preview Llama 70B"},
    {"value": "deepcogito/cogito-v2-preview-llama-405b", "label": "Deepcogito Cogito V2 Preview Llama 405B"},
    {"value": "arcee-ai/arcee-afm-4.5b", "label": "Arcee AI AFM 4.5B"},
    {"value": "Qwen/Qwen2.5-Coder-32B-Instruct", "label": "Qwen 2.5 Coder 32B Instruct"},
    {"value": "openai/gpt-oss-120b", "label": "OpenAI GPT‑OSS 120B"},
    {"value": "jinaai/m2-bert-retrieval-2k", "label": "M2‑BERT‑Retrieval‑2K"},
    {"value": "jinaai/m2-bert-retrieval-8k", "label": "M2‑BERT‑Retrieval‑8k"},
    {"value": "whiterabbitneo/uae-large-v1", "label": "UAE‑Large‑V1"},
    {"value": "meta-llama/Llama-Guard-7b", "label": "Llama Guard (7B)"},
    {"value": "codellama/CodeLlama-34b-Instruct-hf", "label": "Code Llama Instruct (34B)"},
    {"value": "BAAI/bge-large-en-v1.5", "label": "BAAI‑Bge‑Large‑1.5"},
    {"value": "nvidia/Nemotron-Nano-9B-v2", "label": "Nvidia Nemotron Nano 9B V2"},
    {"value": "apriel/apriel-1.5-15b-thinker", "label": "Apriel 1.5 15B Thinker"},
    {"value": "deepseek-ai/DeepSeek-V3.1", "label": "Deepseek V3.1"},
    {"value": "meta-llama/Llama-2-13b-chat-hf", "label": "LLaMA‑2 Chat (13B)"},
    {"value": "deepseek-ai/deepseek-llm-67b-chat", "label": "DeepSeek LLM Chat (67B)"},
    {"value": "meta-llama/Meta-Llama-3-70B-Instruct-Lite", "label": "Meta Llama 3 70B Instruct Lite"},
    {"value": "upstage/SOLAR-10.7B-Instruct-v1.0", "label": "Upstage SOLAR Instruct v1 (11B)"},
    {"value": "BAAI/bge-base-en-v1.5", "label": "BAAI‑Bge‑Base‑1.5"},
]

# Title and description
st.title("🤖 Together AI Chat Interface")
st.markdown("Interact with powerful AI models powered by **Together AI**")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input
    api_key = st.text_input(
        "Together AI API Key",
        type="password",
        value=os.getenv("TOGETHER_API_KEY", ""),
        help="Enter your Together AI API key. You can get one from https://api.together.xyz"
    )
    
    st.divider()
    
    # Template selection
    template_labels = [t["label"] for t in TEMPLATES]
    selected_template_label = st.selectbox(
        "Select Template",
        template_labels,
        help="Choose a system prompt template"
    )
    selected_template = next(t["value"] for t in TEMPLATES if t["label"] == selected_template_label)
    
    st.divider()
    
    # Model selection
    model_labels = ["Default (Meta Llama 3.1 70B Instruct Turbo)"] + [m["label"] for m in MODELS]
    selected_model_label = st.selectbox(
        "Select Model",
        model_labels,
        help="Choose an AI model"
    )
    
    if selected_model_label == "Default (Meta Llama 3.1 70B Instruct Turbo)":
        selected_model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    else:
        selected_model = next(m["value"] for m in MODELS if m["label"] == selected_model_label)
    
    st.divider()
    st.caption("💡 Tip: Select different templates and models to get varied responses!")

# Main content area
prompt = st.text_area(
    "Enter your prompt:",
    height=150,
    placeholder="Type your question or prompt here...",
    help="Enter the text you want the AI to respond to"
)

# Submit button
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    submit_button = st.button("🚀 Send", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

if clear_button:
    st.rerun()

# Process the request
if submit_button:
    if not api_key:
        st.error("⚠️ Please enter your Together AI API key in the sidebar!")
    elif not prompt.strip():
        st.error("⚠️ Please enter a prompt!")
    else:
        with st.spinner("🤔 Thinking..."):
            try:
                # Build messages
                messages = [
                    {"role": "system", "content": selected_template},
                    {"role": "user", "content": prompt}
                ]
                
                # Make API request
                response = requests.post(
                    "https://api.together.xyz/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": selected_model,
                        "messages": messages
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["choices"][0]["message"]["content"]
                    
                    st.success("✅ Response received!")
                    st.markdown("### 💬 Response:")
                    st.markdown(f'<div class="response-box">{answer}</div>', unsafe_allow_html=True)
                    
                    # Show model info
                    with st.expander("ℹ️ Request Details"):
                        st.write(f"**Model:** {selected_model}")
                        st.write(f"**Template:** {selected_template_label}")
                        if "usage" in data:
                            st.write(f"**Tokens Used:** {data['usage'].get('total_tokens', 'N/A')}")
                
                elif response.status_code == 401:
                    st.markdown('<div class="error-box">❌ <strong>Authentication Error:</strong> Invalid API key. Please check your Together AI API key.</div>', unsafe_allow_html=True)
                
                elif response.status_code == 400:
                    error_msg = response.json().get("error", {}).get("message", "Bad request")
                    st.markdown(f'<div class="error-box">❌ <strong>Bad Request:</strong> {error_msg}<br/>The model might not be recognized or the request format is invalid.</div>', unsafe_allow_html=True)
                
                elif response.status_code == 429:
                    st.markdown('<div class="error-box">⏳ <strong>Rate Limit:</strong> You have exceeded the rate limit. Please try again later.</div>', unsafe_allow_html=True)
                
                else:
                    error_msg = response.json().get("error", {}).get("message", "Unknown error")
                    st.markdown(f'<div class="error-box">❌ <strong>Error {response.status_code}:</strong> {error_msg}</div>', unsafe_allow_html=True)
                    
            except requests.exceptions.Timeout:
                st.markdown('<div class="error-box">⏱️ <strong>Timeout:</strong> The request took too long. Please try again.</div>', unsafe_allow_html=True)
            
            except requests.exceptions.RequestException as e:
                st.markdown(f'<div class="error-box">🔌 <strong>Connection Error:</strong> Failed to connect to Together AI. Please check your internet connection.<br/>{str(e)}</div>', unsafe_allow_html=True)
            
            except Exception as e:
                st.markdown(f'<div class="error-box">❌ <strong>Unexpected Error:</strong> {str(e)}</div>', unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Powered by <strong>Together AI</strong> | Built with <strong>Streamlit</strong></p>
        <p style='font-size: 0.8rem;'>Get your API key at <a href='https://api.together.xyz' target='_blank'>api.together.xyz</a></p>
    </div>
""", unsafe_allow_html=True)

