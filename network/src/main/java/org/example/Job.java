package org.example;

import java.util.List;

public class Job {
    private int start;
    private int end;
    private int weight;

    public Job(int start, int end, int weight) {
        this.start = start;
        this.end = end;
        this.weight = weight;
    }
    public Job(){}

    public static Integer getWeightFromListByStartAndEnd(int start, int end, List<Job> list){
        for (Job w: list) {
            if (w.start ==start && w.end ==end)
                return w.weight;
        }
        return null;
    }

    public int getStart() {
        return start;
    }

    public void setStart(int start) {
        this.start = start;
    }

    public int getEnd() {
        return end;
    }

    public void setEnd(int end) {
        this.end = end;
    }

    public int getWeight() {
        return weight;
    }

    public void setWeight(int weight) {
        this.weight = weight;
    }
}