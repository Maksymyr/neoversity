# algo_hw_topic_09_n_10 — Greedy/DP та Монте-Карло

Два незалежних завдання.

- [task_1/readme.md](task_1/readme.md) — видача решти: greedy vs DP (40 балів)
- [task_2/readme.md](task_2/readme.md) — інтегрування методом Монте-Карло vs `scipy.quad` (60 балів)

## Структура

```
algo_hw_topic_09_n_10/
├── task_1/
│   ├── coins.py             # find_coins_greedy + find_min_coins
│   ├── test_coins.py
│   └── readme.md
├── task_2/
│   ├── monte_carlo_integral.py  # mean-value + hit-or-miss MC
│   ├── test_monte_carlo_integral.py
│   ├── integration_area.png     # f(x)=x² з заштрихованою площею
│   ├── convergence.png          # збіжність MC vs N (log-log)
│   └── readme.md
├── requirements.txt
└── readme.md
```

## Залежності

```bash
pip install -r requirements.txt
```

- task_1 — стандартна бібліотека (`timeit`)
- task_2 — `numpy`, `matplotlib`, `scipy`

## Запуск

```bash
python task_1/coins.py                  # демо + бенчмарк
python task_1/test_coins.py             # тести

python task_2/monte_carlo_integral.py   # 1M зразків, інтерактивні графіки
python task_2/monte_carlo_integral.py --save  # зберегти графіки в PNG
python task_2/test_monte_carlo_integral.py    # тести
```
