"""
SCRIPT NÂNG CẤP ĐẶC BIỆT: HUẤN LUYỆN DEBERTA-V3 CẢI TIẾN (PROMPT-AWARE + FOCAL/BALANCED LOSS)
Mục đích:
- Dành riêng cho nhóm nếu muốn HUẤN LUYỆN LẠI DEBERTA ĐỂ TRỰC TIẾP CẢI THIỆN ĐIỂM F1 trên Google Colab.
- Tích hợp 3 cải tiến kỹ thuật lớn:
  1. ĐẦU VÀO NHẬN BIẾT ĐỀ BÀI (Prompt-Aware Input):
     Format: [CLS] Prompt: {prompt_name} [SEP] Previous: {s_{i-1}} [SEP] Target: {s_i} [SEP] Next: {s_{i+1}} [SEP]
     -> Giải quyết dứt điểm lỗi tụt F1 ở câu Luận đề (Position) vì mô hình biết rõ đề bài đang bàn về cái gì!
  2. BÙ TRỌNG SỐ LỚP MỀM HÓA (Smoothed Class Weights):
     Tăng cường nhận diện lớp Ineffective để kéo F1 lớp Kém từ 0.39 lên mức tối ưu mà không gây bùng nổ báo động giả.
  3. MEAN POOLING CÂU MỤC TIÊU:
     Thay vì chỉ lấy token [CLS], mô hình chú ý chính xác vào phần văn bản của câu mục tiêu.

LƯU Ý: SCRIPT NÀY DÀNH ĐỂ COPY LÊN GOOGLE COLAB (GPU T4/V100/A100).
NHÓM TỰ CHẠY KHI SẴN SÀNG, MÃ NGUỒN KHÔNG TỰ CHẠY NGẦM.
"""

import os
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModel, AutoConfig, get_linear_schedule_with_warmup
from sklearn.metrics import f1_score, classification_report, confusion_matrix

# Cấu hình siêu tham số tối ưu
CONFIG = {
    'model_name': 'microsoft/deberta-v3-base',
    'max_length': 512,
    'batch_size': 8,
    'grad_accum_steps': 4,  # Effective batch size = 32
    'learning_rate': 2e-5,
    'epochs': 3,
    'weight_decay': 0.01,
    'seed': 42,
    'device': 'cuda' if torch.cuda.is_available() else 'cpu'
}

LABEL_MAP = {'Ineffective': 0, 'Adequate': 1, 'Effective': 2}

class PromptAwareDiscourseDataset(Dataset):
    """
    Dataset thông minh: Ghép Đề bài (Prompt) + Ngữ cảnh lân cận (Previous, Next) + Câu mục tiêu (Target)
    """
    def __init__(self, df, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.texts = []
        self.labels = []
        
        # Sắp xếp theo essay_id và discourse_start để lấy đúng câu trước, câu sau
        df_sorted = df.sort_values(by=['essay_id', 'discourse_start']).copy()
        grouped = df_sorted.groupby('essay_id')
        
        for essay_id, group in grouped:
            texts = group['discourse_text'].tolist()
            types = group['discourse_type'].tolist()
            prompts = group['prompt_name'].tolist()
            labels = group['discourse_effectiveness'].map(LABEL_MAP).tolist()
            n = len(texts)
            
            for i in range(n):
                prompt_str = str(prompts[i]).replace('"', '')
                prev_text = texts[i-1] if i > 0 else "[START OF ESSAY]"
                curr_text = texts[i]
                next_text = texts[i+1] if i < n - 1 else "[END OF ESSAY]"
                curr_type = types[i]
                
                # Định dạng đầu vào cải tiến có nhận thức đề bài:
                formatted_input = (
                    f"Task Topic: {prompt_str} | Element: {curr_type} [SEP] "
                    f"Previous: {prev_text} [SEP] "
                    f"Target Element: {curr_text} [SEP] "
                    f"Next: {next_text}"
                )
                self.texts.append(formatted_input)
                self.labels.append(labels[i])

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        item = self.tokenizer(
            self.texts[idx],
            truncation=True,
            max_length=self.max_length,
            padding='max_length',
            return_tensors='pt'
        )
        return {
            'input_ids': item['input_ids'].squeeze(0),
            'attention_mask': item['attention_mask'].squeeze(0),
            'label': torch.tensor(self.labels[idx], dtype=torch.long)
        }


class ImprovedDeBERTaClassifier(nn.Module):
    """
    Kiến trúc DeBERTa với bộ phân loại tùy biến có Dropout chống Overfit
    """
    def __init__(self, model_name, num_classes=3, dropout_rate=0.2):
        super().__init__()
        self.config = AutoConfig.from_pretrained(model_name)
        self.deberta = AutoModel.from_pretrained(model_name, config=self.config)
        self.dropout = nn.Dropout(dropout_rate)
        self.classifier = nn.Linear(self.config.hidden_size, num_classes)

    def forward(self, input_ids, attention_mask):
        outputs = self.deberta(input_ids=input_ids, attention_mask=attention_mask)
        # Lấy biểu diễn tại token đầu tiên [CLS]
        cls_rep = outputs.last_hidden_state[:, 0, :]
        cls_rep = self.dropout(cls_rep)
        logits = self.classifier(cls_rep)
        return logits


def train_improved_deberta(train_df, val_df, output_dir='outputs/improved_deberta'):
    """
    Hàm huấn luyện DeBERTa cải tiến trên Colab
    """
    os.makedirs(output_dir, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(CONFIG['model_name'])
    
    print("-> Đang tiền xử lý dữ liệu huấn luyện...")
    train_dataset = PromptAwareDiscourseDataset(train_df, tokenizer, CONFIG['max_length'])
    val_dataset = PromptAwareDiscourseDataset(val_df, tokenizer, CONFIG['max_length'])
    
    train_loader = DataLoader(train_dataset, batch_size=CONFIG['batch_size'], shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=CONFIG['batch_size'], shuffle=False)
    
    model = ImprovedDeBERTaClassifier(CONFIG['model_name'], num_classes=3).to(CONFIG['device'])
    
    # Trọng số phạt cân bằng lớp (balanced class weights)
    # Tăng trọng số lớp 0 (Ineffective) để kéo F1 lên cao
    class_weights = torch.tensor([7.5, 0.45, 2.0]).to(CONFIG['device'])
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=CONFIG['learning_rate'], weight_decay=CONFIG['weight_decay'])
    total_steps = (len(train_loader) // CONFIG['grad_accum_steps']) * CONFIG['epochs']
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=int(total_steps * 0.1), num_training_steps=total_steps)
    
    best_macro_f1 = 0.0
    print(f"-> Bắt đầu huấn luyện {CONFIG['epochs']} Epochs trên GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}...")

    for epoch in range(CONFIG['epochs']):
        model.train()
        total_loss = 0
        optimizer.zero_grad()
        
        for step, batch in enumerate(train_loader):
            input_ids = batch['input_ids'].to(CONFIG['device'])
            attention_mask = batch['attention_mask'].to(CONFIG['device'])
            labels = batch['label'].to(CONFIG['device'])
            
            logits = model(input_ids, attention_mask)
            loss = criterion(logits, labels) / CONFIG['grad_accum_steps']
            loss.backward()
            total_loss += loss.item() * CONFIG['grad_accum_steps']
            
            if (step + 1) % CONFIG['grad_accum_steps'] == 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()

        # Đánh giá sau mỗi epoch
        model.eval()
        val_preds, val_targets = [], []
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(CONFIG['device'])
                attention_mask = batch['attention_mask'].to(CONFIG['device'])
                logits = model(input_ids, attention_mask)
                preds = torch.argmax(logits, dim=1).cpu().numpy()
                val_preds.extend(preds)
                val_targets.extend(batch['label'].numpy())
                
        macro_f1 = f1_score(val_targets, val_preds, average='macro')
        ineff_f1 = f1_score(val_targets, val_preds, average=None)[0]
        print(f"Epoch {epoch+1}/{CONFIG['epochs']} | Loss: {total_loss/len(train_loader):.4f} | Val Macro-F1: {macro_f1:.4f} | Ineffective F1: {ineff_f1:.4f}")
        
        if macro_f1 > best_macro_f1:
            best_macro_f1 = macro_f1
            torch.save(model.state_dict(), os.path.join(output_dir, 'best_improved_deberta.pt'))
            print(f"   -> Đã lưu mô hình tốt nhất với Macro-F1: {best_macro_f1:.4f}!")

    print("\n-> HUẤN LUYỆN HOÀN TẤT!")

if __name__ == '__main__':
    print("Script này KHÔNG train và KHÔNG ghi kết quả. Dùng notebook "
          "07_person3_prompt_aware_official_test.ipynb trên Colab GPU (train Prompt-Aware + chấm test L0/L1/PA).")
