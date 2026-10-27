"""CLS and CLS+target pooling with a portable encoder/head checkpoint."""
import json
from pathlib import Path

import torch
from torch import nn
from transformers import AutoModel

SETTINGS = {}


class SpanClassifier(nn.Module):
    def __init__(self, encoder, pooling):
        super().__init__()
        self.encoder = encoder
        self.config = encoder.config
        self.pooling = pooling
        size = self.config.hidden_size * (2 if pooling == 'cls_target' else 1)
        self.dropout = nn.Dropout(.1)
        self.classifier = nn.Linear(size, 3)

    @classmethod
    def from_pretrained(cls, source, **kwargs):
        root = Path(source)
        record = root / 'span_head.json'
        if record.exists():
            spec = json.loads(record.read_text())
            model = cls(AutoModel.from_pretrained(root / 'encoder'), spec['pooling'])
            model.classifier.load_state_dict(torch.load(root / 'head.pt', map_location='cpu', weights_only=True))
            return model
        model = cls(AutoModel.from_pretrained(source, revision=SETTINGS['revision'],
                                             attn_implementation=SETTINGS.get('attention', 'eager')),
                    SETTINGS['pooling'])
        return model

    def gradient_checkpointing_enable(self, **kwargs):
        self.encoder.gradient_checkpointing_enable(**kwargs)

    def save_pretrained(self, directory, **kwargs):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        self.encoder.save_pretrained(directory / 'encoder', **kwargs)
        torch.save(self.classifier.state_dict(), directory / 'head.pt')
        (directory / 'span_head.json').write_text(json.dumps({'pooling': self.pooling, 'labels':
                                                           ['Ineffective', 'Adequate', 'Effective']}))

    def forward(self, target_mask, labels=None, **inputs):
        from types import SimpleNamespace
        hidden = self.encoder(**inputs).last_hidden_state
        if not target_mask.any(dim=1).all():
            raise ValueError('Empty target mask')
        pooled = hidden[:, 0]
        if self.pooling == 'cls_target':
            mask = target_mask.unsqueeze(-1).to(hidden.dtype)
            mean = (hidden * mask).sum(1) / mask.sum(1)
            pooled = torch.cat([pooled, mean], dim=-1)
        logits = self.classifier(self.dropout(pooled))
        loss = nn.functional.cross_entropy(logits.float(), labels) if labels is not None else None
        return SimpleNamespace(logits=logits, loss=loss)
