# Roteiro de apresentação — Relatório Parcial (Práticas de Extensão V)

**Bracelete inteligente com ESP32 para orientação de pessoas com baixa visão**
Matheus Vitor Lourenço Schionato e Vairtles Nehisen Mounkassa Liel — Orientador: Prof. Alvaro Rogerio Cantieri

Tempo total: 5 a 7 minutos. A ordem segue o relatório.

---

## 1. Abertura (30 s)

> "Nosso projeto é um bracelete com ESP32 para ajudar pessoas com baixa visão a se orientar dentro de um ambiente, por exemplo saber onde fica a porta ou a mesa de uma sala."

## 2. O que mudou desde a proposta (1 min)

É o ponto mais importante; explique logo no começo.

- A proposta previa um **sensor ultrassônico** para detectar obstáculos.
- **Tiramos o sensor** para simplificar o hardware e usar a comunicação sem fio que o ESP32 já tem.
- Com isso, o foco mudou de "detectar obstáculos" para "**localizar pontos de referência**" no ambiente.

## 3. Como funciona (1 min 30 s) — mostrar a Figura 1

> "São três partes. As **balizas** ficam em pontos da sala, como a porta e a mesa, e ficam só anunciando o próprio nome por Bluetooth. O **bracelete** escuta essas balizas e estima a distância de cada uma pela força do sinal. Depois ele manda a lista para o **celular**, que mostra na tela em alto contraste e fala em voz alta: *'Porta próxima, cerca de 1 metro'*."

### A comunicação, explicada de forma simples

```
Balizas  ──(anúncio BLE, a cada 100 ms)──▶  Bracelete  ──(notificação BLE, a cada 500 ms)──▶  Celular
                                                                   o celular NÃO envia comandos
```

- **Baliza → bracelete:** a baliza só "grita" o nome dela no ar. Não existe conexão entre as duas.
- **Bracelete → celular:** aqui há conexão Bluetooth. O bracelete **envia** a lista a cada meio segundo.
- **Mão única:** o celular **não manda comandos** para o bracelete, só recebe. Foi uma decisão nossa.
- **Distância:** quanto mais fraco o sinal que chega, mais longe está a baliza (Equação 1 do relatório).
- **Sem aplicativo:** a interface é uma **página web** aberta no Chrome do Android.

## 4. O que já está pronto (1 min)

- Programa do bracelete e da baliza gravados e funcionando nas placas ESP32-C3.
- Página web com voz, cores por proximidade e o botão **"O que tem por perto?"**.
- **Modo demonstração**, ligado pelo botão BOOT da placa, que simula três balizas.
- Testes: detectou **duas balizas ao mesmo tempo** e a comunicação com o celular funcionou.

## 5. O problema que encontramos (1 min)

Apresente com segurança: é resultado real.

- A distância em metros **não ficou confiável**. Com as placas a 1 m, a tela chegou a mostrar 20 m.
- **Causas:** a antena dessas plaquinhas é pequena, e o sinal muda com a posição, com o corpo no meio e com reflexões.
- **Solução planejada:** trocar os metros por **zonas**: "muito perto", "perto" e "na sala".

> "Em tecnologia assistiva, falar uma distância errada é pior do que não falar. Por isso preferimos zonas, que são mais confiáveis."

## 6. Próximos passos (30 s)

1. Calibrar o sinal e implementar as zonas.
2. Definir o formato físico: bateria e pulseira. O motor de vibração está em avaliação.
3. Instalar balizas numa sala do campus.
4. Testar com pessoas com baixa visão e apresentar o protótipo.

---

## Perguntas prováveis

| Pergunta | Resposta |
|---|---|
| Por que tiraram o sensor? | Para simplificar o hardware e aproveitar a comunicação sem fio do próprio ESP32. |
| Então ele não detecta obstáculos? | Não. Ele detecta pontos que têm baliza. É uma limitação que deixamos clara no relatório. |
| Por que Bluetooth e não Wi-Fi? | O Bluetooth de baixo consumo gasta menos bateria, não depende de rede e dá para medir a força do sinal de cada baliza. |
| Por que página web e não aplicativo? | Não precisa instalar nada; basta abrir o link no Chrome. |
| Qual a precisão? | Em metros, ainda não é boa. Por isso vamos usar zonas de proximidade. |
| E o contato com o público? | Os testes com pessoas com baixa visão estão previstos para a etapa final. |
| Usaram IA? | Sim, está declarado no Apêndice A: apoio no código, na análise dos testes e na redação. Os dados vieram das placas reais. |

## Dicas

- Se der, leve as duas placas e o celular e mostre o **modo demonstração** ao vivo: aperte o BOOT e toque em "O que tem por perto?".
- Página: https://mvitorls.github.io/projeto-extensao/Pratica%203/app-web/ (Chrome no Android; feche o nRF Connect antes).
- Divisão sugerida: partes 1–3 com um, partes 4–6 com o outro.
