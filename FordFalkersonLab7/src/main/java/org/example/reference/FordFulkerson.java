package org.example.reference;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

class FordFulkerson {
    static final int V = 7;
    // Количество вершин в графе

    static int[][] graph = {
            {0, 4, 3, 4, 0, 0, 0},
            {0, 0, 2, 0, 0, 3, 0},
            {0, 2, 0, 3, 1, 2, 0},
            {0, 0, 3, 0, 2, 0, 5},
            {0, 0, 1, 2, 0, 0, 2},
            {0, 3, 2, 0, 0, 0, 3},
            {0, 0, 0, 0, 0, 0, 0}
    };
    // Матрица смежности, представляющая граф, где graph[i][j] — это пропускная способность ребра из вершины i в вершину j

    static boolean bfs(int[][] rGraph, int s, int t, int[] parent) {
        // Метод для поиска увеличивающего пути с помощью обхода в ширину (BFS)

        boolean[] visited = new boolean[V];
        // Массив для отслеживания посещенных вершин

        LinkedList<Integer> queue = new LinkedList<>();
        // Очередь для реализации BFS
        queue.add(s);
        // Добавляем начальную вершину в очередь
        visited[s] = true;
        // Помечаем начальную вершину как посещенную

        while (!queue.isEmpty()) {
            // Пока есть вершины в очереди

            int u = queue.poll();
            // Извлекаем вершину из очереди

            for (int v = 0; v < V; v++) {
                if (!visited[v] && rGraph[u][v] > 0) {
                    // Если вершина v не посещена и существует оставшаяся пропускная способность из u в v
                    parent[v] = u;
                    // Обновляем родителя для вершины v

                    if (v == t) {
                        return true;
                        // Возвращаем true, путь найден
                    }
                    queue.add(v);
                    // Добавляем вершину v в очередь
                    visited[v] = true;
                    // Помечаем вершину v как посещенную
                }
            }
        }

        return false;
        // Возвращаем false, если увеличивающий путь не найден
    }

    static int fordFulkerson(int[][] graph, int s, int t) {
        // Метод для реализации алгоритма Форда-Фалкерсона

        int u, v, k=1;

        int[] parent = new int[V];
        // Массив для хранения найденного пути

        int max_flow = 0;
        // Переменная для хранения максимального потока

        while (bfs(graph, s, t, parent)) {
            // Пока существует увеличивающий путь

            int path_flow = Integer.MAX_VALUE;
            // Инициализируем поток в пути как бесконечность

            List<Integer> output = new ArrayList<>();
            for (v = t; v != s; v = parent[v]) {
                // Обратный путь по найденному пути и находим минимальную пропускную способность
                u = parent[v];
                output.add(u+1);
                path_flow = Math.min(path_flow, graph[u][v]);
            }

            max_flow += path_flow;
            // Добавляем поток пути к общему потоку

            for (v = t; v != s; v = parent[v]) {
                // Обновляем остаточные пропускные способности ребер и обратных ребер
                u = parent[v];
                graph[u][v] -= path_flow;
                graph[v][u] += path_flow;
            }

            System.out.print("Итерация " + k++ + "\nНайденный путь: ");
            for (int i = output.size()-1; i>= 0; i--) {
                System.out.print(output.get(i) + " -> ");
            }
            System.out.println(t+1);
            System.out.println("Пропускная способность пути равна "  + path_flow);
            System.out.println("Размер потока на данной итерации равен " + max_flow);
            System.out.println();
        }

        return max_flow;
        // Возвращаем максимальный поток
    }

    private static void printIntArray(int[] array, int s, int t) {
        System.out.print((s+1) + " -> ");
        for (int v = s; v != t; v = array[v]) {
            System.out.print((v+1) + " -> ");
        }
        System.out.println(t+1);
    }

    public static void main(String[] args) {
        System.out.println("Максимальный поток через данную телефонную сеть равен "
                + fordFulkerson(graph, 0, 6) + " тыс. телефонных переговоров в час.");
        // Вызываем метод для нахождения максимального потока от источника (0) до стока (5)
        System.out.println("Через путь 4-7 для обеспечения максимального потока должно пройти " + graph[6][3] + " тыс. разговоров");
    }
}
