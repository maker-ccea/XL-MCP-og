export type ProviderID =
  | 'openai'
  | 'anthropic'
  | 'google'
  | 'openrouter'
  | 'mistral'
  | 'groq'
  | 'cohere'
  | 'ollama'
  | 'together'
  | 'perplexity'
  | 'custom'

export type ApiFormat = 'openai' | 'anthropic' | 'google'

export interface ProviderModel {
  id: string
  name: string
  contextLength: number
  description: string
  recommended?: boolean
}

export interface ProviderDefinition {
  id: ProviderID
  name: string
  tagline: string
  baseUrl: string
  apiFormat: ApiFormat
  apiKeyPlaceholder: string
  apiKeyLink: string
  abbr: string
  color: string       
  textColor: string   
  badgeColor: string  
  models: ProviderModel[]
  supportsCustomBaseUrl: boolean
  customBaseUrlLabel?: string
  requiresNoKey?: boolean
}

export const PROVIDERS: ProviderDefinition[] = [
  {
    id: 'openai',
    name: 'OpenAI',
    tagline: 'GPT-4o, GPT-4 Turbo and more',
    baseUrl: 'https://api.openai.com/v1',
    apiFormat: 'openai',
    apiKeyPlaceholder: 'sk-...',
    apiKeyLink: 'https://platform.openai.com/api-keys',
    abbr: 'OA',
    color: 'bg-emerald-100',
    textColor: 'text-emerald-700',
    badgeColor: 'bg-emerald-500',
    supportsCustomBaseUrl: false,
    models: [
      { id: 'gpt-4o',            name: 'GPT-4o',            contextLength: 128000, description: 'Most capable multimodal model', recommended: true },
      { id: 'gpt-4o-mini',       name: 'GPT-4o Mini',       contextLength: 128000, description: 'Fast and affordable' },
      { id: 'gpt-4-turbo',       name: 'GPT-4 Turbo',       contextLength: 128000, description: 'Previous generation GPT-4' },
      { id: 'gpt-3.5-turbo',     name: 'GPT-3.5 Turbo',     contextLength: 16385,  description: 'Fast and cost-effective' }
    ]
  },
  {
    id: 'anthropic',
    name: 'Anthropic',
    tagline: 'Claude 3.5 Sonnet, Opus and Haiku',
    baseUrl: 'https://api.anthropic.com/v1',
    apiFormat: 'anthropic',
    apiKeyPlaceholder: 'sk-ant-...',
    apiKeyLink: 'https://console.anthropic.com/keys',
    abbr: 'An',
    color: 'bg-orange-100',
    textColor: 'text-orange-700',
    badgeColor: 'bg-orange-500',
    supportsCustomBaseUrl: false,
    models: [
      { id: 'claude-3-5-sonnet-20241022', name: 'Claude 3.5 Sonnet', contextLength: 200000, description: 'Best balance of speed and intelligence', recommended: true },
      { id: 'claude-3-5-haiku-20241022',  name: 'Claude 3.5 Haiku',  contextLength: 200000, description: 'Fastest Claude model' },
      { id: 'claude-3-opus-20240229',     name: 'Claude 3 Opus',     contextLength: 200000, description: 'Most powerful for complex tasks' },
      { id: 'claude-3-haiku-20240307',    name: 'Claude 3 Haiku',    contextLength: 200000, description: 'Compact and efficient' }
    ]
  },
  {
    id: 'google',
    name: 'Google',
    tagline: 'Gemini 1.5 Pro and Flash',
    baseUrl: 'https://generativelanguage.googleapis.com/v1beta',
    apiFormat: 'google',
    apiKeyPlaceholder: 'AIza...',
    apiKeyLink: 'https://aistudio.google.com/app/apikey',
    abbr: 'Gg',
    color: 'bg-sky-100',
    textColor: 'text-sky-700',
    badgeColor: 'bg-sky-500',
    supportsCustomBaseUrl: false,
    models: [
      { id: 'gemini-1.5-pro-latest',   name: 'Gemini 1.5 Pro',   contextLength: 2000000, description: 'Best quality with 2M context',  recommended: true },
      { id: 'gemini-1.5-flash-latest', name: 'Gemini 1.5 Flash', contextLength: 1000000, description: 'Fast with 1M context window' },
      { id: 'gemini-2.0-flash-exp',    name: 'Gemini 2.0 Flash', contextLength: 1000000, description: 'Next-gen speed and quality' }
    ]
  },
  {
    id: 'openrouter',
    name: 'OpenRouter',
    tagline: 'Access 100+ models via one API',
    baseUrl: 'https://openrouter.ai/api/v1',
    apiFormat: 'openai',
    apiKeyPlaceholder: 'sk-or-...',
    apiKeyLink: 'https://openrouter.ai/keys',
    abbr: 'OR',
    color: 'bg-violet-100',
    textColor: 'text-violet-700',
    badgeColor: 'bg-violet-500',
    supportsCustomBaseUrl: false,
    models: [
      { id: 'anthropic/claude-3.5-sonnet',      name: 'Claude 3.5 Sonnet',     contextLength: 200000, description: 'Via OpenRouter',          recommended: true },
      { id: 'openai/gpt-4o',                    name: 'GPT-4o',                contextLength: 128000, description: 'Via OpenRouter' },
      { id: 'google/gemini-pro-1.5',            name: 'Gemini 1.5 Pro',        contextLength: 2000000,description: 'Via OpenRouter' },
      { id: 'mistralai/mistral-large',          name: 'Mistral Large',         contextLength: 128000, description: 'Via OpenRouter' },
      { id: 'meta-llama/llama-3.3-70b-instruct',name: 'Llama 3.3 70B',         contextLength: 128000, description: 'Via OpenRouter' },
      { id: 'deepseek/deepseek-chat',           name: 'DeepSeek Chat',         contextLength: 64000,  description: 'Via OpenRouter' }
    ]
  },
  {
    id: 'mistral',
    name: 'Mistral',
    tagline: 'Mistral Large, Medium and Small',
    baseUrl: 'https://api.mistral.ai/v1',
    apiFormat: 'openai',
    apiKeyPlaceholder: 'Your Mistral API key',
    apiKeyLink: 'https://console.mistral.ai/api-keys',
    abbr: 'Mi',
    color: 'bg-indigo-100',
    textColor: 'text-indigo-700',
    badgeColor: 'bg-indigo-500',
    supportsCustomBaseUrl: false,
    models: [
      { id: 'mistral-large-latest',  name: 'Mistral Large',   contextLength: 128000, description: 'Top-tier reasoning model', recommended: true },
      { id: 'mistral-small-latest',  name: 'Mistral Small',   contextLength: 128000, description: 'Fast and efficient' },
      { id: 'codestral-latest',      name: 'Codestral',       contextLength: 256000, description: 'Specialized for code' },
      { id: 'open-mistral-nemo',     name: 'Mistral Nemo',    contextLength: 128000, description: 'Compact multilingual model' }
    ]
  },
  {
    id: 'groq',
    name: 'Groq',
    tagline: 'Blazing-fast inference on LPUs',
    baseUrl: 'https://api.groq.com/openai/v1',
    apiFormat: 'openai',
    apiKeyPlaceholder: 'gsk_...',
    apiKeyLink: 'https://console.groq.com/keys',
    abbr: 'Gq',
    color: 'bg-rose-100',
    textColor: 'text-rose-700',
    badgeColor: 'bg-rose-500',
    supportsCustomBaseUrl: false,
    models: [
      { id: 'llama-3.3-70b-versatile',  name: 'Llama 3.3 70B',    contextLength: 128000, description: 'Best quality on Groq',       recommended: true },
      { id: 'llama-3.1-8b-instant',     name: 'Llama 3.1 8B',     contextLength: 128000, description: 'Fastest on Groq' },
      { id: 'mixtral-8x7b-32768',       name: 'Mixtral 8x7B',     contextLength: 32768,  description: 'MoE model on Groq' },
      { id: 'gemma2-9b-it',             name: 'Gemma 2 9B',       contextLength: 8192,   description: 'Google Gemma on Groq' }
    ]
  },
  {
    id: 'cohere',
    name: 'Cohere',
    tagline: 'Command R and R+ for enterprise',
    baseUrl: 'https://api.cohere.com/v2',
    apiFormat: 'openai',
    apiKeyPlaceholder: 'Your Cohere API key',
    apiKeyLink: 'https://dashboard.cohere.com/api-keys',
    abbr: 'Co',
    color: 'bg-teal-100',
    textColor: 'text-teal-700',
    badgeColor: 'bg-teal-500',
    supportsCustomBaseUrl: false,
    models: [
      { id: 'command-r-plus-08-2024', name: 'Command R+', contextLength: 128000, description: 'Most capable Cohere model', recommended: true },
      { id: 'command-r-08-2024',      name: 'Command R',  contextLength: 128000, description: 'Balanced model' },
      { id: 'command-light',          name: 'Command Light', contextLength: 4096, description: 'Fastest Cohere model' }
    ]
  },
  {
    id: 'together',
    name: 'Together AI',
    tagline: 'Open-source models at scale',
    baseUrl: 'https://api.together.xyz/v1',
    apiFormat: 'openai',
    apiKeyPlaceholder: 'Your Together API key',
    apiKeyLink: 'https://api.together.ai/settings/api-keys',
    abbr: 'To',
    color: 'bg-blue-100',
    textColor: 'text-blue-700',
    badgeColor: 'bg-blue-500',
    supportsCustomBaseUrl: false,
    models: [
      { id: 'meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo', name: 'Llama 3.1 70B Turbo', contextLength: 128000, description: 'Best open-source on Together', recommended: true },
      { id: 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo',  name: 'Llama 3.1 8B Turbo',  contextLength: 128000, description: 'Fast and efficient' },
      { id: 'mistralai/Mixtral-8x7B-Instruct-v0.1',         name: 'Mixtral 8x7B',         contextLength: 32768,  description: 'MoE model on Together' },
      { id: 'Qwen/Qwen2.5-72B-Instruct-Turbo',              name: 'Qwen 2.5 72B',         contextLength: 32768,  description: 'Alibaba Qwen on Together' }
    ]
  },
  {
    id: 'perplexity',
    name: 'Perplexity',
    tagline: 'Online models with web search',
    baseUrl: 'https://api.perplexity.ai',
    apiFormat: 'openai',
    apiKeyPlaceholder: 'pplx-...',
    apiKeyLink: 'https://www.perplexity.ai/settings/api',
    abbr: 'Px',
    color: 'bg-cyan-100',
    textColor: 'text-cyan-700',
    badgeColor: 'bg-cyan-500',
    supportsCustomBaseUrl: false,
    models: [
      { id: 'llama-3.1-sonar-large-128k-online', name: 'Sonar Large Online',  contextLength: 127072, description: 'Best with real-time web search', recommended: true },
      { id: 'llama-3.1-sonar-small-128k-online', name: 'Sonar Small Online',  contextLength: 127072, description: 'Fast with web search' },
      { id: 'llama-3.1-sonar-large-128k-chat',   name: 'Sonar Large Chat',    contextLength: 127072, description: 'Offline reasoning' }
    ]
  },
  {
    id: 'ollama',
    name: 'Ollama',
    tagline: 'Run models locally on your machine',
    baseUrl: 'http://localhost:11434/v1',
    apiFormat: 'openai',
    apiKeyPlaceholder: 'ollama (no key required)',
    apiKeyLink: 'https://ollama.com/download',
    abbr: 'Ol',
    color: 'bg-zinc-200',
    textColor: 'text-zinc-600',
    badgeColor: 'bg-zinc-500',
    supportsCustomBaseUrl: true,
    customBaseUrlLabel: 'Ollama server URL',
    requiresNoKey: true,
    models: [
      { id: 'llama3.2',     name: 'Llama 3.2',     contextLength: 128000, description: 'Latest Llama from Meta',    recommended: true },
      { id: 'llama3.1',     name: 'Llama 3.1',     contextLength: 128000, description: 'Previous Llama generation' },
      { id: 'mistral',      name: 'Mistral',        contextLength: 32768,  description: 'Mistral 7B local' },
      { id: 'codellama',    name: 'Code Llama',     contextLength: 100000, description: 'Code-specialized Llama' },
      { id: 'phi3',         name: 'Phi-3',          contextLength: 128000, description: 'Microsoft Phi-3 small' },
      { id: 'gemma2',       name: 'Gemma 2',        contextLength: 8192,   description: 'Google Gemma 2 local' }
    ]
  },
  {
    id: 'custom',
    name: 'Custom OpenAI Compatible',
    tagline: 'Connect to any OpenAI-compatible API endpoint',
    baseUrl: 'https://api.your-provider.com/v1',
    apiFormat: 'openai',
    apiKeyPlaceholder: 'Enter API Key if required...',
    apiKeyLink: '#',
    abbr: 'Cu',
    color: 'bg-purple-100',
    textColor: 'text-purple-700',
    badgeColor: 'bg-purple-500',
    supportsCustomBaseUrl: true,
    customBaseUrlLabel: 'API Base URL',
    models: [
      { id: 'custom-model', name: 'Custom Model', contextLength: 4096, description: 'User-specified model ID' }
    ]
  }
]

export const PROVIDER_MAP = Object.fromEntries(
  PROVIDERS.map((p) => [p.id, p])
) as Record<ProviderID, ProviderDefinition>
