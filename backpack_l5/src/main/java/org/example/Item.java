package org.example;

/**
 * @param name   название вещи
 * @param weight вес
 * @param price  стоимость
 */
public record Item(
        String name,
        int weight,
        int price)
{}
