package org.example;

import java.util.Arrays;

public class HungarianAlgorithm{
    private int minimumPositiveNumber;

    private Integer[][] startCosts;
    protected final int n; // Количество складов
    protected final int m; // Количество пунктов
    protected final int[] resources;
    protected final int[] demand;
    protected final Integer[][] costs;
    protected Integer[][] shipment;
    protected int[] resourcesBalance, demandBalance;

    public HungarianAlgorithm(int n, int m, int[] resources, int[] demand, Integer[][] costs) {
        this.n = n;
        this.m = m;
        this.resources = resources;
        this.demand = demand;
        this.costs = costs;

        shipment = new Integer[n][m];
        resourcesBalance = new int[n];
        demandBalance = new int[m];

        minimumPositiveNumber = Integer.MAX_VALUE;

        startCosts = new Integer[n][m];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                startCosts[i][j] = costs[i][j];
            }
        }
    }

    protected void printIntMatrix(Integer[][] matrix) {
        for (Integer[] ints : matrix) {
            for (Integer num : ints) {
                int spaceCount = 6 - String.valueOf(num).length();
                System.out.print(num + " ".repeat(Math.max(0, spaceCount)));
            }
            System.out.println();
        }
        System.out.println();
    }

    public void checkNondegeneracy() {
        if (Arrays.stream(resources).sum() != Arrays.stream(demand).sum()) {
            throw new RuntimeException("Сумма имеющихся ресурсов не равно сумме необходимых поставок. Венгерский метод нельзя применять");
        }
    }

    public int transportationCost(){
        int summ = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                summ = summ + ((shipment[i][j] != null ? shipment[i][j] : 0) * startCosts[i][j]);
            }
        }
        return summ;
    }

    public void fillArrays() {
        System.arraycopy(resources, 0, resourcesBalance, 0, n);
        System.arraycopy(demand, 0, demandBalance, 0, m);
    }

    public void linesMinimum() {
        for (int i = 0; i < costs.length; i++) {
            int minimal = Integer.MAX_VALUE;
            for (int j = 0; j < costs[i].length; j++) {
                if (costs[i][j] < minimal) {
                    minimal = costs[i][j];
                }
            }
            if (minimal == 0) {
                continue;
            }
            for (int j = 0; j < costs[i].length; j++) {
                costs[i][j] = costs[i][j] - minimal;
            }
        }
    }

    public void columnsMinimum() {
        for (int i = 0; i < costs.length; i++) {
            int minimal = Integer.MAX_VALUE;
            for (int j = 0; j < costs[i].length; j++) {
                if (costs[j][i] < minimal) {
                    minimal = costs[j][i];
                }
            }
            if (minimal == 0) {
                continue;
            }
            for (int j = 0; j < costs[i].length; j++) {
                costs[j][i] = costs[j][i] - minimal;
            }
        }
    }

    public void getSomeNulls() {
        linesMinimum();
        columnsMinimum();
    }

    public boolean isDistributedFully() {
        for (int j : resourcesBalance) {
            if (j != 0) {
                return false;
            }
        }
        for (int j : demandBalance) {
            if (j != 0) {
                return false;
            }
        }
        return true;
    }

    public void distribute() {
        for (int k = 1; k < m+1; k++) {
            for (int i = 0; i < n; i++) {
                if (nullsCount(costs[i]) == k) {
                    if (resourcesBalance[i] == 0) {
                        continue;
                    }
                    //Распределение
                    for (int j = 0; j < m; j++) {
                        if (demandBalance[j] == 0) {
                            continue;
                        }
                        if (costs[i][j] == 0) {
                            int minimal = Math.min(resourcesBalance[i], demandBalance[j]);
                            resourcesBalance[i] = resourcesBalance[i] - minimal;
                            demandBalance[j] = demandBalance[j] - minimal;
                            shipment[i][j] = minimal;
                        }
                    }
                }
            }
        }
    }

    private int nullsCount(Integer[] array) {
        int nulls = 0;
        for (Integer i: array) {
            if (i == 0) nulls++;
        }
        return nulls;
    }

    public int getIndexWithMaximumElement() {
        int maximum = Integer.MIN_VALUE;
        int maximumIndex = 0;
        for (int i = 0; i < n; i++) {
            if (resourcesBalance[i] > maximum) {
                maximum = resourcesBalance[i];
                maximumIndex = i;
            }
        }
        return maximumIndex;
    }

    public void findMinimumPositiveNumber(Integer[] array) {
        for (int number: array) {
            if (number < minimumPositiveNumber && number != 0) {
                minimumPositiveNumber = number;
            }
        }
    }

    public void subtract(int maximumIndex) {
        for (int j = 0; j < m; j++) {
            costs[maximumIndex][j] -= minimumPositiveNumber;
        }
    }

    public void refactor(int maximumIndex) {
        for (int j = 0; j < m; j++) {
            if (costs[maximumIndex][j] < 0) {
                for (int i = 0; i < n; i++) {
                    costs[i][j] += minimumPositiveNumber;
                }
            }
        }
    }

    public void execute() {
        checkNondegeneracy();
        System.out.println("Изначальная матрица стоимостей:");
        printIntMatrix(costs);

        int iter = 1;
        while (true) {
            System.out.println("Итерация №" + (iter));
            fillArrays();
            getSomeNulls();
            distribute();
            System.out.println("Матрица стоимостей после вычитания минимальных элементов из строк и столбцов:");
            printIntMatrix(costs);
            System.out.println("Матрица отгрузок после " + (iter) + " распределения:");
            printIntMatrix(shipment);
            System.out.println("Стоимость транспортировки после " + (iter) + " распределения = " + transportationCost() + "\n");
            System.out.println("Остаток запасов:");
            for (int i = 0; i < n; i++) {
                System.out.print(resourcesBalance[i] + " ");
            }
            System.out.println("\n");
            System.out.println("Остаток потребностей:");
            for (int i = 0; i < n; i++) {
                System.out.print(demandBalance[i] + " ");
            }
            System.out.println("\n");
            if (!isDistributedFully()) {
                System.out.println("Так как не все ресурсы были распределены и не все получатели удовлетворены, приступаем к изменению матрицы стоимостей.\n");
                int maximumIndex = getIndexWithMaximumElement();
                System.out.println("Индекс поставщика, у которого оказалось наибольшее количество нераспределённых ресурсов равен " + (maximumIndex+1));
                findMinimumPositiveNumber(costs[maximumIndex]);
                System.out.println("\nМинимальный положительный элемент в строке под номером " + (maximumIndex+1) + " равен " + minimumPositiveNumber + "\n");
                subtract(maximumIndex);
                System.out.println("Вычитаем число " + minimumPositiveNumber + " из " + (maximumIndex+1) + " строки матрицы стоимостей:");
                printIntMatrix(costs);
                refactor(maximumIndex);
                System.out.println("Прибавляем число " + minimumPositiveNumber + " к тем столбам матрицы стоимостей, где были обнаружены отрицательные элементы:");
                printIntMatrix(costs);
            } else {
                System.out.println("Все запасы поставлены, все потребности удовлетворены. Найденное решение является оптимальным");
                return;
            }
            iter++;
        }
    }
}
