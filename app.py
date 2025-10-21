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

# Custom CSS for dark theme
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #0f172a;
    }
    .stTextArea textarea {
        font-size: 16px;
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border-color: #334155 !important;
    }
    .response-box {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        border: 1px solid #334155;
        color: #f1f5f9;
    }
    .error-box {
        background-color: #7f1d1d;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc2626;
        margin-top: 1rem;
        color: #fecaca;
    }
    .stButton>button {
        background: linear-gradient(90deg, #8b5cf6 0%, #6366f1 100%);
        color: white;
        border: none;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #7c3aed 0%, #4f46e5 100%);
    }
    h1, h2, h3 {
        color: #f1f5f9 !important;
    }
    .stSelectbox label, .stTextArea label {
        color: #cbd5e1 !important;
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

# Models - Only verified working serverless models from Together AI
MODELS = [
    {"value": "moonshotai/Kimi-K2-Instruct-0905", "label": "Kimi K2 Instruct 0905"},
    {"value": "deepseek-ai/DeepSeek-V3.1", "label": "DeepSeek V3.1"},
    {"value": "openai/gpt-oss-120b", "label": "OpenAI GPT-OSS 120B"},
    {"value": "openai/gpt-oss-20b", "label": "OpenAI GPT-OSS 20B"},
    {"value": "moonshotai/Kimi-K2-Instruct", "label": "Kimi K2 Instruct"},
    {"value": "zai-org/GLM-4.5-Air-FP8", "label": "GLM 4.5 Air"},
    {"value": "Qwen/Qwen3-235B-A22B-Thinking-2507", "label": "Qwen3 235B Thinking"},
    {"value": "Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8", "label": "Qwen3 Coder 480B"},
    {"value": "Qwen/Qwen3-235B-A22B-Instruct-2507-tput", "label": "Qwen3 235B Instruct"},
    {"value": "Qwen/Qwen3-Next-80B-A3B-Instruct", "label": "Qwen3 Next 80B Instruct"},
    {"value": "Qwen/Qwen3-Next-80B-A3B-Thinking", "label": "Qwen3 Next 80B Thinking"},
    {"value": "deepseek-ai/DeepSeek-R1", "label": "DeepSeek R1"},
    {"value": "deepseek-ai/DeepSeek-R1-0528-tput", "label": "DeepSeek R1 Throughput"},
    {"value": "deepseek-ai/DeepSeek-V3", "label": "DeepSeek V3"},
    {"value": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8", "label": "Llama 4 Maverick"},
    {"value": "meta-llama/Llama-4-Scout-17B-16E-Instruct", "label": "Llama 4 Scout"},
    {"value": "meta-llama/Llama-3.3-70B-Instruct-Turbo", "label": "Llama 3.3 70B Turbo"},
    {"value": "deepcogito/cogito-v2-preview-llama-70B", "label": "Cogito v2 Preview 70B"},
    {"value": "deepcogito/cogito-v2-preview-llama-109B-MoE", "label": "Cogito v2 Preview 109B MoE"},
    {"value": "deepcogito/cogito-v2-preview-llama-405B", "label": "Cogito v2 Preview 405B"},
    {"value": "deepcogito/cogito-v2-preview-deepseek-671b", "label": "Cogito v2 Preview 671B"},
    {"value": "mistralai/Magistral-Small-2506", "label": "Magistral Small 2506"},
    {"value": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B", "label": "DeepSeek R1 Distill Llama 70B"},
    {"value": "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B", "label": "DeepSeek R1 Distill Qwen 14B"},
    {"value": "marin-community/marin-8b-instruct", "label": "Marin 8B Instruct"},
    {"value": "mistralai/Mistral-Small-24B-Instruct-2501", "label": "Mistral Small 24B"},
    {"value": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", "label": "Llama 3.1 8B Turbo"},
    {"value": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", "label": "Llama 3.3 70B Turbo (Free)"},
    {"value": "Qwen/Qwen2.5-7B-Instruct-Turbo", "label": "Qwen 2.5 7B Turbo"},
    {"value": "Qwen/Qwen2.5-72B-Instruct-Turbo", "label": "Qwen 2.5 72B Turbo"},
    {"value": "Qwen/Qwen2.5-VL-72B-Instruct", "label": "Qwen 2.5 VL 72B"},
    {"value": "Qwen/Qwen2.5-Coder-32B-Instruct", "label": "Qwen 2.5 Coder 32B"},
    {"value": "Qwen/QwQ-32B", "label": "QwQ 32B"},
    {"value": "Qwen/Qwen3-235B-A22B-fp8-tput", "label": "Qwen3 235B Throughput"},
    {"value": "arcee-ai/virtuoso-medium-v2", "label": "Arcee Virtuoso Medium"},
    {"value": "arcee-ai/coder-large", "label": "Arcee Coder Large"},
    {"value": "arcee-ai/virtuoso-large", "label": "Arcee Virtuoso Large"},
    {"value": "arcee-ai/maestro-reasoning", "label": "Arcee Maestro"},
    {"value": "arcee-ai/caller", "label": "Arcee Caller"},
    {"value": "arcee-ai/arcee-blitz", "label": "Arcee Blitz"},
    {"value": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo", "label": "Llama 3.1 405B Turbo"},
    {"value": "meta-llama/Llama-3.2-3B-Instruct-Turbo", "label": "Llama 3.2 3B Turbo"},
    {"value": "meta-llama/Meta-Llama-3-8B-Instruct-Lite", "label": "Llama 3 8B Lite"},
    {"value": "meta-llama/Llama-3-70b-chat-hf", "label": "Llama 3 70B Reference"},
    {"value": "google/gemma-2b-it", "label": "Gemma 2B Instruct"},
    {"value": "google/gemma-3n-E4B-it", "label": "Gemma 3N E4B"},
    {"value": "Gryphe/MythoMax-L2-13b", "label": "MythoMax L2 13B"},
    {"value": "mistralai/Mistral-7B-Instruct-v0.1", "label": "Mistral 7B v0.1"},
    {"value": "mistralai/Mistral-7B-Instruct-v0.2", "label": "Mistral 7B v0.2"},
    {"value": "mistralai/Mistral-7B-Instruct-v0.3", "label": "Mistral 7B v0.3"},
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
    model_labels = ["Default (Llama 3.3 70B Turbo)"] + [m["label"] for m in MODELS]
    selected_model_label = st.selectbox(
        "Select Model",
        model_labels,
        help="Choose an AI model"
    )
    
    if selected_model_label == "Default (Llama 3.3 70B Turbo)":
        selected_model = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
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
                
                elif response.status_code == 404:
                    error_msg = response.json().get("error", {}).get("message", "Model not found")
                    st.markdown(f'<div class="error-box">❌ <strong>Model Not Found:</strong> {error_msg}<br/>This model may not be available. Try using the default model.</div>', unsafe_allow_html=True)
                
                elif response.status_code == 429:
                    st.markdown('<div class="error-box">⏳ <strong>Rate Limit:</strong> You have exceeded the rate limit. Please try again later.</div>', unsafe_allow_html=True)
                
                elif response.status_code == 503:
                    st.markdown('<div class="error-box">🔧 <strong>Service Unavailable:</strong> Together AI service is temporarily unavailable. Please try again in a moment.</div>', unsafe_allow_html=True)
                
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
    <div style='text-align: center; color: #94a3b8; padding: 1rem;'>
        <p>Powered by <strong>Together AI</strong> | Built with <strong>Streamlit</strong></p>
        <p style='font-size: 0.8rem;'>Get your API key at <a href='https://api.together.xyz' target='_blank' style='color: #8b5cf6;'>api.together.xyz</a></p>
    </div>
""", unsafe_allow_html=True)

