# Resultados medidos

Gerado por `python -m experiments.apresentar`. Tempos em milissegundos; ambiente e resultados brutos em `resultados/`.

| Família | Tamanho | E | Operação | Mediana (ms) | Mín.–máx. (ms) | Desvio (ms) | Resultado | Tentativas |
| --- | ---: | ---: | --- | ---: | ---: | ---: | --- | ---: |
| cadeia | 100 | 99 | construcao | 0.1892 | 0.1813–0.2879 | 0.0381 |  |  |
| cadeia | 100 | 99 | dfs | 0.1086 | 0.0961–0.4237 | 0.1203 |  |  |
| cadeia | 100 | 99 | kahn | 0.1152 | 0.1130–0.1538 | 0.0147 |  |  |
| cadeia | 100 | 99 | dependentes | 0.0324 | 0.0303–0.1287 | 0.0365 |  |  |
| cadeia | 1000 | 999 | construcao | 2.1826 | 2.0536–2.4930 | 0.1507 |  |  |
| cadeia | 1000 | 999 | dfs | 1.1631 | 1.0079–1.3076 | 0.0977 |  |  |
| cadeia | 1000 | 999 | kahn | 1.2162 | 1.1906–1.3306 | 0.0518 |  |  |
| cadeia | 1000 | 999 | dependentes | 0.3090 | 0.2943–0.3410 | 0.0189 |  |  |
| cadeia | 5000 | 4999 | construcao | 10.2183 | 8.6924–15.6522 | 2.2659 |  |  |
| cadeia | 5000 | 4999 | dfs | 4.3407 | 3.5586–5.3611 | 0.6682 |  |  |
| cadeia | 5000 | 4999 | kahn | 5.3798 | 4.7084–6.4995 | 0.5822 |  |  |
| cadeia | 5000 | 4999 | dependentes | 1.2895 | 1.0721–1.6209 | 0.1875 |  |  |
| compartilhado | 100 | 764 | construcao | 0.7573 | 0.7090–1.2195 | 0.2228 |  |  |
| compartilhado | 100 | 764 | dfs | 0.1458 | 0.1366–0.2157 | 0.0343 |  |  |
| compartilhado | 100 | 764 | kahn | 0.1840 | 0.1797–0.2457 | 0.0259 |  |  |
| compartilhado | 100 | 764 | dependentes | 0.0463 | 0.0434–0.1076 | 0.0234 |  |  |
| compartilhado | 1000 | 7964 | construcao | 10.9781 | 9.9995–11.7181 | 0.6657 |  |  |
| compartilhado | 1000 | 7964 | dfs | 2.1372 | 2.0982–3.6253 | 0.5535 |  |  |
| compartilhado | 1000 | 7964 | kahn | 2.6346 | 2.1978–3.1690 | 0.3731 |  |  |
| compartilhado | 1000 | 7964 | dependentes | 0.8698 | 0.5801–1.1645 | 0.2033 |  |  |
| compartilhado | 5000 | 39964 | construcao | 66.3368 | 43.9189–122.6490 | 25.5299 |  |  |
| compartilhado | 5000 | 39964 | dfs | 12.9790 | 9.1385–28.9920 | 6.7538 |  |  |
| compartilhado | 5000 | 39964 | kahn | 13.8249 | 11.4330–21.2216 | 3.1030 |  |  |
| compartilhado | 5000 | 39964 | dependentes | 3.9832 | 3.0841–5.4646 | 0.8441 |  |  |
| ciclo | 100 | 100 | construcao | 0.1841 | 0.1720–0.2325 | 0.0229 |  |  |
| ciclo | 100 | 100 | dfs | 0.0717 | 0.0657–0.1045 | 0.0159 |  |  |
| ciclo | 100 | 100 | kahn | 0.0419 | 0.0352–0.0690 | 0.0136 |  |  |
| ciclo | 100 | 100 | dependentes | 0.0360 | 0.0295–0.0892 | 0.0210 |  |  |
| ciclo | 1000 | 1000 | construcao | 1.8293 | 1.7281–7.3981 | 2.1009 |  |  |
| ciclo | 1000 | 1000 | dfs | 0.7795 | 0.6498–1.2515 | 0.2161 |  |  |
| ciclo | 1000 | 1000 | kahn | 0.2950 | 0.2631–0.4003 | 0.0464 |  |  |
| ciclo | 1000 | 1000 | dependentes | 0.2612 | 0.2157–0.4471 | 0.0797 |  |  |
| ciclo | 5000 | 5000 | construcao | 9.0765 | 8.8324–10.4726 | 0.5831 |  |  |
| ciclo | 5000 | 5000 | dfs | 3.1473 | 2.6913–8.1986 | 1.9561 |  |  |
| ciclo | 5000 | 5000 | kahn | 1.2877 | 1.1798–1.4530 | 0.1016 |  |  |
| ciclo | 5000 | 5000 | dependentes | 1.1250 | 1.0791–1.2682 | 0.0823 |  |  |
| resolvedor_cadeia | 16 | 15 | resolucao | 0.2609 | 0.1980–0.3388 | 0.0474 | valido | 16 |
| resolvedor_cadeia | 64 | 63 | resolucao | 1.7240 | 1.4434–10.4100 | 3.2985 | valido | 64 |
| resolvedor_cadeia | 128 | 127 | resolucao | 5.3190 | 5.2059–16.0645 | 4.0162 | valido | 128 |
| resolvedor_retrocesso | 4 | 4 | resolucao | 0.4903 | 0.4611–0.6388 | 0.0794 | valido | 46 |
| resolvedor_retrocesso | 8 | 8 | resolucao | 8.0809 | 7.6195–8.5179 | 0.2628 | valido | 766 |
| resolvedor_retrocesso | 12 | 12 | resolucao | 144.2176 | 142.9780–157.0542 | 5.3866 | valido | 12286 |
