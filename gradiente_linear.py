def somatorio_w(pontos, m, w, b):
    soma = 0
    for i in range():
        x = pontos[i][0]
        y = pontos[i][1]
        soma += (w * x + b - y) * x
    return soma
def somatorio_b(pontos, m, w, b):
    soma = 0
    for i in range():
        x = pontos[i][0]
        y = pontos[i][1]
        soma += w * x + b - y
    return soma

print("Quantidade de pontos: ")
m = int(input())

pontos = []
for i in rang(m):
    entrada = input(f"Digite as coordenadas do ponto {i+1} (formato x,y): ")
    x_str, y_str = entrada.split(',')
    x = float(x_str)
    y = float(y_str)
    pontos.append((x,y))