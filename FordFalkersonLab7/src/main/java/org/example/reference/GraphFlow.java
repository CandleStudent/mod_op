package org.example.reference;

import java.util.*;

// Основной класс для управления графами и потоками
public class GraphFlow {

    // Вложенный класс для представления рёбер графа
    static class Edge {
        int v, capacity, cost, flow; // Конечная вершина, пропускная способность, стоимость и текущий поток

        Edge(int v, int capacity, int cost) {
            this.v = v;
            this.capacity = capacity;
            this.cost = cost;
            this.flow = 0; // Изначально поток равен нулю
        }
    }

    // Вложенный класс для представления рёбер модифицированного графа
    static class ModifiedEdge {
        int v, cost; // Конечная вершина и стоимость

        ModifiedEdge(int v, int cost) {
            this.v = v;
            this.cost = cost;
        }
    }

    // Вложенный класс для хранения информации о пути
    static class PathInfo {
        List<Integer> path; // Список вершин, составляющих путь
        int flow; // Объём потока по этому пути
        int cost; // Стоимость пути

        PathInfo(List<Integer> path, int flow, int cost) {
            this.path = path;
            this.flow = flow;
            this.cost = cost;
        }
    }

    int V; // Количество вершин в графе
    Map<Integer, List<Edge>> graph; // Граф представлен в виде карты списков рёбер

    GraphFlow(int vertices) {
        this.V = vertices;
        this.graph = new HashMap<>();
        for (int i = 0; i < vertices; i++) {
            this.graph.put(i, new ArrayList<>()); // Инициализация списка рёбер для каждой вершины
        }
    }

    // Метод для добавления ребра в граф
    void addEdge(int u, int v, int capacity, int cost) {
        graph.get(u).add(new Edge(v, capacity, cost));
    }

    // Метод для поиска пути увеличения потока с использованием BFS
    boolean bfs(int source, int sink, int[] parent) {
        boolean[] visited = new boolean[V]; // Массив для отслеживания посещённых вершин
        Queue<Integer> queue = new LinkedList<>();
        queue.add(source); // Начинаем с источника
        visited[source] = true;
        Arrays.fill(parent, -1); // Инициализация массива предков

        while (!queue.isEmpty()) {
            int u = queue.poll();
            for (Edge edge : graph.get(u)) { // Итерируем по всем рёбрам из текущей вершины
                int v = edge.v;
                if (!visited[v] && edge.capacity > edge.flow) { // Если вершина не посещена и есть остаточная пропускная способность
                    parent[v] = u; // Записываем предка
                    if (v == sink) {
                        return true; // Если достигли стока, путь найден
                    }
                    queue.add(v);
                    visited[v] = true;
                }
            }
        }
        return false; // Путь не найден
    }

    // Метод для нахождения максимального потока и путей в графе
    int findFlow(int source, int sink, int m, List<PathInfo> paths)  {
        int[] parent = new int[V]; // Массив для хранения пути
        int totalFlow = 0; // Общее количество потока

        while (bfs(source, sink, parent)) {
            int pathFlow = Integer.MAX_VALUE; // Изначально путь имеет максимальную возможную пропускную способность
            int s = sink;
            List<Integer> path = new ArrayList<>();
            while (s != source) { // Восстанавливаем путь от стока к источнику
                path.add(s);
                pathFlow = Math.min(pathFlow, getCapacity(parent[s], s)); // Находим минимальную остаточную пропускную способность
                s = parent[s];
            }
            path.add(source);
            Collections.reverse(path); // Переворачиваем путь для правильного порядка

            if (pathFlow > m - totalFlow) {
                pathFlow = m - totalFlow; // Ограничиваем поток, чтобы не превысить требуемый
            }
            totalFlow += pathFlow; // Увеличиваем общий поток
            int pathCost = calculatePathCost(path, pathFlow); // Вычисляем стоимость пути
            paths.add(new PathInfo(path, pathFlow, pathCost)); // Сохраняем информацию о пути

            s = sink;
            while (s != source) { // Обновляем поток в графе
                int u = parent[s];
                updateFlow(u, s, pathFlow);
                s = parent[s];
            }
            if (totalFlow == m) {
                break; // Если достигли требуемого потока, прекращаем
            }
        }
        return totalFlow; // Возвращаем общий поток
    }

    // Метод для вычисления стоимости пути
    int calculatePathCost(List<Integer> path, int flow) {
        int cost = 0;
        for (int i = 0; i < path.size() - 1; i++) {
            int u = path.get(i), v = path.get(i + 1);
            for (Edge edge : graph.get(u)) {
                if (edge.v == v) {
                    cost += edge.cost * flow; // Добавляем стоимость ребра, умноженную на поток
                    break;
                }
            }
        }
        return cost; // Возвращаем общую стоимость пути
    }

    // Метод для получения остаточной пропускной способности ребра
    int getCapacity(int u, int v) {
        for (Edge edge : graph.get(u)) {
            if (edge.v == v) {
                return edge.capacity - edge.flow; // Возвращаем остаточную пропускную способность
            }
        }
        return 0;
    }

    // Метод для обновления потока в графе
    void updateFlow(int u, int v, int flow) {
        for (Edge edge : graph.get(u)) {
            if (edge.v == v) {
                edge.flow += flow; // Увеличиваем поток в прямом направлении
                break;
            }
        }
        for (Edge edge : graph.get(v)) {
            if (edge.v == u) {
                edge.flow -= flow; // Уменьшаем поток в обратном направлении
                break;
            }
        }
    }

    // Метод для построения графа с модифицированными стоимостями
    Map<Integer, List<ModifiedEdge>> buildModifiedCostGraph() {
        Map<Integer, List<ModifiedEdge>> modifiedGraph = new HashMap<>();
        for (int i = 0; i < V; i++) {
            modifiedGraph.put(i, new ArrayList<>());
        }

        for (int u = 0; u < V; u++) {
            for (Edge edge : graph.get(u)) {
                int v = edge.v;
                int c = edge.capacity, f = edge.flow, d = edge.cost;
                if (f == 0) {
                    modifiedGraph.get(u).add(new ModifiedEdge(v, d)); // Добавляем прямое ребро
                } else if (f == c) {
                    modifiedGraph.get(v).add(new ModifiedEdge(u, -d)); // Добавляем обратное ребро
                } else if (0 < f && f < c) {
                    modifiedGraph.get(u).add(new ModifiedEdge(v, d));
                    modifiedGraph.get(v).add(new ModifiedEdge(u, -d));
                }
            }
        }
        return modifiedGraph; // Возвращаем модифицированный граф
    }

    // Метод для вывода графа с модифицированными стоимостями
    void printModifiedCostGraph(Map<Integer, List<ModifiedEdge>> modifiedGraph) {
        System.out.println("Модифицированные стоимости:");
        for (Map.Entry<Integer, List<ModifiedEdge>> entry : modifiedGraph.entrySet()) {
            int u = entry.getKey();
            for (ModifiedEdge edge : entry.getValue()) {
                System.out.println(u + " -> " + edge.v + ", Стоимость: " + edge.cost);
            }
        }
    }

    List<Integer> findNegativeCostCycle(Map<Integer, List<ModifiedEdge>> modifiedGraph) {
        // Инициализируем массив для хранения кратчайших расстояний от источника
        int[] distance = new int[V];
        Arrays.fill(distance, Integer.MAX_VALUE); // Заполняем его значением "бесконечность"

        // Инициализируем массив для хранения предков каждой вершины
        int[] parent = new int[V];
        Arrays.fill(parent, -1); // Заполняем его значением -1, что означает отсутствие предка

        // Устанавливаем расстояние до начальной вершины (предполагаем, что это 0) равным 0
        distance[0] = 0;

        // Проходим через все вершины V-1 раз (алгоритм Беллмана-Форда)
        for (int i = 0; i < V - 1; i++) {
            // Итерируем по всем вершинам и их исходящим рёбрам
            for (Map.Entry<Integer, List<ModifiedEdge>> entry : modifiedGraph.entrySet()) {
                int u = entry.getKey(); // Текущая вершина
                for (ModifiedEdge edge : entry.getValue()) {
                    int v = edge.v; // Конечная вершина ребра
                    int cost = edge.cost; // Стоимость ребра
                    // Если найден более короткий путь до вершины v через u
                    if (distance[u] != Integer.MAX_VALUE && distance[u] + cost < distance[v]) {
                        distance[v] = distance[u] + cost; // Обновляем расстояние до v
                        parent[v] = u; // Обновляем предка для v
                    }
                }
            }
        }

        // Дополнительный проход для обнаружения отрицательных циклов
        for (Map.Entry<Integer, List<ModifiedEdge>> entry : modifiedGraph.entrySet()) {
            int u = entry.getKey(); // Текущая вершина
            for (ModifiedEdge edge : entry.getValue()) {
                int v = edge.v; // Конечная вершина ребра
                int cost = edge.cost; // Стоимость ребра
                // Если расстояние до v можно уменьшить, это указывает на наличие отрицательного цикла
                if (distance[u] != Integer.MAX_VALUE && distance[u] + cost < distance[v]) {
                    return reconstructNegativeCycle(parent, v); // Возвращаем найденный цикл
                }
            }
        }
        return null; // Если цикл не найден, возвращаем null
    }

    private List<Integer> reconstructNegativeCycle(int[] parent, int start) {
        // Множество для отслеживания посещённых вершин
        Set<Integer> visited = new HashSet<>();
        // Список для хранения вершин, составляющих цикл
        List<Integer> cycle = new ArrayList<>();
        int current = start; // Начинаем с вершины, указывающей на цикл

        // Идём по предкам, пока не найдём вершину, которая уже была посещена
        while (!visited.contains(current)) {
            visited.add(current); // Помечаем вершину как посещённую
            current = parent[current]; // Переходим к предку
        }

        int cycleStart = current; // Вершина, с которой начинается цикл
        do {
            cycle.add(current); // Добавляем вершину в цикл
            current = parent[current]; // Переходим к следующему предку
        } while (current != cycleStart); // Повторяем, пока не вернёмся к началу цикла

        cycle.add(cycleStart); // Добавляем начальную вершину ещё раз, чтобы замкнуть цикл
        Collections.reverse(cycle); // Переворачиваем цикл, чтобы он шёл в правильном порядке
        return cycle; // Возвращаем список вершин, составляющих цикл
    }

    // Метод для вычисления стоимости отрицательного цикла
    int calculateNegativeCycleCost(List<Integer> cycle, Map<Integer, List<ModifiedEdge>> modifiedGraph) {
        int cost = 0;
        for (int i = 0; i < cycle.size() - 1; i++) {
            int u = cycle.get(i);
            int v = cycle.get(i + 1);
            for (ModifiedEdge edge : modifiedGraph.get(u)) {
                if (edge.v == v) {
                    cost += edge.cost; // Суммируем стоимость рёбер в цикле
                    break;
                }
            }
        }
        return cost; // Возвращаем общую стоимость цикла
    }

    // Метод для вычисления минимального r для корректировки потока
    int calculateR(List<Integer> cycle) {
        int minR = Integer.MAX_VALUE;
        for (int i = 0; i < cycle.size() - 1; i++) {
            int u = cycle.get(i);
            int v = cycle.get(i + 1);
            for (Edge edge : graph.get(u)) {
                if (edge.v == v) {
                    int r = edge.capacity - edge.flow;
                    minR = Math.min(minR, r); // Находим минимальную остаточную пропускную способность
                    break;
                }
            }
            for (Edge edge : graph.get(v)) {
                if (edge.v == u) {
                    int r = edge.flow;
                    minR = Math.min(minR, r); // Находим минимальный поток в обратном направлении
                    break;
                }
            }
        }
        return minR; // Возвращаем минимальное значение r
    }

    // Метод для обновления потока в найденном цикле
    void updateFlowInCycle(List<Integer> cycle, int r) {
        for (int i = 0; i < cycle.size() - 1; i++) {
            int u = cycle.get(i);
            int v = cycle.get(i + 1);
            for (Edge edge : graph.get(u)) {
                if (edge.v == v) {
                    edge.flow += r; // Увеличиваем поток в прямом направлении
                    break;
                }
            }
            for (Edge edge : graph.get(v)) {
                if (edge.v == u) {
                    edge.flow -= r; // Уменьшаем поток в обратном направлении
                    break;
                }
            }
        }
    }

    public static void main(String[] args) {
        // Создаём граф с 5 вершинами
        GraphFlow g = new GraphFlow(5);
        g.addEdge(0, 1, 4, 1); // Добавляем ребро с пропускной способностью и стоимостью
        g.addEdge(0, 3, 3, 3);
        g.addEdge(1, 2, 3, 2);
        g.addEdge(1, 3, 3, 2);
        g.addEdge(2, 4, 5, 2);
        g.addEdge(3, 2, 2, 1);
        g.addEdge(3, 4, 3, 8);

        int source = 0; // Источник
        int sink = 4; // Сток
        int m = 5; // Требуемый поток

        List<PathInfo> paths = new ArrayList<>(); // Список путей
        int maxFlow = g.findFlow(source, sink, m, paths); // Поиск максимального потока

        System.out.println("Необходимо найти допустимый поток величины " + m); // Вывод разрешённого потока
        System.out.println("\nПути, по которым проходит поток с их стоимостью:");
        int totalCost = 0;
        for (PathInfo pathInfo : paths) {
            System.out.println("Путь: " + pathInfo.path + ", Поток: " + pathInfo.flow + ", Стоимость: " + pathInfo.cost);
            totalCost += pathInfo.cost; // Суммируем стоимость всех путей
        }
        System.out.println("Суммарная стоимость потока: " + totalCost);

        int iteration = 0;
        while (true) {
            iteration++;
            System.out.println("\nИТЕРАЦИЯ №" + iteration);
            Map<Integer, List<ModifiedEdge>> modifiedGraph = g.buildModifiedCostGraph(); // Строим модифицированный граф
            g.printModifiedCostGraph(modifiedGraph); // Выводим модифицированный граф

            List<Integer> negativeCycle = g.findNegativeCostCycle(modifiedGraph); // Ищем отрицательный цикл
            if (negativeCycle != null) {
                System.out.println("Найден цикл с отрицательной удельной стоимостью:");
                System.out.println(negativeCycle);

                int negativeCycleCost = g.calculateNegativeCycleCost(negativeCycle, modifiedGraph); // Вычисляем стоимость цикла
                System.out.println("Стоимость отрицательного цикла: " + negativeCycleCost);

                int rValue = g.calculateR(negativeCycle); // Вычисляем значение r
                System.out.println("Значение r для найденного отрицательного цикла: " + rValue);

                g.updateFlowInCycle(negativeCycle, rValue); // Обновляем поток в цикле
                totalCost += negativeCycleCost * rValue; // Обновляем общую стоимость
                System.out.println("Стоимость нового потока: " + totalCost);
            } else {
                System.out.println("\nЦиклов с отрицательной удельной стоимостью не найдено.");
                System.out.println("Минимальная стоимость потока: " + totalCost); // Выводим минимальную стоимость
                break;
            }
        }
    }
}
