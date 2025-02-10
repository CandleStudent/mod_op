package org.example;

public class Main {
    public static void main(String[] args) {
        int n = 3;
        int m = 3;
        int[] resources = new int[]{1000, 1700, 1600};
        int[] demand = new int[]{1600, 1000, 1700};
        Integer[][] costs = new Integer[n][m];
        costs[0] = new Integer[]{4893, 4280, 6213};
        costs[1] = new Integer[]{5327, 4296, 6188};
        costs[2] = new Integer[]{6006, 5030, 7224};
        HungarianAlgorithm algorithm = new HungarianAlgorithm(n, m, resources, demand, costs);
        algorithm.execute();
    }
}