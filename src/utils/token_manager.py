import os
from pathlib import Path

class TokenManager:
    def __init__(self):
        self.data_dir = os.getenv('DATA_DIR', './data')
        self.tokens_file = os.path.join(self.data_dir, 'tokens.txt')
        
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        self.tokens = self._load()
    
    def _load(self):
        try:
            if os.path.exists(self.tokens_file):
                with open(self.tokens_file, 'r') as f:
                    return [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f'[Emorce] Error loading tokens: {e}')
        return []
    
    def _save(self):
        try:
            with open(self.tokens_file, 'w') as f:
                f.write('\n'.join(self.tokens))
        except Exception as e:
            print(f'[Emorce] Error saving tokens: {e}')
    
    def add(self, tokens):
        new_tokens = [t.strip() for t in tokens if t.strip()]
        self.tokens.extend(new_tokens)
        self._save()
        return len(new_tokens)
    
    def get_all(self):
        return self.tokens.copy()
    
    def get_count(self):
        return len(self.tokens)
    
    def get_preview(self, count=10):
        preview = []
        for token in self.tokens[:count]:
            visible = token[:8]
            hidden = '*' * max(0, len(token) - 8)
            preview.append(visible + hidden)
        return preview
    
    def clear(self):
        self.tokens = []
        self._save()
    
    def export(self):
        return '\n'.join(self.tokens).encode('utf-8')
