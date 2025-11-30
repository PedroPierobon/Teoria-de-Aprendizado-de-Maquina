import time
import math
import numpy as np
import matplotlib.pyplot as plt

def relu(Z):
    return np.maximum(0, Z)

def sigmoid(Z):
    return 1 / (1 + np.exp(-Z))

def init(neu_por_layers):
    np.random.seed(3)
    parametros = {}
    L = len(neu_por_layers)
    for l in range(1, L):
        # Convenção (Features, Units)
        parametros['W' + str(l)] = np.random.randn(neu_por_layers[l-1], neu_por_layers[l]) * 0.01
        parametros['b' + str(l)] = np.zeros((1, neu_por_layers[l]))
    return parametros

def ativacao_linear(A_prev, W, b, ativacao):
    Z = np.matmul(A_prev, W) + b
    if ativacao == "sigmoid":
        A = sigmoid(Z)
    elif ativacao == "relu":
        A = relu(Z)
    elif ativacao == "linear":
        A = Z
    return A

# Implementação Vetorizada
def forward_vetorizado(X, parametros, hidden_activation='relu', output_activation='sigmoid'):
    A = X
    L = len(parametros) // 2
    for l in range(1, L):
        A_prev = A
        W = parametros['W' + str(l)]
        b = parametros['b' + str(l)]
        A = ativacao_linear(A_prev, W, b, ativacao=hidden_activation)
    
    # Camada de Saída
    W = parametros['W' + str(L)]
    b = parametros['b' + str(L)]
    AL = ativacao_linear(A, W, b, ativacao=output_activation)
    return AL

# Implementação Não-Vetorizada
def forward_nao_vetorizado(X, parametros, hidden_activation='relu', output_activation='sigmoid'):
    A_prev = X
    L = len(parametros) // 2
    
    for l in range(1, L + 1):
        W = parametros['W' + str(l)]
        b = parametros['b' + str(l)]
        m_exemplos = A_prev.shape[0]
        n_in = W.shape[0]
        n_out = W.shape[1]
        A_next = np.zeros((m_exemplos, n_out))
        
        # Define ativação da camada atual
        act = output_activation if l == L else hidden_activation

        for i in range(m_exemplos):
            for j in range(n_out):
                soma_z = 0.0
                for k in range(n_in):
                    soma_z += A_prev[i, k] * W[k, j]
                soma_z += b[0, j]
                
                if act == "relu":
                    A_next[i, j] = max(0, soma_z)
                elif act == "sigmoid":
                    A_next[i, j] = 1 / (1 + math.exp(-soma_z))
                elif act == "linear":
                    A_next[i, j] = soma_z
        A_prev = A_next
    return A_prev

# ==========================================
# TESTES
# ==========================================

n_x = 100
m_exemplos = 1000 
X = np.random.randn(m_exemplos, n_x)

print(f"--- Testes ---")
print(f"Dataset X shape: {X.shape}")
print(f"Features: {n_x}, Exemplos: {m_exemplos}")
print("-" * 30)

# Pequena: 2 camadas ocultas
# Média: 4 camadas ocultas
# Grande: 8 camadas ocultas
# Extrema: 10 camadas profundas e largas
configs = {
    "Pequena": [n_x, 32, 16, 1],
    "Média":   [n_x, 128, 64, 32, 16, 1],
    "Grande":  [n_x, 128, 128, 128, 128, 128, 128, 128, 128, 1],
    "Extrema": [n_x, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 1]
}

def medir_tempo(func, loops=10):
    tempos = []
    for i in range(loops + 1):
        inicio = time.time()
        func()
        fim = time.time()
        if i > 0:
            tempos.append(fim - inicio)
    return np.mean(tempos), np.std(tempos)

resultados = []

print(f"{'Config':<10} | {'Impl':<15} | {'Activ':<8} | {'Tempo Médio (s)':<15} | {'Status'}")
print("-" * 70)

for nome_config, layers in configs.items():
    parametros = init(layers)
    
    # 1. Teste Vetorizado (ReLU e Sigmoid)
    for ativacao in ['relu', 'sigmoid']:
        tempo_medio, _ = medir_tempo(
            lambda: forward_vetorizado(X, parametros, hidden_activation=ativacao),
            loops=20
        )
        print(f"{nome_config:<10} | {'Vetorizada':<15} | {ativacao:<8} | {tempo_medio:.6f} s       | OK")
        resultados.append([nome_config, 'Vetorizada', ativacao, tempo_medio])

    # 2. Teste Não-Vetorizado
    X_lento = X
    fator_reducao = 1
    
    if nome_config in ["Grande", "Extrema"]:
        X_lento = X[:10, :] 
        fator_reducao = m_exemplos / 10
        status = "Estimado (Dataset Reduzido)"
    else:
        status = "Real"

    # Rodamos menos loops para a versão lenta
    tempo_amostra, _ = medir_tempo(
        lambda: forward_nao_vetorizado(X_lento, parametros, hidden_activation='relu'),
        loops=3
    )
    
    tempo_final_estimado = tempo_amostra * fator_reducao
    
    print(f"{nome_config:<10} | {'Não-Vet':<15} | {'relu':<8} | {tempo_final_estimado:.6f} s       | {status}")
    resultados.append([nome_config, 'Não-Vetorizada', 'relu', tempo_final_estimado])

# ==========================================
# GERAÇÃO DO GRÁFICO
# ==========================================

configs_labels = list(configs.keys())
tempos_vet = [r[3] for r in resultados if r[1] == 'Vetorizada' and r[2] == 'relu']
tempos_nao_vet = [r[3] for r in resultados if r[1] == 'Não-Vetorizada' and r[2] == 'relu']

x = np.arange(len(configs_labels))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, tempos_vet, width, label='Vetorizada (NumPy)')
rects2 = ax.bar(x + width/2, tempos_nao_vet, width, label='Não-Vetorizada (Loops)')

ax.set_ylabel('Tempo de Execução (segundos)')
ax.set_title('Comparação de Desempenho: Forward Propagation')
ax.set_xticks(x)
ax.set_xticklabels(configs_labels)
ax.legend()

ax.set_yscale('log') 

plt.tight_layout()
plt.show()