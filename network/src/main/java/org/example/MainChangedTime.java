package org.example;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class MainChangedTime {

    static int n = 9;

    public static void main(String[] args) {
        // Изменили продолжительность работы (6 9) + 8. Как повлияло на (6, 7)?
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
        graph.add(new Job(6, 9, 18 + 8));
        graph.add(new Job(7, 9, 17));
        graph.add(new Job(8, 9, 16));

        System.out.println("\n=======================================");
        System.out.println("РАННИЕ СРОКИ СОВЕРШЕНИЯ СОБЫТИЙ"); // слайд 59
        int[] earlyArr = new int[n];
        boolean isNothingChanged = false;
        while (!isNothingChanged) {
            int[] oldArrayCopy = Arrays.copyOf(earlyArr, earlyArr.length);
            for (Job job : graph) {
                int startPoint = job.getStart() - 1;
                int endPoint = job.getEnd() - 1;
                int prevValue = earlyArr[endPoint];
                int earlyAtStart = earlyArr[startPoint];
                earlyArr[endPoint] = Integer.max(prevValue, earlyAtStart + job.getWeight());
            }
            for (int i = 0; i < n; i++) {
                if (earlyArr[i] != oldArrayCopy[i]) {
                    break;
                }
                isNothingChanged = true;
            }
        }
        for (int i = 0; i < n; i++) {
            if (i == 6 - 1 || i == 7 - 1) {
                System.out.println("Ранний срок совершения события " + (i + 1) + ": " + earlyArr[i]);
            }
        }

        System.out.println("\n=======================================");
        System.out.println("ДЛИНА КРИТИЧЕСКОГО ПУТИ"); // <==> длительность проекта
        System.out.println("Время выполнения проекта (длина критического пути): " + earlyArr[n - 1]);
        int critical_time = earlyArr[n - 1];

        System.out.println("\n=======================================");
        System.out.println("ПОЗДНИЕ СРОКИ СОВЕРШЕНИЯ СОБЫТИЙ"); // слайд 63
        int[] lateArr = new int[n];
        Arrays.fill(lateArr, 0, lateArr.length, critical_time);

        isNothingChanged = false;
        while (!isNothingChanged) {
            int[] oldArrayCopy = Arrays.copyOf(lateArr, lateArr.length);
            for (Job job : graph) {
                int endPoint = job.getEnd() - 1;
                int startPoint = job.getStart() - 1;
                int prevValue = lateArr[startPoint];
                int lateAtEnd = lateArr[endPoint];
                lateArr[startPoint] = Integer.min(prevValue, lateAtEnd - job.getWeight());
            }
            for (int i = 0; i < n; i++) {
                if (lateArr[i] != oldArrayCopy[i]) {
                    break;
                }
                isNothingChanged = true;
            }
        }
        for (int i = 0; i < n; i++) {
            if (i == 6 - 1 || i == 7 - 1) {
                System.out.println("Поздний срок совершения события " + (i + 1) + ": " + lateArr[i]);
            }
        }

        System.out.println("\n=======================================");
        // Определить, насколько можно отложить выполнение работы без задержки всего проекта.
        // Полный Резерв времени = LF - EF
        System.out.println("ПОЛНЫЕ РЕЗЕРВЫ ДЛЯ РАБОТЫ");
        int index = 0;
        int[] fullReserve = new int[graph.size()];
        for (Job job : graph) {
            int currentFullReserve = lateArr[job.getEnd() - 1] - job.getWeight() - earlyArr[job.getStart() - 1]; // slide 57
            fullReserve[index] = currentFullReserve;
            if (index == 11) {
                System.out.printf("Полный резерв для работы %d : %d%n", index + 1, currentFullReserve);
            }
            index++;
        }

        System.out.println("\n=======================================");
        System.out.println("СВОБОДНЫЕ РЕЗЕРВЫ ДЛЯ РАБОТЫ"); // Определить, насколько можно отложить работу без задержки начала следующей работы.
        index = 0;
        int[] freeReserve = new int[graph.size()];
        for (Job w : graph) {
            int currentFreeReserve = earlyArr[w.getEnd() - 1] - w.getWeight() - earlyArr[w.getStart() - 1];
            freeReserve[index] = currentFreeReserve;
            if (index == 11) {
                System.out.print("Свободный резерв для работы " + (index + 1) + ": ");
                System.out.println(currentFreeReserve);
            }
            index++;
        }

        System.out.println("\n=======================================");
        System.out.println("КРИТИЧЕСКИЕ РАБОТЫ"); // Это работы, которые не имеют резервов времени (полного или свободного). Задержка в их выполнении неминуемо приведёт к задержке всего проекта.
        List<Integer> critJobs = new ArrayList<>();
        System.out.print("Критические работы: ");
        for (int i = 0; i < fullReserve.length; i++) {
            if (fullReserve[i] == 0) {
                int jobNumber = i + 1;
                critJobs.add(jobNumber);
                Job correspondingJobFromGraph = graph.get(i);
                System.out.printf(
                        "работа №%d (из %d в %d), ",
                        jobNumber,
                        correspondingJobFromGraph.getStart(),
                        correspondingJobFromGraph.getEnd());
            }
        }

        System.out.println("\n\n=======================================");
        System.out.println("КРИТИЧЕСКИЙ ПУТЬ"); // Это последовательность критических работ, определяющая минимальное время завершения проекта. Его продолжительность равна времени, необходимому для выполнения всех работ проекта без учёта резервов.
        ArrayList<Integer> critWay = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if (lateArr[i] == earlyArr[i])
                critWay.add(i + 1);
        }
        System.out.println("Критический путь: " + critWay);

    }

    private static ArrayList<Integer> getPoints() {
        ArrayList<Integer> points = new ArrayList<>();
        for (int i = 1; i <= n; i++) {
            points.add(i);
        }

        return points;
    }
}