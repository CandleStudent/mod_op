package org.example;

import static java.lang.System.*;
import java.text.DecimalFormat;

public class EntryPoint {
    public static void main(String[] args) {
        // Матрица коэффициентов: первая колонка — свободные члены, остальные — коэффициенты перед x1, x2...
//        double[][] coefficients = {
//                {6, 0, 3},
//                {4, 2, 4},
//                {7, 4, 2},
//                {6, 2, 4}
//        };
        double[][] coefficients = {
                {2, 0, 1},
                {7, 4, 2},
                {0, 0, 1}
        };


        // Массив коэффициентов целевой функции
        double[] targetFunction = {0, 1};

        String[] constraints = {">=", "<=", "max"};


        Gomory solver = new Gomory(coefficients, constraints);
        double[] solution = new double[targetFunction.length];
        double[][] resultTable;


        resultTable = solver.getSolve(solution);

        printSolution(resultTable, solution, targetFunction);

//        out.println(3.15 % 1);
    }

    private static void printSolution(double[][] resultTable, double[] solution, double[] targetFunction) {
        DecimalFormat df = new DecimalFormat("0.00");

        out.println("-------------Итоговая таблица--------:");
        Matrix.printMatrix(resultTable,Gomory.basis);

        out.println("--------Решение-----------");
        out.println("X1 = " + df.format(solution[0]));
        out.println("X2 = " + df.format(solution[1]));

        out.println("-------------Значение функции------------");
        out.println("Z = x1("+targetFunction[0]*solution[0]+")+x2("+targetFunction[1]*solution[1]+") = " + df.format(solution[0] * targetFunction[0] + solution[1] * targetFunction[1]));
    }
}