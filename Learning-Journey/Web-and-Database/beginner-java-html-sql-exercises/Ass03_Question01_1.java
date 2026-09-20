// PROG23863 - Assignment 3 - Question 1
// This program creates an Employee class and tests it with 2 objects

class Employee {

    // instance variables
    private String name;
    private int id;
    private String department;
    private String position;

    // default constructor
    public Employee() {
        name = "";
        id = 0;
        department = "";
        position = "";
    }

    // constructor with parameters
    public Employee(String name, int id, String department, String position) {
        this.name = name;
        this.id = id;
        this.department = department;
        this.position = position;
    }

    // getter for name
    public String getName() {
        return name;
    }

    // setter for name
    public void setName(String name) {
        this.name = name;
    }

    // getter for id
    public int getId() {
        return id;
    }

    // setter for id
    public void setId(int id) {
        this.id = id;
    }

    // getter for department
    public String getDepartment() {
        return department;
    }

    // setter for department
    public void setDepartment(String department) {
        this.department = department;
    }

    // getter for position
    public String getPosition() {
        return position;
    }

    // setter for position
    public void setPosition(String position) {
        this.position = position;
    }

    // toString method to display employee info
    public String toString() {
        return "Name: " + name + "\nID: " + id + "\nDepartment: " + department + "\nPosition: " + position;
    }

}

public class Ass03_Question01 {

    public static void main(String[] args) {

        // create first employee object with parameterized constructor (my info)
        Employee emp1 = new Employee("Alex Johnson", 10234, "Computer Studies", "Junior Developer");

        // create second employee object with default constructor then use setters (friend's info)
        Employee emp2 = new Employee();
        emp2.setName("Sarah Williams");
        emp2.setId(10891);
        emp2.setDepartment("Information Technology");
        emp2.setPosition("Network Technician");

        // print both employees
        System.out.println("Employee 1:");
        System.out.println(emp1.toString());

        System.out.println("\nEmployee 2:");
        System.out.println(emp2.toString());

    }

}
