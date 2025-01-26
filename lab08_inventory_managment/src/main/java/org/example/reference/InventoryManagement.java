package org.example.reference;

public class InventoryManagement {

    public static void main(String[] args) {
        // Константы
        double v = 260_000; // Годовой спрос, единиц.
        double s = 0.02 * 365; // Годовая стоимость хранения (единица/год)
        double K_production = 20; // затраты на запуск производства
        double P_annual = 100 * 365; // Годовая производственная мощность (единиц/год)
        double K_purchase = 15; // затраты на размещение заказа

        // Оптимальный размер заказа (EOQ) для производства
        // = sqrt( (2* затраты на запуск производств  * Годовой спрос) / Годовая стоимость хранения)
        double Q_production = Math.sqrt((2 * K_production * v) / s);

        // Проверка, возможно ли производство
        boolean productionFeasible = Q_production <= P_annual;

        // Оптимальный размер заказа (EOQ) для закупки
        // = sqrt((2*затраты на размещение заказа * Годовой спрос) / Годовая стоимость хранения)
        double Q_purchase = Math.sqrt((2 * K_purchase * v) / s);

        // Общие затраты для производства
        // (затраты на производство * годовой спрос / оптимальный план производства) +
        // + (Годовая стоимость хранения * оптимальный план размера для производства / 2)
        double L_production = (K_production * v / Q_production) + (s * Q_production / 2);

        // Общие затраты для закупки
        // = (затраты на размещение заказа *  Годовой спроc / Оптимальный размер заказа для закупки) +
        // + (Годовая стоимость хранения * Оптимальный размер заказа / 2 );
        double L_purchase = (K_purchase * v / Q_purchase) + (s * Q_purchase / 2);

        // Вывод результатов
        System.out.printf("Оптимальный размер заказа для производства: %.2f единиц\n", Q_production);
        System.out.println("Возможно ли производство: " + productionFeasible);
        System.out.printf("Оптимальный размер заказа для закупки: %.2f единиц\n", Q_purchase);
        System.out.printf("Общие затраты на производство: %.2f год\n", L_production);
        System.out.printf("Общие затраты на закупку: %.2f год\n", L_purchase);

        // Решение
        if (L_purchase < L_production) {
            System.out.println("Закупка товаров более экономически выгодна.");
        } else {
            System.out.println("Производство товаров более экономически выгодно.");
        }
    }
}
