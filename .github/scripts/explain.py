from google import genai
import os
import time
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


with open("changed_files.txt") as f:
    files = [l.strip() for l in f.readlines() if l.strip().endswith(".py")]

if not files:
    with open("explanation_output.md", "w") as f:
        f.write("No Python files changed.")
    exit(0)

output = []

for filepath in files:
    if not os.path.exists(filepath):
        continue

    with open(filepath) as f:
        code = f.read()

    prompt = f"""Analyze this Python file and provide:

1. **Purpose** — what this module does in 2-3 sentences
2. **How it works** — step by step explanation of the logic
3. **Key functions/classes** — brief description of each
4. **Mermaid flowchart** — showing the main execution flow

File: `{filepath}`

```python
{code}
```

Format the Mermaid diagram inside a ```mermaid code block.
Keep the explanation concise and developer-friendly."""
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
    
)
    explanation = response.text
    output.append(f"##  `{filepath}`\n\n{explanation}\n\n---\n")

with open("explanation_output.md", "w") as f:
    f.write("#Code Explanation Report\n\n")
    f.write("\n".join(output))