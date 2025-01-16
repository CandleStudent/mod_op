package org.example;

import java.util.ArrayList;
import java.util.Arrays;

public class Main {

    static int n = 9;

    public static void main(String[] args) {
        ArrayList<Job> graph = new ArrayList<>();
        graph.add(new Job(1, 2, 11));
        graph.add(new Job(1, 3, 20));
        graph.add(new Job(1, 4, 14));
        graph.add(new Job(2, 3, 12));
        graph.add(new Job(2, 5, 13));
        graph.add(new Job(2, 7, 18));
        graph.add(new Job(3, 4, 17));
        graph.add(new Job(3, 6, 8));
        graph.add(new Job(4, 6, 0));
        graph.add(new Job(4, 8, 20));
        graph.add(new Job(5, 7, 14));
        graph.add(new Job(6, 7, 12));
        graph.add(new Job(6, 8, 13));
        graph.add(new Job(6, 9, 18));
        graph.add(new Job(7, 9, 17));
        graph.add(new Job(8, 9, 16));

        System.out.println("=======================================");
        System.out.println("ВХОДЫ И ВЫХОДЫ СИСТЕМЫ");
        ArrayList<Integer> points = getPoints();
        for (Job g : graph) {
            if (points.contains(g.getEnd())) {
                points.remove(points.indexOf(g.getEnd()));
            }
        }
        System.out.println("Все входы системы: " + points);

        points = getPoints();
        for (Job g : graph) {
            if (points.contains(g.getStart())) {
                points.remove(points.indexOf(g.getStart()));
            }
        }
        System.out.println("Все выходы системы: " + points);

        System.out.println("\n=======================================");
        System.out.println("РАННИЕ СРОКИ СОВЕРШЕНИЯ СОБЫТИЙ");
        int[] earlyArr = new int[n];
        System.out.println("Ранний срок совершения события 1: " + earlyArr[0]);
        boolean isNothingChanged = false;
        while (!isNothingChanged) {
            int[] oldArrayCopy = Arrays.copyOf(earlyArr, earlyArr.length);
            for (Job job : graph) {
                int endPoint = job.getEnd() - 1;
                int prevValue = earlyArr[endPoint];
                int earlyAtStart = earlyArr[job.getStart() - 1];
                earlyArr[endPoint] = Integer.max(prevValue, earlyAtStart + job.getWeight());
            }
            for (int i = 0; i < n; i++) {
                if (earlyArr[i] != oldArrayCopy[i]) {
                    break;
                }
                isNothingChanged = true;
            }
//            for (int i = 1; i < n; i++) {
//            int max = Integer.MIN_VALUE;
//            if (Job.getWeightFromListByStartAndEnd(1, i + 1, graph) != null) {
//                max = Job.getWeightFromListByStartAndEnd(1, i + 1, graph);
//            }
//            for (int j = 0; j < i; j++) {
//                if (Job.getWeightFromListByStartAndEnd(j + 1, i + 1, graph) != null && max < earlyArr[j] + Job.getWeightFromListByStartAndEnd(j + 1, i + 1, graph)) {
//                    max = earlyArr[j] + Job.getWeightFromListByStartAndEnd(j + 1, i + 1, graph);
//                }
//            }
//            earlyArr[i] = max;
//            }
        }
        for (int i = 0; i < n; i++) {
            System.out.println("Ранний срок совершения события " + (i + 1) + ": " + earlyArr[i]);
        }

        System.out.println("\n=======================================");
        System.out.println("ДЛИНА КРИТИЧЕСКОГО ПУТИ");
        System.out.println("Время выполнения проекта (длина критического пути): " + earlyArr[n - 1]);

        System.out.println("\n=======================================");
        System.out.println("ПОЗДНИЕ СРОКИ СОВЕРШЕНИЯ СОБЫТИЙ");
        int[] lateArr = {earlyArr[n - 1], earlyArr[n - 1], earlyArr[n - 1], earlyArr[n - 1], earlyArr[n - 1], earlyArr[n - 1], earlyArr[n - 1], earlyArr[n - 1], earlyArr[n - 1]};
        for (int i = n - 2; i >= 0; i--) {
            int min = Integer.MAX_VALUE;
            if (Job.getWeightFromListByStartAndEnd(i + 1, n, graph) != null) {
                min = lateArr[i] - Job.getWeightFromListByStartAndEnd(i + 1, n, graph);
            }
            for (int j = n - 2; j > i; j--) {
                if (Job.getWeightFromListByStartAndEnd(i + 1, j + 1, graph) != null && min > lateArr[i] - Job.getWeightFromListByStartAndEnd(i + 1, j + 1, graph) - (lateArr[n - 1] - lateArr[j])) {
                    min = lateArr[i] - Job.getWeightFromListByStartAndEnd(i + 1, j + 1, graph) - (lateArr[n - 1] - lateArr[j]);
                }
            }
            lateArr[i] = min;
        }
        for (int i = 0; i < n; i++) {
            System.out.println("Поздний срок совершения события " + (i + 1) + ": " + lateArr[i]);
        }

        System.out.println("\n=======================================");
        System.out.println("ПОЛНЫЕ РЕЗЕРВЫ ДЛЯ РАБОТЫ");
        int count = 1;
        int[] fullReserve = new int[graph.size()];
        for (Job w : graph) {
            System.out.print("Полный резерв для работы " + count + ": ");
            int res = lateArr[w.getEnd() - 1] - w.getWeight() - earlyArr[w.getStart() - 1];
            fullReserve[count - 1] = res;
            System.out.println(res);
            count++;
        }

        System.out.println("\n=======================================");
        System.out.println("СВОБОДНЫЕ РЕЗЕРВЫ ДЛЯ РАБОТЫ");
        count = 1;
        int[] freeReserve = new int[graph.size()];
        for (Job w : graph) {
            System.out.print("Свободный резерв для работы " + count + ": ");
            int res = earlyArr[w.getEnd() - 1] - w.getWeight() - earlyArr[w.getStart() - 1];
            freeReserve[count - 1] = res;
            System.out.println(res);
            count++;
        }

        System.out.println("\n=======================================");
        System.out.println("КРИТИЧЕСКИЕ РАБОТЫ");
        ArrayList<Integer> critWorks = new ArrayList<>();
        System.out.print("Критические работы: ");
        for (int i = 0; i < fullReserve.length; i++) {
            if (fullReserve[i] == 0) {
                critWorks.add(i + 1);
                System.out.print((i + 1) + ", ");
            }
        }

        System.out.println("\n\n=======================================");
        System.out.println("КРИТИЧЕСКИЙ ПУТЬ");
        ArrayList<Integer> critWay = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if (lateArr[i] == earlyArr[i])
                critWay.add(i + 1);
        }
        System.out.println("Критический путь: " + critWay);

        System.out.println("\n=======================================");
        System.out.println("ИЗМЕНЕНИЕ ПОЛНОГО РЕЗЕРВА ДЛЯ (6,9)");
        if (freeReserve[10] == 0) {
            System.out.println("Не изменится");
        } else {
            for (Job w : graph) {
                if (w.getStart() == 6 && w.getEnd() == 9) {
                    System.out.print("Новый полный резерв для работы " + count + "(6,9) ");
                    int res = lateArr[w.getEnd() - 1] + 4 - w.getWeight() - earlyArr[w.getStart() - 1];
                    System.out.println(res);
                    System.out.println("Разница: " + (fullReserve[count - 1] - res));
                }
                count++;
            }
        }

        System.out.println("\n=======================================");
        System.out.println("ИЗМЕНЕНИЕ ВРЕМЕНИ ВЫПОЛНЕНИЯ ПРОЕКТА");
        int res = earlyArr[n - 1];
        if (critWay.contains(6) && critWay.contains(8)) {
            res += 4;
            System.out.println("Старое время выполнения проекта: " + res);
            System.out.println("Новое время выполнения проекта: " + res);
            System.out.println("Разница: " + (earlyArr[n - 1] - res));
        } else {
            System.out.println("Не изменится");
        }
    }

    private static ArrayList<Integer> getPoints() {
        ArrayList<Integer> points = new ArrayList<>();
        for (int i = 1; i <= n; i++) {
            points.add(i);
        }

        return points;
    }
}