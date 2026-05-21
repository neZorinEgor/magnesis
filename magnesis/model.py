import torch.nn as nn


class GeomagneticModelV1(nn.Module):
    def __init__(
        self,
        lstm_input_size,
        lstm_hidden_size,
        lstm_num_layers,
        lstm_dropout,
        dst_attention_heads,
        ae_attention_heads,
        forecasts_len,
    ):
        super().__init__()

        self.dst_attention = nn.MultiheadAttention(
            lstm_input_size,
            dst_attention_heads,
            dropout=lstm_dropout,
            batch_first=True,
        )
        self.dst_attention_norm = nn.LayerNorm(lstm_input_size)
        self.ae_attention = nn.MultiheadAttention(
            lstm_input_size, ae_attention_heads, dropout=lstm_dropout, batch_first=True
        )
        self.ae_attention_norm = nn.LayerNorm(lstm_input_size)

        self.dst_lstm = nn.LSTM(
            lstm_input_size,
            lstm_hidden_size,
            lstm_num_layers,
            dropout=lstm_dropout,
            batch_first=True,
        )
        self.ae_lstm = nn.LSTM(
            lstm_input_size,
            lstm_hidden_size,
            lstm_num_layers,
            dropout=lstm_dropout,
            batch_first=True,
        )

        self.dropout = nn.Dropout(lstm_dropout)
        heads_hidden_size = lstm_hidden_size

        self.dst_head = nn.Sequential(
            nn.Linear(lstm_hidden_size, heads_hidden_size),
            nn.LeakyReLU(0.1),
            nn.Dropout(lstm_dropout),
            nn.Linear(heads_hidden_size, forecasts_len),
        )

        self.ae_head = nn.Sequential(
            nn.Linear(lstm_hidden_size, heads_hidden_size),
            nn.LeakyReLU(0.1),
            nn.Dropout(lstm_dropout),
            nn.Linear(heads_hidden_size, forecasts_len),
        )

    def forward(self, x):
        dst_attn_out, dst_attn_w = self.dst_attention(x, x, x)
        dst_x = self.dst_attention_norm(x + dst_attn_out)
        dst_out, _ = self.dst_lstm(dst_x)
        dst_features = self.dropout(dst_out[:, -1, :])
        dst = self.dst_head(dst_features)

        ae_attn_out, ae_attn_w = self.ae_attention(x, x, x)
        ae_x = self.ae_attention_norm(x + ae_attn_out)
        ae_out, _ = self.ae_lstm(ae_x)
        ae_features = self.dropout(ae_out[:, -1, :])
        ae = self.ae_head(ae_features)

        return dst, ae, (dst_attn_w, ae_attn_w)
