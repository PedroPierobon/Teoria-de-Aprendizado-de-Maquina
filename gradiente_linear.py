def somatorio_w(pontos, m, w, b):
    soma = 0
    for i in range(m):
        x = pontos[i][0]
        y = pontos[i][1]
        soma += (w * x + b - y) * x
    return soma
def somatorio_b(pontos, m, w, b):
    soma = 0
    for i in range(m):
        x = pontos[i][0]
        y = pontos[i][1]
        soma += w * x + b - y
    return soma

print("Quantidade de pontos: ")
m = int(input())

pontos = []
for i in range(m):
    entrada = input(f"Digite as coordenadas do ponto {i+1} (formato x,y): ")
    x_str, y_str = entrada.split(',')
    x = float(x_str)
    y = float(y_str)
    pontos.append((x,y))
gradiente_w = 2
gradiente_b = 2
w = b = 0
alpha = 0.01
while (abs(gradiente_b) > 0.0001 and abs(gradiente_w) > 0.0001):
    gradiente_w = somatorio_w(pontos, m, w, b)/m
    gradiente_b = somatorio_b(pontos, m, w, b)/m
    temp_w = w - alpha*gradiente_w
    temp_b = b - alpha*gradiente_b
    w = temp_w
    print(w)
    b = temp_b
    print(b)

print(f"A reta otima: y = {w:.2f}x + {b:.2f}")
