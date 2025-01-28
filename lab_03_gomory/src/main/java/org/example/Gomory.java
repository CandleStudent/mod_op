package org.example;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Arrays;

import static java.lang.System.out;

public class Gomory {
    static double[][] table;
    static int m, n;
    static ArrayList<Integer> basis;

    public Gomory(double[][] matrix, String[] array) {
        System.out.println("-------------Изначальная матрица-------------");
        int [] arr = new int[]{3,4,5};
        ArrayList<Integer> tempBase = new ArrayList<>();
        for(int i = 0; i < arr.length; i++){
            tempBase.add(arr[i]);
        }
        Matrix.printMatrix(matrix);
        //меняем знаки у коэффициентов по знакам уравнения
        Matrix.changeBySign(matrix, array);
        m = matrix.length; // rows
        n = matrix[0].length; // columns
        table = new double[m][n + m - 1]; // столбцы включают как базисные, так и небазисные переменные
        basis = new ArrayList<>(); // index == разрешающие строки, значения по индексу -- разрешающие столбцы

        //заполнение матрицы для работы
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < table[0].length; j++) {
                if (j < n)
                    table[i][j] = matrix[i][j];
                else
                    table[i][j] = 0;
            }
            //определение доп коэффициентов, заполнение базиса
            if (n + i < table[0].length) {
                table[i][n + i] = 1;
                basis.add(n + i);
            }
        }
        n = table[0].length;
        System.out.println("----------Матрица с доп коэффициентами--------");
        Matrix.printMatrix(table,tempBase);

        Simplex.getMatrixWithoutNegativeFreeElems();
    }

    //алгоритм поиска ответа
    public double[][] getSolve(double[] result) {
        //простой симплекс-метод
        Simplex.makeSimplex();

        res(result);

        //применение метода Гомори для получения целых ответов
        //все ли свободные члены целые
        while (!isUnit(result)) {
            //добавление ограничения
            methodGomory(result);
            //до отсутствия отрицательных в последней строке
            if (!Simplex.isEnd()) {
                //симплекс для Гомори (один прогон)
                gomorySimplex();
                //получение промежуточного результата
                res(result);

            }
            //итоговый результат
            res(result);
        }

        return table;
    }

    //вывод результата
    private void res(double[] result) {
        for (int i = 0; i < result.length; i++) {
            int k = basis.indexOf(i + 1);
            if (k != -1)
                result[i] = table[k][0];
            else
                result[i] = 0;
        }
        DecimalFormat df = new DecimalFormat("0.00");

        System.out.println("Промежуточное решение:");
        System.out.println("X1 = " + result[0]);
        System.out.println("X2 = " + result[1]+"\n");
        out.println("Z = x1("+1*result[0]+")+x2("+1*result[1]+") = " + df.format(result[0] * 1 + result[1] * 1));

    }

    //симплекс-метод для Гомори (по-другому ищем строку и столбец)
    private void simplexForGomory() {
        System.out.println("С применением прохода по симплекс-методу для Гомори:");
        int mainCol, mainRow;
        mainRow = basis.size() - 1;
        mainCol = findMainColGomory(mainRow);
        basis.set(mainRow, mainCol);

        Simplex.transformation(mainRow, mainCol);
        Matrix.printMatrix(table,basis);
    }

    //остались ли в последней строке только целые числа
    private boolean isUnit(double[] res) {
        if (res[0] % 1 == 0 && res[1] % 1 == 0)
            return true;
        else
            return false;
    }

    //добавление ограничения
    private void methodGomory(double[] res) {
        int bas;
        m += 1;
        n += 1;
        //увеличенная матрица
        double[][] newMatrix = new double[table.length + 1][table[0].length + 1];

        //определяем индекс в базисе ответа с большей дробной частью
        Double max_reminder = (double) Integer.MIN_VALUE;
        bas = 0;
        for (int i = 0; i < res.length; i++) {
            if (res[i] % 1 > 0 && res[i] > max_reminder) {
                max_reminder = res[i];
                bas = i;
            }
        }
//        if (res[0] % 1 > res[1] % 1) {
//            bas = basis.get(0); // сейчас в базисе лежат 2 и 3, например. 2 -- x2, 3 -- s1
//        } else {
//            bas = basis.get(1);
//        }

        //определение новой строки в матрице
        double[] magicCoef = new double[table[0].length + 1];
        for (int i = 0; i < table[0].length; i++) {

            magicCoef[i] = table[bas][i] % 1;

            if (magicCoef[i] < 0)
                magicCoef[i] = magicCoef[i] + 1;

            if (magicCoef[i] != 0) magicCoef[i] *= -1;

        }

        //заполнение матрицы
        for (int i = 0; i <= table.length; i++) {
            for (int j = 0; j <= table[0].length; j++) {
                //тут надо перенести новые найденные коэффициенты
                if (i == table.length - 1) {
                    if (j != table[0].length)
                        newMatrix[i][j] = magicCoef[j];
                    else {
                        //это доп коэффициент для строки
                        newMatrix[i][j] = 1;
                    }
                }
                //тут заполняем последнюю строку
                else if (i == table.length) {
                    if (j != table[0].length && table[i - 1][j] != 0)
                        newMatrix[i][j] = table[i - 1][j];
                    else
                        newMatrix[i][j] = 0;
                }
                //тут остальные
                else {
                    if (j != table[0].length)
                        newMatrix[i][j] = table[i][j];
                    else
                        newMatrix[i][j] = 0;
                }
            }
        }
        table = Matrix.cloneMatrix(newMatrix);
        //добавление вновь добавленной строки в базис
        basis.add(newMatrix[0].length - 1);

        System.out.println("-------------С ограничением по методу Гомори-------------");
        Matrix.printMatrix(table,basis);

        Simplex.getMatrixWithoutNegativeFreeElems();
    }

    //после применения Гомори ищем колонку по-другому
    private int findMainColGomory(int mainRow) {
        int mainCol = 1;
        int min = Integer.MAX_VALUE;

        //ищем минимум при вычислении по формуле
        for (int i = 2; i < table[0].length - 1; i++) {
            if (table[mainRow][i] != 0 && table[mainRow + 1][i] / table[mainRow][i] < min)
                mainCol = i;
        }

        return mainCol;
    }

    private void gomorySimplex(){
        simplexForGomory();
        //простой симплекс
        Simplex.makeSimplex();
    }

    private void printBasis(){
        System.out.println("Базисы");
        for(Integer one: basis){
            System.out.print(one+" ");
        }
        System.out.println();
    }
}
