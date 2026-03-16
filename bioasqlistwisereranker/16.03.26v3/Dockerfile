FROM vllm/vllm-openai:v0.11.0

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/root/.cache/huggingface

WORKDIR /app

# Keep the vLLM stack from the base image stable.
# Add the packages your script actually imports / benefits from.
RUN uv pip install --system \
    numpy \
    pandas \
    matplotlib \
    tqdm \
    transformers \
    tokenizers \
    huggingface_hub \
    accelerate \
    jupyterlab \
    ipykernel \
    jupytext \
    faiss-cpu

# # Install RankLLM without trying to replace the base image's vLLM/torch stack.
# RUN uv pip install --system --no-deps rank-llm==0.25.7

# # Optional: only if later you want RankLLM's built-in retriever / pyserini path
# # RUN apt-get update && apt-get install -y openjdk-21-jre-headless maven && rm -rf /var/lib/apt/lists/*
# # RUN uv pip install --system "rank-llm[pyserini]"

# # Build-time smoke test: imports + tokenizer, but no full 7B weights.
# RUN python - <<'PY'
# import sys
# print("Python:", sys.version)

# import vllm
# print("vllm:", vllm.__version__)

# import numpy as np
# import pandas as pd
# import matplotlib
# from tqdm.auto import tqdm
# import transformers
# import tokenizers
# import huggingface_hub
# import accelerate

# print("numpy:", np.__version__)
# print("pandas:", pd.__version__)
# print("matplotlib:", matplotlib.__version__)
# print("transformers:", transformers.__version__)
# print("tokenizers:", tokenizers.__version__)
# print("huggingface_hub:", huggingface_hub.__version__)
# print("accelerate:", accelerate.__version__)

# from transformers import AutoTokenizer
# tok = AutoTokenizer.from_pretrained("castorini/rank_zephyr_7b_v1_full")
# print("tokenizer:", tok.__class__.__name__)

# from rank_llm.data import Request, Candidate, Query
# from rank_llm.rerank import Reranker
# from rank_llm.rerank.listwise import ZephyrReranker

# print("rank_llm imports OK")
# print("All imports OK")
# PY