// 3 Working free models on OpenRouter (must match backend config.py)
export const MODEL_OPTIONS = [
    { value: 'meta-llama/llama-3.3-70b-instruct:free', label: 'Llama 3.3 70B' },
    { value: 'google/gemma-3-27b-it:free', label: 'Gemma 3 27B' },
    { value: 'google/gemini-2.0-flash-exp:free', label: 'Gemini 2.0 Flash' },
];

export const DEFAULT_MODEL = 'meta-llama/llama-3.3-70b-instruct:free';