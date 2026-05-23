# algo_final_project — фінальний проєкт з алгоритмів

Сім незалежних завдань, що покривають структури даних, рекурсію, графи, обходи, динамічне програмування та симуляцію Монте-Карло.

## Завдання

| #  | Назва                                  | Тема                                  | Балів |
|----|-----------------------------------------|----------------------------------------|-------|
| 1  | [Однозв'язний список](task_1_linked_list/readme.md)        | Структури даних, сортування            | 15    |
| 2  | [Дерево Піфагора](task_2_pythagoras_tree/readme.md)        | Рекурсія, фрактали                     | 15    |
| 3  | [Алгоритм Дейкстри](task_3_dijkstra/readme.md)             | Графи, бінарна купа                    | 10    |
| 4  | [Візуалізація купи](task_4_heap_viz/readme.md)             | Дерева, networkx                       | 15    |
| 5  | [DFS / BFS обхід](task_5_tree_traversal/readme.md)         | Стек, черга, градієнт кольорів         | 15    |
| 6  | [Greedy vs DP — їжа](task_6_food_selection/readme.md)      | Жадібний алгоритм, динаміка            | 15    |
| 7  | [Монте-Карло — кубики](task_7_monte_carlo/readme.md)       | Симуляція, теорія ймовірностей         | 15    |
|    |                                         | **Разом**                              | **100** |

## Структура

```
algo_final_project/
├── task_1_linked_list/      # reverse, sort (merge), merge_two_sorted + тести
├── task_2_pythagoras_tree/  # фрактал у matplotlib + тести (мат. інваріанти)
├── task_3_dijkstra/         # Dijkstra з heapq + тести
├── task_4_heap_viz/         # heap → tree → networkx draw
├── task_5_tree_traversal/   # iterative DFS/BFS + кольоровий градієнт + тести
├── task_6_food_selection/   # 0/1 knapsack greedy vs DP + тести
├── task_7_monte_carlo/      # симуляція двох кубиків + графік + висновки
├── requirements.txt         # matplotlib, networkx
└── readme.md                # цей файл
```

## Залежності

```bash
pip install -r requirements.txt
```

- `matplotlib` — task_2, task_4, task_5, task_7
- `networkx` — task_4, task_5
- Решта — стандартна бібліотека (`heapq`, `collections.deque`, `uuid`, `argparse`, `random`).

## Запуск усього

```bash
# Алгоритмічні (без візуалізації — для CI/перевірки)
python task_1_linked_list/test_linked_list.py
python task_2_pythagoras_tree/test_pythagoras_tree.py
python task_3_dijkstra/test_dijkstra.py
python task_5_tree_traversal/test_tree_traversal.py
python task_6_food_selection/test_food_selection.py
python task_7_monte_carlo/test_monte_carlo_dice.py

# Демо-запуски (відкриють вікна matplotlib або консольний вивід)
python task_1_linked_list/linked_list.py
python task_2_pythagoras_tree/pythagoras_tree.py 8
python task_3_dijkstra/dijkstra.py
python task_4_heap_viz/heap_viz.py
python task_5_tree_traversal/tree_traversal.py
python task_6_food_selection/food_selection.py
python task_7_monte_carlo/monte_carlo_dice.py -n 1000000 --seed 42
```

## Конвенції

- Усі функції з type hints.
- Тести написано без зовнішніх фреймворків — звичайні `assert` у функції `run_tests()`.
- Усі рекурсивні візуалізації мають soft-cap з підтвердженням, щоб уникнути несподівано довгих рендерів.
- Алгоритми, де можливі недопустимі вхідні дані (порожня структура, від'ємна вага тощо), кидають `ValueError` з пояснювальним повідомленням.
