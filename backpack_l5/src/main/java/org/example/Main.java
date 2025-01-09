package org.example;


import java.util.ArrayList;
import java.util.List;

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

        for (int i = 0; i < itemAmount + 1; i++) {
            for (int j = 0; j < backpackCapacity + 1; j++) {
                if (i == 0 || j == 0) { //нулевую строку и столбец заполняем нулями
                    bp[i][j] = new Backpack(new Item[]{}, 0);
                } else if (i == 1) {
                    /* Первая строка заполняется просто: первый предмет кладём или не кладём в зависимости от веса */
                    bp[1][j] = items[0].weight() <= j ? new Backpack(new Item[]{items[0]}, items[0].price())
                            : new Backpack(new Item[]{}, 0);
                } else {
                    if (items[i - 1].weight() > j) //если очередной предмет не влезает в рюкзак,
                        bp[i][j] = bp[i - 1][j]; //записываем предыдущий максимум
                    else {
                        /* Рассчитаем цену очередного предмета + максимальную цену для (максимально возможный для рюкзака вес − вес предмета) */
                        int newPrice = items[i - 1].price()
                                + bp[i - 1][j - items[i - 1].weight()].price();
                        if (bp[i - 1][j].price() > newPrice) //если предыдущий максимум больше
                            bp[i][j] = bp[i - 1][j]; //запишем его
                        else {
                            /* Иначе фиксируем новый максимум: текущий предмет + стоимость свободного пространства */
                            Item currentItem = items[i - 1]; // Получаем текущий элемент
                            Item[] previousItems = bp[i - 1][j - currentItem.weight()].items(); // Получаем массив элементов из предыдущего состояния рюкзака
                            Item[] newItems = new Item[previousItems.length + 1]; // Создаем новый массив, который будет содержать текущий элемент и все элементы из предыдущего состояния рюкзака
                            newItems[0] = currentItem; // Копируем текущий элемент в начало нового массива
                            System.arraycopy(previousItems, 0, newItems, 1, previousItems.length); // Копируем элементы из предыдущего состояния рюкзака в новый массив
                            bp[i][j] = new Backpack(newItems, newPrice); // Создаем новый объект org.example.Backpack с новыми элементами и новой ценой
                        }
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
            System.out.println("Рассматриваем " + items[i-1].name() + ", текущий вес = " + remainingWeight + "." +
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
        for (int i = 1; i < k+1; i++) {
            System.out.print(i + (i > 9 ? " " : "  "));
        }
        System.out.println();
        for (int i = 0; i < n; i++) {
            System.out.print(items[i].name() + "  ");
            for (int j = 0; j < k; j++) {
                System.out.print(bp[i+1][j+1].price() + (bp[i+1][j+1].price() > 9 ? " " : "  "));
            }
            System.out.println();
        }
    }
}
