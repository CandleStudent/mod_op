package org.example;

import java.text.DecimalFormat;
import java.util.ArrayList;

public class Matrix {
    public static double[][] cloneMatrix(double[][] martrix) {
        double[][] clone = new double[martrix.length][];
        int count = 0;
        for (double[] line : martrix) {
            clone[count++] = line.clone();
        }
        return clone;
    }

    public static double[][] changeBySign(double[][] matrix, String[] arr) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i].equals(">=") || arr[i].equals("max")) {
                for (int j = 0; j < matrix[0].length; j++) {
                    matrix[i][j] = matrix[i][j] * -1;
                }
            }
        }
        return matrix;
    }

    public static void printMatrix(double[][] matrix, ArrayList<Integer> basis) {
        DecimalFormat df = new DecimalFormat("0.00");

        // Определяем количество свободных переменных
        int numberOfFreeVariables = matrix[0].length;

        // Создаем заголовок
        System.out.printf("%-10s %-10s", "Базисные", "Свободные");
        for (int i = 1; i < numberOfFreeVariables; i++) {
            System.out.printf("%-10s", "x" + i); // Добавляем x1, x2, ..., xn
        }
        System.out.println();

        // Создаем массив строк для базисных переменных
        String[] baseVariables = new String[basis.size() + 1];
        for (int i = 0; i < basis.size(); i++) {
            baseVariables[i] = "х" + basis.get(i); // Добавляем префикс "х"
        }
        baseVariables[baseVariables.length - 1] = "F"; // Последний элемент - свободная переменная

        // Выводим строки матрицы
        for (int i = 0; i < matrix.length; i++) {
            // Выводим базисные переменные
            System.out.printf("%-10s", baseVariables[i]); // Выравниваем по левому краю

            // Выводим элементы матрицы
            for (int j = 0; j < matrix[i].length; j++) {
                System.out.printf("%-10s", df.format(matrix[i][j])); // Выравниваем по левому краю
            }
            System.out.println();
        }
        System.out.println();
    }



    public static void reformateMatrix(double[][] newTable, int i, int j) {
        if (1 - (Math.abs(newTable[i][j]) * 10) % 1 < 0.0001) {
            newTable[i][j] = (double) (Math.round(newTable[i][j] * 10)) / 10;
        }
    }

    public static void printMatrix(double[][] matrix) {
        DecimalFormat df = new DecimalFormat("0.00");
        System.out.println();
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[0].length; j++) {
                System.out.print(df.format(matrix[i][j]) + "   ");
            }
            System.out.println();
        }
        System.out.println();
    }

    public static void printMatrix2(double[][] matrix) {
        System.out.print("Базисные\tСвободные");

        for (int i = 0; i < matrix.length + 2; i++) {
            System.out.print("x" + (i + 1) + "     ");
        }

        System.out.println();
        for (int i = 0; i < matrix.length; i++) {

            for (int j = 0; j < matrix[0].length; j++) {

                if (Double.toString(matrix[i][j]).charAt(0) == '-') {
                    System.out.print(" " + (Math.ceil(matrix[i][j] * 100.0) / 100.0) + "  ");
                }
                else {
                    System.out.print("  " + (Math.ceil(matrix[i][j] * 100.0) / 100.0) + "  ");
                }
            }
            System.out.println();
        }
        System.out.println();
    }

}