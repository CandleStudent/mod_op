package org.example;


import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Main {
    public static void main(String[] args) {
        int itemAmount = 8;
        int backpackCapacity = 70;
        Item[] items = {
                new Item("Предмет_№1", 2, 2),
                new Item("Предмет_№2", 3, 3),
                new Item("Предмет_№3", 4, 4),
                new Item("Предмет_№4", 5, 5),
                new Item("Предмет_№5", 6, 6),
                new Item("Предмет_№6", 7, 7),
                new Item("Предмет_№7", 8, 8),
                new Item("Предмет_№8", 9, 9)};
        Backpack[][] bp = new Backpack[itemAmount + 1][backpackCapacity + 1]; //массив промежуточных состояний рюкзака

        for (int currentItem = 0; currentItem < itemAmount + 1; currentItem++) {
            for (int currentCapacity = 0; currentCapacity < backpackCapacity + 1; currentCapacity++) {
                if (currentItem == 0 || currentCapacity == 0) { //нулевую строку и столбец заполняем нулями
                    bp[currentItem][currentCapacity] = new Backpack(new Item[]{}, 0);
                } else {
                    if (items[currentItem - 1].weight() <= currentCapacity) {// если вес текущего предмета не более текущей вместимости
                        // в items[] исп currentItem - 1 <==> bp[currentItem], потому что items на один элемент короче
                        var newPrice = Math.max(
                                bp[currentItem - 1][currentCapacity].price(),
                                bp[currentItem - 1][currentCapacity - items[currentItem - 1].weight()].price() + items[currentItem - 1].price());
                        var newBackpack = new Backpack(
                                newPrice == bp[currentItem - 1][currentCapacity].price()
                                        ? bp[currentItem - 1][currentCapacity].items()
                                        : Stream.concat(
                                        Arrays.stream(bp[currentItem - 1][currentCapacity].items()),
                                        Arrays.stream(new Item[]{items[currentItem - 1]})).toArray(Item[]::new),
                                newPrice);
                        bp[currentItem][currentCapacity] = newBackpack;
                    } else {
                        bp[currentItem][currentCapacity] = bp[currentItem - 1][currentCapacity];
                    }
                }
            }
        }

        printBP(bp, itemAmount, backpackCapacity, items);

        /* Метод обратного прохода для проверки */
        System.out.println("\nОбратный проход:");
        List<Item> selectedItems = new ArrayList<>();
        int remainingWeight = backpackCapacity;
        for (int i = itemAmount; i > 0 && remainingWeight > 0; i--) {
            System.out.println("Рассматриваем " + items[i - 1].name() + ", текущий вес = " + remainingWeight + "." +
                    "\nУ предыдущего предмета для этого веса общая стоимость предметов = " + bp[i - 1][remainingWeight].price() + ", " +
                    "y текущего предмета для этого веса общая стоимость предметов = " + bp[i][remainingWeight].price());

            if (bp[i][remainingWeight].price() != bp[i - 1][remainingWeight].price()) {
                System.out.println("Стоимости не равны, следовательно на данном шаге " + items[i - 1].name() + " был взят!");
                selectedItems.add(items[i - 1]);
                remainingWeight -= items[i - 1].weight();
            }
            System.out.println();
        }

        /* Вывод выбранных предметов */
        System.out.println("Выбранные предметы:");
        for (Item item : selectedItems) {
            System.out.println(item.name() + " (Вес: " + item.weight() + ", Цена: " + item.price() + ")");
        }

        /* Вывод конечного состояния рюкзака */
        System.out.println("Конечное состояние рюкзака:");
        System.out.println(bp[itemAmount][backpackCapacity].getDescription());

    }

    public static void printBP(Backpack[][] bp, int n, int k, Item[] items) {
        System.out.print("            ");
        for (int i = 1; i < k + 1; i++) {
            System.out.print(i + (i > 9 ? " " : "  "));
        }
        System.out.println();
        for (int i = 0; i < n; i++) {
            System.out.print(items[i].name() + "  ");
            for (int j = 0; j < k; j++) {
                System.out.print(bp[i + 1][j + 1].price() + (bp[i + 1][j + 1].price() > 9 ? " " : "  "));
            }
            System.out.println();
        }
    }
}
